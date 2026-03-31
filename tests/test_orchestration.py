"""
Tests for Orchestration Module
"""
import pytest
from project_vajra.orchestration.playbook_generator import PlaybookGenerator
from project_vajra.orchestration.openclaw import OpenClawClient


class TestPlaybookGenerator:
    """Test OpenClaw playbook generation"""
    
    @pytest.fixture
    def generator(self):
        return PlaybookGenerator()
    
    @pytest.fixture
    def sample_threat_matches(self):
        return [
            {
                "entity": "wallet_A",
                "threat": "Lazarus Group",
                "confidence": 0.92,
                "patterns": ["fee_evasion"],
                "mitre_techniques": ["T1496 - Resource Hijacking"]
            }
        ]
    
    def test_generate_crypto_fraud_response(self, generator, sample_threat_matches):
        high_risk_targets = ["wallet_A", "wallet_B"]
        
        playbook = generator.generate_crypto_fraud_response(
            sample_threat_matches,
            high_risk_targets,
            severity="high"
        )
        
        assert "name: Crypto Fraud Response" in playbook
        assert "wallet_A" in playbook
        assert "wallet_B" in playbook
    
    def test_generate_ransomware_response(self, generator):
        playbook = generator.generate_ransomware_response(
            "DarkSide",
            ["ransom_wallet_1", "ransom_wallet_2"],
            severity="critical"
        )
        
        assert "name: Ransomware Response" in playbook


class TestOpenClawClient:
    """Test OpenClaw API client"""
    
    @pytest.fixture
    def client(self):
        return OpenClawClient(api_url="https://api.test.openclaw.io")
    
    def test_initialization(self, client):
        assert client.api_url == "https://api.test.openclaw.io"
    
    def test_validate_playbook_structure(self, client):
        playbook_yaml = """
name: Test Playbook
steps:
  - name: Test step
    action: test.action
"""
        result = client.validate_playbook(playbook_yaml)
        
        # In test mode, should return error or mock response
        assert isinstance(result, dict)

    def test_simulation_mode(self):
        """Test playbook execution in simulation mode."""
        client = OpenClawClient(api_url="https://api.test.openclaw.io", simulation_mode=True)
        playbook_yaml = """
name: Simulated Playbook
steps:
  - name: Step 1
    action: vajra.analyze
  - name: Step 2
    action: vajra.report
"""
        result = client.execute_playbook(playbook_yaml)
        
        assert result["status"] == "simulated_success"
        assert "execution_id" in result
        assert result["steps_run"] == 2
        assert len(client._execution_history) == 1
        assert client._execution_history[0]["execution_id"] == result["execution_id"]