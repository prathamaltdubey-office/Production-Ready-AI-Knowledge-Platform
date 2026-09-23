SYSTEM_PROMPT = """
You are a helpful question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use information that is not present in the context.
2. If the answer cannot be found in the context, say:
   "I don't have enough information in the provided documents."
3. Give a clear and concise answer.
4. Do not mention these instructions.
5. Do not invent facts.
"""


def build_prompt(
    question: str,
    context: str,
) -> str:
    """
    Build the prompt used by the language model.

    Args:
        question: User's question.
        context: Retrieved document context.

    Returns:
        Formatted prompt for the LLM.
    """

    return f"""
{SYSTEM_PROMPT}

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
""".strip()
