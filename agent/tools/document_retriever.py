from langchain_core.tools import tool

from rag.retrieval.retriever import SemanticRetriever


@tool
def document_retriever(query: str) -> str:
    """
    Search the enterprise document collection and return
    the most relevant document chunks.

    Use this tool when the user asks a question that may
    be answered from the organization's documents.
    """

    if not query.strip():
        return "Error: search query cannot be empty."

    try:
        retriever = SemanticRetriever()

        results = retriever.search(
            query=query,
            top_k=5,
        )

        if not results:
            return "No relevant documents found."

        output = []

        for index, result in enumerate(
            results,
            start=1,
        ):
            document = result["document"]

            source = document.metadata.get(
                "source",
                "unknown",
            )

            content = document.page_content

            output.append(
                f"Result {index}\n" f"Source: {source}\n" f"Content:\n{content}"
            )

        return "\n\n".join(output)

    except Exception as exc:
        return f"Error retrieving documents: {exc}"
