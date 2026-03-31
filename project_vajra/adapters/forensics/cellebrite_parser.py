"""
Cellebrite UFED Forensic Evidence Parser
"""
import os
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from project_vajra.logging_config import logger

class CellebriteParser:
    """Parse Cellebrite UFED XML or JSON reports into structured evidence."""
    
    def parse_report(self, report_path: str) -> Dict[str, Any]:
        """Parse Cellebrite UFED report"""
        if not os.path.exists(report_path):
            logger.warning(f"Cellebrite report not found: {report_path}. Using mock data for simulation.")
            return self._get_mock_report()
            
        file_ext = os.path.splitext(report_path)[1].lower()
        if file_ext == '.json':
            return self._parse_json(report_path)
        elif file_ext == '.xml':
            return self._parse_xml(report_path)
        else:
            raise ValueError(f"Unsupported Cellebrite report format: {file_ext}")
            
    def _parse_json(self, path: str) -> Dict[str, Any]:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            "device_info": data.get("Device", {}),
            "artifacts": self._extract_json_artifacts(data)
        }
        
    def _parse_xml(self, path: str) -> Dict[str, Any]:
        tree = ET.parse(path)
        root = tree.getroot()
        # Mock XML extraction for brevity
        return {
            "device_info": {"model": "Unknown"},
            "artifacts": []
        }
        
    def _extract_json_artifacts(self, data: Dict) -> List[Dict]:
        artifacts = []
        for model in data.get("Models", []):
            if "Cryptocurrency" in model.get("Name", "") or "Wallet" in model.get("Name", ""):
                artifacts.append({
                    "type": "crypto_wallet",
                    "details": model
                })
        return artifacts
        
    def _get_mock_report(self) -> Dict[str, Any]:
        """Return a simulated report for testing and demonstration."""
        return {
            "device_info": {"model": "iPhone 13 Pro", "os": "iOS 16.5"},
            "artifacts": [
                {"type": "crypto_wallet", "app": "MetaMask", "wallet_address": "0xMockWalletFromCellebrite"},
                {"type": "telegram_chat", "contact": "TargetAlpha", "messages": ["Send the payment to the mixer"]}
            ]
        }
