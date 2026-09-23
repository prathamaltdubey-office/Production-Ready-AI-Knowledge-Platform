import json
import re
from typing import Any

from chatbot.llm import get_llm

EXTRACTION_PROMPT = """
You extract customer information for a telecom customer churn prediction system.

Extract ONLY information explicitly provided by the user.

Return ONLY valid JSON.

Allowed fields:

gender
SeniorCitizen
Partner
Dependents
tenure
PhoneService
MultipleLines
InternetService
OnlineSecurity
OnlineBackup
DeviceProtection
TechSupport
StreamingTV
StreamingMovies
Contract
PaperlessBilling
PaymentMethod
MonthlyCharges
TotalCharges

Rules:

- Do not invent missing values.
- Do not guess values.
- If a field is not mentioned, do not include it.
- SeniorCitizen must be 0 or 1.
- tenure must be a number.
- MonthlyCharges must be a number.
- TotalCharges must be a number.
- Return only a JSON object.
"""


def _extract_json(text: str) -> dict[str, Any]:
    """Extract a JSON object from the LLM response."""

    text = text.strip()

    # ---------------------------------------------------------
    # Try parsing the complete response as JSON
    # ---------------------------------------------------------

    try:
        result = json.loads(text)

        if isinstance(result, dict):
            return result

    except json.JSONDecodeError:
        pass

    # ---------------------------------------------------------
    # Try finding a JSON object inside the response
    # ---------------------------------------------------------

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            result = json.loads(match.group())

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

    return {}


def _content_to_string(content: Any) -> str:
    """
    Convert LangChain response content into a plain string.

    LangChain may return content as either:
        - a string
        - a list containing strings/dictionaries

    This function normalizes both cases to a string.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                # Some LangChain providers return dictionaries
                # containing text.
                if "text" in item:
                    parts.append(str(item["text"]))

                elif "content" in item:
                    parts.append(str(item["content"]))

                else:
                    parts.append(str(item))

            else:
                parts.append(str(item))

        return "".join(parts)

    return str(content)


def extract_customer_data(message: str) -> dict[str, Any]:
    """
    Extract explicitly provided customer information from a message.

    Args:
        message:
            Natural-language customer information.

    Returns:
        Dictionary containing extracted customer fields.
    """

    llm = get_llm()

    prompt = f"""
{EXTRACTION_PROMPT}

User message:
{message}
"""

    response = llm.invoke(prompt)

    # ---------------------------------------------------------
    # Normalize LangChain response content to string
    # ---------------------------------------------------------

    response_text = _content_to_string(response.content)

    # ---------------------------------------------------------
    # Extract JSON
    # ---------------------------------------------------------

    return _extract_json(response_text)
