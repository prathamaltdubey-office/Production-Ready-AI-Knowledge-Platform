"""
Application logging configuration.

Logs are written to:
    backend/logs/app.log
    backend/logs/error.log

They are also displayed in the terminal.
"""

import logging
import sys
from pathlib import Path

# ============================================================
# LOG DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOG FILES
# ============================================================

APP_LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger("customer_churn_api")

logger.setLevel(logging.INFO)

logger.propagate = False


# ============================================================
# PREVENT DUPLICATE HANDLERS
# ============================================================

if not logger.handlers:

    # --------------------------------------------------------
    # FORMAT
    # --------------------------------------------------------

    formatter = logging.Formatter(
        fmt=("%(asctime)s | " "%(levelname)s | " "%(name)s | " "%(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --------------------------------------------------------
    # CONSOLE HANDLER
    # --------------------------------------------------------

    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # APPLICATION LOG
    # --------------------------------------------------------

    app_file_handler = logging.FileHandler(
        APP_LOG_FILE,
        encoding="utf-8",
    )

    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # ERROR LOG
    # --------------------------------------------------------

    error_file_handler = logging.FileHandler(
        ERROR_LOG_FILE,
        encoding="utf-8",
    )

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # ADD HANDLERS
    # --------------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(app_file_handler)
    logger.addHandler(error_file_handler)


# ============================================================
# TEST FUNCTION
# ============================================================

if __name__ == "__main__":
    logger.info("Logger test: INFO message")
    logger.error("Logger test: ERROR message")
