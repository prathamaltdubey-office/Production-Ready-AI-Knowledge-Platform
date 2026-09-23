from pathlib import Path

import faiss
import numpy as np

from rag.chunking.text_chunker import chunk_documents
from rag.embeddings.embedder import DocumentEmbedder
from rag.ingestion.document_loader import load_all_documents

INDEX_PATH = Path("rag/vectorstore/index.faiss")


class SemanticRetriever:
    """Retrieve document chunks using semantic similarity."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:

        self.embedder = DocumentEmbedder()

        self.index = faiss.read_index(str(INDEX_PATH))

        documents = load_all_documents("documents")

        self.chunks = chunk_documents(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
        source: str | None = None,
    ) -> list[dict]:
        """
        Retrieve relevant chunks using semantic similarity.

        Args:
            query: User's search query.
            top_k: Number of results to return.
            source: Optional document source filter.

        Returns:
            Retrieved chunks with similarity distances.
        """

        query_embedding = self.embedder.embed_query(query)

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        # Search all candidates when filtering.
        search_k = len(self.chunks) if source else top_k

        distances, indices = self.index.search(
            query_embedding,
            search_k,
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0],
        ):
            if index == -1:
                continue

            document = self.chunks[index]

            # Apply metadata filter (compare by filename only,
            # since metadata "source" may include a directory prefix).
            if source is not None:
                document_source = document.metadata.get("source")

                if document_source is None:
                    continue

                if Path(document_source).name != Path(source).name:
                    continue

            results.append(
                {
                    "document": document,
                    "distance": float(distance),
                }
            )

            if len(results) >= top_k:
                break

        return results
