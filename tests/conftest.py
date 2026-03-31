"""
Shared test fixtures for Project Vajra test suite.
"""
import pytest


@pytest.fixture
def sample_case_data():
    """Standard test case with 5 wallets for consistent testing.

    Uses Vajra's internal normalized format: type_txhash where
    txhash is a full-length hex string derived from the source address.
    """
    return {
        "case_id": "CRYPTO-FRAUD-2024-001",
        "evidence": [
            {
                "source": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
                "type": "crypto_wallet",
                "transactions": [
                    "deposit_0x742d35cc6634c0532925a3b844bc9e7595f2bd18a1b2c3d4e5f6a7b8c9d0e1f2",
                    "withdraw_0x742d35cc6634c0532925a3b844bc9e7595f2bd18d4e5f6a7b8c9d0e1f2a3b4c5",
                    "transfer_0x742d35cc6634c0532925a3b844bc9e7595f2bd18f7a8b9c0d1e2f3a4b5c6d7e8",
                ],
                "behavior": ["fee_evasion", "micro_transactions"],
                "related_to": [
                    "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
                    "0x1aD91ee08f21bE3dE0BA2ba6918E714dA6B45836",
                ],
            },
            {
                "source": "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
                "type": "crypto_wallet",
                "transactions": [
                    "deposit_0x8ba1f109551bd432803012645ac136ddd64dba72a1b2c3d4e5f6a7b8c9d0e1f2",
                    "withdraw_0x8ba1f109551bd432803012645ac136ddd64dba72e5f6a7b8c9d0e1f2a3b4c5d6",
                    "transfer_0x8ba1f109551bd432803012645ac136ddd64dba72c9d0e1f2a3b4c5d6e7f8a9b0",
                ],
                "behavior": ["fee_evasion", "micro_transactions"],
                "related_to": [
                    "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
                    "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                ],
            },
            {
                "source": "0x1aD91ee08f21bE3dE0BA2ba6918E714dA6B45836",
                "type": "crypto_wallet",
                "transactions": [
                    "deposit_0x1ad91ee08f21be3de0ba2ba6918e714da6b45836a1b2c3d4e5f6a7b8c9d0e1f2",
                    "withdraw_0x1ad91ee08f21be3de0ba2ba6918e714da6b45836d4e5f6a7b8c9d0e1f2a3b4c5",
                ],
                "behavior": ["time_delayed"],
                "related_to": [
                    "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
                ],
            },
            {
                "source": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "type": "crypto_wallet",
                "transactions": [
                    "deposit_0xdac17f958d2ee523a2206206994597c13d831ec7a9b0c1d2e3f4a5b6c7d8e9f0",
                    "withdraw_0xdac17f958d2ee523a2206206994597c13d831ec7e5f6a7b8c9d0e1f2a3b4c5d6",
                    "transfer_0xdac17f958d2ee523a2206206994597c13d831ec7c9d0e1f2a3b4c5d6e7f8a9b0",
                ],
                "behavior": ["fee_evasion", "micro_transactions"],
                "related_to": [
                    "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
                    "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                ],
            },
            {
                "source": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "type": "crypto_wallet",
                "transactions": [
                    "deposit_0x6b175474e89094c44da98b954eedeac495271d0fa9b0c1d2e3f4a5b6c7d8e9f0",
                    "withdraw_0x6b175474e89094c44da98b954eedeac495271d0fe5f6a7b8c9d0e1f2a3b4c5d6",
                    "transfer_0x6b175474e89094c44da98b954eedeac495271d0fc9d0e1f2a3b4c5d6e7f8a9b0",
                ],
                "behavior": ["fee_evasion"],
                "related_to": [
                    "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                ],
            },
        ],
    }


@pytest.fixture
def minimal_case_data():
    """Minimal valid case data for unit tests."""
    return {
        "case_id": "TEST-MINIMAL-001",
        "evidence": [
            {
                "source": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "type": "crypto_wallet",
                "transactions": [
                    "deposit_0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48a1b2c3d4e5f6a7b8c9d0e1f2",
                ],
                "behavior": [],
                "related_to": [],
            }
        ],
    }


@pytest.fixture
def empty_evidence_case():
    """Case with no evidence items."""
    return {
        "case_id": "TEST-EMPTY-001",
        "evidence": [],
    }
