#!/usr/bin/env python3
"""
Coinbase Cloud Transaction Monitor
Real-time monitoring of blockchain transactions for your wallets
"""

import json
import time
import requests
from datetime import datetime

# Coinbase Cloud Configuration (⚠️ REVOKE THESE IMMEDIATELY)
COINBASE_PROJECT_ID = "92d85142-1115-49df-8eab-9177ae50693b"
COINBASE_API_KEY = "09uwnC3SBAm2eg99nHSVr08g1ud8Fq1mJvhNpHebJDFuFKO1E+2ndIffRHQ2Bc+PF8pQnduo535va6kvOmSR2Q=="

POLYGON_RPC = f"https://api.developer.coinbase.com/rpc/v1/polygon-amoy/{COINBASE_PROJECT_ID}"

# Wallets to monitor
WALLETS = [
    "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6",  # Bitget
    "0xC4f7BaFDC2f7036B5e4Da73B0E77BBe0f0157145",  # Secondary
]

print("=" * 80)
print("📡 Real-Time Transaction Monitor")
print("=" * 80)
print()
print("⚠️  SECURITY WARNING: Revoke these credentials immediately!")
print("   https://portal.cdp.coinbase.com/")
print()

def rpc_call(method, params=[]):
    """Make Coinbase Cloud RPC call"""
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
        return response.json().get("result")
    except:
        return None

def get_latest_block():
    """Get latest block number"""
    result = rpc_call("eth_blockNumber")
    return int(result, 16) if result else None

def get_block_transactions(block_num):
    """Get all transactions in a block"""
    block_hex = hex(block_num)
    block_data = rpc_call("eth_getBlockByNumber", [block_hex, True])
    return block_data.get("transactions", []) if block_data else []

def monitor_transactions():
    """Monitor new transactions"""
    print("Starting transaction monitor...")
    print(f"Monitoring {len(WALLETS)} wallets")
    print()

    # Get starting block
    last_block = get_latest_block()
    if not last_block:
        print("❌ Failed to connect to Coinbase Cloud")
        return

    print(f"✅ Connected at block {last_block}")
    print(f"⏳ Watching for new transactions...")
    print()
    print("-" * 80)
    print()

    monitored_wallets = set(w.lower() for w in WALLETS)

    while True:
        try:
            current_block = get_latest_block()

            if current_block and current_block > last_block:
                # Check new blocks
                for block_num in range(last_block + 1, current_block + 1):
                    transactions = get_block_transactions(block_num)

                    for tx in transactions:
                        from_addr = tx.get('from', '').lower()
                        to_addr = tx.get('to', '').lower() if tx.get('to') else ''

                        # Check if transaction involves monitored wallets
                        if from_addr in monitored_wallets or to_addr in monitored_wallets:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            value = int(tx.get('value', '0x0'), 16) / 10**18

                            print(f"🔔 NEW TRANSACTION at {timestamp}")
                            print(f"   Block: {block_num}")
                            print(f"   Hash: {tx['hash']}")
                            print(f"   From: {tx['from']}")
                            print(f"   To: {tx.get('to', 'Contract Creation')}")
                            print(f"   Value: {value:.6f} MATIC")
                            print(f"   Explorer: https://amoy.polygonscan.com/tx/{tx['hash']}")
                            print()
                            print("-" * 80)
                            print()

                            # Save to log
                            log_entry = {
                                "timestamp": timestamp,
                                "block": block_num,
                                "hash": tx['hash'],
                                "from": tx['from'],
                                "to": tx.get('to'),
                                "value": value
                            }

                            with open('transaction_log.jsonl', 'a') as f:
                                f.write(json.dumps(log_entry) + '\n')

                last_block = current_block

            time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            print()
            print("Monitor stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_transactions()
