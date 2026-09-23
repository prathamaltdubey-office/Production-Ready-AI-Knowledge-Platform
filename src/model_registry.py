"""
Lightweight model registry.

Tracks versions of trained models with metadata, instead of
overwriting a single fixed file per model type.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path("models/registry.json")


def _load_registry() -> dict[str, Any]:
    """Load the registry file, creating an empty one if missing."""

    if not REGISTRY_PATH.exists():
        return {}

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_registry(registry: dict[str, Any]) -> None:
    """Persist the registry to disk."""

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def register_model(
    model_name: str,
    file_path: str,
    metrics: dict[str, float] | None = None,
    mlflow_run_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> int:
    """
    Register a new version of a trained model.

    Args:
        model_name: Logical model name, e.g. "random_forest".
        file_path: Path to the saved model artifact.
        metrics: Evaluation metrics for this version.
        mlflow_run_id: MLflow run ID that produced this version.
        params: Hyperparameters used for this version.

    Returns:
        The new version number assigned to this model.
    """

    registry = _load_registry()

    if model_name not in registry:
        registry[model_name] = {"versions": []}

    existing_versions = registry[model_name]["versions"]
    new_version = len(existing_versions) + 1

    entry = {
        "version": new_version,
        "file_path": file_path,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics or {},
        "mlflow_run_id": mlflow_run_id,
        "params": params or {},
    }

    existing_versions.append(entry)
    registry[model_name]["latest_version"] = new_version

    _save_registry(registry)

    return new_version


def get_version_info(
    model_name: str,
    version: int | str = "latest",
) -> dict[str, Any]:
    """
    Get metadata for a specific model version.

    Args:
        model_name: Logical model name, e.g. "random_forest".
        version: A specific version number, or "latest".

    Returns:
        The registry entry for that version.

    Raises:
        ValueError: If the model or version doesn't exist.
    """

    registry = _load_registry()

    if model_name not in registry:
        raise ValueError(f"No registered versions for model: {model_name}")

    versions = registry[model_name]["versions"]

    if version == "latest":
        version = registry[model_name]["latest_version"]

    for entry in versions:
        if entry["version"] == version:
            return entry

    raise ValueError(f"Version {version} not found for model: {model_name}")


def list_versions(model_name: str) -> list[dict[str, Any]]:
    """List all registered versions for a model, newest first."""

    registry = _load_registry()

    if model_name not in registry:
        return []

    return sorted(
        registry[model_name]["versions"],
        key=lambda entry: entry["version"],
        reverse=True,
    )


def list_all_models() -> dict[str, Any]:
    """Return the full registry."""

    return _load_registry()
