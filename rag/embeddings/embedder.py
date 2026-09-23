from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


class DocumentEmbedder:
    """Generate embeddings for document chunks."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents):
        """
        Generate embeddings for LangChain documents.

        Args:
            documents: List of LangChain Document objects.

        Returns:
            List of numerical embedding vectors.
        """

        texts = [document.page_content for document in documents]

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

    def embed_query(self, query: str):
        """
        Generate an embedding for a user query.

        Args:
            query: User's question.

        Returns:
            Numerical embedding vector.
        """

        return self.model.encode(
            query,
            convert_to_numpy=True,
        )
