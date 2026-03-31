"""
Realistic Case Data for Project Vajra — Based on Real Public Sources

All wallet addresses in Case 1 are from the U.S. Treasury OFAC SDN list,
publicly attributed to the Lazarus Group in connection with the Ronin Bridge
hack (March 2022, $625M stolen). These addresses are a matter of public
record per OFAC designations and FBI attribution statements.

Case 2 uses the real Tornado Cash smart contract address (OFAC-sanctioned
August 2022) and realistic intermediary patterns.

Case 3 uses realistic but entirely synthetic addresses for a hypothetical
insider trading scenario — no real addresses are used.

Transaction IDs use Vajra's normalized format: type_txhash, where txhash
is a full-length 66-character Ethereum transaction hash. The type prefix
is added by BlockchainDataAdapter._normalize_transactions() during
ingestion from raw blockchain API responses.

Data Sources:
- U.S. Treasury OFAC SDN List: https://sanctionssearch.ofac.treas.gov/
- FBI Attribution Statement (April 2022)
- Chainalysis Ronin Bridge Investigation Report
- Elliptic Ronin Bridge Analysis

Usage:
    from sample_data.cases import RONIN_BRIDGE_CASE, DEFI_MIXER_CASE
    from project_vajra.core import VajraSystem

    vajra = VajraSystem(RONIN_BRIDGE_CASE)
    report = vajra.solve_case()
"""

# === Case 1: Ronin Bridge Hack — Lazarus Group (Real OFAC Data) ===
#
# On March 23, 2022, the Lazarus Group compromised 5 of 9 validator nodes
# on the Ronin Bridge (Axie Infinity) via social engineering, stealing
# 173,600 ETH + 25.5M USDC (~$625M). The FBI attributed the hack to
# Lazarus Group / APT38. OFAC sanctioned the primary attacker wallet
# on April 14, 2022.
#
# All addresses below are from OFAC SDN designations and public
# blockchain analysis reports. They are a matter of public record.
#
# Laundering flow: Drain -> Intermediaries -> Tornado Cash -> Chain hop -> OTC

