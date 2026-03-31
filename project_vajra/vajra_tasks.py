"""
Project Vajra - Celery Async Task Definitions

Handles long-running forensic processing as background tasks.
Requires Redis as broker: redis://localhost:6379/0
"""
from celery import Celery
import os

# Configure Celery
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

app = Celery(
    "vajra_tasks",
    broker=broker_url,
    backend=result_backend,
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minute hard limit
    task_soft_time_limit=540,  # 9 minute soft limit
)


@app.task(bind=True, name="vajra.analyze_case")
def analyze_case_async(self, case_data: dict) -> dict:
    """
    Asynchronous case analysis task.

    Args:
        case_data: Dict with case_id and evidence list.

    Returns:
        Dict with report, processing time, and metadata.
    """
    from project_vajra.core import VajraSystem
    from project_vajra.logging_config import logger

    case_id = case_data.get("case_id", "UNKNOWN")
    logger.info(f"[Celery] Starting async analysis for case: {case_id}")

    self.update_state(state="PROCESSING", meta={"case_id": case_id, "stage": "initialization"})

    try:
        vajra = VajraSystem(case_data)

        self.update_state(state="PROCESSING", meta={"case_id": case_id, "stage": "correlation"})
        report = vajra.solve_case()

        result = {
            "case_id": case_id,
            "report": report,
            "processing_time": vajra._last_processing_time,
            "entity_count": len(vajra._last_entity_graph),
            "threat_count": len(vajra._last_threat_matches),
            "status": "completed",
        }

        logger.info(f"[Celery] Completed analysis for case: {case_id}")
        return result

    except Exception as e:
        logger.error(f"[Celery] Analysis failed for case {case_id}: {e}")
        return {
            "case_id": case_id,
            "status": "failed",
            "error": str(e),
        }


@app.task(name="vajra.correlate_evidence")
def correlate_evidence_async(case_data: dict) -> dict:
    """Run evidence correlation only (lightweight task)."""
    from project_vajra.core import VajraSystem

    vajra = VajraSystem(case_data)
    graph = vajra.correlator.link_evidence()
    return {
        "case_id": case_data.get("case_id"),
        "entity_count": len(graph),
        "entities": {k: v["connections"] for k, v in graph.items()},
    }

# Import advanced async tasks
from project_vajra.tasks.async_tasks import *
