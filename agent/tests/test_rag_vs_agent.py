from agent.agent import create_enterprise_agent
from rag.generation.rag_chain import RAGChain

QUESTIONS = [
    "What are the key features of the SmartHome Hub?",
    "What is SmartTech Co.'s market share?",
    "What is 125 multiplied by 48?",
]


def run_standard_rag(question: str):
    """Run the question using the standard RAG pipeline."""

    rag = RAGChain(top_k=7)

    result = rag.answer(question)

    return result


def run_agent(question: str, agent, thread_id: str):
    """Run the question using the multi-tool agent."""

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

    return result


def main():
    """Compare standard RAG with Agentic AI."""

    print("\n" + "=" * 70)
    print("STANDARD RAG VS AGENTIC AI")
    print("=" * 70)

    rag = RAGChain(top_k=7)
    agent = create_enterprise_agent()

    for index, question in enumerate(
        QUESTIONS,
        start=1,
    ):
        print("\n" + "=" * 70)
        print(f"QUESTION {index}")
        print("=" * 70)

        print(f"\nQuestion:\n{question}")

        # --------------------------------------------------
        # STANDARD RAG
        # --------------------------------------------------

        print("\n" + "-" * 70)
        print("STANDARD RAG")
        print("-" * 70)

        rag_result = rag.answer(question)

        print("\nAnswer:")
        print(rag_result["answer"])

        print("\nSources:")
        print(rag_result["sources"])

        # --------------------------------------------------
        # AGENTIC AI
        # --------------------------------------------------

        print("\n" + "-" * 70)
        print("AGENTIC AI")
        print("-" * 70)

        agent_result = run_agent(
            question,
            agent,
            f"comparison-{index}",
        )

        print("\nExecution:")

        for message in agent_result["messages"]:

            if message.type == "ai":
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"Tool selected: " f"{tool_call['name']}")

            elif message.type == "tool":
                print(f"Tool result: " f"{message.name}")

        print("\nFinal Answer:")
        print(agent_result["messages"][-1].content)

    print("\n" + "=" * 70)
    print("COMPARISON COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
