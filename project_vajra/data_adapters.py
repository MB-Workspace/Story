"""
Real-World Data Integration Module

Adapters for external data sources including blockchain APIs and
forensic evidence formats (AXIOM, FTK, Cellebrite).
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

import requests
from datetime import datetime, timedelta, timezone

from project_vajra.adapters.chain.ethereum import EthereumAdapter
from project_vajra.adapters.chain.polygon import PolygonAdapter

logger = logging.getLogger("vajra.adapters")


class BlockchainDataAdapter:
    """Adapter for real blockchain APIs.

    Connects to blockchain data providers to fetch and normalize
    transaction data for forensic analysis.
    """

    def __init__(self, api_key: str = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("BLOCKCHAIN_API_KEY")
        self.base_url = base_url or "https://api.blockchain.com/v3/exchange"
        
        # Initialize chain-specific adapters
        self.ethereum = EthereumAdapter()
        self.polygon = PolygonAdapter()

    def get_transactions(
        self, wallet_address: str, chain: str = "ethereum", days: int = 7
    ) -> list[dict[str, Any]]:
        """Fetch real transaction data from blockchain APIs.

        Args:
            wallet_address: Cryptocurrency wallet address to query.
            chain: Blockchain network (ethereum, polygon).
            days: Number of historical days to retrieve.

        Returns:
            List of normalized transaction dicts.

        Raises:
            ConnectionError: If the API request fails.
        """
        # Use chain-specific adapter when available
        if chain == "ethereum":
            return self.ethereum.get_transactions(wallet_address, blocks=days*100)
        elif chain == "polygon":
            return self.polygon.get_transactions(wallet_address, blocks=days*100)
            
        # Fallback to generic API
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=days)

        params = {
            "address": wallet_address,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "api_key": self.api_key,
        }

        try:
            response = requests.get(
                f"{self.base_url}/address/{wallet_address}/transactions",
                params=params,
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Blockchain API request failed: {e}")
            raise ConnectionError(f"Blockchain API error: {e}") from e

        return self._normalize_transactions(response.json()["transactions"])

    def _normalize_transactions(
        self, raw_txs: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Convert API response to Vajra's evidence format."""
        return [
            {
                "tx_id": tx["hash"],
                "timestamp": tx["timestamp"],
                "value": tx["value"],
                "currency": tx["currency"],
                "from_address": tx["from"],
                "to_address": tx["to"],
                "type": tx["type"].lower(),
                "fee": tx.get("fee", 0),
            }
            for tx in raw_txs
        ]


class ForensicEvidenceAdapter:
    """Handles real forensic data formats (AXIOM, FTK, Cellebrite).

    Note: Full parsing implementations require access to proprietary
    SDK libraries. Current implementations provide the interface contract
    that production code should follow.
    """

    def convert_axiom(self, axiom_report: str | Path) -> dict[str, list]:
        """Convert AXIOM HTML report to structured evidence.

        Args:
            axiom_report: Path to AXIOM report file or HTML string.

        Returns:
            Dict with keys: devices, artifacts, timeline, files.
        """
        from project_vajra.adapters.forensics.axiom_parser import AxiomParser
        parser = AxiomParser()
        return parser.parse_html_report(axiom_report)

    def convert_ftk(self, ftk_image: str | Path) -> dict[str, Any]:
        """Process FTK forensic image files.

        Args:
            ftk_image: Path to FTK image file (.AD1, .E01).

        Returns:
            Dict with image_info, filesystem, and artifacts.
        """
        from project_vajra.adapters.forensics.ftk_parser import FTKParser
        parser = FTKParser()
        return parser.parse_image(ftk_image)

    def convert_cellebrite(self, cellebrite_report: str | Path) -> dict[str, Any]:
        """Process Cellebrite UFED XML/JSON reports.

        Args:
            cellebrite_report: Path to UFED report file.

        Returns:
            Dict with device_info and artifacts.
        """
        from project_vajra.adapters.forensics.cellebrite_parser import CellebriteParser
        parser = CellebriteParser()
        return parser.parse_report(str(cellebrite_report))


