from pathlib import Path

import pandas as pd
from fastapi import (
    Depends,
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.config import API_TOKEN
from backend.logger import logger
from backend.model_loader import get_model
from backend.schemas import ChatRequest, Customer, PredictionResponse
from chatbot.chains import ChurnChatbot
from rag.chunking.text_chunker import chunk_documents
from rag.ingestion.document_loader import load_document
from rag.vectorstore.faiss_store import build_faiss_index
from src.model_registry import list_versions

# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Customer Churn Prediction API",
    description=(
        "FastAPI service for customer churn prediction, "
        "AI chatbot, and document upload."
    ),
    version="1.0.0",
)


# ============================================================
# AUTHENTICATION
# ============================================================

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> bool:
    """Verify the API bearer token."""

    if credentials.credentials != API_TOKEN:
        logger.warning("Authentication failed")

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    logger.info("Authentication successful")

    return True


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CONFIGURATION
# ============================================================

DOCUMENTS_DIR = Path("documents")

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# Create documents directory if it does not exist.
DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CHATBOT (per-session, not global)
# ============================================================

chatbot_sessions: dict[str, ChurnChatbot] = {}


def get_chatbot(session_id: str) -> ChurnChatbot:
    """Get or create a chatbot instance for this session."""

    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = ChurnChatbot()

    return chatbot_sessions[session_id]


# ============================================================
# ROOT ENDPOINT
# ============================================================


@app.get("/")
def root() -> dict[str, str]:
    """Return basic API information."""

    return {
        "message": "Customer Churn Prediction API",
        "version": "1.0.0",
        "status": "running",
    }


# ============================================================
# HEALTH CHECK
# ============================================================


@app.get("/api/v1/health")
def health() -> dict:
    """Check whether the API and its dependencies are healthy."""

    ollama_healthy = True

    try:
        import requests as _requests

        ollama_response = _requests.get(
            "http://localhost:11434",
            timeout=2,
        )

        ollama_healthy = ollama_response.status_code == 200

    except Exception:
        ollama_healthy = False

    index_path = Path("rag/vectorstore/index.faiss")
    index_healthy = index_path.exists()

    overall_status = "healthy" if ollama_healthy and index_healthy else "degraded"

    return {
        "status": overall_status,
        "ollama": "up" if ollama_healthy else "down",
        "faiss_index": "loaded" if index_healthy else "missing",
    }


# ============================================================
# AVAILABLE MODELS
# ============================================================


@app.get("/api/v1/models")
def available_models(
    authenticated: bool = Depends(verify_token),
) -> dict[str, list[str]]:
    """Return the ML models available for prediction."""

    return {
        "models": [
            "logistic_regression",
            "random_forest",
            "xgboost",
        ]
    }


@app.get("/api/v1/models/{model_name}/versions")
def get_model_versions(
    model_name: str,
    authenticated: bool = Depends(verify_token),
) -> dict:
    """List all registered versions of a specific model."""

    versions = list_versions(model_name)

    return {
        "model": model_name,
        "versions": versions,
    }


# ============================================================
# CUSTOMER CHURN PREDICTION
# ============================================================


@app.post(
    "/api/v1/predict",
    response_model=PredictionResponse,
)
def predict(
    customer: Customer,
    model_name: str = "random_forest",
    model_version: str = "latest",
    authenticated: bool = Depends(verify_token),
) -> PredictionResponse:
    """
    Predict customer churn.

    Args:
        customer:
            Customer information validated by Pydantic.

        model_name:
            ML model to use for prediction.

        model_version:
            Specific registered version to use, or "latest".

    Returns:
        Prediction result containing churn probability and risk level.
    """

    logger.info(
        "Prediction request received | model=%s | version=%s",
        model_name,
        model_version,
    )

    try:
        # ----------------------------------------------------
        # Load requested model
        # ----------------------------------------------------

        version_param: int | str = model_version

        if model_version.isdigit():
            version_param = int(model_version)

        model = get_model(model_name, version_param)

        # ----------------------------------------------------
        # Convert Pydantic model to DataFrame
        # ----------------------------------------------------

        customer_data = pd.DataFrame([customer.model_dump()])

        # ----------------------------------------------------
        # Make prediction
        # ----------------------------------------------------

        prediction = int(model.predict(customer_data)[0])

        probability = float(model.predict_proba(customer_data)[0][1])

        # ----------------------------------------------------
        # Determine risk level
        # ----------------------------------------------------

        if probability >= 0.7:
            risk_level = "High"

        elif probability >= 0.4:
            risk_level = "Medium"

        else:
            risk_level = "Low"

        logger.info(
            "Prediction completed | model=%s | probability=%.4f",
            model_name,
            probability,
        )

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return PredictionResponse(
            prediction=prediction,
            churn_probability=probability,
            risk_level=risk_level,
            model=model_name,
        )

    except ValueError as exc:
        logger.error(
            "Invalid model requested: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Prediction failed")

        raise HTTPException(
            status_code=500,
            detail="Prediction failed.",
        ) from exc


