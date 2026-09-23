from rag.retrieval.retriever import SemanticRetriever

retriever = SemanticRetriever(
    chunk_size=500,
    chunk_overlap=50,
)


queries = [
    "What are the key features of the SmartHome Hub?",
    "What is the marketing strategy for the SmartHome Hub?",
    "What are the next steps for the SmartHome Hub?",
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY")
    print("=" * 70)
    print(query)

    results = retriever.search(
        query,
        top_k=11,
    )

    for i, result in enumerate(results, start=1):

        document = result["document"]
        distance = result["distance"]

        print("\n" + "-" * 70)
        print(f"RANK {i}")
        print("-" * 70)

        print(f"Distance: {distance:.4f}")
        print(f"Source: {document.metadata.get('source')}")
        print()
        print(document.page_content)
