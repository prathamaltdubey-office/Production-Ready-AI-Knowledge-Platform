from typing import Any

CUSTOMER_FIELDS: tuple[str, ...] = (
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
)


def get_missing_fields(customer: dict[str, Any]) -> list[str]:
    """
    Return the customer fields that have not been provided.

    Args:
        customer:
            Dictionary containing customer information.

    Returns:
        List of missing customer field names.
    """

    return [
        field
        for field in CUSTOMER_FIELDS
        if field not in customer or customer[field] in (None, "")
    ]


def is_customer_complete(customer: dict[str, Any]) -> bool:
    """
    Check whether all required customer fields are available.

    Args:
        customer:
            Dictionary containing customer information.

    Returns:
        True when all required fields are present.
    """

    return len(get_missing_fields(customer)) == 0


def update_customer_data(
    customer: dict[str, Any],
    updates: dict[str, Any],
) -> dict[str, Any]:
    """
    Add or update customer information.

    Args:
        customer:
            Existing customer information.

        updates:
            New customer information.

    Returns:
        Updated customer dictionary.
    """

    updated_customer = customer.copy()
    updated_customer.update(updates)

    return updated_customer
