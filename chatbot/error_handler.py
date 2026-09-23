class ChatbotError(Exception):
    """Base exception for chatbot-related errors."""


class LLMError(ChatbotError):
    """Raised when the LLM cannot be reached or fails."""


class PredictionError(ChatbotError):
    """Raised when ML prediction fails."""


class InvalidResponseError(ChatbotError):
    """Raised when the LLM returns an invalid response."""


def handle_error(error: Exception) -> dict:
    """Convert an exception into a safe chatbot response."""

    if isinstance(error, LLMError):
        message = (
            "The AI service is currently unavailable. "
            "Please make sure Ollama is running."
        )

    elif isinstance(error, PredictionError):
        message = (
            "I could not complete the churn prediction. "
            "Please check the customer information and try again."
        )

    elif isinstance(error, InvalidResponseError):
        message = (
            "The AI returned an invalid response. "
            "Please try asking the question again."
        )

    else:
        message = (
            "Something went wrong while processing your request. " "Please try again."
        )

    return {
        "answer": message,
        "topic": "error",
        "confidence": 0.0,
        "prediction": None,
        "churn_probability": None,
        "risk_level": None,
        "model": None,
    }