# ============================================================
# AI CHATBOT
# ============================================================


@app.post("/api/v1/chat")
def chat(
    request: ChatRequest,
    authenticated: bool = Depends(verify_token),
) -> dict:
    """
    Chat with the local AI assistant.

    The chatbot uses Ollama + LangChain. Each session_id gets
    its own chatbot instance, so conversation memory and
    customer data don't leak between different users.
    """

    logger.info(
        "Chat request received | session=%s | message_length=%d",
        request.session_id,
        len(request.message),
    )

    try:
        session_chatbot = get_chatbot(request.session_id)

        response = session_chatbot.chat(
            request.message,
            source=request.source,
        )

        logger.info(
            "Chat response generated successfully | session=%s",
            request.session_id,
        )

        return response.model_dump()

    except Exception as exc:
        logger.exception(
            "Chat request failed | session=%s",
            request.session_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Chatbot request failed.",
        ) from exc


@app.post("/api/v1/chat/stream")
def chat_stream(
    request: ChatRequest,
    authenticated: bool = Depends(verify_token),
) -> StreamingResponse:
    """
    Stream a chat response token by token, using the same
    prediction/summary/document-list/RAG routing as the
    non-streaming /api/v1/chat endpoint.
    """

    logger.info(
        "Stream request received | session=%s | message_length=%d",
        request.session_id,
        len(request.message),
    )

    session_chatbot = get_chatbot(request.session_id)

    def generate():
        try:
            for token in session_chatbot.chat_stream(
                request.message,
                source=request.source,
            ):
                yield str(token)

            logger.info(
                "Stream completed | session=%s",
                request.session_id,
            )

        except Exception as exc:
            logger.exception(
                "Stream failed | session=%s",
                request.session_id,
            )
            yield f"\n\n[Error: {exc}]"

    return StreamingResponse(generate(), media_type="text/plain")


# ============================================================
# FILE UPLOAD
# ============================================================


