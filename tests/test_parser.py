from chatbot.parser import parse_response


def test_parse_valid_response():
    response = """
    {
        "answer": "Customer churn is when a customer leaves.",
        "topic": "churn",
        "confidence": 0.9
    }
    """

    result = parse_response(response)

    assert result["answer"] == "Customer churn is when a customer leaves."
    assert result["topic"] == "churn"
    assert result["confidence"] == 0.9


def test_parse_prediction_response():
    response = """
    {
        "answer": "The customer has low churn risk.",
        "topic": "churn prediction",
        "confidence": 1.0,
        "prediction": 0,
        "churn_probability": 0.2938,
        "risk_level": "Low",
        "model": "random_forest"
    }
    """

    result = parse_response(response)

    assert result["prediction"] == 0
    assert result["churn_probability"] == 0.2938
    assert result["risk_level"] == "Low"
    assert result["model"] == "random_forest"


def test_parse_invalid_response():
    response = "This is not JSON."

    result = parse_response(response)

    assert result["answer"] == "This is not JSON."
    assert result["confidence"] == 0.0
    assert result["prediction"] is None
