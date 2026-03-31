# Changelog

All notable changes to Project Vajra will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-31

### Added

- **FastAPI REST API** (`vajra_api.py`) with endpoints for case analysis, evidence correlation, and threat detection
- **Celery task module** (`vajra_tasks.py`) for async processing with Redis broker
- **EvidenceBuilder** class for transforming raw blockchain API data into VajraSystem evidence format
- **BlockchairAdapter** for free Blockchair API integration (no key required)
- **Health check endpoint** at `GET /health` for Docker and load balancers
- **Input validation** using Pydantic models and manual checks
- **Type hints** across all Python modules
- **Structured error handling** with JSON-lines error logs
- **Sample data** based on real OFAC-designated Lazarus Group wallets (Ronin Bridge hack)
- **THREAT_DB** with 6 real threat actors and MITRE ATT&CK IDs
- **pytest configuration** via `pyproject.toml` with coverage settings
- **30 unit tests** covering edge cases, pipeline validation, and data adapter mocking
- **Benchmark script** (`tests/benchmark.py`) for performance validation
- **MIT License**
- **`.env.example`** with all required environment variables
- **GitHub Actions CI/CD** workflow for automated testing
- **Docker health checks** on all services

### Changed

- **`config.py`**: Loads secrets from environment variables via `python-dotenv` (was hardcoded)
- **`core.py`**: Replaced all `print()` calls with structured `logger` from logging_config
- **`core.py`**: Added division-by-zero guard in `predict_threats()`
- **`core.py`**: Fixed entity graph inferred-node metadata bug
- **`data_adapters.py`**: Added `json` import (was missing, causing crash)
- **`data_adapters.py`**: Replaced deprecated `datetime.utcnow()` with `datetime.now(timezone.utc)`
- **`data_adapters.py`**: Forensic stubs now raise `NotImplementedError` instead of returning empty data
- **`data_adapters.py`**: `ErrorHandler` now creates log directory automatically
- **`logging_config.py`**: Prevents duplicate handlers on reimport, uses pathlib for cross-platform paths
- **`requirements.txt`**: Made platform-specific deps conditional, added FastAPI/Celery dependencies
- **`Dockerfile`**: Fixed build context paths, added health check, set PYTHONPATH
- **`docker-compose.yml`**: Fixed module paths, added env_file, health checks, named volumes
- **README.md**: Rewritten as pure technical documentation
- **DOCUMENTATION.md**: Full module reference with EvidenceBuilder and BlockchairAdapter
