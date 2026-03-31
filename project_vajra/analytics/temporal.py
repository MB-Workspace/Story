"""
Enhanced Evidence Correlator with Temporal Analysis and Benford's Law
"""
from project_vajra.core import EvidenceCorrelator
from datetime import datetime
from typing import Any, Dict, List

class EnhancedCorrelator(EvidenceCorrelator):
    """Extends base correlator with blockchain-specific forensic methods"""
    
    def analyze_crypto_transactions(self) -> Dict[str, List[Dict]]:
        """Cluster transactions using temporal and value patterns
        
        Returns:
            Dict with signature keys and list of matching transactions
        """
        # Aggregate all transactions from evidence
        all_transactions = []
        for item in self.case_data.get("evidence", []):
            if "transactions" in item:
                all_transactions.extend(item["transactions"])
                
        if not all_transactions:
            return {}
            
        clusters = {}
        for tx in all_transactions:
            # Skip string transactions (format: "type_hash")
            if isinstance(tx, str):
                continue
                
            # Skip if not a dict with required keys
            if not isinstance(tx, dict):
                continue
                
            # Get timestamp - skip if not present
            tx_timestamp = tx.get("timestamp")
            if not tx_timestamp:
                continue
                
            # Parse timestamp if needed
            try:
                if isinstance(tx_timestamp, str):
                    tx_time = datetime.fromisoformat(tx_timestamp)
                else:
                    tx_time = tx_timestamp
            except (ValueError, TypeError):
                continue
            
            # Get value - default to 0 if not present
            tx_value = tx.get("value", 0)
            
            # Create temporal signature (hourly patterns)
            time_sig = f"{tx_time.hour}-{tx_value//1000}k"
            
            # Create behavioral signature
            behavior_sig = ":".join(sorted(tx.get("tags", [])))
            
            # Composite signature
            signature = f"{time_sig}|{behavior_sig}"
            
            if signature not in clusters:
                clusters[signature] = []
            clusters[signature].append(tx)
            
        return clusters
    
    def identify_money_laundering(self) -> List[Dict[str, Any]]:
        """Detect structuring patterns using Benford's Law
        
        Returns:
            List of anomalies with digit, actual, expected, and deviation
        """
        # Aggregate all transaction amounts
        amounts = []
        for item in self.case_data.get("evidence", []):
            if "transactions" in item:
                for tx in item["transactions"]:
                    # Skip string transactions
                    if isinstance(tx, str):
                        continue
                    if isinstance(tx, dict) and tx.get("value", 0) > 0:
                        amounts.append(tx["value"])
                
        if not amounts:
            return []
            
        # Get first digits
        first_digits = [int(str(amt)[0]) for amt in amounts]
        
        # Benford's expected distribution
        benford = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
        
        anomalies = []
        total = len(first_digits)
        for digit in range(1, 10):
            actual = first_digits.count(digit) / total
            expected = benford[digit-1]
            deviation = abs(actual - expected)
            
            if deviation > 0.15:  # 15% deviation threshold
                anomalies.append({
                    'digit': digit,
                    'actual': actual,
                    'expected': expected,
                    'deviation': deviation
                })
        
        return anomalies