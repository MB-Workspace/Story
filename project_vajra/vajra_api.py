"""
Project Vajra - FastAPI REST API

Exposes the forensic automation pipeline as HTTP endpoints.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from project_vajra.core import VajraSystem
from project_vajra.logging_config import logger
from project_vajra import __version__

app = FastAPI(
    title="Project Vajra API",
    description="AI-Powered Forensic Automation System",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Models ===

class EvidenceItem(BaseModel):
    source: str
    type: str = "crypto_wallet"
    transactions: list[str] = Field(default_factory=list)
    behavior: list[str] = Field(default_factory=list)
    related_to: list[str] = Field(default_factory=list)


class CaseRequest(BaseModel):
    case_id: str
    evidence: list[EvidenceItem]


class CaseResponse(BaseModel):
    case_id: str
    report: str
    processing_time: float
    entity_count: int
    threat_count: int
    timestamp: str


# === Endpoints ===

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers."""
    return {
        "status": "healthy",
        "version": __version__,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/api/v1/cases/analyze", response_model=CaseResponse)
async def analyze_case(request: CaseRequest):
    """
    Submit a case for full forensic analysis pipeline.

    Processes evidence through:
    1. Entity correlation
    2. Shell company detection
    3. Threat actor matching
    4. Court-ready report generation
    """
    try:
        case_data = {
            "case_id": request.case_id,
            "evidence": [item.model_dump() for item in request.evidence],
        }

        vajra = VajraSystem(case_data)
        report = vajra.solve_case()

        return CaseResponse(
            case_id=request.case_id,
            report=report,
            processing_time=vajra._last_processing_time,
            entity_count=len(vajra._last_entity_graph),
            threat_count=len(vajra._last_threat_matches),
            timestamp=datetime.utcnow().isoformat(),
        )

    except KeyError as e:
        logger.error(f"Missing required field: {e}")
        raise HTTPException(status_code=422, detail=f"Missing required field: {e}")
    except Exception as e:
        logger.error(f"Analysis failed for case {request.case_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/v1/cases/correlate")
async def correlate_evidence(request: CaseRequest):
    """Run evidence correlation only (entity graph construction)."""
    case_data = {
        "case_id": request.case_id,
        "evidence": [item.model_dump() for item in request.evidence],
    }
    vajra = VajraSystem(case_data)
    graph = vajra.correlator.link_evidence()
    return {
        "case_id": request.case_id,
        "entity_count": len(graph),
        "entities": {k: v["connections"] for k, v in graph.items()},
    }


@app.post("/api/v1/cases/threats")
async def detect_threats(request: CaseRequest):
    """Run threat detection on case evidence."""
    case_data = {
        "case_id": request.case_id,
        "evidence": [item.model_dump() for item in request.evidence],
    }
    vajra = VajraSystem(case_data)
    graph = vajra.correlator.link_evidence()
    threats = vajra.analyzer.predict_threats(graph)
    return {
        "case_id": request.case_id,
        "threats": threats,
    }


# === Entry Point ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
