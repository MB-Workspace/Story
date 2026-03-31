"""
Functional Tests for Project Vajra

Tests the core forensic automation pipeline including entity
correlation, shell company detection, threat analysis, and reporting.
"""
import pytest
from project_vajra.core import (
    VajraSystem,
    EvidenceCorrelator,
    PatternAnalyzer,
    ReportAutomator,
)


class TestEvidenceCorrelator:
    """Tests for the evidence correlation engine."""

    def test_entity_graph_creation(self, sample_case_data):
        """Test that evidence linking creates correct entity graph."""
        correlator = EvidenceCorrelator(sample_case_data)
        graph = correlator.link_evidence()
        assert len(graph) == 5
        w_a = "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"
        w_b = "0x8ba1f109551bD432803012645Ac136ddd64DBA72"
        w_c = "0x1aD91ee08f21bE3dE0BA2ba6918E714dA6B45836"
        w_d = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        w_e = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
        assert set(graph[w_a]["connections"]) == {w_b, w_c}
        assert set(graph[w_d]["connections"]) == {w_b, w_e}

    def test_bidirectional_links(self, sample_case_data):
        """Verify all connections are bidirectional."""
        correlator = EvidenceCorrelator(sample_case_data)
        graph = correlator.link_evidence()
        for source, data in graph.items():
            for target in data["connections"]:
                assert source in graph[target]["connections"], (
                    f"Missing reverse link: {target} -> {source}"
                )

    def test_empty_evidence(self, empty_evidence_case):
        """Test graceful handling of no evidence."""
        correlator = EvidenceCorrelator(empty_evidence_case)
        graph = correlator.link_evidence()
        assert graph == {}

    def test_single_evidence_item(self, minimal_case_data):
        """Test processing a single evidence item."""
        correlator = EvidenceCorrelator(minimal_case_data)
        graph = correlator.link_evidence()
        assert len(graph) == 1
        w_x = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        assert graph[w_x]["connections"] == []


class TestShellCompanyDetection:
    """Tests for shell company identification."""

    def test_shell_detection(self, sample_case_data):
        """Test shell company identification with matching transaction patterns."""
        correlator = EvidenceCorrelator(sample_case_data)
        correlator.link_evidence()
        shells = correlator.identify_shell_companies()
        assert len(shells) == 1
        cluster_wallets = shells[list(shells.keys())[0]]
        assert len(cluster_wallets) >= 3
        w_b = "0x8ba1f109551bD432803012645Ac136ddd64DBA72"
        w_d = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        w_e = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
        assert w_b in cluster_wallets
        assert w_d in cluster_wallets
        assert w_e in cluster_wallets

    def test_no_shells_with_unique_patterns(self):
        """Test that unique transaction patterns don't form clusters."""
        case = {
            "case_id": "TEST-UNIQUE",
            "evidence": [
                {
                    "source": f"wallet_{i}",
                    "type": "crypto_wallet",
                    "transactions": [f"type{i}_tx1"],
                    "behavior": [],
                    "related_to": [],
                }
                for i in range(5)
            ],
        }
        correlator = EvidenceCorrelator(case)
        correlator.link_evidence()
        shells = correlator.identify_shell_companies()
        assert len(shells) == 0

    def test_shell_detection_without_transactions(self):
        """Test handling of evidence items without transaction data."""
        case = {
            "case_id": "TEST-NO-TX",
            "evidence": [
                {
                    "source": "device_A",
                    "type": "mobile_device",
                    "behavior": ["suspicious_access"],
                    "related_to": [],
                }
            ],
        }
        correlator = EvidenceCorrelator(case)
        correlator.link_evidence()
        shells = correlator.identify_shell_companies()
        assert len(shells) == 0


