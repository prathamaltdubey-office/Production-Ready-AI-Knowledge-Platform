"""
Model loading utilities for the FastAPI inference service.
"""

from pathlib import Path

from joblib import load
from sklearn.pipeline import Pipeline

from src.model_registry import get_version_info

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"


MODEL_FILES = {
    "logistic_regression": "best_logistic_model.pkl",
    "random_forest": "best_rf_model.pkl",
    "xgboost": "best_xgb_model.pkl",
}


def load_model(
    model_name: str,
    version: int | str = "latest",
) -> Pipeline:
    """
    Load a trained machine learning pipeline.

    Uses the model registry if version information exists;
    falls back to the fixed file path for models trained
    before the registry existed.
    """

    if model_name not in MODEL_FILES:
        raise ValueError(f"Unknown model: {model_name}")

    try:
        version_info = get_version_info(model_name, version)
        model_path = BASE_DIR / version_info["file_path"]

    except ValueError:
        # No registry entry yet — fall back to the fixed path.
        model_path = MODEL_DIR / MODEL_FILES[model_name]

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = load(model_path)

    if not isinstance(model, Pipeline):
        raise TypeError(f"Expected sklearn Pipeline, got {type(model).__name__}")

    return model


def load_all_models() -> dict[str, Pipeline]:
    """Load the latest version of all production models."""

    return {model_name: load_model(model_name) for model_name in MODEL_FILES}


def get_model(
    model_name: str,
    version: int | str = "latest",
) -> Pipeline:
    """Return the requested machine learning model version."""

    return load_model(model_name, version)
