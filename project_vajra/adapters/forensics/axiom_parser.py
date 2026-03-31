"""
AXIOM Forensic Evidence Parser
"""
import os
import re
from bs4 import BeautifulSoup
from typing import Dict, List

class AxiomParser:
    """Parse AXIOM HTML reports into structured evidence"""
    
    def parse_html_report(self, report_path: str) -> Dict[str, List]:
        """Parse AXIOM HTML report into structured evidence"""
        if not os.path.exists(report_path):
            raise FileNotFoundError(f"AXIOM report not found: {report_path}")
            
        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract devices
        devices = []
        for device_div in soup.select('div.device-section'):
            try:
                h3 = device_div.select_one('h3')
                device_type = device_div.select_one('.device-type')
                devices.append({
                    "name": h3.text.strip() if h3 else "Unknown",
                    "type": device_type.text.strip() if device_type else "Unknown"
                })
            except Exception:
                continue
            
        # Extract artifacts
        artifacts = []
        for artifact_row in soup.select('tr.artifact-row'):
            try:
                cells = artifact_row.select('td')
                if len(cells) >= 3:
                    count_text = cells[2].text.strip()
                    artifacts.append({
                        "name": cells[0].text.strip(),
                        "category": cells[1].text.strip(),
                        "count": int(count_text) if count_text.isdigit() else 0
                    })
            except Exception:
                continue
                
        # Extract timeline events
        timeline = []
        for event_div in soup.select('div.timeline-event'):
            try:
                event_time = event_div.select_one('.event-time')
                event_desc = event_div.select_one('.event-desc')
                timeline.append({
                    "timestamp": event_time.text.strip() if event_time else "Unknown",
                    "description": event_desc.text.strip() if event_desc else ""
                })
            except Exception:
                continue
            
        # Extract files
        files = []
        for file_row in soup.select('tr.file-row'):
            try:
                cells = file_row.select('td')
                if len(cells) >= 4:
                    files.append({
                        "name": cells[0].text.strip(),
                        "path": cells[1].text.strip(),
                        "size": cells[2].text.strip(),
                        "hash": cells[3].text.strip()
                    })
            except Exception:
                continue
                
        return {
            "devices": devices,
            "artifacts": artifacts,
            "timeline": timeline,
            "files": files
        }