"""
OpenClaw Client for Playbook Execution
"""
import requests
import json
from typing import Dict, Any

class OpenClawClient:
    """Client for executing OpenClaw playbooks"""
    
    def __init__(self, api_url: str = "https://api.openclaw.io/v1", simulation_mode: bool = False) -> None:
        self.api_url = api_url
        self.simulation_mode = simulation_mode
        self._execution_history = []
        
    def execute_playbook(self, playbook_yaml: str) -> Dict[str, Any]:
        """Execute a playbook via OpenClaw API or local simulation."""
        if self.simulation_mode:
            return self._simulate_playbook(playbook_yaml)
            
        payload = {
            "playbook": playbook_yaml,
            "mode": "async"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/execute",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}

    def _simulate_playbook(self, playbook_yaml: str) -> Dict[str, Any]:
        """Simulate execution of a playbook by parsing and logging its steps."""
        from project_vajra.logging_config import logger
        import yaml
        import uuid
        import time
        
        try:
            playbook = yaml.safe_load(playbook_yaml)
            run_id = str(uuid.uuid4())
            logger.info(f"[OpenClaw-SIM] Starting execution of playbook: {playbook.get('name', 'Unknown')}")
            
            steps_executed = 0
            for step in playbook.get("steps", []):
                logger.info(f"[OpenClaw-SIM] Executing step: {step.get('name')} (Action: {step.get('action')})")
                time.sleep(0.1) # Simulate minor delay
                steps_executed += 1
                
            result = {
                "status": "simulated_success",
                "execution_id": run_id,
                "steps_run": steps_executed
            }
            self._execution_history.append(result)
            return result
        except BaseException as e:
            logger.error(f"[OpenClaw-SIM] Failed to simulate playbook: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Check status of a playbook execution"""
        try:
            response = requests.get(
                f"{self.api_url}/executions/{execution_id}",
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def validate_playbook(self, playbook_yaml: str) -> Dict[str, Any]:
        """Validate playbook syntax and structure"""
        payload = {
            "playbook": playbook_yaml
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/validate",
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}