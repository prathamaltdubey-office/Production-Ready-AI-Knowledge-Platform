from typing import Final

PREDICTION_KEYWORDS: Final[tuple[str, ...]] = (
    "predict churn",
    "predict whether",
    "will this customer churn",
    "will the customer churn",
    "churn prediction",
    "predict customer",
    "churn risk",
    "risk of churn",
)


def is_prediction_request(message: str) -> bool:
    """
    Determine whether a user message is asking for a churn prediction.

    Args:
        message:
            User's natural-language message.

    Returns:
        True if the message appears to request a churn prediction.
        Otherwise False.
    """

    normalized = message.lower().strip()

    return any(keyword in normalized for keyword in PREDICTION_KEYWORDS)
