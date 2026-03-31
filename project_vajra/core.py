"""
Functional Implementation of Project Vajra - Forensic Automation System

Modules:
    EvidenceCorrelator: Graph-based evidence linking and shell company detection
    PatternAnalyzer: Threat actor matching against known threat profiles
    ReportAutomator: Court-ready forensic report generation
    VajraSystem: End-to-end orchestration pipeline
"""
from __future__ import annotations

import json
import hashlib
import time
from datetime import datetime
from typing import Any, Optional

from project_vajra.logging_config import logger


# === Evidence Processing Engine ===

class EvidenceCorrelator:
    """Process raw evidence into correlated entity graphs."""

    def __init__(self, case_data: dict[str, Any]) -> None:
        self.case_data = case_data
        self.entity_graph: dict[str, dict[str, Any]] = {}
        self.temporal_clusters: dict[str, list] = {}
        self.benford_anomalies: list[dict] = []

    def link_evidence(self) -> dict[str, dict[str, Any]]:
        """Process raw evidence into correlated entities.

        Builds a bidirectional entity graph from the evidence items,
        linking sources to their related entities.

        Returns:
            Entity graph as {source: {connections: [...], metadata: {...}}}
        """
        evidence = self.case_data.get("evidence", [])
        
        # Initialize graph attributes even if no evidence
        self.shell_networks: list[list[str]] = []
        self.centralities: dict[str, dict[str, float]] = {}
        self.key_nodes: list[tuple[str, float]] = []
        self.rings: list[list[str]] = []
        
        if not evidence:
            logger.warning("[Vajra] No evidence items to process")
            return self.entity_graph

        logger.info(f"[Vajra] Processing {len(evidence)} evidence items...")

        # Create entity graph
        for item in evidence:
            source = item["source"]
            if source not in self.entity_graph:
                self.entity_graph[source] = {
                    "connections": [],
                    "metadata": item,
                }
            else:
                # Update metadata if this node was previously inferred
                if self.entity_graph[source]["metadata"].get("type") == "inferred":
                    self.entity_graph[source]["metadata"] = item

            # Link related entities
            for target in item.get("related_to", []):
                if target not in self.entity_graph[source]["connections"]:
                    self.entity_graph[source]["connections"].append(target)
                    # Ensure bidirectional relationship
                    if target not in self.entity_graph:
                        self.entity_graph[target] = {
                            "connections": [source],
                            "metadata": {"type": "inferred"},
                        }
                    elif source not in self.entity_graph[target]["connections"]:
                        self.entity_graph[target]["connections"].append(source)

        logger.info(f"[Vajra] Created entity graph with {len(self.entity_graph)} nodes")
        
        # Process with NetworkX for advanced analysis (only if we have nodes)
        if self.entity_graph:
            from project_vajra.analytics import GraphProcessor
            self.graph_processor = GraphProcessor(self.entity_graph)
            self.shell_networks = self.graph_processor.detect_shell_networks()
            self.centralities = self.graph_processor.calculate_centralities()
            self.key_nodes = self.graph_processor.find_key_nodes()
            self.rings = self.graph_processor.detect_rings()
            
            logger.info(
                f"[Vajra] Found {len(self.shell_networks)} shell networks, "
                f"{len(self.rings)} ring structures, and {len(self.key_nodes)} key nodes"
            )
        
        return self.entity_graph

    def identify_shell_companies(self) -> dict[str, list[str]]:
        """Detect shell company patterns using transaction type clustering.

        Groups wallets by their transaction type patterns (e.g. deposit, withdraw,
        transfer). Clusters with 3+ wallets sharing the same pattern are flagged
        as potential shell companies.

        Returns:
            Dict mapping pattern signatures to wallet lists.
        """
        clusters: dict[str, list[str]] = {}
        for wallet, data in self.entity_graph.items():
            if "transactions" in data.get("metadata", {}):
                transactions = data["metadata"]["transactions"]
                if transactions:
                    # Extract only transaction types (ignore amounts/IDs)
                    tx_types = sorted(set(tx.split("_")[0] for tx in transactions))
                    pattern = ",".join(tx_types)

                    if pattern not in clusters:
                        clusters[pattern] = []
                    clusters[pattern].append(wallet)

        # Filter significant clusters (min 3 wallets with same pattern)
        shell_clusters = {k: v for k, v in clusters.items() if len(v) >= 3}
        logger.info(
            f"[Vajra] Identified {len(shell_clusters)} potential shell company clusters"
        )
        return shell_clusters

    def run_advanced_analytics(self) -> None:
        """Run temporal and statistical analysis on transactions"""
        from project_vajra.analytics import EnhancedCorrelator
        
        # Initialize attributes
        self.temporal_clusters: dict[str, list] = {}
        self.benford_anomalies: list[dict] = []
        
        enhanced = EnhancedCorrelator(self.case_data)
        self.temporal_clusters = enhanced.analyze_crypto_transactions()
        self.benford_anomalies = enhanced.identify_money_laundering()
        
        logger.info(
            f"[Vajra] Found {len(self.temporal_clusters)} temporal clusters "
            f"and {len(self.benford_anomalies)} Benford anomalies"
        )


