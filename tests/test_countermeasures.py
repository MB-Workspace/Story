"""
Tests for Antigravity countermeasures module
"""
import pytest
from project_vajra.countermeasures import AntigravityDeployer

class TestAntigravityDeployer:
    """Test countermeasures orchestration"""
    
    @pytest.fixture
    def deployer(self):
        # We don't provide rpc_url so it uses default/simulated
        return AntigravityDeployer()
    
    def test_blockchain_monitor(self, deployer):
        result = deployer.execute_countermeasure(
            "blockchain_monitor", 
            {"wallet_address": "0x1234abcd"}
        )
        assert result["status"] == "success"
        assert result["wallet"] == "0x1234abcd"
        assert "0x1234Abcd" in deployer.monitor.watch_list or "0x1234abcd" in deployer.monitor.watch_list

    def test_honeycontract_simulation(self, deployer):
        result = deployer.execute_countermeasure(
            "honeycontract",
            {"bait_amount": "0.5", "attacker_pattern": "Lazarus Group"}
        )
        assert result["status"] == "simulated"
        assert "contract_address" in result
        assert result["contract_address"].startswith("0xDeC0y")
        
    def test_unknown_module(self, deployer):
        result = deployer.execute_countermeasure("fake_module", {})
        assert result["status"] == "error"