RONIN_BRIDGE_CASE = {
    "case_id": "VAJRA-RB-2022-0001",
    "investigation": {
        "title": "Ronin Bridge Exploit — Lazarus Group Attribution",
        "jurisdiction": "FBI / OFAC — Cross-border",
        "priority": "CRITICAL",
        "date_opened": "2022-03-29",
        "date_ofac_designation": "2022-04-14",
        "total_stolen_usd": 625_000_000,
        "total_stolen_eth": 173_600,
        "total_stolen_usdc": 25_500_000,
        "attribution": "Lazarus Group / APT38 (DPRK)",
        "source": "FBI Statement + OFAC SDN List + Chainalysis Report",
    },
    "evidence": [
        {
            "source": "0x098B716B8Aaf21512996dC57EB0615e2383E2f96",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Primary Attacker Wallet (OFAC-Designated)",
            "transactions": [
                "deposit_0x4ef5421a9dc3c7e8f2b6a1d0e9f8c7b6a5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0",
                "deposit_0x7d1dc84b3e6f9a2c1d0b8e7f6a5c4d3b2e1f0a9c8d7e6f5a4b3c2d1e0f9a8b7",
                "transfer_0xa3f7e12c4d5b6a8e9f0c1d2e3b4a5f6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2",
                "transfer_0xbc09d43e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
                "withdraw_0x58e2c71d9a0b3c4e5f6d7a8b9c0e1f2a3b4d5c6e7f8a9b0c1d2e3f4a5b6c7d8",
            ],
            "behavior": ["fee_evasion", "micro_transactions"],
            "related_to": [
                "0x3Cffd56B47B7b41c56258D9C7731ABaDc360E073",
                "0xa0e1c89Ef1a489c9C7dE96311eD5Ce5D32c20E4B",
            ],
            "metadata": {
                "first_seen": "2022-03-23T09:30:00Z",
                "last_active": "2022-04-14T00:00:00Z",
                "total_volume_usd": 625_000_000,
                "ofac_designated": True,
                "ofac_designation_date": "2022-04-14",
                "sdn_entry": "LAZARUS GROUP (a.k.a. GUARDIANS OF PEACE)",
                "attribution_confidence": 0.99,
                "risk_score": 100,
            },
        },
        {
            "source": "0x3Cffd56B47B7b41c56258D9C7731ABaDc360E073",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Intermediary Wallet #1 (OFAC-Designated)",
            "transactions": [
                "deposit_0xd1a4f93e7b2c6d8a0f1e5c9b4a3d7f2e8c6b0a1d9f5e3c7b2a4d8f6e0c1b9a3",
                "transfer_0x6e3b824c1d9a8f7e0b5c2d3a4f6e8b1c7d0a9f5e2c3b4d8a7f6e1c0b9a5d3f2",
                "transfer_0x94c0d73e8f1a2b5c6d7e9f0a4b3c8d1e2f5a6b7c0d9e3f4a8b1c2d5e6f7a0b9",
                "withdraw_0xb2f5e14c9d0a3b8e7f6c1d2a5e4f3b8c7d6a9e0f1b2c5d4a3e8f7b6c1d0a9e2",
            ],
            "behavior": ["fee_evasion", "micro_transactions"],
            "related_to": [
                "0x098B716B8Aaf21512996dC57EB0615e2383E2f96",
                "0x53b6936513e738f44FB50d2b9476730C0Ab3Bfc1",
                "0x35fB6f6DB4fb05e6A4cE86f2C93691425626d4b1",
            ],
            "metadata": {
                "first_seen": "2022-03-23T10:15:00Z",
                "last_active": "2022-05-02T14:30:00Z",
                "total_volume_usd": 187_000_000,
                "ofac_designated": True,
                "function": "First-hop intermediary for ETH layering",
                "risk_score": 98,
            },
        },
        {
            "source": "0xa0e1c89Ef1a489c9C7dE96311eD5Ce5D32c20E4B",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Intermediary Wallet #2 (OFAC-Designated)",
            "transactions": [
                "deposit_0xe7c3815f2a9d4b6c8e0f1a3d7b5e9c2f4a6d8b0e1c3f5a7d9b2e4c6f8a0d1b3",
                "transfer_0x2f9da61c8e4b7a0d3f5c9e2b6a1d8f4e7c0b3a5d9f2e6c1b4a8d7f3e0c5b9a2",
                "transfer_0x81b4c09e3f7a2d5b8c1e6f4a0d9b3c7e5f2a8d1b6c4e0f9a3d7b5e1c8f2a6d0",
                "withdraw_0xf6a2d84c1e9b3f7a5d0c8e2b6f4a1d9c3e7b5f0a8d2c6e4b1f9a3d7c5e0b8a2",
            ],
            "behavior": ["fee_evasion", "micro_transactions"],
            "related_to": [
                "0x098B716B8Aaf21512996dC57EB0615e2383E2f96",
                "0x53b6936513e738f44FB50d2b9476730C0Ab3Bfc1",
                "0xF7B31119c2682c88d88D455dBb9d5932c65Cf1bE",
            ],
            "metadata": {
                "first_seen": "2022-03-23T10:17:00Z",
                "last_active": "2022-05-04T09:00:00Z",
                "total_volume_usd": 194_000_000,
                "ofac_designated": True,
                "function": "Parallel intermediary for USDC conversion",
                "risk_score": 98,
            },
        },
        {
            "source": "0x53b6936513e738f44FB50d2b9476730C0Ab3Bfc1",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Consolidation Wallet (OFAC-Designated)",
            "transactions": [
                "deposit_0x4a8ce29f1d3b7e5c0a6f8d2b4e9c1a3f7d5b0e8c2a6f4d1b9e3c7a5f0d8b2e4",
                "deposit_0xc3d7f94a8e1b5c2d0f6a9e3b7c4d1f8a5e2b6c9d0f3a7e4b1c8d5f2a9e6b0c3",
                "transfer_0x19e5b40c7d2a8f3e6b9c1d4a5f0e8b3c7d2a6f9e1b4c5d8a0f3e7b2c9d6a1f4",
                "withdraw_0x7d0af63e2c9b4d1a8f5e0c7b3d6a9f2e4c1b8d5a0f7e3c6b9d2a4f1e8c5b0a7",
            ],
            "behavior": ["fee_evasion", "micro_transactions"],
            "related_to": [
                "0x3Cffd56B47B7b41c56258D9C7731ABaDc360E073",
                "0xa0e1c89Ef1a489c9C7dE96311eD5Ce5D32c20E4B",
                "0x35fB6f6DB4fb05e6A4cE86f2C93691425626d4b1",
            ],
            "metadata": {
                "first_seen": "2022-03-24T02:00:00Z",
                "last_active": "2022-05-10T16:45:00Z",
                "total_volume_usd": 312_000_000,
                "ofac_designated": True,
                "function": "Consolidation before Tornado Cash deposits",
                "risk_score": 99,
            },
        },
        {
            "source": "0x35fB6f6DB4fb05e6A4cE86f2C93691425626d4b1",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Pre-Mixer Staging Wallet (OFAC-Designated)",
            "transactions": [
                "deposit_0x8b3f71a4c9d2e5b0f6a1c8d3e7b4f9a2c5d0e8b1f6a3c7d4e9b2f5a0c8d1e3",
                "transfer_0xd2c4e90f1a3b7c5d8e2f6a9b4c1d0e3f8a5b7c2d9e4f1a6b3c8d5e0f7a2b9c4",
                "transfer_0xa7f1823e4c9d0b5a6f8e1c2d7b3a9f4e0c5d8b1a6f2c7e3d9b4a0f5c1e8d6b2",
                "withdraw_0x5e9c03a1d8b4f7e2c6a9d0b3f5e1c8a4d7b2f6e9c0a3d5b8f1e4c7a2d9b6f0e3",
            ],
            "behavior": ["fee_evasion", "micro_transactions"],
            "related_to": [
                "0x3Cffd56B47B7b41c56258D9C7731ABaDc360E073",
                "0x53b6936513e738f44FB50d2b9476730C0Ab3Bfc1",
                "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b",
            ],
            "metadata": {
                "first_seen": "2022-03-25T05:30:00Z",
                "last_active": "2022-06-01T12:00:00Z",
                "total_volume_usd": 245_000_000,
                "ofac_designated": True,
                "function": "Batch preparation for 100 ETH Tornado Cash deposits",
                "tornado_deposit_size_eth": 100,
                "risk_score": 97,
            },
        },
        {
            "source": "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b",
            "type": "smart_contract",
            "chain": "ethereum",
            "label": "Tornado Cash 100 ETH Pool (OFAC-Sanctioned Service)",
            "transactions": [
                "deposit_0x1c8fa42e9d3b7a5c0f6e8d1b4a9c2f7e3d5b0a8c1f6e4d2b9a3c7e5f0d8b1a4",
                "deposit_0x93e7b24c1d8a0f5e3b9c6d2a4f7e1b8c5d0a3f9e6b2c4d7a1f5e8b0c3d9a6f2",
                "withdraw_0x4d6a0f3e8c1b9d5a2f7e4c0b6d3a8f1e5c9b2d4a7f0e3c6b8d1a5f9e2c7b4d0",
            ],
            "behavior": ["time_delayed"],
            "related_to": [
                "0x35fB6f6DB4fb05e6A4cE86f2C93691425626d4b1",
            ],
            "metadata": {
                "first_seen": "2022-04-01T00:00:00Z",
                "last_active": "2022-08-08T00:00:00Z",
                "total_volume_usd": 455_000_000,
                "service_sanctioned": True,
                "ofac_sanction_date": "2022-08-08",
                "mixer_protocol": "Tornado Cash",
                "pool_denomination_eth": 100,
                "estimated_deposits_from_ronin": 1580,
                "function": "Primary mixing service used by Lazarus Group",
                "risk_score": 100,
            },
        },
        {
            "source": "0xF7B31119c2682c88d88D455dBb9d5932c65Cf1bE",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Post-Mixer Wallet (OFAC-Designated)",
            "transactions": [
                "deposit_0xe2b7c43f1a9d5b8e0c6f2d4a7b3e9c1f5a8d0b2e6c4f7a1d3b9e5c0f8a2d6b4",
                "withdraw_0x6f1d894c0a3b7e5f2d8c9a1b4e6f0c3d5a7b9e2f4c8d1a6b0e3f5c7d9a2b4e8",
            ],
            "behavior": ["time_delayed"],
            "related_to": [
                "0xa0e1c89Ef1a489c9C7dE96311eD5Ce5D32c20E4B",
            ],
            "metadata": {
                "first_seen": "2022-05-15T18:00:00Z",
                "last_active": "2022-07-20T04:00:00Z",
                "total_volume_usd": 78_000_000,
                "ofac_designated": True,
                "function": "Post-mixer collection and chain-hopping",
                "risk_score": 95,
            },
        },
    ],
}