# === Threat Intelligence Integration ===

class PatternAnalyzer:
    """Analyze behavior patterns against known threat actor profiles."""

    THREAT_DB: dict[str, dict[str, Any]] = {
        "Lazarus Group": {
            "patterns": ["fee_evasion", "micro_transactions"],
            "confidence": 0.92,
            "mitre_id": "G0032",
            "description": "North Korean state-sponsored APT targeting crypto exchanges",
        },
        "APT29 (Cozy Bear)": {
            "patterns": ["time_delayed", "multi_hop"],
            "confidence": 0.87,
            "mitre_id": "G0016",
            "description": "Russian SVR-linked group using patient, low-profile TTPs",
        },
        "FIN7": {
            "patterns": ["fee_evasion", "multi_hop"],
            "confidence": 0.84,
            "mitre_id": "G0046",
            "description": "Financially motivated group targeting payment systems",
        },
        "Scattered Spider": {
            "patterns": ["social_engineering", "credential_theft"],
            "confidence": 0.79,
            "mitre_id": "G1015",
            "description": "Young threat actors using social engineering for crypto theft",
        },
        "BlueNoroff": {
            "patterns": ["fee_evasion", "micro_transactions", "time_delayed"],
            "confidence": 0.88,
            "mitre_id": "G0120",
            "description": "Lazarus sub-group specializing in DeFi/crypto operations",
        },
        "DarkSide": {
            "patterns": ["ransomware_payment", "mixer_usage"],
            "confidence": 0.81,
            "mitre_id": "G0139",
            "description": "Ransomware-as-a-service operator using crypto for payments",
        },
    }
    
    def __init__(self, use_advanced: bool = False) -> None:
        """Initialize with optional advanced analyzer"""
        self.advanced = AdvancedAnalyzer() if use_advanced else None

    def predict_threats(
        self, entity_graph: dict[str, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Analyze behavior patterns against threat database.

        Args:
            entity_graph: Processed entity graph from EvidenceCorrelator.

        Returns:
            List of threat match dicts with entity, threat name, confidence, and patterns.
        """
        threat_matches: list[dict[str, Any]] = []

        for entity, data in entity_graph.items():
            behavior = data["metadata"].get("behavior", [])
            if not behavior:
                continue

            for threat, profile in self.THREAT_DB.items():
                if not profile["patterns"]:
                    continue  # Guard against empty pattern lists

                matched = set(behavior) & set(profile["patterns"])
                match_score = len(matched) / len(profile["patterns"])
                if match_score > 0.7:
                    threat_matches.append(
                        {
                            "entity": entity,
                            "threat": threat,
                            "confidence": min(profile["confidence"], match_score),
                            "patterns": list(matched),
                        }
                    )
        
        # Apply advanced enrichment if available
        if self.advanced:
            threat_matches = self.advanced.enrich_threats(threat_matches)

        logger.info(f"[Vajra] Detected {len(threat_matches)} threat actor matches")
        return threat_matches

    def predict_next_targets(
        self, wallet_cluster: dict[str, list[str]]
    ) -> list[str]:
        """Predict future targets based on historical patterns.

        Args:
            wallet_cluster: Shell company clusters from identify_shell_companies().

        Returns:
            List of high-risk wallet addresses.
        """
        targets: list[str] = []
        for pattern, wallets in wallet_cluster.items():
            if len(wallets) > 2:
                targets.extend(wallets[:2])  # First two in cluster

        logger.info(f"[Vajra] Predicted {len(targets)} high-risk targets")
        return targets


# === Report Generation ===

class ReportAutomator:
    """Generate court-ready forensic reports from analysis insights."""

    TEMPLATE = """
FORENSIC REPORT - {case_id}
Generated: {timestamp}

=== EXECUTIVE SUMMARY ===
{summary}

=== THREAT ANALYSIS ===
{threat_analysis}

=== RECOMMENDED ACTIONS ===
{actions}
"""

    def generate(self, insights: dict[str, Any]) -> str:
        """Generate court-ready forensic report.

        Args:
            insights: Dict containing entity_graph, threat_matches,
                      processing_time, and case_data.

        Returns:
            Formatted report string.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format threat analysis
        threat_analysis = "\n".join(
            f"- {m['entity']}: Likely {m['threat']} "
            f"(confidence: {m['confidence']*100:.1f}%)"
            for m in insights["threat_matches"]
        )

        # Generate report
        report = self.TEMPLATE.format(
            case_id=insights["case_data"]["case_id"],
            timestamp=timestamp,
            summary=(
                f"Analysis completed in {insights['processing_time']:.2f}s. "
                f"Identified {len(insights['entity_graph'])} entities with "
                f"{len(insights['threat_matches'])} threat matches."
            ),
            threat_analysis=threat_analysis or "No significant threats detected",
            actions=(
                "1. Freeze identified high-risk accounts\n"
                "2. Initiate blockchain monitoring\n"
                "3. Notify regulatory authorities"
            ),
        )

        logger.info(
            f"[Vajra] Generated court-ready report for "
            f"{insights['case_data']['case_id']}"
        )
        return report


# === Main Orchestration ===

class VajraSystem:
    """End-to-end forensic case processing pipeline.

    Orchestrates evidence correlation, threat analysis, and report
    generation in a single solve_case() call.
    """

    def __init__(self, case_data: dict[str, Any], use_advanced_threat: bool = False) -> None:
        if "case_id" not in case_data:
            raise ValueError("case_data must contain 'case_id'")
        if "evidence" not in case_data:
            raise ValueError("case_data must contain 'evidence' list")

        self.case_data = case_data
        self.correlator = EvidenceCorrelator(case_data)
        self.analyzer = PatternAnalyzer(use_advanced=use_advanced_threat)
        self.reporter = ReportAutomator()

        # Pipeline results (populated after solve_case)
        self._last_processing_time: float = 0.0
        self._last_entity_graph: dict[str, Any] = {}
        self._last_threat_matches: list[dict[str, Any]] = []

    def solve_case(self) -> str:
        """End-to-end case processing pipeline.

        Steps:
            1. Link evidence → entity graph
            2. Detect shell companies
            3. Match threat actors
            4. Predict high-risk targets
            5. Generate court-ready report

        Returns:
            Formatted forensic report string.
        """
        start_time = time.time()

        # Processing pipeline
        entity_graph = self.correlator.link_evidence()
        shell_companies = self.correlator.identify_shell_companies()
        self.correlator.run_advanced_analytics()  # Run temporal/Benford analysis
        threat_matches = self.analyzer.predict_threats(entity_graph)
        high_risk_targets = self.analyzer.predict_next_targets(shell_companies)

        # Compile insights
        processing_time = time.time() - start_time
        insights = {
            "entity_graph": entity_graph,
            "shell_companies": shell_companies,
            "temporal_clusters": self.correlator.temporal_clusters,
            "benford_anomalies": self.correlator.benford_anomalies,
            "threat_matches": threat_matches,
            "high_risk_targets": high_risk_targets,
            "shell_networks": self.correlator.shell_networks,
            "centralities": self.correlator.centralities,
            "key_nodes": self.correlator.key_nodes,
            "rings": self.correlator.rings,
            "processing_time": processing_time,
            "case_data": self.case_data,
        }

        # Store results for API access
        self._last_processing_time = processing_time
        self._last_entity_graph = entity_graph
        self._last_threat_matches = threat_matches

        # Generate final report
        return self.reporter.generate(insights)


# === Example Execution ===

if __name__ == "__main__":
    # Sample case data
    case_data = {
        "case_id": "CRYPTO-FRAUD-2024-001",
        "evidence": [
            {
                "source": "wallet_A",
                "type": "crypto_wallet",
                "transactions": ["deposit_1", "withdraw_2", "transfer_3"],
                "behavior": ["fee_evasion", "micro_transactions"],
                "related_to": ["wallet_B", "wallet_C"],
            },
            {
                "source": "wallet_B",
                "type": "crypto_wallet",
                "transactions": ["deposit_4", "withdraw_5"],
                "behavior": ["fee_evasion", "micro_transactions"],
                "related_to": ["wallet_A", "wallet_D"],
            },
            {
                "source": "wallet_C",
                "type": "crypto_wallet",
                "transactions": ["deposit_1", "withdraw_6"],
                "behavior": ["time_delayed"],
                "related_to": ["wallet_A"],
            },
        ],
    }

    # Process case
    vajra = VajraSystem(case_data)
    report = vajra.solve_case()
    print("\n" + "=" * 50)
    print("FINAL REPORT")
    print("=" * 50)
    print(report)