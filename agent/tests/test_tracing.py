from agent.agent import create_enterprise_agent


def main():
    """Test and display agent execution tracing."""

    agent = create_enterprise_agent()

    thread_id = "tracing-test-1"

    question = (
        "What is SmartTech Co.'s market share according to "
        "the SmartHome Hub document, and calculate what 35% "
        "of the projected $135.3 billion smart home market would be?"
    )

    print("\n" + "=" * 70)
    print("AGENT EXECUTION TRACE")
    print("=" * 70)

    print("\nUSER QUESTION:")
    print(question)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    print("\n" + "-" * 70)
    print("EXECUTION STEPS")
    print("-" * 70)

    tool_call_count = 0

    for index, message in enumerate(
        result["messages"],
        start=1,
    ):
        print(f"\nSTEP {index}")
        print(f"Message type: {message.type}")

        if message.type == "human":
            print("Role: USER")
            print(f"Content: {message.content}")

        elif message.type == "ai":
            print("Role: AGENT")

            if message.tool_calls:
                print("Tool calls:")

                for tool_call in message.tool_calls:
                    tool_call_count += 1

                    print(f"  - {tool_call['name']}")

                    print(f"    Arguments: " f"{tool_call['args']}")

            if message.content:
                print(f"Agent content: " f"{message.content}")

        elif message.type == "tool":
            print("Role: TOOL")
            print(f"Tool name: " f"{message.name}")

            print(f"Tool result:\n" f"{message.content}")

    print("\n" + "-" * 70)
    print("TRACE SUMMARY")
    print("-" * 70)

    print(f"Total messages: " f"{len(result['messages'])}")

    print(f"Total tool calls: " f"{tool_call_count}")

    print("\n" + "=" * 70)
    print("EXECUTION TRACE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