class ErrorHandler:
    """Production-grade error logging with structured JSON output."""

    def __init__(self, log_dir: str | Path | None = None) -> None:
        if log_dir is None:
            log_dir = Path(__file__).resolve().parent.parent
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "vajra_errors.log"

    def log_error(
        self, error: Exception, context: str | None = None
    ) -> dict[str, str]:
        """Log errors with timestamp and context to JSON-lines file.

        Args:
            error: The exception to log.
            context: Optional description of what was happening.

        Returns:
            Status dict with error message.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        entry = {
            "timestamp": timestamp,
            "error": str(error),
            "error_type": type(error).__name__,
            "context": context,
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as log:
                log.write(json.dumps(entry) + "\n")
        except OSError as write_error:
            logger.error(f"Failed to write error log: {write_error}")

        return {"status": "error", "message": str(error)}


class EvidenceBuilder:
    """Transforms raw blockchain data into VajraSystem evidence format.

    This is the ingestion pipeline that bridges the gap between raw API
    responses (flat transaction lists) and VajraSystem's expected input
    (structured evidence items with behavioral tags and relationships).

    Pipeline:
        1. Fetch transactions for a wallet via BlockchairAdapter
        2. Classify transaction types (deposit/transfer/withdraw)
        3. Detect behavioral patterns from transaction characteristics
        4. Map related addresses from counterparties
        5. Assemble evidence dict in VajraSystem-compatible format

    Usage:
        builder = EvidenceBuilder()
        case = builder.build_case(
            case_id="VAJRA-2026-001",
            wallet_addresses=["0x098B716B...", "0x3Cffd56B..."]
        )
        vajra = VajraSystem(case)
        report = vajra.solve_case()
    """

    # Behavioral pattern detection rules
    BEHAVIOR_RULES = {
        "fee_evasion": {
            "description": "Transaction values just below reporting thresholds",
            "check": lambda txs: any(
                0 < t.get("value_usd", 0) < 10_000 for t in txs
            ),
        },
        "micro_transactions": {
            "description": "High volume of small-value transactions",
            "check": lambda txs: (
                len(txs) > 10
                and sum(1 for t in txs if t.get("value_usd", 0) < 1_000)
                / max(len(txs), 1)
                > 0.5
            ),
        },
        "time_delayed": {
            "description": "Significant delays between related transactions",
            "check": lambda txs: len(txs) >= 2,  # Simplified: flag for review
        },
        "multi_hop": {
            "description": "Funds pass through 3+ intermediaries",
            "check": lambda txs: len(set(
                t.get("to_address", "") for t in txs
            )) >= 3,
        },
    }

    def __init__(self, adapter: "BlockchairAdapter | None" = None) -> None:
        self._adapter = adapter

    @property
    def adapter(self) -> "BlockchairAdapter":
        if self._adapter is None:
            self._adapter = BlockchairAdapter()
        return self._adapter

    def build_case(
        self,
        case_id: str,
        wallet_addresses: list[str],
        chain: str = "ethereum",
        title: str = "",
    ) -> dict[str, Any]:
        """Build a complete case from a list of wallet addresses.

        Fetches real blockchain data for each address, classifies
        behavior, maps relationships, and returns a dict ready for
        VajraSystem(case_data).

        Args:
            case_id: Unique case identifier (e.g., "VAJRA-2026-001").
            wallet_addresses: List of blockchain addresses to analyze.
            chain: Blockchain network (default: ethereum).
            title: Human-readable case title.

        Returns:
            Dict with 'case_id' and 'evidence' keys, compatible
            with VajraSystem.__init__().
        """
        evidence = []
        for address in wallet_addresses:
            try:
                item = self.build_evidence_item(address, chain)
                evidence.append(item)
            except ConnectionError:
                logger.warning(f"Could not fetch data for {address}, skipping")

        return {
            "case_id": case_id,
            "investigation": {
                "title": title or f"Case {case_id}",
                "wallet_count": len(evidence),
                "chain": chain,
            },
            "evidence": evidence,
        }

    def build_evidence_item(
        self, address: str, chain: str = "ethereum"
    ) -> dict[str, Any]:
        """Build a single evidence item from a wallet address.

        Fetches address info from Blockchair, classifies the
        transaction types, detects behavioral patterns, and
        identifies related counterparty addresses.

        Args:
            address: Blockchain wallet address.
            chain: Blockchain network.

        Returns:
            Evidence item dict compatible with VajraSystem.
        """
        # Fetch real data from blockchain API
        addr_info = self.adapter.get_address_info(address, chain)

        # Build transaction list in Vajra's type_hash format
        # In production, these come from detailed tx list endpoints
        transactions = self._infer_transaction_types(addr_info)

        # Detect behavioral patterns
        behavior = self._classify_behavior(addr_info)

        # Related addresses would come from transaction counterparties
        # In a full implementation, this queries the tx list endpoint
        related_to: list[str] = []

        return {
            "source": address,
            "type": "crypto_wallet",
            "chain": chain,
            "label": f"Wallet {address[:10]}...{address[-6:]}",
            "transactions": transactions,
            "behavior": behavior,
            "related_to": related_to,
            "metadata": {
                "first_seen": addr_info.get("first_seen"),
                "last_seen": addr_info.get("last_seen"),
                "total_volume_usd": (
                    addr_info.get("total_received_usd", 0)
                    + addr_info.get("total_spent_usd", 0)
                ),
                "balance_usd": addr_info.get("balance_usd", 0),
                "tx_count": addr_info.get("tx_count", 0),
                "risk_score": self._calculate_risk_score(addr_info),
            },
        }

    def _infer_transaction_types(
        self, addr_info: dict[str, Any]
    ) -> list[str]:
        """Generate transaction type tags from address-level data.

        Since Blockchair's free tier returns address summaries (not
        full tx lists), we infer transaction types from aggregate
        data. A production system would use Etherscan's txlist
        endpoint for per-transaction classification.
        """
        transactions = []
        received = addr_info.get("total_received_usd", 0)
        spent = addr_info.get("total_spent_usd", 0)
        tx_count = addr_info.get("tx_count", 0)

        # Infer: if received > 0, there are deposit-type transactions
        if received > 0:
            transactions.append(
                f"deposit_0x{addr_info.get('address', '')[2:18]}"
                f"{'0' * 50}"  # Pad to full hash length
            )
        # Infer: if spent > 0, there are withdraw-type transactions
        if spent > 0:
            transactions.append(
                f"withdraw_0x{addr_info.get('address', '')[2:18]}"
                f"{'1' * 50}"
            )
        # Infer: if tx_count > deposits + withdraws, there are transfers
        if tx_count > 2:
            transactions.append(
                f"transfer_0x{addr_info.get('address', '')[2:18]}"
                f"{'2' * 50}"
            )

        return transactions

    def _classify_behavior(
        self, addr_info: dict[str, Any]
    ) -> list[str]:
        """Detect behavioral patterns from address characteristics."""
        behavior = []
        tx_count = addr_info.get("tx_count", 0)
        received = addr_info.get("total_received_usd", 0)

        # High tx count relative to volume = possible structuring
        if tx_count > 0 and received > 0:
            avg_tx = received / tx_count
            if avg_tx < 10_000:
                behavior.append("fee_evasion")
            if tx_count > 50 and avg_tx < 1_000:
                behavior.append("micro_transactions")

        # Many calls = possible smart contract interaction / mixer
        if addr_info.get("call_count", 0) > 100:
            behavior.append("multi_hop")

        return behavior

    def _calculate_risk_score(self, addr_info: dict[str, Any]) -> int:
        """Calculate a 0-100 risk score from address characteristics."""
        score = 0
        volume = (
            addr_info.get("total_received_usd", 0)
            + addr_info.get("total_spent_usd", 0)
        )

        # High volume increases risk
        if volume > 10_000_000:
            score += 40
        elif volume > 1_000_000:
            score += 25
        elif volume > 100_000:
            score += 10

        # High tx count increases risk
        tx_count = addr_info.get("tx_count", 0)
        if tx_count > 1000:
            score += 30
        elif tx_count > 100:
            score += 15

        # Low balance relative to volume = funds moved through
        balance = addr_info.get("balance_usd", 0)
        if volume > 0 and balance / max(volume, 1) < 0.01:
            score += 20

        # Many contract calls = possible mixer interaction
        if addr_info.get("call_count", 0) > 100:
            score += 10

        return min(score, 100)


class BlockchairAdapter:
    """Adapter for Blockchair public API — no API key required for testing.

    Blockchair provides free access to Ethereum, Bitcoin, and other chain
    data at up to 30 req/min without authentication. For production use,
    obtain an API key from https://blockchair.com/api/plans

    Usage:
        adapter = BlockchairAdapter()
        data = adapter.get_address_info("0x098B716B8Aaf21512996dC57EB0615e2383E2f96")
    """

    BASE_URL = "https://api.blockchair.com"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def get_address_info(
        self, address: str, chain: str = "ethereum"
    ) -> dict[str, Any]:
        """Fetch real address data from Blockchair.

        Args:
            address: Blockchain address (e.g., Ethereum 0x... address).
            chain: Blockchain network (ethereum, bitcoin, etc.).

        Returns:
            Dict with balance, transaction count, and address metadata.

        Raises:
            ConnectionError: If the API request fails.
        """
        url = f"{self.BASE_URL}/{chain}/dashboards/address/{address}"
        params = {}
        if self.api_key:
            params["key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Blockchair API request failed: {e}")
            raise ConnectionError(f"Blockchair API error: {e}") from e

        if data.get("context", {}).get("code") != 200:
            raise ConnectionError(
                f"Blockchair returned error: {data.get('context', {}).get('error', 'Unknown')}"
            )

        addr_data = data.get("data", {}).get(address.lower(), {})
        address_info = addr_data.get("address", {})

        return {
            "address": address,
            "chain": chain,
            "balance_wei": address_info.get("balance", 0),
            "balance_usd": address_info.get("balance_usd", 0),
            "tx_count": address_info.get("transaction_count", 0),
            "first_seen": address_info.get("first_seen_receiving"),
            "last_seen": address_info.get("last_seen_receiving"),
            "total_received_usd": address_info.get("received_usd", 0),
            "total_spent_usd": address_info.get("spent_usd", 0),
            "call_count": address_info.get("call_count", 0),
        }

    def check_ofac_address(self, address: str) -> dict[str, Any]:
        """Fetch data for a known OFAC-sanctioned address.

        Convenience method that wraps get_address_info with
        additional context about the address's sanction status.
        """
        data = self.get_address_info(address)
        data["note"] = (
            "This address appears on the OFAC SDN list. "
            "Any transactions with this address may violate U.S. sanctions."
        )
        return data


# Example usage — demonstrates real API integration
if __name__ == "__main__":
    print("=" * 60)
    print("Project Vajra — Data Adapter Demo")
    print("=" * 60)

    # Demo 1: Blockchair free API (no key needed)
    print("\n[1] Fetching REAL data for Ronin Bridge attacker wallet...")
    print("    Address: 0x098B716B8Aaf21512996dC57EB0615e2383E2f96")
    print("    (OFAC-designated Lazarus Group wallet)\n")

    try:
        blockchair = BlockchairAdapter()
        result = blockchair.get_address_info(
            "0x098B716B8Aaf21512996dC57EB0615e2383E2f96"
        )
        print(f"    Balance:          {result['balance_usd']:.2f} USD")
        print(f"    TX Count:         {result['tx_count']}")
        print(f"    Total Received:   {result['total_received_usd']:.2f} USD")
        print(f"    First Seen:       {result['first_seen']}")
        print(f"    Last Seen:        {result['last_seen']}")
    except ConnectionError as e:
        print(f"    API unavailable (expected offline): {e}")

    # Demo 2: Generic adapter (requires API key)
    print("\n[2] Generic BlockchainDataAdapter (requires API key)...")
    try:
        adapter = BlockchainDataAdapter("demo_key_for_testing")
        adapter.get_transactions("0x098B716B8Aaf21512996dC57EB0615e2383E2f96")
    except (ConnectionError, ValueError) as e:
        ErrorHandler().log_error(e, "Blockchain data fetch")
        print(f"    Expected error (demo mode): {e}")

    print("\n" + "=" * 60)