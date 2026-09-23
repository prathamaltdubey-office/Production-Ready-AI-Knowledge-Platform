import wikipedia
from langchain_core.tools import tool


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for information about a topic.

    Args:
        query: Topic to search for.

    Returns:
        A concise Wikipedia summary.
    """

    try:
        if not query.strip():
            return "Error: search query cannot be empty."

        search_results = wikipedia.search(
            query,
            results=3,
        )

        if not search_results:
            return f"No Wikipedia results found for: {query}"

        page_title = search_results[0]

        summary = wikipedia.summary(
            page_title,
            sentences=5,
            auto_suggest=False,
        )

        return f"Wikipedia result for '{page_title}':\n" f"{summary}"

    except wikipedia.exceptions.DisambiguationError as exc:
        options = exc.options[:5]

        return "The query is ambiguous. " "Possible topics:\n" + "\n".join(
            f"- {option}" for option in options
        )

    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for: {query}"

    except Exception as exc:
        return f"Error searching Wikipedia: {exc}"
