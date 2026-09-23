import os
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama


class RAGGenerator:
    """Generate grounded answers using retrieved document context."""

    def __init__(self) -> None:
        self.llm = ChatOllama(
            model="llama3:8b",
            temperature=0.2,
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            ),
        )

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate a grounded answer from retrieved document context.

        Args:
            question: User's question.
            context: Retrieved document content including sources.

        Returns:
            LLM-generated answer.
        """

        system_prompt = """
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the provided
document context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts.
3. If the answer is not present in the context,
   say that the information is not available
   in the provided documents.
4. Give a concise and clear answer.
5. Use the document context to support every factual claim.
6. Do not create fake citations.
7. Do not mention information that is not present
   in the provided context.
"""

        user_prompt = f"""
Document Context:

{context}

Question:

{question}

Answer:
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        response: Any = self.llm.invoke(messages)

        content = response.content

        # ChatOllama can expose content as either a string
        # or structured content blocks.
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts: list[str] = []

            for item in content:
                if isinstance(item, str):
                    text_parts.append(item)

                elif isinstance(item, dict):
                    text = item.get("text")

                    if isinstance(text, str):
                        text_parts.append(text)

            return "".join(text_parts)

        return str(content)
