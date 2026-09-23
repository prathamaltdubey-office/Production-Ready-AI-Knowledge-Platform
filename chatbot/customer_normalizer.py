from typing import Any


def _yes_no(value: Any) -> str:
    """Convert boolean-like values to the API's Yes/No format."""

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, int):
        return "Yes" if value == 1 else "No"

    text = str(value).strip().lower()

    if text in {"yes", "y", "true", "1"}:
        return "Yes"

    if text in {"no", "n", "false", "0"}:
        return "No"

    return str(value)


def _senior_citizen(value: Any) -> int:
    """Convert SeniorCitizen to 0 or 1."""

    if isinstance(value, bool):
        return 1 if value else 0

    if isinstance(value, int):
        return 1 if value == 1 else 0

    text = str(value).strip().lower()

    if text in {"yes", "y", "true", "1"}:
        return 1

    return 0


def _gender(value: Any) -> str:
    """Normalize gender."""

    text = str(value).strip().lower()

    if text == "male":
        return "Male"

    if text == "female":
        return "Female"

    return str(value)


def _contract(value: Any) -> str:
    """Normalize contract type."""

    text = str(value).strip().lower()

    mapping = {
        "month-to-month": "Month-to-month",
        "monthly": "Month-to-month",
        "month to month": "Month-to-month",
        "one year": "One year",
        "1 year": "One year",
        "two year": "Two year",
        "2 year": "Two year",
    }

    return mapping.get(text, str(value))


def _payment_method(value: Any) -> str:
    """Normalize payment method."""

    text = str(value).strip().lower()

    mapping = {
        "electronic check": "Electronic check",
        "mailed check": "Mailed check",
        "bank transfer": "Bank transfer (automatic)",
        "bank transfer automatic": "Bank transfer (automatic)",
        "credit card": "Credit card (automatic)",
        "credit card automatic": "Credit card (automatic)",
    }

    return mapping.get(text, str(value))


def _internet_service(value: Any) -> str:
    """Normalize internet service."""

    text = str(value).strip().lower()

    mapping = {
        "dsl": "DSL",
        "fiber optic": "Fiber optic",
        "fiber": "Fiber optic",
        "no": "No",
    }

    return mapping.get(text, str(value))


def _service_field(value: Any) -> str:
    """
    Normalize service fields.

    Examples:
        True -> Yes
        False -> No
        yes -> Yes
        no -> No
    """

    return _yes_no(value)


def _safe_int(value: Any) -> int | None:
    """
    Safely convert a value to int.

    Returns None if the value is empty, whitespace, or not a
    valid integer, instead of raising an exception.
    """

    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    try:
        return int(float(text))
    except (ValueError, TypeError):
        return None


def _safe_float(value: Any) -> float | None:
    """
    Safely convert a value to float.

    Returns None if the value is empty, whitespace, or not a
    valid number, instead of raising an exception.
    """

    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    try:
        return float(text)
    except (ValueError, TypeError):
        return None


def normalize_customer_data(
    customer_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize extracted customer information into the exact format
    expected by the FastAPI prediction API.

    Args:
        customer_data:
            Raw customer information extracted by the LLM.

    Returns:
        Normalized customer dictionary.
    """

    normalized = dict(customer_data)

    # ---------------------------------------------------------
    # Basic categorical fields
    # ---------------------------------------------------------

    if "gender" in normalized and normalized["gender"] is not None:
        normalized["gender"] = _gender(normalized["gender"])

    if "SeniorCitizen" in normalized and normalized["SeniorCitizen"] is not None:
        normalized["SeniorCitizen"] = _senior_citizen(normalized["SeniorCitizen"])

    if "Partner" in normalized and normalized["Partner"] is not None:
        normalized["Partner"] = _yes_no(normalized["Partner"])

    if "Dependents" in normalized and normalized["Dependents"] is not None:
        normalized["Dependents"] = _yes_no(normalized["Dependents"])

    # ---------------------------------------------------------
    # Customer services
    # ---------------------------------------------------------

    for field in [
        "PhoneService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "PaperlessBilling",
    ]:
        if field in normalized and normalized[field] is not None:
            normalized[field] = _service_field(normalized[field])

    # ---------------------------------------------------------
    # MultipleLines
    # ---------------------------------------------------------

    if "MultipleLines" in normalized:
        value = normalized["MultipleLines"]

        if value is not None:
            if isinstance(value, bool):
                normalized["MultipleLines"] = "Yes" if value else "No"

            else:
                text = str(value).strip().lower()

                if text in {"yes", "y", "true", "1"}:
                    normalized["MultipleLines"] = "Yes"

                elif text in {"no", "n", "false", "0"}:
                    normalized["MultipleLines"] = "No"

                elif "no phone" in text:
                    normalized["MultipleLines"] = "No phone service"

    # ---------------------------------------------------------
    # Internet service
    # ---------------------------------------------------------

    if "InternetService" in normalized:
        if normalized["InternetService"] is not None:
            normalized["InternetService"] = _internet_service(
                normalized["InternetService"]
            )

    # ---------------------------------------------------------
    # Contract
    # ---------------------------------------------------------

    if "Contract" in normalized:
        if normalized["Contract"] is not None:
            normalized["Contract"] = _contract(normalized["Contract"])

    # ---------------------------------------------------------
    # Payment method
    # ---------------------------------------------------------

    if "PaymentMethod" in normalized:
        if normalized["PaymentMethod"] is not None:
            normalized["PaymentMethod"] = _payment_method(normalized["PaymentMethod"])

    # ---------------------------------------------------------
    # Numeric fields (safe conversion, no crash on empty/invalid values)
    # ---------------------------------------------------------

    if "tenure" in normalized:
        normalized["tenure"] = _safe_int(normalized["tenure"])

    if "MonthlyCharges" in normalized:
        normalized["MonthlyCharges"] = _safe_float(normalized["MonthlyCharges"])

    if "TotalCharges" in normalized:
        normalized["TotalCharges"] = _safe_float(normalized["TotalCharges"])

    return normalized
