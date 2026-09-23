from rag.retrieval.retriever import SemanticRetriever

EVALUATION_DATASET = [
    {
        "query": "What factors are associated with customer churn?",
        "expected_source": "documents\\sample.txt",
        "expected_keywords": [
            "customer tenure",
            "contract type",
            "monthly charges",
            "internet service",
            "additional services",
        ],
    },
    {
        "query": "Which customers generally have higher churn risk?",
        "expected_source": "documents\\sample.txt",
        "expected_keywords": [
            "month-to-month",
            "higher churn risk",
            "long-term contracts",
        ],
    },
    {
        "query": "How can companies reduce customer churn?",
        "expected_source": "documents\\sample.md",
        "expected_keywords": [
            "customer retention",
            "retention programs",
        ],
    },
    {
        "query": "What are the key features of the SmartHome Hub?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "Universal Compatibility",
            "AI-Powered Assistant",
            "Enhanced Security",
        ],
    },
    {
        "query": "What is the projected smart home market size?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "$135.3 billion",
            "11.6%",
        ],
    },
    {
        "query": "What is SmartTech's market share?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "SmartTech Co.",
            "35%",
        ],
    },
    {
        "query": "What is the marketing strategy for the SmartHome Hub?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "Digital Marketing",
            "Trade Shows",
            "Retail Partnerships",
        ],
    },
    {
        "query": "What are the next steps for the SmartHome Hub?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "Finalize production agreements",
            "pre-order website",
            "official launch event",
        ],
    },
]


def calculate_recall_at_k(
    retriever: SemanticRetriever,
    evaluation_dataset: list[dict],
    k: int,
    verbose: bool = True,
) -> float:
    """
    Calculate content-aware Recall@K.

    A query is successful when:
    1. The expected source appears in the top K results.
    2. At least one expected keyword appears
       in the retrieved content.
    """

    successful_queries = 0

    if verbose:
        print("\n" + "=" * 70)
        print(f"CONTENT-AWARE RECALL@{k} EVALUATION")
        print("=" * 70)

    for index, item in enumerate(
        evaluation_dataset,
        start=1,
    ):
        query = item["query"]
        expected_source = item["expected_source"]
        expected_keywords = item["expected_keywords"]

        results = retriever.search(
            query,
            top_k=k,
        )

        retrieved_sources = [
            result["document"].metadata.get("source") for result in results
        ]

        retrieved_text = " ".join(
            result["document"].page_content for result in results
        ).lower()

        matched_keywords = [
            keyword
            for keyword in expected_keywords
            if keyword.lower() in retrieved_text
        ]

        source_hit = expected_source in retrieved_sources

        content_hit = len(matched_keywords) > 0

        hit = source_hit and content_hit

        if hit:
            successful_queries += 1

        if verbose:
            print("\n" + "-" * 70)
            print(f"Query {index}: {query}")
            print(f"Expected source: {expected_source}")
            print(f"Retrieved sources: {retrieved_sources}")
            print(f"Expected keywords: {expected_keywords}")
            print(f"Matched keywords: {matched_keywords}")
            print(f"Source hit: " f"{'YES' if source_hit else 'NO'}")
            print(f"Content hit: " f"{'YES' if content_hit else 'NO'}")
            print(f"Hit@{k}: " f"{'YES' if hit else 'NO'}")

    recall = successful_queries / len(evaluation_dataset)

    if verbose:
        print("\n" + "=" * 70)
        print(f"Successful queries: " f"{successful_queries}")
        print(f"Total queries: " f"{len(evaluation_dataset)}")
        print(f"Content Recall@{k}: " f"{recall:.4f}")
        print(f"Content Recall@{k}: " f"{recall * 100:.2f}%")
        print("=" * 70)

    return recall


def main() -> None:
    """Compare retrieval performance at different K values."""

    retriever = SemanticRetriever()

    k_values = [3, 5, 7]

    results = {}

    for k in k_values:
        recall = calculate_recall_at_k(
            retriever,
            EVALUATION_DATASET,
            k=k,
            verbose=False,
        )

        results[k] = recall

    print("\n")
    print("=" * 70)
    print("RETRIEVAL PERFORMANCE COMPARISON")
    print("=" * 70)

    for k, recall in results.items():
        print(f"Recall@{k}: " f"{recall * 100:.2f}%")

    print("=" * 70)

    best_k = max(
        results,
        key=lambda k: results[k],
    )

    print(f"\nBest retrieval depth: " f"Recall@{best_k}")


if __name__ == "__main__":
    main()
