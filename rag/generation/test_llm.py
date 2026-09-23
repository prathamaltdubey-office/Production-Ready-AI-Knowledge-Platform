from rag.generation.llm import OllamaLLM


def main() -> None:
    """Test the local Ollama LLM."""

    llm = OllamaLLM()

    prompt = """
Answer this question in one sentence:

What is customer churn?
"""

    response = llm.generate(prompt)

    print("\n==============================")
    print("LLM RESPONSE")
    print("==============================")
    print(response)


if __name__ == "__main__":
    main()
