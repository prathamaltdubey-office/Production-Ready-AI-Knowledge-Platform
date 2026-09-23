from chatbot.error_handler import (
    ChatbotError,
    InvalidResponseError,
    LLMError,
    PredictionError,
    handle_error,
)


def test_llm_error():
    error = LLMError("Ollama unavailable")

    result = handle_error(error)

    assert result["answer"] == (
        "The AI service is currently unavailable. "
        "Please make sure Ollama is running."
    )
    assert result["topic"] == "error"
    assert result["confidence"] == 0.0
    assert result["prediction"] is None
    assert result["churn_probability"] is None
    assert result["risk_level"] is None
    assert result["model"] is None


def test_prediction_error():
    error = PredictionError("Prediction failed")

    result = handle_error(error)

    assert result["answer"] == (
        "I could not complete the churn prediction. "
        "Please check the customer information and try again."
    )
    assert result["topic"] == "error"
    assert result["confidence"] == 0.0


def test_invalid_response_error():
    error = InvalidResponseError("Invalid JSON")

    result = handle_error(error)

    assert result["answer"] == (
        "The AI returned an invalid response. " "Please try asking the question again."
    )
    assert result["topic"] == "error"
    assert result["confidence"] == 0.0


def test_generic_chatbot_error():
    error = ChatbotError("Something went wrong")

    result = handle_error(error)

    assert result["topic"] == "error"
    assert result["confidence"] == 0.0
    assert result["prediction"] is None
    assert result["churn_probability"] is None
    assert result["risk_level"] is None
    assert result["model"] is None


def test_unexpected_error():
    error = ValueError("Unexpected error")

    result = handle_error(error)

    assert result["topic"] == "error"
    assert result["confidence"] == 0.0
