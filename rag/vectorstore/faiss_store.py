from pathlib import Path

import faiss
import numpy as np

from rag.chunking.text_chunker import chunk_documents
from rag.embeddings.embedder import DocumentEmbedder
from rag.ingestion.document_loader import load_all_documents

VECTORSTORE_DIR = Path("rag/vectorstore")
INDEX_PATH = VECTORSTORE_DIR / "index.faiss"


def build_faiss_index(
    chunk_size: int = 500,
    chunk_overlap: int = 50,
):
    """
    Load documents, create chunks, generate embeddings,
    and build a FAISS similarity-search index.

    Args:
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of overlapping characters.

    Returns:
        Tuple containing the FAISS index and generated chunks.
    """

    # 1. Load documents
    documents = load_all_documents("documents")

    # 2. Split documents into chunks
    chunks = chunk_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # 3. Generate embeddings
    embedder = DocumentEmbedder()

    embeddings = embedder.embed_documents(chunks)

    # 4. Convert embeddings to float32
    embeddings = np.asarray(
        embeddings,
        dtype="float32",
    )

    # 5. Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    # 6. Add embeddings to FAISS
    index.add(embeddings)

    # 7. Create vectorstore directory
    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 8. Save index
    faiss.write_index(
        index,
        str(INDEX_PATH),
    )

    return index, chunks