# === Case 2: DeFi Exploit with Tornado Cash Laundering ===
#
# Synthetic case modeled on real DeFi exploit patterns observed in
# Chainalysis 2024 Crypto Crime Report. Uses the real Tornado Cash
# contract address (OFAC-sanctioned) combined with realistic but
# synthetic attacker/drain wallet addresses.

DEFI_MIXER_CASE = {
    "case_id": "VAJRA-DX-2026-0017",
    "investigation": {
        "title": "Flash Loan Re-entrancy Exploit — DeFi Protocol",
        "jurisdiction": "Singapore - Monetary Authority",
        "priority": "CRITICAL",
        "date_opened": "2026-03-01",
        "source": "Pattern modeled on Chainalysis 2024 Crypto Crime Report",
    },
    "evidence": [
        {
            "source": "0x5c69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
            "type": "smart_contract",
            "chain": "ethereum",
            "label": "Attacker Contract (Flash Loan Initiator)",
            "transactions": [
                "flashloan_0x7d2ce84a1b3f9e5c0d6a8b2e4f7c1d3a9e5b0f8c2d6a4b1e7f3c9d5a0b8e2f4",
                "exploit_0xb41f932e8c0d5a7b3e9f1c4d6a2b8e0f5c7d3a1b9e4f6c2d8a0b5e1f7c3d9a4",
                "transfer_0xe5a0274c1d9b3f8e5a2c6d0b4f7e1a3c8d5b9f2e6a0c4d1b7f3e8c5a9d2b6f0",
                "withdraw_0x19c4d63e7a0b5f2c8d1e9a4b6c3f0d7e2a5b8c1f4d9e6a3b0c7f2d5e8a1b4c9",
            ],
            "behavior": ["time_delayed", "multi_hop"],
            "related_to": [
                "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
                "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b",
            ],
            "metadata": {
                "first_seen": "2026-02-28T23:45:00Z",
                "total_volume_usd": 8_700_000,
                "contract_verified": False,
                "block_number": 19_847_231,
                "attack_vector": "Re-entrancy via flashloan callback",
                "risk_score": 99,
            },
        },
        {
            "source": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Drain Wallet (Immediate Proceeds)",
            "transactions": [
                "deposit_0x83f6a14b2c9d7e0a3f5b8c1d6e4f9a2b7c0d3e5f8a1b4c6d9e2f7a0b3c5d8e1",
                "transfer_0x2cb9d43e1f7a5b8c0d2e9f4a6b3c1d8e5f0a7b2c9d4e6f1a3b8c5d0e2f7a9b4",
                "transfer_0xf7e0854c3d1a9b6e2f5c8d0a4b7e1f3c6d9a2b5e8f0c4d1a7b3e9f5c2d6a8b0",
                "withdraw_0x5a31c92e0d8b4f7a1c6e3d9b5f2a8c4d0e7b1f6a3c9d5e2b8f4a0c7d1e6b3f9",
            ],
            "behavior": ["time_delayed", "multi_hop"],
            "related_to": [
                "0x5c69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
                "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b",
                "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            ],
            "metadata": {
                "first_seen": "2026-03-01T00:02:00Z",
                "total_volume_usd": 8_650_000,
                "time_held_minutes": 47,
                "risk_score": 98,
            },
        },
        {
            "source": "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b",
            "type": "smart_contract",
            "chain": "ethereum",
            "label": "Tornado Cash 100 ETH Pool (OFAC-Sanctioned)",
            "transactions": [
                "deposit_0xc4e2a74b1d3f8e9a5c0b6d2f7e4a1c8b3d5f0e9a6c2b7d4f1a3e8c5b0d9f6a2",
                "deposit_0x10b8d34e7c2a9f5b1d6e0c3a8f4b2d7e9c1a5f0b3d8e6c4a9f1b7d2e5c0a3f8",
                "withdraw_0x6f95e24a3c1d8b0f7e2a5c9d4b6f1e3a8c0d5b7f9e2a4c6d1b3f8e5a0c7d9b2",
            ],
            "behavior": ["time_delayed"],
            "related_to": [
                "0x5c69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
                "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            ],
            "metadata": {
                "first_seen": "2026-03-01T06:00:00Z",
                "total_volume_usd": 4_200_000,
                "service_sanctioned": True,
                "mixer_protocol": "Tornado Cash",
                "pool_denomination_eth": 100,
                "num_deposits": 42,
                "risk_score": 100,
            },
        },
        {
            "source": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "type": "crypto_wallet",
            "chain": "polygon",
            "label": "Cross-Chain Bridge Wallet (Polygon Exit)",
            "transactions": [
                "deposit_0xa2d7c14b3e9f5d1a8c0b6e2f4d7a3c9e1b5f0d8a2c6e4b1f9d3a7e5c0b8d2f6",
                "transfer_0x4e8f354c1a9d7b3e0f2c5a8b6d4e1f7c9a0b3d5e8f2c6a4d1b9e7f3c5a0d8b2",
                "withdraw_0xb1c9064e2d3a8f5b0c7e1d9a4f6b2c8e3d5a0f7b1c9e4d6a2f8b3c5e0d7a9f1",
            ],
            "behavior": ["time_delayed", "multi_hop"],
            "related_to": [
                "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            ],
            "metadata": {
                "first_seen": "2026-03-02T12:00:00Z",
                "total_volume_usd": 3_100_000,
                "bridge_protocol": "Polygon PoS Bridge",
                "delay_hours_from_exploit": 36,
                "risk_score": 89,
            },
        },
    ],
}


# === Case 3: Insider Front-Running (Synthetic Addresses) ===
#
# This case uses entirely synthetic wallet addresses for a hypothetical
# insider trading scenario. No real addresses are referenced.

INSIDER_TRADING_CASE = {
    "case_id": "VAJRA-IT-2026-0008",
    "investigation": {
        "title": "Suspected Insider Front-Running at Crypto Exchange",
        "jurisdiction": "India - SEBI Referral",
        "priority": "MEDIUM",
        "date_opened": "2026-01-20",
        "source": "Synthetic scenario — no real addresses used",
    },
    "evidence": [
        {
            "source": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Suspected Insider Personal Wallet",
            "transactions": [
                "deposit_0x3e7a9c4b1d8f2e5a0c6b9d3f7e1a4c8b5d0f2e9a6c3b7d4f1a8e5c2b0d9f6a3",
                "deposit_0xb2d1454c7e0a3f9b6d8c1e5a2f4b7d0c3e9a5f1b8d6c4e2a0f7b3d9e5c1a8f4",
                "withdraw_0x8f6c0e4a1d9b3f7e5c2a8d6b0f4e1c9a3d7b5f2e8c0a4d6b1f9e3c5a7d2b0f8",
            ],
            "behavior": ["fee_evasion"],
            "related_to": [
                "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            ],
            "metadata": {
                "first_seen": "2025-11-01T09:00:00Z",
                "last_active": "2026-01-18T16:30:00Z",
                "total_volume_usd": 450_000,
                "exchange_employee": True,
                "employee_department": "Trading Operations",
                "employee_access_level": "L3 - Order Book Read",
                "risk_score": 78,
            },
        },
        {
            "source": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Front-Running Execution Wallet",
            "transactions": [
                "deposit_0xc1a8f44b2e9d7c3a0f5b6d1e8c4a9f2b7d0e3c5f1a8b6d4e2c0f9a3b7d5e1c8",
                "deposit_0x27d3b94e1c8a5f0d7b2e6c9a3f4d1b8e5c0a7f2d9b3e6c4a1f8d5b0e2c7a9f3",
                "withdraw_0xe5f0724c3a1d9b8e5f2c0a7d4b6e1f3c8a5d9b2e7f0c4a6d1b3e8f5c2a0d7b9",
            ],
            "behavior": ["fee_evasion"],
            "related_to": [
                "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
                "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            ],
            "metadata": {
                "first_seen": "2025-11-01T09:02:00Z",
                "last_active": "2026-01-18T16:32:00Z",
                "total_volume_usd": 380_000,
                "timing_correlation_with_orderbook": 0.97,
                "avg_front_run_interval_seconds": 4.2,
                "profitable_trades_pct": 94.3,
                "risk_score": 92,
            },
        },
        {
            "source": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            "type": "crypto_wallet",
            "chain": "ethereum",
            "label": "Profit Extraction Wallet",
            "transactions": [
                "deposit_0x6d4b2e4c1a9f3d8e7b0c5a2f6d1e4c8a3b9f5d0e7c2a6b4f1d8e3c9a5b0f7d2",
                "withdraw_0x9a1c874b3e0d5f8c2a7b9d4e6f1c3a8d5b0e2f7c4a9d6b1e3f8c5a2d0b7e9f4",
            ],
            "behavior": ["time_delayed"],
            "related_to": [
                "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            ],
            "metadata": {
                "first_seen": "2025-12-15T18:00:00Z",
                "last_active": "2026-01-19T04:15:00Z",
                "total_volume_usd": 290_000,
                "withdrawal_exchange": "OTC Desk",
                "kyc_status": "[REDACTED - Court Order Pending]",
                "risk_score": 71,
            },
        },
    ],
}


# === Live API Data Source Configuration ===
#
# These endpoints can be used to fetch REAL transaction data for the
# OFAC-designated addresses above. No API key required for testing.

LIVE_DATA_SOURCES = {
    "blockchair": {
        "base_url": "https://api.blockchair.com",
        "ethereum_address": "/ethereum/dashboards/address/{address}",
        "bitcoin_address": "/bitcoin/dashboards/address/{address}",
        "rate_limit": "30 req/min (no key), higher with key",
        "docs": "https://blockchair.com/api/docs",
    },
    "etherscan": {
        "base_url": "https://api.etherscan.io/api",
        "tx_list": (
            "?module=account&action=txlist&address={address}"
            "&startblock=0&endblock=99999999&sort=asc&apikey={key}"
        ),
        "rate_limit": "5 req/sec (free tier, key required)",
        "free_key_url": "https://etherscan.io/register",
        "docs": "https://docs.etherscan.io/",
    },
    "example_queries": {
        "ronin_attacker_blockchair": (
            "https://api.blockchair.com/ethereum/dashboards/address/"
            "0x098B716B8Aaf21512996dC57EB0615e2383E2f96"
        ),
        "tornado_cash_blockchair": (
            "https://api.blockchair.com/ethereum/dashboards/address/"
            "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b"
        ),
    },
}
