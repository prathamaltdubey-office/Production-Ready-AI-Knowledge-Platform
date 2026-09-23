from rag.retrieval.retriever import SemanticRetriever

queries = [
    "What are the key features of the SmartHome Hub?",
    "What is the marketing strategy for the SmartHome Hub?",
]


retriever = SemanticRetriever(
    chunk_size=500,
    chunk_overlap=50,
)


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY")
    print("=" * 70)

    print(query)

    results = retriever.search(
        query,
        top_k=3,
    )

    for rank, result in enumerate(results, start=1):

        document = result["document"]
        distance = result["distance"]

        print("\n" + "-" * 70)
        print(f"RESULT {rank}")
        print("-" * 70)

        print(f"Distance: {distance:.4f}")
        print(f"Source: " f"{document.metadata.get('source')}")

        print("\nContent:")
        print(document.page_content)
