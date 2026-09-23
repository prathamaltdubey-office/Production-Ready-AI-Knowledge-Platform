from rag.generation.rag_generator import RAGGenerator
from rag.retrieval.retriever import SemanticRetriever


class RAGChain:
    """Complete Retrieval-Augmented Generation pipeline."""

    def __init__(
        self,
        top_k: int = 7,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
    ) -> None:
        self.retriever = SemanticRetriever(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.generator = RAGGenerator()

        self.top_k = top_k

    def answer(
        self,
        question: str,
        source: str | None = None,
    ) -> dict:
        """
        Retrieve relevant documents and generate an answer.

        Args:
            question: User's question.
            source: Optional filename to restrict retrieval to
                a single document. When None, searches all
                documents.

        Returns:
            Dictionary containing the answer and sources.
        """

        if not question.strip():
            raise ValueError("question cannot be empty")

        # 1. Retrieve relevant chunks (optionally scoped to one document)
        results = self.retriever.search(
            query=question,
            top_k=self.top_k,
            source=source,
        )

        if source is not None and not results:
            return {
                "answer": (
                    f"I couldn't find any relevant information "
                    f"in '{source}' to answer that question."
                ),
                "sources": [],
            }

        # 2. Build context from retrieved chunks
        context_parts = []
        sources = []

        for result in results:
            document = result["document"]

            doc_source = document.metadata.get(
                "source",
                "unknown",
            )

            content = document.page_content

            context_parts.append(f"Source: {doc_source}\n" f"Content:\n{content}")

            if doc_source not in sources:
                sources.append(doc_source)

        context = "\n\n".join(context_parts)

        # 3. Generate grounded answer
        answer = self.generator.generate(
            question=question,
            context=context,
        )

        # 4. Return answer + sources
        return {
            "answer": answer,
            "sources": sources,
        }
