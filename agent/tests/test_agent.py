from agent.agent import run_agent


def main() -> None:
    """Test the multi-tool enterprise agent."""

    questions = [
        "What are the key features of the SmartHome Hub?",
        "What is 125 multiplied by 48?",
        "What is artificial intelligence?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print("QUESTION")
        print("=" * 70)

        print(question)

        result = run_agent(question)

        print("\n" + "=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        messages = result["messages"]

        for message in reversed(messages):

            if message.type == "ai" and message.content:
                print(message.content)
                break


if __name__ == "__main__":
    main()
