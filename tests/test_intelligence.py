"""
Tests for Threat Intelligence Module
"""
import pytest
from project_vajra.intelligence.claude_client import ClaudeAnalyzer
from project_vajra.intelligence.threat_intel import AdvancedAnalyzer


class TestClaudeAnalyzer:
    """Test Claude NLP threat extraction"""
    
    @pytest.fixture
    def analyzer(self):
        return ClaudeAnalyzer(api_key="test_key")
    
    def test_initialization(self, analyzer):
        assert analyzer.model == "claude-3-opus-20240229"
    
    def test_extract_threat_actors(self, analyzer):
        text_data = "Lazarus Group was observed conducting crypto theft operations."
        result = analyzer.extract_threat_actors(text_data)
        
        assert isinstance(result, list)
    
    def test_predict_tactics(self, analyzer):
        entity_graph = {
            "wallet_A": {
                "behavior": ["fee_evasion", "micro_transactions"],
                "connections": ["wallet_B"]
            }
        }
        tactics = analyzer.predict_tactics(entity_graph)
        
        assert isinstance(tactics, list)


class TestAdvancedAnalyzer:
    """Test MITRE ATT&CK enrichment"""
    
    @pytest.fixture
    def analyzer(self):
        return AdvancedAnalyzer(claude_api_key="test_key")
    
    @pytest.fixture
    def sample_threat_matches(self):
        return [
            {
                "entity": "wallet_A",
                "threat": "Lazarus Group",
                "confidence": 0.92,
                "patterns": ["fee_evasion", "micro_transactions"]
            },
            {
                "entity": "wallet_B",
                "threat": "APT29",
                "confidence": 0.87,
                "patterns": ["time_delayed", "multi_hop"]
            }
        ]
    
    def test_enrich_threats(self, analyzer, sample_threat_matches):
        enriched = analyzer.enrich_threats(sample_threat_matches)
        
        assert len(enriched) == 2
        assert "mitre_techniques" in enriched[0]
    
    def test_sigma_rule_generation(self, analyzer):
        patterns = ["fee_evasion", "micro_transactions"]
        threat_group = "Lazarus Group"
        
        rule = analyzer.generate_sigma_rule(patterns, threat_group)
        
        assert "title: Detect Lazarus Group Activity" in rule
        assert "level: high" in rule
    
    def test_mitre_mapping(self):
        analyzer = AdvancedAnalyzer()
        
        assert "fee_evasion" in analyzer.MITRE_MAPPING
        assert "T1496" in analyzer.MITRE_MAPPING["fee_evasion"]