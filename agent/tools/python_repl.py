from langchain_core.tools import tool

# Only these builtins are allowed inside the Python REPL tool.
# This blocks file access, imports, and system calls, while still
# allowing normal calculations and data manipulation.
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "print": print,
    "range": range,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}


@tool
def python_repl(code: str) -> str:
    """
    Execute Python code and return the result.

    For safety, only a restricted set of builtins is available —
    file access, network calls, imports, and system commands are
    blocked. This tool is intended for calculations and simple
    data processing only.

    Args:
        code: Python code to execute.

    Returns:
        Output or result produced by the code.
    """

    try:
        if not code.strip():
            return "Error: Python code cannot be empty."

        # Block obviously dangerous patterns before execution,
        # as a first line of defense in addition to restricted builtins.
        forbidden_patterns = [
            "import ",
            "__import__",
            "open(",
            "exec(",
            "eval(",
            "compile(",
            "input(",
            "__builtins__",
            "os.",
            "sys.",
            "subprocess",
        ]

        lowered_code = code.lower()

        for pattern in forbidden_patterns:
            if pattern in lowered_code:
                return (
                    f"Error: use of '{pattern.strip()}' is not "
                    "allowed in this sandboxed environment."
                )

        namespace = {}

        exec(
            code,
            {"__builtins__": SAFE_BUILTINS},
            namespace,
        )

        if "result" in namespace:
            return str(namespace["result"])

        return "Python code executed successfully."

    except Exception as exc:
        return f"Error executing Python code: {exc}"
