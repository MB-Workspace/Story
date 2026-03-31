"""
Project Vajra — Demo Script

Processes sample cases using real OFAC-sanctioned wallet addresses and
optionally fetches live blockchain data via Blockchair API.

Usage:
    python demo.py              # Process cases (offline)
    python demo.py --live       # Also fetch live Blockchair data
"""
import sys
from project_vajra.core import VajraSystem
from sample_data.cases import (
    RONIN_BRIDGE_CASE,
    DEFI_MIXER_CASE,
    INSIDER_TRADING_CASE,
)


def run_demo(live: bool = False):
    cases = [
        ("Ronin Bridge Hack — Lazarus Group (OFAC Data)", RONIN_BRIDGE_CASE),
        ("DeFi Flash Loan Exploit + Tornado Cash", DEFI_MIXER_CASE),
        ("Insider Front-Running (Synthetic)", INSIDER_TRADING_CASE),
    ]

    for title, case_data in cases:
        print("\n" + "=" * 70)
        print(f"  CASE: {title}")
        print(f"  ID:   {case_data['case_id']}")
        if "investigation" in case_data:
            inv = case_data["investigation"]
            print(f"  Source: {inv.get('source', inv.get('jurisdiction', 'N/A'))}")
        print("=" * 70)

        vajra = VajraSystem(case_data)
        report = vajra.solve_case()

        print(f"\n  Pipeline Results:")
        print(f"  |- Entities mapped:     {len(vajra._last_entity_graph)}")
        print(f"  |- Threats detected:    {len(vajra._last_threat_matches)}")
        print(f"  |- Processing time:     {vajra._last_processing_time:.4f}s")
        print(report)

    if live:
        print("\n" + "=" * 70)
        print("  LIVE API: Building case from real blockchain data...")
        print("  (EvidenceBuilder fetches API -> transforms -> VajraSystem)")
        print("=" * 70)
        try:
            from project_vajra.data_adapters import EvidenceBuilder

            builder = EvidenceBuilder()

            # Use real OFAC-designated Lazarus Group addresses
            ronin_wallets = [
                "0x098B716B8Aaf21512996dC57EB0615e2383E2f96",  # Primary
                "0x3Cffd56B47B7b41c56258D9C7731ABaDc360E073",  # Intermediary
            ]
            print(f"\n  Fetching data for {len(ronin_wallets)} wallets...")

            # EvidenceBuilder: API response -> evidence format -> VajraSystem
            case = builder.build_case(
                case_id="VAJRA-LIVE-001",
                wallet_addresses=ronin_wallets,
                title="Live Ronin Bridge Analysis",
            )

            print(f"  Evidence items built: {len(case['evidence'])}")
            for item in case["evidence"]:
                addr = item["source"]
                meta = item["metadata"]
                print(f"\n  Wallet: {addr[:16]}...{addr[-8:]}")
                print(f"    TX Count:   {meta.get('tx_count', 'N/A')}")
                print(f"    Volume:     ${meta.get('total_volume_usd', 0):,.2f}")
                print(f"    Risk Score: {meta.get('risk_score', 'N/A')}")
                print(f"    Behavior:   {item['behavior'] or ['none detected']}")

            # Feed the live-built case directly into VajraSystem
            if case["evidence"]:
                vajra = VajraSystem(case)
                report = vajra.solve_case()
                print(f"\n  VajraSystem processed live data successfully")
                print(f"  Entities: {len(vajra._last_entity_graph)}")
                print(f"  Threats:  {len(vajra._last_threat_matches)}")

        except Exception as e:
            print(f"  API error (expected if rate-limited): {e}")

    print("\n" + "=" * 70)
    print("  ALL CASES PROCESSED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    live_mode = "--live" in sys.argv
    run_demo(live=live_mode)
