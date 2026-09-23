from rag.chunking.text_chunker import chunk_documents
from rag.embeddings.embedder import DocumentEmbedder
from rag.ingestion.document_loader import load_all_documents

documents = load_all_documents("documents")

chunks = chunk_documents(
    documents,
    chunk_size=200,
    chunk_overlap=30,
)

embedder = DocumentEmbedder()

embeddings = embedder.embed_documents(chunks)

print("Documents:", len(documents))
print("Chunks:", len(chunks))
print("Embeddings shape:", embeddings.shape)

query = "What factors increase customer churn?"

query_embedding = embedder.embed_query(query)

print("Query embedding shape:", query_embedding.shape)
