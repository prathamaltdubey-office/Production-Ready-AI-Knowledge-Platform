"""
Application configuration for the FastAPI inference service.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"


# ============================================================
# MODEL FILES
# ============================================================

LOGISTIC_MODEL = "best_logistic_model.pkl"
RANDOM_FOREST_MODEL = "best_rf_model.pkl"
XGBOOST_MODEL = "best_xgb_model.pkl"

DEFAULT_MODEL = "random_forest"


# ============================================================
# API INFORMATION
# ============================================================

API_TITLE = "Customer Churn Prediction API"

API_DESCRIPTION = (
    "FastAPI inference service for the Customer Churn " "Prediction ML pipeline."
)

API_VERSION = "1.0.0"


# ============================================================
# AUTHENTICATION
# ============================================================

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("API_TOKEN environment variable is not configured.")
