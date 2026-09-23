import requests

API_URL = "http://127.0.0.1:8000"


def predict_customer(
    customer: dict,
    model_name: str = "random_forest",
) -> dict:
    """
    Send customer information to the FastAPI prediction endpoint.

    Args:
        customer: Customer information required by the ML model.
        model_name: Model to use for prediction.

    Returns:
        Prediction response from the FastAPI service.

    Raises:
        requests.RequestException: If the prediction API cannot be reached.
        ValueError: If the API returns an unsuccessful response.
    """

    response = requests.post(
        f"{API_URL}/predict",
        params={"model_name": model_name},
        json=customer,
        timeout=30,
    )

    if response.status_code != 200:
        raise ValueError(
            f"Prediction API returned {response.status_code}: " f"{response.text}"
        )

    return response.json()
