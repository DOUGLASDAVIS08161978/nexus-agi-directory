#!/usr/bin/env python3
"""
Coinbase Cloud Portfolio Tracker
Monitors your blockchain wallets and tracks WTBTC deployment
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Coinbase Cloud Configuration
COINBASE_PROJECT_ID = "92d85142-1115-49df-8eab-9177ae50693b"
COINBASE_API_KEY = "09uwnC3SBAm2eg99nHSVr08g1ud8Fq1mJvhNpHebJDFuFKO1E+2ndIffRHQ2Bc+PF8pQnduo535va6kvOmSR2Q=="
COINBASE_API_KEY_ID = "b0ea4228-a1e0-4f9a-89d3-b413b6799a94"

# Your wallets
BITGET_WALLET = "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6"
OTHER_WALLET = "0xC4f7BaFDC2f7036B5e4Da73B0E77BBe0f0157145"

# Coinbase Cloud API endpoints
COINBASE_BASE_URL = "https://api.developer.coinbase.com"
POLYGON_RPC = f"{COINBASE_BASE_URL}/rpc/v1/polygon-amoy/{COINBASE_PROJECT_ID}"

print("=" * 80)
print("🔍 Coinbase Cloud Portfolio Tracker")
print("=" * 80)
print()
print("⚠️  WARNING: Your API credentials were shared publicly!")
print("   Please revoke them at: https://portal.cdp.coinbase.com/")
print()
print("=" * 80)
print()

def coinbase_rpc_call(method, params=[]):
    """Make RPC call via Coinbase Cloud"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COINBASE_API_KEY}"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    try:
        response = requests.post(POLYGON_RPC, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        result = response.json()
        return result.get("result")
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_balance(address):
    """Get ETH/MATIC balance for address"""
    result = coinbase_rpc_call("eth_getBalance", [address, "latest"])
    if result:
        balance = int(result, 16) / 10**18
        return balance
    return 0

def get_transaction_count(address):
    """Get number of transactions"""
    result = coinbase_rpc_call("eth_getTransactionCount", [address, "latest"])
    if result:
        return int(result, 16)
    return 0

def get_token_balance(token_address, wallet_address):
    """Get ERC-20 token balance"""
    # ERC-20 balanceOf function selector
    data = "0x70a08231" + wallet_address[2:].zfill(64)

    result = coinbase_rpc_call("eth_call", [{
        "to": token_address,
        "data": data
    }, "latest"])

    if result and result != "0x":
        balance = int(result, 16)
        return balance
    return 0

# Check connection
print("Testing Coinbase Cloud connection...")
chain_id = coinbase_rpc_call("eth_chainId")

if not chain_id:
    print("❌ Failed to connect to Coinbase Cloud")
    print()
    print("Possible reasons:")
    print("  1. API credentials already revoked (good!)")
    print("  2. Project not configured for Polygon Amoy")
    print("  3. Network issues")
    exit(1)

chain_id_int = int(chain_id, 16)
print(f"✅ Connected to Polygon Amoy (Chain ID: {chain_id_int})")
print()

# Check for WTBTC deployment
wtbtc_contract = None
if Path('wtbtc_deployment_success.json').exists():
    with open('wtbtc_deployment_success.json') as f:
        deployment = json.load(f)
        wtbtc_contract = deployment.get('contract')
        print(f"✅ Found WTBTC deployment: {wtbtc_contract}")
        print()

# Analyze wallets
print("=" * 80)
print("💼 Portfolio Analysis")
print("=" * 80)
print()

wallets = {
    "Bitget Wallet": BITGET_WALLET,
    "Secondary Wallet": OTHER_WALLET
}

# Load deployer wallet if exists
if Path('.env').exists():
    with open('.env') as f:
        for line in f:
            if line.startswith('WALLET_ADDRESS='):
                deployer = line.split('=')[1].strip()
                wallets["Deployer Wallet"] = deployer
                break

total_matic = 0
portfolio = []

for name, address in wallets.items():
    print(f"📊 {name}: {address}")
    print("-" * 80)

    # Get MATIC balance
    balance = get_balance(address)
    total_matic += balance
    print(f"   MATIC Balance: {balance:.6f} MATIC")

    # Get transaction count
    tx_count = get_transaction_count(address)
    print(f"   Transactions: {tx_count}")

    # Get WTBTC balance if deployed
    if wtbtc_contract:
        wtbtc_balance = get_token_balance(wtbtc_contract, address)
        wtbtc_readable = wtbtc_balance / 10**8  # 8 decimals
        print(f"   WTBTC Balance: {wtbtc_readable:,.0f} WTBTC")

        portfolio.append({
            "name": name,
            "address": address,
            "matic": balance,
            "wtbtc": wtbtc_readable,
            "transactions": tx_count
        })
    else:
        portfolio.append({
            "name": name,
            "address": address,
            "matic": balance,
            "transactions": tx_count
        })

    print()

# Summary
print("=" * 80)
print("📈 Portfolio Summary")
print("=" * 80)
print()
print(f"Total MATIC: {total_matic:.6f} MATIC")

if wtbtc_contract:
    total_wtbtc = sum(w.get('wtbtc', 0) for w in portfolio)
    print(f"Total WTBTC: {total_wtbtc:,.0f} WTBTC")
    print()
    print(f"WTBTC Contract: {wtbtc_contract}")
    print(f"Explorer: https://amoy.polygonscan.com/address/{wtbtc_contract}")

print()

# Save portfolio
portfolio_data = {
    "timestamp": datetime.now().isoformat(),
    "network": "Polygon Amoy Testnet",
    "chain_id": chain_id_int,
    "wallets": portfolio,
    "totals": {
        "matic": total_matic,
        "wtbtc": sum(w.get('wtbtc', 0) for w in portfolio) if wtbtc_contract else 0
    },
    "wtbtc_contract": wtbtc_contract
}

with open('portfolio_tracker.json', 'w') as f:
    json.dump(portfolio_data, f, indent=2)

print("✅ Portfolio saved to: portfolio_tracker.json")
print()

# Recommendations
print("=" * 80)
print("💡 Recommendations")
print("=" * 80)
print()

if total_matic < 0.1:
    print("⚠️  Low MATIC balance detected")
    print("   Get free testnet MATIC: https://faucet.polygon.technology/")
    print()

if wtbtc_contract:
    print("✅ WTBTC deployed successfully")
    print("   Import to Bitget:")
    print(f"   - Contract: {wtbtc_contract}")
    print("   - Symbol: WTBTC")
    print("   - Decimals: 8")
    print()

print("🔒 Security:")
print("   1. Revoke exposed API credentials immediately")
print("   2. Store new credentials in .env file")
print("   3. Never share API keys publicly")
print()

# Create monitoring script
print("=" * 80)
print("🔄 Continuous Monitoring")
print("=" * 80)
print()
print("To monitor your portfolio continuously:")
print()
print("  # Run every 5 minutes")
print("  watch -n 300 python3 coinbase_portfolio_tracker.py")
print()
print("  # Or schedule with cron")
print("  */5 * * * * cd /path/to/project && python3 coinbase_portfolio_tracker.py")
print()