@app.post("/api/v1/upload")
async def upload_file(
    file: UploadFile = File(...),
    authenticated: bool = Depends(verify_token),
) -> dict:
    """
    Upload a PDF, TXT, or Markdown document.

    The uploaded document is saved to the documents directory.

    Supported file types:
        - PDF
        - TXT
        - Markdown

    Maximum file size:
        10 MB
    """

    logger.info(
        "File upload request received | filename=%s",
        file.filename,
    )

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    filename = Path(file.filename).name
    extension = Path(filename).suffix.lower()

    # --------------------------------------------------------
    # Validate file extension
    # --------------------------------------------------------

    if extension not in SUPPORTED_EXTENSIONS:
        logger.warning(
            "Unsupported file type | filename=%s",
            filename,
        )

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Only PDF, TXT, and Markdown files are allowed."
            ),
        )

    # --------------------------------------------------------
    # Prevent unsafe filenames
    # --------------------------------------------------------

    if filename in {".", "..", ""}:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    destination = DOCUMENTS_DIR / filename

    # --------------------------------------------------------
    # Save file
    # --------------------------------------------------------

    try:
        total_size = 0

        with destination.open("wb") as buffer:

            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                # Prevent files larger than 10 MB.
                if total_size > MAX_FILE_SIZE:
                    buffer.close()

                    if destination.exists():
                        destination.unlink()

                    logger.warning(
                        "File upload rejected because it exceeded size limit | "
                        "filename=%s",
                        filename,
                    )

                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds the 10 MB limit.",
                    )

                buffer.write(chunk)

        logger.info(
            "File uploaded successfully | filename=%s | size=%d",
            filename,
            total_size,
        )

        # ----------------------------------------------------
        # Validate that the document can be loaded
        # ----------------------------------------------------

        try:
            documents = load_document(str(destination))

        except Exception as exc:
            logger.exception(
                "Uploaded file could not be processed | filename=%s",
                filename,
            )

            if destination.exists():
                destination.unlink()

            raise HTTPException(
                status_code=400,
                detail=(
                    "The uploaded file could not be processed. "
                    "Please upload a valid document."
                ),
            ) from exc

        # ----------------------------------------------------
        # Create chunks
        # ----------------------------------------------------

        chunks = chunk_documents(
            documents,
            chunk_size=800,
            chunk_overlap=100,
        )

        logger.info(
            "Document processed | filename=%s | pages=%d | chunks=%d",
            filename,
            len(documents),
            len(chunks),
        )

        # ----------------------------------------------------
        # Rebuild FAISS index
        # ----------------------------------------------------

        try:
            build_faiss_index(
                chunk_size=800,
                chunk_overlap=100,
            )

            logger.info(
                "FAISS index rebuilt successfully | filename=%s",
                filename,
            )

        except Exception as exc:
            logger.exception(
                "FAISS index rebuild failed | filename=%s",
                filename,
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "File uploaded successfully, "
                    "but the vector index could not be rebuilt."
                ),
            ) from exc

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return {
            "message": "File uploaded and indexed successfully.",
            "filename": filename,
            "file_type": extension,
            "size_bytes": total_size,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
        }

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "File upload failed | filename=%s",
            filename,
        )

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=500,
            detail="File upload failed.",
        ) from exc

    finally:
        await file.close()


# ============================================================
# LIST UPLOADED DOCUMENTS
# ============================================================


@app.get("/api/v1/documents")
def list_documents(
    authenticated: bool = Depends(verify_token),
) -> dict:
    """
    Return the documents currently stored by the application.
    """

    logger.info("Document list requested")

    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        documents.append(
            {
                "filename": file_path.name,
                "file_type": file_path.suffix.lower(),
                "size_bytes": file_path.stat().st_size,
            }
        )

    return {
        "documents": documents,
        "count": len(documents),
    }


# ============================================================
# GET DOCUMENT CONTENT (for preview)
# ============================================================


@app.get("/api/v1/documents/{filename}/content")
def get_document_content(
    filename: str,
    authenticated: bool = Depends(verify_token),
) -> dict:
    """
    Return the text content of a single document for preview.
    """

    logger.info(
        "Document content requested | filename=%s",
        filename,
    )

    safe_name = Path(filename).name
    file_path = DOCUMENTS_DIR / safe_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {filename}",
        )

    try:
        documents = load_document(str(file_path))

        content = "\n\n".join(document.page_content for document in documents)

        return {
            "filename": safe_name,
            "content": content[:5000],
            "truncated": len(content) > 5000,
        }

    except Exception as exc:
        logger.exception(
            "Failed to load document content | filename=%s",
            safe_name,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to read document content.",
        ) from exc


# ============================================================
# DELETE DOCUMENT
# ============================================================


@app.delete("/api/v1/documents/{filename}")
def delete_document(
    filename: str,
    authenticated: bool = Depends(verify_token),
) -> dict:
    """
    Delete a document and rebuild the FAISS index.
    """

    logger.info(
        "Document deletion requested | filename=%s",
        filename,
    )

    safe_name = Path(filename).name
    file_path = DOCUMENTS_DIR / safe_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {filename}",
        )

    try:
        file_path.unlink()

        logger.info(
            "Document deleted | filename=%s",
            safe_name,
        )

        build_faiss_index(
            chunk_size=800,
            chunk_overlap=100,
        )

        logger.info(
            "FAISS index rebuilt after deletion | filename=%s",
            safe_name,
        )

        return {
            "message": "Document deleted and index rebuilt.",
            "filename": safe_name,
        }

    except Exception as exc:
        logger.exception(
            "Document deletion failed | filename=%s",
            safe_name,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to delete document.",
        ) from exc
