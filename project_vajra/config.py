"""
Production Configuration

Loads sensitive values from environment variables (.env file supported).
See .env.example for required variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")

# API Credentials
BLOCKCHAIN_API_KEY = os.environ.get("BLOCKCHAIN_API_KEY", "")

# Performance Settings
MAX_CONCURRENT_REQUESTS = int(os.environ.get("MAX_CONCURRENT_REQUESTS", "10"))
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))  # seconds

# Data Processing
MAX_TRANSACTIONS_PER_ANALYSIS = int(os.environ.get("MAX_TRANSACTIONS_PER_ANALYSIS", "10000"))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "500"))

# Logging Configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = os.environ.get("LOG_FILE", "vajra_system.log")

# Forensic Tools Integration
SUPPORTED_FORMATS = [
    "FTK", "AD1", "E01", "AFF4", "RAW", "DD",
    "AXIOM", "Cellebrite", "Oxygen"
]