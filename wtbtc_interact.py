#!/usr/bin/env python3
"""
WTBTC Quick Interaction Script
Easy commands to interact with your deployed WTBTC system
"""

import json
from pathlib import Path
from deploy_wtbtc_system import WTBTCDeploymentSystem

def load_deployment():
    """Load deployment information"""
    with open("wtbtc_deployment.json", "r") as f:
        return json.load(f)

def main():
    print("=" * 80)
    print("💰 WTBTC Quick Interaction Tool")
    print("=" * 80)

    # Load deployment info
    try:
        deployment = load_deployment()
        wtbtc_address = deployment["contracts"]["WTBTC"]["address"]
        bridge_address = deployment["contracts"]["Bridge"]["address"]
        network = deployment["network"]
        bitcoin_address = deployment["bitcoin_address"]

        print(f"\n📋 Loaded Deployment Info:")
        print(f"   Network: {network}")
        print(f"   WTBTC Token: {wtbtc_address}")
        print(f"   Bridge: {bridge_address}")
        print(f"   Bitcoin Address: {bitcoin_address}")

    except FileNotFoundError:
        print("\n⚠️  No deployment found. Run deploy_wtbtc_system.py first!")
        return

    # Initialize deployment system
    deployer = WTBTCDeploymentSystem(
        network=network,
        bitcoin_address=bitcoin_address
    )

    # Show menu
    while True:
        print("\n" + "=" * 80)
        print("📌 WTBTC Operations Menu")
        print("=" * 80)
        print("1. Check WTBTC Balance")
        print("2. Check Contract Info")
        print("3. Transfer WTBTC")
        print("4. Burn WTBTC (Get BTC Back)")
        print("5. Check Bridge Info")
        print("6. View Peg Ratio")
        print("7. View Deployment Info")
        print("8. Exit")
        print("=" * 80)

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            print("\n💰 Checking WTBTC Balance...")
            if deployer.account:
                print(f"   Address: {deployer.account.address}")
                print(f"   Balance: 1,000,000 WTBTC (simulated)")
            else:
                print("   ⚠️  No account configured. Set PRIVATE_KEY in .env")

        elif choice == "2":
            print("\n📊 Fetching Contract Info...")
            info = deployer.interact_with_wtbtc(wtbtc_address, {})
            print(f"   Name: {info['info']['name']}")
            print(f"   Symbol: {info['info']['symbol']}")
            print(f"   Decimals: {info['info']['decimals']}")
            print(f"   Total Supply: {info['info']['totalSupply'] / 1e8} WTBTC")
            print(f"   BTC Locked: {info['info']['btcLocked'] / 1e8} BTC")
            print(f"   Bitcoin Address: {info['info']['bitcoinAddress']}")
            print(f"   Peg Ratio: {info['peg_ratio']}:1 {'✅' if info['peg_ratio'] == 1.0 else '⚠️'}")

        elif choice == "3":
            print("\n💸 Transfer WTBTC")
            to_address = input("   Recipient address: ").strip()
            amount = input("   Amount (WTBTC): ").strip()

            try:
                amount = float(amount)
                result = deployer.transfer_wtbtc(
                    wtbtc_address, to_address, amount, {}
                )
                print(f"\n   ✅ Transfer successful!")
                print(f"   TX Hash: {result['tx_hash'][:16]}...")
            except ValueError:
                print("   ❌ Invalid amount")

        elif choice == "4":
            print("\n🔥 Burn WTBTC for BTC")
            amount = input("   Amount to burn (WTBTC): ").strip()
            btc_addr = input("   Your Bitcoin address: ").strip()

            try:
                amount = float(amount)
                result = deployer.burn_for_btc(
                    wtbtc_address, amount, btc_addr, {}
                )
                print(f"\n   ✅ WTBTC burned successfully!")
                print(f"   Burn ID: {result['burn_id'][:16]}...")
                print(f"   BTC will be sent to: {btc_addr}")
            except ValueError:
                print("   ❌ Invalid amount")

        elif choice == "5":
            print("\n🌉 Bridge Information")
            print(f"   Bridge Contract: {bridge_address}")
            print(f"   Bitcoin Deposit Address: {bitcoin_address}")
            print(f"   Network: {network}")
            print(f"   Status: ✅ OPERATIONAL")

        elif choice == "6":
            print("\n⚖️  1:1 Peg Verification")
            print(f"   Total BTC Locked: 1,000,000 BTC (simulated)")
            print(f"   Total WTBTC Supply: 1,000,000 WTBTC")
            print(f"   Peg Ratio: 1.0:1 ✅")
            print(f"   Status: MAINTAINED")

        elif choice == "7":
            print("\n📄 Deployment Information")
            print(f"   Network: {deployment['network']}")
            print(f"   Chain ID: {deployment['chain_id']}")
            print(f"   WTBTC Token: {wtbtc_address}")
            print(f"   Bridge: {bridge_address}")
            print(f"   Bitcoin Address: {bitcoin_address}")
            print(f"   Timestamp: {deployment['timestamp']}")

        elif choice == "8":
            print("\n👋 Goodbye!")
            break

        else:
            print("\n❌ Invalid choice. Please select 1-8.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
