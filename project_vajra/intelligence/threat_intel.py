"""
Advanced Threat Intelligence Module
"""
from typing import List, Dict, Any
from project_vajra.intelligence.claude_client import ClaudeAnalyzer
from project_vajra.logging_config import logger

class AdvancedAnalyzer:
    """Extends PatternAnalyzer with dynamic threat intel"""
    
    MITRE_MAPPING = {
        "fee_evasion": "T1496 - Resource Hijacking",
        "micro_transactions": "T1485 - Data Destruction",
        "time_delayed": "T1205 - Traffic Signaling",
        "ransomware_payment": "T1486 - Data Encrypted for Impact",
        "mixer_usage": "T1410 - Obfuscated Files or Information"
    }
    
    def __init__(self, claude_api_key: str = None) -> None:
        self.claude = ClaudeAnalyzer(api_key=claude_api_key)
        
    def enrich_threats(self, threat_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add MITRE techniques and detection guidance"""
        for match in threat_matches:
            techniques = []
            for pattern in match['patterns']:
                if pattern in self.MITRE_MAPPING:
                    techniques.append(self.MITRE_MAPPING[pattern])
            
            match['mitre_techniques'] = techniques
            
            # Generate detection logic
            if techniques:
                match['detection'] = self.generate_sigma_rule(
                    match['patterns'],
                    match['threat']
                )
        
        logger.info(f"[Vajra] Enriched {len(threat_matches)} threat matches with MITRE techniques")
        return threat_matches
    
    def generate_sigma_rule(self, patterns: List[str], threat_group: str) -> str:
        """Create Sigma rule for detection"""
        conditions = " or ".join([f"{p} in patterns" for p in patterns])
        return f"""
title: Detect {threat_group} Activity
status: experimental
description: Detects patterns associated with {threat_group}
detection:
    selection:
        patterns|contains:
            - {conditions}
    condition: selection
level: high"""
    
    def update_threat_db(self, intel_report: str) -> None:
        """Dynamically update threat DB from unstructured intel"""
        threat_actors = self.claude.extract_threat_actors(intel_report)
        logger.info(f"[Vajra] Extracted {len(threat_actors)} threat actors from intel report")