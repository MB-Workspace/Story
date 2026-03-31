"""
Advanced Async Tasks for Celery
"""
from celery import shared_task
from project_vajra.core import EvidenceCorrelator, PatternAnalyzer
from project_vajra.orchestration import PlaybookGenerator, OpenClawClient
from project_vajra.logging_config import logger

@shared_task(name="vajra.process_advanced_analytics")
def process_advanced_analytics(case_data: dict) -> dict:
    """Async task for temporal and graph analysis"""
    try:
        correlator = EvidenceCorrelator(case_data)
        correlator.link_evidence()  # This sets shell_networks, centralities, key_nodes, rings
        correlator.run_advanced_analytics()  # This sets temporal_clusters, benford_anomalies
        
        return {
            "temporal_clusters": correlator.temporal_clusters,
            "benford_anomalies": correlator.benford_anomalies,
            "shell_networks": getattr(correlator, 'shell_networks', []),
            "centralities": getattr(correlator, 'centralities', {}),
            "key_nodes": getattr(correlator, 'key_nodes', []),
            "rings": getattr(correlator, 'rings', [])
        }
    except Exception as e:
        logger.error(f"Advanced analytics task failed: {e}")
        return {"status": "error", "error": str(e)}

@shared_task(name="vajra.enrich_threat_intel")
def enrich_threat_intel(entity_graph: dict) -> list:
    """Async task for threat intelligence enrichment"""
    try:
        analyzer = PatternAnalyzer(use_advanced=True)
        return analyzer.predict_threats(entity_graph)
    except Exception as e:
        logger.error(f"Threat intel enrichment failed: {e}")
        return []

@shared_task(name="vajra.generate_playbook")
def generate_playbook(threat_matches: list, high_risk_targets: list) -> str:
    """Async task for playbook generation"""
    try:
        generator = PlaybookGenerator()
        return generator.generate_crypto_fraud_response(
            threat_matches, 
            high_risk_targets
        )
    except Exception as e:
        logger.error(f"Playbook generation failed: {e}")
        return ""

@shared_task(name="vajra.execute_playbook")
def execute_playbook(playbook_yaml: str) -> dict:
    """Async task for playbook execution"""
    try:
        client = OpenClawClient()
        return client.execute_playbook(playbook_yaml)
    except Exception as e:
        logger.error(f"Playbook execution failed: {e}")
        return {"status": "error", "error": str(e)}