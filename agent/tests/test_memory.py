from agent.agent import create_enterprise_agent


def main():
    """Test conversation memory."""

    agent = create_enterprise_agent()

    thread_id = "memory-test-1"

    print("=" * 70)
    print("AGENT MEMORY TEST")
    print("=" * 70)

    # First question
    question_1 = (
        "What is the market share of SmartTech Co. "
        "according to the SmartHome Hub document?"
    )

    print("\nUSER:")
    print(question_1)

    result_1 = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question_1,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    answer_1 = result_1["messages"][-1].content

    print("\nAGENT:")
    print(answer_1)

    # Follow-up question
    question_2 = "What is the projected market size mentioned " "in the same document?"

    print("\nUSER:")
    print(question_2)

    result_2 = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question_2,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    answer_2 = result_2["messages"][-1].content

    print("\nAGENT:")
    print(answer_2)

    print("\n" + "=" * 70)
    print("MEMORY TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
