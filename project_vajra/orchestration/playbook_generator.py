"""
OpenClaw Playbook Generator
"""
import yaml
from typing import Dict, Any, List

class PlaybookGenerator:
    """Generate OpenClaw playbooks from Vajra insights"""
    
    def generate_crypto_fraud_response(
        self,
        threat_matches: List[Dict[str, Any]],
        high_risk_targets: List[str],
        severity: str = "high"
    ) -> str:
        """Generate YAML playbook for crypto fraud response"""
        playbook = {
            "name": "Crypto Fraud Response",
            "description": "Automated response to crypto fraud detection",
            "steps": [
                {
                    "name": "Collect blockchain evidence",
                    "action": "antigravity.collect",
                    "params": {
                        "sources": ["blockchain", "exchange"],
                        "time_range": "72h"
                    }
                },
                {
                    "name": "Analyze transaction patterns",
                    "action": "vajra.analyze",
                    "params": {
                        "modules": ["temporal", "benford"]
                    }
                },
                {
                    "name": "Enrich with threat intel",
                    "action": "claude.enrich",
                    "params": {
                        "threat_db": "latest"
                    }
                },
                {
                    "name": "Generate containment plan",
                    "action": "vajra.contain",
                    "params": {
                        "severity": severity
                    }
                },
                {
                    "name": "Execute wallet freezing",
                    "action": "exchange_api.freeze",
                    "params": {
                        "wallets": high_risk_targets
                    }
                },
                {
                    "name": "Produce court documentation",
                    "action": "vajra.report",
                    "params": {
                        "template": "legal_affidavit"
                    }
                }
            ]
        }
        
        # Add threat-specific steps
        for threat in threat_matches:
            playbook["steps"].insert(3, {
                "name": f"Deploy {threat['threat']} countermeasures",
                "action": "vajra.deploy",
                "params": {
                    "threat": threat["threat"],
                    "techniques": threat.get("mitre_techniques", [])
                }
            })
            
        return yaml.dump(playbook, sort_keys=False)
    
    def generate_ransomware_response(
        self,
        ransomware_type: str,
        payment_addresses: List[str],
        severity: str = "critical"
    ) -> str:
        """Generate YAML playbook for ransomware response"""
        return yaml.dump({
            "name": "Ransomware Response",
            "description": "Automated response to ransomware detection",
            "steps": [
                {
                    "name": "Identify ransomware wallets",
                    "action": "vajra.identify",
                    "params": {
                        "type": ransomware_type
                    }
                },
                {
                    "name": "Freeze payment addresses",
                    "action": "exchange_api.freeze",
                    "params": {
                        "wallets": payment_addresses
                    }
                },
                {
                    "name": "Deploy decoy contract",
                    "action": "antigravity.honeycontract",
                    "params": {
                        "bait_amount": "0.5",
                        "attacker_pattern": ransomware_type
                    }
                },
                {
                    "name": "Generate incident report",
                    "action": "vajra.report",
                    "params": {
                        "template": "ransomware_response"
                    }
                }
            ]
        }, sort_keys=False)