class TestPatternAnalyzer:
    """Tests for threat actor matching."""

    def test_lazarus_group_detection(self, sample_case_data):
        """Test that Lazarus Group patterns are correctly matched."""
        correlator = EvidenceCorrelator(sample_case_data)
        graph = correlator.link_evidence()
        analyzer = PatternAnalyzer()
        threats = analyzer.predict_threats(graph)
        assert len(threats) > 0
        lazarus_matches = [t for t in threats if t["threat"] == "Lazarus Group"]
        assert len(lazarus_matches) > 0

    def test_no_threats_with_clean_behavior(self):
        """Test that clean behavior produces no threat matches."""
        graph = {
            "clean_wallet": {
                "connections": [],
                "metadata": {"behavior": ["normal_trading"]},
            }
        }
        analyzer = PatternAnalyzer()
        threats = analyzer.predict_threats(graph)
        assert len(threats) == 0

    def test_no_crash_on_empty_behavior(self):
        """Test that entities without behavior data don't crash."""
        graph = {
            "wallet_no_behavior": {
                "connections": [],
                "metadata": {"type": "inferred"},
            }
        }
        analyzer = PatternAnalyzer()
        threats = analyzer.predict_threats(graph)
        assert threats == []

    def test_predict_targets(self, sample_case_data):
        """Test high-risk target prediction from shell clusters."""
        analyzer = PatternAnalyzer()
        mock_clusters = {"deposit,transfer,withdraw": ["w1", "w2", "w3"]}
        targets = analyzer.predict_next_targets(mock_clusters)
        assert len(targets) == 2
        assert targets == ["w1", "w2"]

    def test_predict_targets_small_cluster(self):
        """Test that small clusters (< 3) don't produce targets."""
        analyzer = PatternAnalyzer()
        mock_clusters = {"pattern": ["w1", "w2"]}
        targets = analyzer.predict_next_targets(mock_clusters)
        assert len(targets) == 0


class TestReportAutomator:
    """Tests for report generation."""

    def test_report_contains_required_sections(self):
        """Verify report has all required forensic sections."""
        reporter = ReportAutomator()
        insights = {
            "entity_graph": {"w1": {}, "w2": {}},
            "threat_matches": [
                {
                    "entity": "w1",
                    "threat": "Lazarus Group",
                    "confidence": 0.92,
                    "patterns": ["fee_evasion"],
                }
            ],
            "processing_time": 1.23,
            "case_data": {"case_id": "TEST-001"},
        }
        report = reporter.generate(insights)
        assert "FORENSIC REPORT" in report
        assert "TEST-001" in report
        assert "EXECUTIVE SUMMARY" in report
        assert "THREAT ANALYSIS" in report
        assert "RECOMMENDED ACTIONS" in report
        assert "Lazarus Group" in report

    def test_report_with_no_threats(self):
        """Verify report handles zero threat matches gracefully."""
        reporter = ReportAutomator()
        insights = {
            "entity_graph": {},
            "threat_matches": [],
            "processing_time": 0.5,
            "case_data": {"case_id": "CLEAN-001"},
        }
        report = reporter.generate(insights)
        assert "No significant threats detected" in report


class TestVajraSystem:
    """Integration tests for the full pipeline."""

    def test_end_to_end_processing(self, sample_case_data):
        """Test full case processing pipeline from evidence to report."""
        vajra = VajraSystem(sample_case_data)
        report = vajra.solve_case()
        assert "FORENSIC REPORT" in report
        assert "Lazarus Group" in report
        assert "CRYPTO-FRAUD-2024-001" in report

    def test_pipeline_metadata_tracking(self, sample_case_data):
        """Verify that pipeline stores metadata for API access."""
        vajra = VajraSystem(sample_case_data)
        vajra.solve_case()
        assert vajra._last_processing_time > 0
        assert len(vajra._last_entity_graph) == 5
        assert len(vajra._last_threat_matches) > 0

    def test_missing_case_id_raises(self):
        """Test that missing case_id raises ValueError."""
        with pytest.raises(ValueError, match="case_id"):
            VajraSystem({"evidence": []})

    def test_missing_evidence_raises(self):
        """Test that missing evidence raises ValueError."""
        with pytest.raises(ValueError, match="evidence"):
            VajraSystem({"case_id": "TEST"})

    def test_empty_evidence_runs(self, empty_evidence_case):
        """Test that empty evidence produces a valid report."""
        vajra = VajraSystem(empty_evidence_case)
        report = vajra.solve_case()
        assert "FORENSIC REPORT" in report
        assert "No significant threats detected" in report