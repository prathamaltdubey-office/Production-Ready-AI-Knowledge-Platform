from rag.generation.rag_chain import RAGChain


def main() -> None:
    """Test the complete RAG pipeline."""

    rag = RAGChain(top_k=5)

    question = "What factors are associated with customer churn?"

    result = rag.answer(question)

    print("\n" + "=" * 60)
    print("RAG ANSWER")
    print("=" * 60)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(f"- {source}")

    print("=" * 60)


if __name__ == "__main__":
    main()
