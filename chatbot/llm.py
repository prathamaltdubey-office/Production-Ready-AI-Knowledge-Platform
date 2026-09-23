import os

from langchain_ollama import ChatOllama


def get_llm():
    """Return the local Ollama Llama 3 model."""

    return ChatOllama(
        model="llama3.2:3b",
        temperature=0.2,
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
    )


def stream_response(message: str):
    """Stream an LLM response token by token."""

    llm = get_llm()

    for chunk in llm.stream(message):
        if chunk.content:
            yield chunk.content
