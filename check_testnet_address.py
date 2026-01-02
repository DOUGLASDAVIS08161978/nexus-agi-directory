#!/usr/bin/env python3
"""
Quick script to check Bitcoin testnet address balance
"""

import requests
import json
import sys

address = "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"

print(f"\n{'='*80}")
print(f" BITCOIN TESTNET ADDRESS LOOKUP")
print(f"{'='*80}\n")
print(f"Address: {address}")
print(f"Network: Bitcoin Testnet")
print(f"Type: Bech32 (Native SegWit)\n")

# Note: This is the famous BIP173 test vector address
print(f"📝 Note: This is the BIP173 example address from the Bitcoin specification!")
print(f"   It's used in documentation and testing.\n")

print(f"{'='*80}")
print(f" CHECKING BALANCE VIA MULTIPLE APIS")
print(f"{'='*80}\n")

# Try multiple APIs
apis = [
    {
        "name": "Blockstream.info",
        "url": f"https://blockstream.info/testnet/api/address/{address}",
        "parser": lambda r: {
            "funded_txo_sum": r.get("chain_stats", {}).get("funded_txo_sum", 0) / 100000000,
            "spent_txo_sum": r.get("chain_stats", {}).get("spent_txo_sum", 0) / 100000000,
            "tx_count": r.get("chain_stats", {}).get("tx_count", 0)
        }
    },
    {
        "name": "Mempool.space",
        "url": f"https://mempool.space/testnet/api/address/{address}",
        "parser": lambda r: {
            "funded_txo_sum": r.get("chain_stats", {}).get("funded_txo_sum", 0) / 100000000,
            "spent_txo_sum": r.get("chain_stats", {}).get("spent_txo_sum", 0) / 100000000,
            "tx_count": r.get("chain_stats", {}).get("tx_count", 0)
        }
    }
]

success = False

for api in apis:
    print(f"Trying {api['name']}...")
    try:
        response = requests.get(api['url'], timeout=10)
        if response.status_code == 200:
            data = response.json()
            parsed = api['parser'](data)

            print(f"✓ {api['name']} - SUCCESS\n")

            funded = parsed.get('funded_txo_sum', 0)
            spent = parsed.get('spent_txo_sum', 0)
            balance = funded - spent
            tx_count = parsed.get('tx_count', 0)

            print(f"   Total Received: {funded:.8f} tBTC")
            print(f"   Total Spent:    {spent:.8f} tBTC")
            print(f"   Current Balance: {balance:.8f} tBTC")
            print(f"   Transaction Count: {tx_count}")

            if balance == 0:
                print(f"\n   ⚠️  Address has ZERO balance")
            else:
                print(f"\n   ✓ Address has {balance:.8f} tBTC")

            success = True
            break
        else:
            print(f"✗ {api['name']} - HTTP {response.status_code}\n")
    except Exception as e:
        print(f"✗ {api['name']} - Error: {e}\n")

if not success:
    print(f"{'='*80}")
    print(f" ⚠️  ALL APIS FAILED - MANUAL CHECK REQUIRED")
    print(f"{'='*80}\n")

    print(f"Check the address manually at these explorers:\n")
    print(f"1. Blockstream: https://blockstream.info/testnet/address/{address}")
    print(f"2. Mempool.space: https://mempool.space/testnet/address/{address}")
    print(f"3. Blockchain.com: https://www.blockchain.com/explorer/addresses/btc-testnet/{address}")

    print(f"\n📝 About This Address:")
    print(f"   This is the BIP173 test vector address used in Bitcoin documentation.")
    print(f"   It's derived from the example in the Bech32 specification.")
    print(f"   Address: tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx")
    print(f"   Purpose: Testing and documentation examples")

print(f"\n{'='*80}")
print(f" 🚰 NEED TESTNET COINS? USE THESE FREE FAUCETS:")
print(f"{'='*80}\n")

faucets = [
    ("Mempool.space Faucet", "https://testnet-faucet.mempool.co/", "0.01 tBTC"),
    ("Bitcoin Faucet UO1", "https://bitcoinfaucet.uo1.net/", "0.001-0.01 tBTC"),
    ("Testnet Help", "https://testnet.help/", "Variable"),
    ("Coinfaucet.eu", "https://coinfaucet.eu/en/btc-testnet/", "0.001 tBTC")
]

for i, (name, url, amount) in enumerate(faucets, 1):
    print(f"{i}. {name}")
    print(f"   URL: {url}")
    print(f"   Amount: {amount}\n")

print(f"{'='*80}\n")
