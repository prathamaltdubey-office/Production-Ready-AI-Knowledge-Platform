from rag.retrieval.retriever import SemanticRetriever

retriever = SemanticRetriever()


QUERIES = [
    "What are the key features of the SmartHome Hub?",
    "What is the marketing strategy for the SmartHome Hub?",
]


for query in QUERIES:

    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    for top_k in [3, 5, 7]:

        results = retriever.search(
            query=query,
            top_k=top_k,
        )

        print("\n" + "-" * 70)
        print(f"TOP_K = {top_k}")
        print("-" * 70)

        print(f"Results returned: {len(results)}")

        for index, result in enumerate(results, start=1):

            document = result["document"]

            print("\n" + "-" * 40)
            print(f"RESULT {index}")
            print("-" * 40)

            print("Distance:", result["distance"])
            print("Source:", document.metadata.get("source"))

            print("Content:")
            print(document.page_content)
