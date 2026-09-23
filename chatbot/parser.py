import json
from typing import Any

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """Structured response returned by the chatbot."""

    answer: str

    topic: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    prediction: int | None = None

    churn_probability: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    risk_level: str | None = None

    model: str | None = None

    # Sources returned by the RAG pipeline.
    sources: list[str] = Field(default_factory=list)


def parse_response(response: str) -> dict[str, Any]:
    """Parse the LLM JSON response into a validated dictionary."""

    try:
        data = json.loads(response)

        parsed = ChatResponse.model_validate(data)

        return parsed.model_dump()

    except (json.JSONDecodeError, ValueError, TypeError):
        return {
            "answer": response.strip(),
            "topic": "Customer Churn Prediction",
            "confidence": 0.0,
            "prediction": None,
            "churn_probability": None,
            "risk_level": None,
            "model": None,
            "sources": [],
        }
