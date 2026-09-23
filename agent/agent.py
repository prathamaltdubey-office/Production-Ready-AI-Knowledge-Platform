from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from agent.tools.calculator import calculator
from agent.tools.document_retriever import document_retriever
from agent.tools.file_reader import file_reader
from agent.tools.python_repl import python_repl
from agent.tools.web_search import web_search
from agent.tools.wikipedia import wikipedia_search

MODEL_NAME = "qwen2.5:7b"
OLLAMA_BASE_URL = "http://localhost:11434"


SYSTEM_PROMPT = """
You are an enterprise knowledge assistant.

You have access to several tools.

Use the tools intelligently based on the user's request.

Available tools:

1. Calculator
   Use for mathematical calculations.

2. Wikipedia
   Use for general factual knowledge and explanations.

3. DuckDuckGo Search
   Use when the user needs web search or current information.

4. Python REPL
   Use when Python execution is useful for calculations,
   data processing, or programming-related tasks.

5. File Reader
   Use when the user explicitly asks to read a local file.

6. Document Retriever
   Use when the question may be answered using the
   enterprise document collection.

Rules:

- Select the most appropriate tool for the user's request.
- You may use multiple tools when necessary.
- Do not invent tool results.
- If a tool returns an error, handle the error gracefully.
- For enterprise document questions, prefer the Document Retriever.
- Use conversation history when answering follow-up questions.
- Give a concise final answer.
"""


# Module-level checkpointer, shared across all calls to run_agent().
# This is what makes conversation memory actually persist between
# calls for the same thread_id, instead of resetting every time.
_shared_checkpointer = InMemorySaver()

# Module-level agent, built once and reused, rather than rebuilt
# (and re-initialized with a fresh checkpointer) on every call.
_shared_agent = None


def create_enterprise_agent():
    """
    Create the enterprise multi-tool AI agent with memory.

    Uses a module-level checkpointer so that memory actually
    persists across separate calls to run_agent() for the same
    thread_id, rather than being wiped every call.
    """

    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=0.2,
        base_url=OLLAMA_BASE_URL,
    )

    tools = [
        calculator,
        wikipedia_search,
        web_search,
        python_repl,
        file_reader,
        document_retriever,
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=_shared_checkpointer,
    )

    return agent


def get_agent():
    """
    Return a single, reused agent instance.

    Building the agent once (rather than per-call) avoids
    reloading the LLM connection and tools on every request,
    and ensures the shared checkpointer is actually shared.
    """

    global _shared_agent

    if _shared_agent is None:
        _shared_agent = create_enterprise_agent()

    return _shared_agent


def run_agent(
    question: str,
    thread_id: str = "enterprise-session",
):
    """
    Run the agent while preserving conversation history.

    The same thread_id represents the same conversation.
    Because the agent and its checkpointer are now reused
    across calls (see get_agent()), memory genuinely persists
    for a given thread_id across multiple run_agent() calls —
    unlike the previous version, which rebuilt the checkpointer
    (and therefore wiped memory) on every single call.
    """

    agent = get_agent()

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


if __name__ == "__main__":
    result = run_agent("What are the key features of the SmartHome Hub?")

    print("\n" + "=" * 70)
    print("AGENT RESPONSE")
    print("=" * 70)

    for message in result["messages"]:
        print(f"\n{message.type}:")
        print(message.content)
