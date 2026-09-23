from agent.agent import create_enterprise_agent


def main():
    """Test agent error recovery."""

    agent = create_enterprise_agent()

    thread_id = "error-recovery-test-1"

    questions = [
        "Calculate 100 divided by 0.",
        "Read the file does_not_exist.txt.",
        "Search Wikipedia for an empty query.",
    ]

    print("\n" + "=" * 70)
    print("AGENT ERROR RECOVERY TEST")
    print("=" * 70)

    for index, question in enumerate(
        questions,
        start=1,
    ):
        print("\n" + "-" * 70)
        print(f"TEST {index}")
        print("-" * 70)

        print("\nUSER:")
        print(question)

        try:
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

            print("\nAGENT:")
            print(result["messages"][-1].content)

            print("\nEXECUTION:")
            for message in result["messages"]:
                if message.type == "ai":
                    if message.tool_calls:
                        for tool_call in message.tool_calls:
                            print(f"Tool selected: " f"{tool_call['name']}")

                elif message.type == "tool":
                    print(f"Tool result from " f"{message.name}:")
                    print(message.content)

        except Exception as error:
            print("\nAGENT ERROR:")
            print(error)

    print("\n" + "=" * 70)
    print("ERROR RECOVERY TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
