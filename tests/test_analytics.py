"""
Tests for Analytics Module
"""
import pytest
from project_vajra.analytics.temporal import EnhancedCorrelator
from project_vajra.analytics.graph import GraphProcessor
from datetime import datetime


class TestEnhancedCorrelator:
    """Test temporal analysis and Benford's Law detection"""
    
    @pytest.fixture
    def sample_case_data(self):
        return {
            "case_id": "TEST-001",
            "evidence": [
                {
                    "source": "wallet_A",
                    "transactions": [
                        {"timestamp": "2024-01-15T10:00:00", "value": 1000, "tags": ["fee_evasion"]},
                        {"timestamp": "2024-01-15T10:30:00", "value": 2000, "tags": ["fee_evasion"]},
                        {"timestamp": "2024-01-15T11:00:00", "value": 3000, "tags": ["micro_transactions"]},
                    ],
                    "behavior": ["fee_evasion"]
                },
                {
                    "source": "wallet_B",
                    "transactions": [
                        {"timestamp": "2024-01-15T12:00:00", "value": 5000, "tags": ["fee_evasion"]},
                    ],
                    "behavior": ["fee_evasion"]
                }
            ]
        }
    
    def test_temporal_clustering(self, sample_case_data):
        correlator = EnhancedCorrelator(sample_case_data)
        clusters = correlator.analyze_crypto_transactions()
        
        assert isinstance(clusters, dict)
        assert len(clusters) > 0
    
    def test_benford_law_detection(self, sample_case_data):
        correlator = EnhancedCorrelator(sample_case_data)
        anomalies = correlator.identify_money_laundering()
        
        assert isinstance(anomalies, list)


class TestGraphProcessor:
    """Test NetworkX graph algorithms"""
    
    @pytest.fixture
    def sample_entity_graph(self):
        return {
            "wallet_A": {
                "connections": ["wallet_B", "wallet_C"],
                "metadata": {"type": "crypto_wallet", "behavior": ["fee_evasion"]}
            },
            "wallet_B": {
                "connections": ["wallet_A", "wallet_C"],
                "metadata": {"type": "crypto_wallet", "behavior": ["fee_evasion"]}
            },
            "wallet_C": {
                "connections": ["wallet_A", "wallet_B"],
                "metadata": {"type": "crypto_wallet", "behavior": ["micro_transactions"]}
            },
            "wallet_D": {
                "connections": [],
                "metadata": {"type": "exchange", "behavior": []}
            }
        }
    
    def test_graph_conversion(self, sample_entity_graph):
        processor = GraphProcessor(sample_entity_graph)
        
        assert processor.nx_graph is not None
        assert len(processor.nx_graph.nodes()) == 4
    
    def test_shell_network_detection(self, sample_entity_graph):
        processor = GraphProcessor(sample_entity_graph)
        shell_networks = processor.detect_shell_networks()
        
        assert isinstance(shell_networks, list)
    
    def test_centrality_calculation(self, sample_entity_graph):
        processor = GraphProcessor(sample_entity_graph)
        centralities = processor.calculate_centralities()
        
        # Centralities returns {node_name: {metric: value}}
        assert isinstance(centralities, dict)
        assert len(centralities) > 0
        # Each node should have degree and betweenness
        first_node = next(iter(centralities))
        assert "degree" in centralities[first_node]
        assert "betweenness" in centralities[first_node]
    
    def test_key_nodes_identification(self, sample_entity_graph):
        processor = GraphProcessor(sample_entity_graph)
        key_nodes = processor.find_key_nodes()
        
        assert isinstance(key_nodes, list)
        assert len(key_nodes) <= 5