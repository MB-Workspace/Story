"""
Production Logging Setup

Configures rotating file handler and console output for the Vajra system.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from project_vajra.config import LOG_LEVEL, LOG_FILE
except ImportError:
    LOG_LEVEL = "INFO"
    LOG_FILE = "vajra_system.log"

# Calculate log file path (relative to project root)
_log_path = Path(LOG_FILE)
if not _log_path.is_absolute():
    _project_root = Path(__file__).resolve().parent.parent
    _log_path = _project_root / LOG_FILE

# Ensure log directory exists
_log_path.parent.mkdir(parents=True, exist_ok=True)

# Configure root logger
logger = logging.getLogger("vajra")
logger.setLevel(LOG_LEVEL)

# Prevent duplicate handlers on reimport
if not logger.handlers:
    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        str(_log_path),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(LOG_LEVEL)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)