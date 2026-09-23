from pathlib import Path

from rag.ingestion.document_loader import load_document

# Rough character budget per LLM call, conservative for a
# 7B local model's context window.
MAX_CHARS_PER_CALL = 6000


class DocumentSummarizer:
    """Summarize a whole document, bypassing chunk retrieval."""

    def __init__(self, llm) -> None:
        """
        Args:
            llm: A LangChain-compatible chat model with an
                .invoke() method accepting plain strings or
                message lists.
        """

        self.llm = llm

    def _load_full_text(self, filename: str) -> str:
        """Load and concatenate the full text of a document."""

        documents_dir = Path("documents")
        file_path = documents_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {filename}")

        documents = load_document(str(file_path))

        return "\n\n".join(document.page_content for document in documents)

    def _summarize_chunk(self, text: str, question: str) -> str:
        """Summarize a single chunk of text with respect to the question."""

        prompt = (
            "You are summarizing part of a larger document. "
            "Answer the user's request using only the text below. "
            "Be concise and factual.\n\n"
            f"User request: {question}\n\n"
            f"Document section:\n{text}\n\n"
            "Summary of this section:"
        )

        response = self.llm.invoke(prompt)

        return getattr(response, "content", str(response))

    def summarize(self, filename: str, question: str) -> dict:
        """
        Summarize a full document, using map-reduce if it
        exceeds a single LLM call's practical size.

        Args:
            filename: The document to summarize.
            question: The user's original request (e.g.
                "summarize this" or "give me the table of contents").

        Returns:
            Dictionary with "answer" and "sources".
        """

        full_text = self._load_full_text(filename)

        if not full_text.strip():
            return {
                "answer": (
                    f"'{filename}' appears to contain no "
                    "extractable text, so I can't summarize it. "
                    "This can happen with scanned or image-only PDFs."
                ),
                "sources": [filename],
            }

        # --------------------------------------------------------
        # Short document: summarize directly in one call.
        # --------------------------------------------------------

        if len(full_text) <= MAX_CHARS_PER_CALL:
            answer = self._summarize_chunk(full_text, question)

            return {
                "answer": answer,
                "sources": [filename],
            }

        # --------------------------------------------------------
        # Long document: map-reduce.
        # Step 1: split into sections and summarize each.
        # Step 2: combine section summaries into one final answer.
        # --------------------------------------------------------

        sections = [
            full_text[i : i + MAX_CHARS_PER_CALL]
            for i in range(0, len(full_text), MAX_CHARS_PER_CALL)
        ]

        section_summaries = [
            self._summarize_chunk(section, question) for section in sections
        ]

        combined = "\n\n".join(
            f"Section {index + 1} summary:\n{summary}"
            for index, summary in enumerate(section_summaries)
        )

        final_prompt = (
            "Below are summaries of consecutive sections of a "
            "document, in order. Combine them into one coherent "
            f"response to the user's original request.\n\n"
            f"User request: {question}\n\n"
            f"{combined}\n\n"
            "Combined response:"
        )

        final_response = self.llm.invoke(final_prompt)

        answer = getattr(final_response, "content", str(final_response))

        return {
            "answer": answer,
            "sources": [filename],
        }
