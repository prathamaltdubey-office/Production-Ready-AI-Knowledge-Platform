from rag.generation.rag_chain import RAGChain

EVALUATION_DATASET = [
    {
        "query": "What factors are associated with customer churn?",
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
        "expected_keywords": [
            "month-to-month",
            "higher churn risk",
            "long-term contracts",
        ],
    },
    {
        "query": "How can companies reduce customer churn?",
        "expected_keywords": [
            "customer retention",
            "retention programs",
        ],
    },
    {
        "query": "What are the key features of the SmartHome Hub?",
        "expected_keywords": [
            "universal compatibility",
            "ai-powered assistant",
            "enhanced security",
        ],
    },
    {
        "query": "What is the projected smart home market size?",
        "expected_keywords": [
            "$135.3 billion",
            "11.6%",
        ],
    },
    {
        "query": "What is SmartTech's market share?",
        "expected_keywords": [
            "smarttech co.",
            "35%",
        ],
    },
    {
        "query": "What is the marketing strategy for the SmartHome Hub?",
        "expected_keywords": [
            "digital marketing",
            "trade shows",
            "retail partnerships",
        ],
    },
    {
        "query": "What are the next steps for the SmartHome Hub?",
        "expected_keywords": [
            "finalize production agreements",
            "pre-order website",
            "official launch event",
        ],
    },
]


def evaluate_answer(answer: str, expected_keywords: list[str]) -> list[str]:
    """Return expected keywords found in the generated answer."""

    answer_lower = answer.lower()

    return [keyword for keyword in expected_keywords if keyword.lower() in answer_lower]


def main() -> None:
    """Evaluate generated RAG answers."""

    rag = RAGChain()

    successful_queries = 0

    print("=" * 70)
    print("RAG GENERATION EVALUATION")
    print("=" * 70)

    for index, item in enumerate(EVALUATION_DATASET, start=1):

        query = item["query"]
        expected_keywords = item["expected_keywords"]

        result = rag.answer(query)

        answer = result["answer"]

        matched_keywords = evaluate_answer(
            answer,
            expected_keywords,
        )

        content_score = len(matched_keywords) / len(expected_keywords)

        success = content_score >= 0.5

        if success:
            successful_queries += 1

        print("\n" + "-" * 70)
        print(f"Query {index}: {query}")
        print("-" * 70)

        print("\nGenerated Answer:")
        print(answer)

        print("\nExpected Keywords:")
        print(expected_keywords)

        print("\nMatched Keywords:")
        print(matched_keywords)

        print(f"\nContent Score: " f"{content_score:.2f}")

        print(f"Result: " f"{'PASS' if success else 'FAIL'}")

    total_queries = len(EVALUATION_DATASET)

    evaluation_score = successful_queries / total_queries

    print("\n" + "=" * 70)
    print("FINAL GENERATION EVALUATION")
    print("=" * 70)

    print(f"Successful queries: {successful_queries}")
    print(f"Total queries: {total_queries}")

    print(f"Generation Success Rate: " f"{evaluation_score:.4f}")

    print(f"Generation Success Rate: " f"{evaluation_score * 100:.2f}%")

    print("=" * 70)


if __name__ == "__main__":
    main()
