"""
Document upload and RAG indexing service.
"""

from pathlib import Path

import faiss
import numpy as np

from rag.chunking.text_chunker import chunk_documents
from rag.embeddings.embedder import DocumentEmbedder
from rag.ingestion.document_loader import (
    SUPPORTED_EXTENSIONS,
    load_document,
)
from rag.vectorstore.faiss_store import (
    INDEX_PATH,
    VECTORSTORE_DIR,
)

DOCUMENTS_DIR = Path("documents")


def process_uploaded_document(
    file_path: str,
) -> dict:
    """
    Process an uploaded document and rebuild the FAISS index.

    Args:
        file_path:
            Path of the uploaded document.

    Returns:
        Processing information containing filename,
        number of chunks, and status.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Uploaded document not found: {path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    # --------------------------------------------------------
    # 1. Load document
    # --------------------------------------------------------

    documents = load_document(str(path))

    # --------------------------------------------------------
    # 2. Chunk document
    # --------------------------------------------------------

    chunks = chunk_documents(
        documents,
        chunk_size=500,
        chunk_overlap=50,
    )

    if not chunks:
        raise ValueError("No usable text was found in the uploaded document.")

    # --------------------------------------------------------
    # 3. Generate embeddings
    # --------------------------------------------------------

    embedder = DocumentEmbedder()

    embeddings = embedder.embed_documents(chunks)

    embeddings = np.asarray(
        embeddings,
        dtype="float32",
    )

    # --------------------------------------------------------
    # 4. Create FAISS index
    # --------------------------------------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    # --------------------------------------------------------
    # 5. Save FAISS index
    # --------------------------------------------------------

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss.write_index(
        index,
        str(INDEX_PATH),
    )

    # --------------------------------------------------------
    # 6. Return result
    # --------------------------------------------------------

    return {
        "filename": path.name,
        "chunks": len(chunks),
        "status": "processed",
    }
