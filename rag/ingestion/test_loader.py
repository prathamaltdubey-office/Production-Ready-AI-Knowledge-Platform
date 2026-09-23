from rag.ingestion.document_loader import load_all_documents

documents = load_all_documents("documents")

print(f"Total documents/pages loaded: {len(documents)}")

for index, document in enumerate(documents, start=1):
    print("\n==============================")
    print(f"DOCUMENT {index}")
    print("==============================")

    print("Source:")
    print(document.metadata.get("source"))

    print("\nContent:")
    print(document.page_content[:500])
