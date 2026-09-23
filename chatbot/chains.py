from pathlib import Path
from typing import Any

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from chatbot.customer_extractor import extract_customer_data
from chatbot.customer_normalizer import normalize_customer_data
from chatbot.document_intent import is_document_list_request
from chatbot.error_handler import (
    LLMError,
    PredictionError,
    handle_error,
)
from chatbot.llm import get_llm
from chatbot.memory import ConversationMemory
from chatbot.parser import ChatResponse
from chatbot.prediction_client import predict_customer
from chatbot.prediction_intent import is_prediction_request
from chatbot.prompts import SYSTEM_PROMPT
from chatbot.summarization_intent import is_summary_request
from rag.generation.rag_chain import RAGChain
from rag.generation.summarizer import DocumentSummarizer

REQUIRED_CUSTOMER_FIELDS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]

DOCUMENTS_DIR = Path("documents")

SUPPORTED_DOCUMENT_EXTENSIONS = {".pdf", ".txt", ".md"}


class ChurnChatbot:
    """Customer churn chatbot with memory, ML prediction, and RAG."""

    def __init__(self) -> None:
        """Initialize chatbot components."""

        self.llm = get_llm()

        self.structured_llm = self.llm.with_structured_output(ChatResponse)

        self.memory = ConversationMemory()

        # RAG pipeline for document questions.
        self.rag_chain = RAGChain(top_k=5)

        # Whole-document summarizer, bypasses chunk retrieval.
        self.summarizer = DocumentSummarizer(self.llm)

        # Stores customer information collected across messages.
        self.customer_data: dict[str, Any] = {}

    # ============================================================
    # MESSAGE BUILDING
    # ============================================================

    def _build_messages(
        self,
        user_message: str,
    ) -> list[BaseMessage]:
        """Build the complete message history for the LLM."""

        messages: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]

        messages.extend(self.memory.get_messages())

        messages.append(HumanMessage(content=user_message))

        return messages

    # ============================================================
    # CUSTOMER DATA
    # ============================================================

    def _update_customer_data(
        self,
        user_message: str,
    ) -> dict[str, Any]:
        """Extract and normalize customer information."""

        extracted = extract_customer_data(user_message)

        if not extracted:
            return self.customer_data

        normalized = normalize_customer_data(extracted)

        for key, value in normalized.items():
            if value is not None:
                self.customer_data[key] = value

        return self.customer_data

    # ============================================================
    # MISSING FIELDS
    # ============================================================

    def _missing_customer_fields(self) -> list[str]:
        """Return customer fields that have not been collected."""

        return [
            field
            for field in REQUIRED_CUSTOMER_FIELDS
            if self.customer_data.get(field) is None
        ]

    # ============================================================
    # PREDICTION
    # ============================================================

    def _predict(self) -> ChatResponse:
        """Run ML prediction or request missing information."""

        missing_fields = self._missing_customer_fields()

        if missing_fields:

            field_questions = {
                "gender": "What is your gender (Male/Female)?",
                "SeniorCitizen": "Are you a senior citizen (Yes/No)?",
                "Partner": "Do you have a partner (Yes/No)?",
                "Dependents": "Do you have dependents (Yes/No)?",
                "tenure": "How many months have you been with the company?",
                "PhoneService": "Do you have phone service (Yes/No)?",
                "MultipleLines": (
                    "Do you have multiple lines " "(Yes/No/No phone service)?"
                ),
                "InternetService": (
                    "Which internet service do you use " "(DSL/Fiber optic/No)?"
                ),
                "OnlineSecurity": (
                    "Do you have online security " "(Yes/No/No internet service)?"
                ),
                "OnlineBackup": (
                    "Do you have online backup " "(Yes/No/No internet service)?"
                ),
                "DeviceProtection": (
                    "Do you have device protection " "(Yes/No/No internet service)?"
                ),
                "TechSupport": (
                    "Do you have tech support " "(Yes/No/No internet service)?"
                ),
                "StreamingTV": (
                    "Do you have streaming TV " "(Yes/No/No internet service)?"
                ),
                "StreamingMovies": (
                    "Do you have streaming movies " "(Yes/No/No internet service)?"
                ),
                "Contract": (
                    "What type of contract do you have "
                    "(Month-to-month/One year/Two year)?"
                ),
                "PaperlessBilling": ("Do you use paperless billing (Yes/No)?"),
                "PaymentMethod": ("What payment method do you use?"),
                "MonthlyCharges": ("What is your monthly charge?"),
                "TotalCharges": ("What are your total charges?"),
            }

            questions = [
                field_questions[field]
                for field in missing_fields
                if field in field_questions
            ]

            questions_to_show = questions[:5]

            answer = (
                "I can predict the customer's churn risk, but I still "
                "need a few more details.\n\n"
                + "\n".join(f"- {question}" for question in questions_to_show)
            )

            if len(questions) > 5:
                answer += (
                    "\n\nYou can provide these details in multiple "
                    "messages, or provide several of them together."
                )

            return ChatResponse(
                answer=answer,
                topic="customer churn prediction",
                confidence=1.0,
            )

        try:

            result = predict_customer(
                self.customer_data,
                model_name="random_forest",
            )

            prediction = result["prediction"]
            probability = result["churn_probability"]
            risk_level = result["risk_level"]
            model = result["model"]

            if prediction == 1:
                prediction_text = "likely to churn"
            else:
                prediction_text = "unlikely to churn"

            answer = (
                f"The {model.replace('_', ' ').title()} model predicts "
                f"that this customer is {prediction_text}. "
                f"The estimated churn probability is "
                f"{probability:.2%}, giving a {risk_level} risk level."
            )

            return ChatResponse(
                answer=answer,
                topic="churn prediction",
                confidence=1.0,
                prediction=prediction,
                churn_probability=probability,
                risk_level=risk_level,
                model=model,
            )

        except Exception as exc:

            print(f"Prediction error: {exc}")

            error_response = handle_error(PredictionError(str(exc)))

            return ChatResponse.model_validate(error_response)

    # ============================================================
    # DOCUMENT LISTING
    # ============================================================

    def _list_documents_answer(self) -> ChatResponse:
        """
        Answer meta-questions about which documents exist,
        by reading the documents directory directly rather
        than relying on RAG's semantic retrieval.
        """

        if not DOCUMENTS_DIR.exists():
            filenames: list[str] = []
        else:
            filenames = sorted(
                file_path.name
                for file_path in DOCUMENTS_DIR.iterdir()
                if file_path.is_file()
                and file_path.suffix.lower() in SUPPORTED_DOCUMENT_EXTENSIONS
            )

        if not filenames:
            answer = "There are currently no documents uploaded."

        else:
            listed = "\n".join(
                f"{index}. {filename}"
                for index, filename in enumerate(
                    filenames,
                    start=1,
                )
            )

            answer = (
                f"There {'is' if len(filenames) == 1 else 'are'} "
                f"{len(filenames)} document"
                f"{'' if len(filenames) == 1 else 's'} available:\n\n"
                f"{listed}"
            )

        return ChatResponse(
            answer=answer,
            topic="document listing",
            confidence=1.0,
            sources=filenames,
        )

    # ============================================================
    # SUMMARIZATION
    # ============================================================

    def _summarize_answer(
        self,
        user_message: str,
        source: str | None,
    ) -> ChatResponse:
        """
        Answer whole-document summary/outline questions by
        reading the full document instead of relying on
        chunk retrieval.
        """

        if source is None:
            return ChatResponse(
                answer=(
                    "To summarize a document, please select a "
                    "specific document from the 'Chat with' dropdown "
                    "first, rather than 'All Documents'."
                ),
                topic="document summary",
                confidence=1.0,
            )

        try:
            result = self.summarizer.summarize(
                source,
                user_message,
            )

            return ChatResponse(
                answer=result["answer"],
                topic="document summary",
                confidence=1.0,
                sources=result["sources"],
            )

        except FileNotFoundError:
            return ChatResponse(
                answer=f"I couldn't find the document '{source}'.",
                topic="document summary",
                confidence=1.0,
            )

        except Exception as exc:

            print(f"Summarization error: {exc}")

            return ChatResponse(
                answer=(
                    "I ran into an error trying to summarize that "
                    "document. Please try again."
                ),
                topic="document summary",
                confidence=1.0,
            )

    # ============================================================
    # RAG
    # ============================================================

    def _rag_answer(
        self,
        user_message: str,
        source: str | None = None,
    ) -> ChatResponse:
        """Answer a document-related question using RAG."""

        result = self.rag_chain.answer(
            user_message,
            source=source,
        )

        return ChatResponse(
            answer=result["answer"],
            topic="document question",
            confidence=1.0,
            sources=result["sources"],
        )

    # ============================================================
    # CHAT
    # ============================================================

    def chat(
        self,
        user_message: str,
        source: str | None = None,
    ) -> ChatResponse:
        """Generate a chatbot response."""

        # Collect customer information.
        self._update_customer_data(user_message)

        # --------------------------------------------------------
        # Prediction request
        # --------------------------------------------------------

        if is_prediction_request(user_message):

            response = self._predict()

        # --------------------------------------------------------
        # Whole-document summary / outline request
        # --------------------------------------------------------

        elif is_summary_request(user_message):

            response = self._summarize_answer(
                user_message,
                source,
            )

        # --------------------------------------------------------
        # Document listing meta-question
        # --------------------------------------------------------

        elif is_document_list_request(user_message):

            response = self._list_documents_answer()

        else:

            # ----------------------------------------------------
            # RAG document question
            # ----------------------------------------------------

            try:

                response = self._rag_answer(
                    user_message,
                    source=source,
                )

            except Exception as exc:

                print(f"RAG error: {exc}")

                # ------------------------------------------------
                # Fallback to normal LLM conversation.
                # ------------------------------------------------

                try:

                    messages = self._build_messages(user_message)

                    response: Any = self.structured_llm.invoke(messages)

                    if not isinstance(
                        response,
                        ChatResponse,
                    ):
                        response = ChatResponse.model_validate(response)

                except Exception as llm_exc:

                    print(f"LLM error: {llm_exc}")

                    error_response = handle_error(LLMError(str(llm_exc)))

                    response = ChatResponse.model_validate(error_response)

        # --------------------------------------------------------
        # Store conversation memory.
        # --------------------------------------------------------

        self.memory.add_user_message(user_message)

        self.memory.add_ai_message(response.answer)

        return response

    # ============================================================
    # STREAMING CHAT
    # ============================================================

    def chat_stream(
        self,
        user_message: str,
        source: str | None = None,
    ):
        """
        Generate a chatbot response as a stream of text chunks,
        while still going through the same routing logic as chat()
        (prediction, summary, document-list, or RAG).

        Yields:
            str chunks of the answer as they become available.
        """

        self._update_customer_data(user_message)

        full_answer = ""
        sources: list[str] = []

        if is_prediction_request(user_message):
            response = self._predict()
            full_answer = response.answer
            sources = response.sources or []
            yield full_answer

        elif is_summary_request(user_message):
            response = self._summarize_answer(user_message, source)
            full_answer = response.answer
            sources = response.sources or []
            yield full_answer

        elif is_document_list_request(user_message):
            response = self._list_documents_answer()
            full_answer = response.answer
            sources = response.sources or []
            yield full_answer

        else:

            try:
                results = self.rag_chain.retriever.search(
                    query=user_message,
                    top_k=self.rag_chain.top_k,
                    source=source,
                )

                context_parts = []

                for result in results:
                    document = result["document"]
                    doc_source = document.metadata.get("source", "unknown")
                    content = document.page_content

                    context_parts.append(f"Source: {doc_source}\nContent:\n{content}")

                    if doc_source not in sources:
                        sources.append(doc_source)

                context = "\n\n".join(context_parts)

                prompt = (
                    f"Answer the question using only the context "
                    f"below.\n\n"
                    f"Context:\n{context}\n\n"
                    f"Question: {user_message}\n\n"
                    f"Answer:"
                )

                for chunk in self.llm.stream(prompt):
                    token = getattr(chunk, "content", str(chunk))

                    if token:
                        full_answer += token
                        yield token

            except Exception as exc:

                print(f"RAG streaming error: {exc}")

                messages = self._build_messages(user_message)

                for chunk in self.llm.stream(messages):
                    token = getattr(chunk, "content", str(chunk))

                    if token:
                        full_answer += token
                        yield token

        self.memory.add_user_message(user_message)
        self.memory.add_ai_message(full_answer)

    # ============================================================
    # MEMORY
    # ============================================================

    def clear_memory(self) -> None:
        """Clear conversation memory and customer information."""

        self.memory.clear()

        self.customer_data.clear()
