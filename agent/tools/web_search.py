from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query.

    Returns:
        Search results containing titles, URLs, and snippets.
    """

    try:
        if not query.strip():
            return "Error: search query cannot be empty."

        results = DDGS().text(
            query,
            max_results=5,
        )

        results = list(results)

        if not results:
            return f"No web search results found for: {query}"

        formatted_results = []

        for index, result in enumerate(
            results,
            start=1,
        ):
            title = result.get(
                "title",
                "No title",
            )

            url = result.get(
                "href",
                "No URL",
            )

            snippet = result.get(
                "body",
                "No description",
            )

            formatted_results.append(
                f"{index}. {title}\n" f"URL: {url}\n" f"Summary: {snippet}"
            )

        return "\n\n".join(formatted_results)

    except Exception as exc:
        return f"Error performing web search: {exc}"
