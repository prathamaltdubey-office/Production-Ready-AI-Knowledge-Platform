from agent.agent import run_agent


def main() -> None:
    question = (
        "What is SmartTech Co.'s market share according to "
        "the SmartHome Hub document, and calculate what "
        "35% of the projected $135.3 billion smart home "
        "market would be?"
    )

    print("\n" + "=" * 70)
    print("MULTI-STEP AGENT TEST")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    result = run_agent(question)

    print("\n" + "=" * 70)
    print("AGENT EXECUTION")
    print("=" * 70)

    for message in result["messages"]:
        print(f"\nMessage type: {message.type}")

        if hasattr(message, "tool_calls") and message.tool_calls:
            print("Tool calls:")

            for tool_call in message.tool_calls:
                print(f"- {tool_call['name']}: " f"{tool_call['args']}")

        if message.content:
            print("Content:")
            print(message.content)

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    final_message = result["messages"][-1]

    print(final_message.content)


if __name__ == "__main__":
    main()
