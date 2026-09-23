from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Args:
        expression: Mathematical expression such as
            '25 * 18' or '(100 + 50) / 2'.

    Returns:
        Result of the calculation.
    """

    try:
        allowed_characters = set("0123456789+-*/().% ")

        if not set(expression) <= allowed_characters:
            return "Error: expression contains " "unsupported characters."

        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return str(result)

    except Exception as exc:
        return f"Error calculating expression: {exc}"
