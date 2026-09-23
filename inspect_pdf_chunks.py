from rag.chunking.text_chunker import chunk_documents
from rag.ingestion.document_loader import load_all_documents

documents = load_all_documents("documents")

chunks = chunk_documents(
    documents,
    chunk_size=500,
    chunk_overlap=50,
)

for index, chunk in enumerate(chunks):

    source = chunk.metadata.get("source", "")

    if "sample.pdf" in source:

        print("\n" + "=" * 70)
        print(f"CHUNK {index}")
        print("=" * 70)

        print(f"Source: {source}")

        print("\nContent:")
        print(chunk.page_content)
