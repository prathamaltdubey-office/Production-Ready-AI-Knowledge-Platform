from rag.chunking.text_chunker import chunk_documents
from rag.ingestion.document_loader import load_all_documents

documents = load_all_documents("documents")

chunks = chunk_documents(
    documents,
    chunk_size=200,
    chunk_overlap=30,
)

print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print("\n==============================")
    print(f"CHUNK {index}")
    print("==============================")

    print("Source:")
    print(chunk.metadata.get("source"))

    print("\nContent:")
    print(chunk.page_content)
