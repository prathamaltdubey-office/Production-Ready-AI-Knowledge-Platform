"""
Utility functions for the FastAPI inference service.
"""

from typing import Any

import pandas as pd


def customer_to_dataframe(customer: Any) -> pd.DataFrame:
    """
    Convert validated customer data into a pandas DataFrame.

    Args:
        customer: Pydantic customer request object.

    Returns:
        DataFrame containing one customer record.
    """

    if hasattr(customer, "model_dump"):
        data = customer.model_dump()
    else:
        data = customer.dict()

    return pd.DataFrame([data])


def get_risk_level(churn_probability: float) -> str:
    """
    Convert churn probability into a risk category.

    Args:
        churn_probability: Probability of customer churn.

    Returns:
        Risk category.
    """

    if churn_probability >= 0.70:
        return "High"

    if churn_probability >= 0.40:
        return "Medium"

    return "Low"


def get_prediction_result(
    prediction: int,
    probability: float,
) -> dict[str, Any]:
    """
    Create a standardized prediction result.

    Args:
        prediction: Model prediction, 0 or 1.
        probability: Probability of churn.

    Returns:
        Dictionary containing prediction information.
    """

    return {
        "prediction": int(prediction),
        "churn_probability": float(probability),
        "risk_level": get_risk_level(probability),
    }
