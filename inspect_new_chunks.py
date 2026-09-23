from rag.chunking.text_chunker import chunk_documents
from rag.ingestion.document_loader import load_all_documents

documents = load_all_documents("documents")

chunks = chunk_documents(
    documents,
    chunk_size=500,
    chunk_overlap=50,
)

print("=" * 70)
print("NEW CHUNKING RESULT")
print("=" * 70)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):

    print("\n" + "-" * 70)
    print(f"CHUNK {i}")
    print("-" * 70)

    print(f"Source: " f"{chunk.metadata.get('source')}")

    print("\nContent:")
    print(chunk.page_content)
