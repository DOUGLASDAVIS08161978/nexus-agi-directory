#!/usr/bin/env python3
"""
Bitcoin Network Tool
Analyze, track, and broadcast Bitcoin transactions and network data

Usage:
  python3 bitcoin_network_tool.py <data>

Examples:
  python3 bitcoin_network_tool.py <txid>
  python3 bitcoin_network_tool.py <raw_transaction_hex>
  python3 bitcoin_network_tool.py <node_address>
"""

import sys
import re
import json
import subprocess
from typing import Dict, Tuple, Optional

class BitcoinNetworkTool:
    """Comprehensive Bitcoin network operations tool"""

    def __init__(self, rpc_url: str = "http://127.0.0.1:18332",
                 rpc_user: str = "bitcoinrpc",
                 rpc_password: str = "testnet123"):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password

    def analyze_input(self, data: str) -> Tuple[str, Dict]:
        """Analyze input to determine what type of data it is"""
        print("="*80)
        print(" 🔍 ANALYZING INPUT")
        print("="*80)
        print(f"\nInput: {data[:100]}{'...' if len(data) > 100 else ''}")
        print(f"Length: {len(data)} characters")

        # Check for node address format (pubkey@ip:port or txid@ip:port)
        node_pattern = r'^([0-9a-fA-F]+)@([\d\.]+):(\d+)$'
        node_match = re.match(node_pattern, data)

        if node_match:
            hex_part = node_match.group(1)
            ip = node_match.group(2)
            port = node_match.group(3)

            print(f"\n✅ Format: NODE ADDRESS")
            print(f"   Hex Part: {hex_part}")
            print(f"   IP: {ip}")
            print(f"   Port: {port}")

            # Determine if it's a Lightning node or Bitcoin peer
            if len(hex_part) == 66:  # 33 bytes = Lightning pubkey
                print(f"   Type: Likely Lightning Network node public key")
                return 'lightning_node', {
                    'pubkey': hex_part,
                    'ip': ip,
                    'port': int(port)
                }
            elif len(hex_part) == 64:  # 32 bytes = could be txid
                print(f"   Type: Could be transaction ID with node info")
                return 'node_address', {
                    'hex': hex_part,
                    'ip': ip,
                    'port': int(port)
                }
            else:
                print(f"   Type: Unknown format")
                return 'unknown_node', {
                    'hex': hex_part,
                    'ip': ip,
                    'port': int(port)
                }

        # Check for transaction ID (64 hex characters)
        if len(data) == 64 and all(c in '0123456789abcdefABCDEF' for c in data):
            print(f"\n✅ Format: TRANSACTION ID (TXID)")
            return 'txid', {'txid': data}

        # Check for raw transaction hex (even length, all hex)
        if len(data) % 2 == 0 and len(data) > 64 and all(c in '0123456789abcdefABCDEF' for c in data):
            print(f"\n✅ Format: RAW TRANSACTION HEX")
            return 'raw_tx', {'hex': data}

        # Check for Bitcoin address
        if data.startswith('tb1') or data.startswith('bc1') or data.startswith('1') or data.startswith('3'):
            print(f"\n✅ Format: BITCOIN ADDRESS")
            return 'address', {'address': data}

        print(f"\n❓ Format: UNKNOWN")
        return 'unknown', {'data': data}

    def handle_lightning_node(self, info: Dict):
        """Handle Lightning Network node address"""
        print("\n" + "="*80)
        print(" ⚡ LIGHTNING NETWORK NODE")
        print("="*80)

        pubkey = info['pubkey']
        ip = info['ip']
        port = info['port']

        print(f"\n📡 Node Information:")
        print(f"   Public Key: {pubkey}")
        print(f"   IP Address: {ip}")
        print(f"   Port: {port}")

        print(f"\n💡 This is a Lightning Network node address format")
        print(f"   Format: pubkey@host:port")

        print(f"\n🔗 To connect to this Lightning node:")
        print(f"   lncli connect {pubkey}@{ip}:{port}")

        print(f"\n⚠️  NOTE: This is NOT a Bitcoin transaction!")
        print(f"   Lightning Network is a Layer 2 payment protocol on top of Bitcoin")

        print(f"\n📚 What you can do:")
        print(f"   1. Connect to this node using Lightning Network software (LND, c-lightning, Eclair)")
        print(f"   2. Open payment channels with this node")
        print(f"   3. Route payments through this node")

        print(f"\n🔍 To explore this node:")
        print(f"   • Use Lightning Network explorers:")
        print(f"     - https://1ml.com/")
        print(f"     - https://amboss.space/")
        print(f"   • Search by public key: {pubkey}")

        print("\n" + "="*80)

    def handle_node_address(self, info: Dict):
        """Handle node address with possible TXID"""
        print("\n" + "="*80)
        print(" 📡 NODE ADDRESS WITH TRANSACTION DATA")
        print("="*80)

        hex_part = info['hex']
        ip = info['ip']
        port = info['port']

        print(f"\n📊 Parsed Information:")
        print(f"   Hex Data: {hex_part}")
        print(f"   IP: {ip}")
        print(f"   Port: {port}")

        print(f"\n❓ This format is unusual for Bitcoin")
        print(f"   Standard Bitcoin formats:")
        print(f"   • Transaction ID: 64 hex characters (no @ or IP)")
        print(f"   • Node address: IP:port (for addnode command)")
        print(f"   • Lightning node: 66-char-pubkey@IP:port")

        print(f"\n💡 Possible interpretations:")
        print(f"   1. Custom application format")
        print(f"   2. Peer-to-peer network announcement")
        print(f"   3. Transaction routing information")

        print(f"\n🔍 To investigate the hex part as a TXID:")
        print(f"   python3 track_transaction.py {hex_part}")

        print(f"\n🔍 To check the node:")
        print(f"   bitcoin-cli addnode {ip}:{port} onetry")

        print("\n" + "="*80)

    def track_transaction(self, txid: str):
        """Track a transaction"""
        print("\n" + "="*80)
        print(" 🔍 TRACKING TRANSACTION")
        print("="*80)

        print(f"\n📝 TXID: {txid}")
        print(f"\n🔗 View on explorers:")
        print(f"   Testnet: https://mempool.space/testnet/tx/{txid}")
        print(f"   Mainnet: https://mempool.space/tx/{txid}")
        print(f"   Local: http://localhost:8080/tx/{txid}")

        # Try to get transaction
        result = self.rpc_call("getrawtransaction", [txid, True])

        if 'error' in result:
            print(f"\n⚠️  Transaction not found in local blockchain")
            print(f"   • Not yet broadcast to network")
            print(f"   • Or not in this chain (check testnet vs mainnet)")
            print(f"   • Or node not fully synced")
        else:
            tx = result['result']
            print(f"\n✅ Transaction found!")
            print(f"   Confirmations: {tx.get('confirmations', 0)}")
            print(f"   Block: {tx.get('blockhash', 'In mempool')[:20]}...")

        print("\n" + "="*80)

    def broadcast_transaction(self, raw_hex: str):
        """Broadcast a raw transaction"""
        print("\n" + "="*80)
        print(" 📡 BROADCASTING TRANSACTION")
        print("="*80)

        print(f"\nRaw transaction hex: {raw_hex[:100]}...")
        print(f"Length: {len(raw_hex)} characters ({len(raw_hex)//2} bytes)")

        # First, decode to see what it is
        result = self.rpc_call("decoderawtransaction", [raw_hex])

        if 'error' in result:
            print(f"\n❌ Invalid transaction hex")
            print(f"   Error: {result['error']}")
            return

        tx = result['result']
        print(f"\n✅ Valid transaction format")
        print(f"   TXID: {tx.get('txid', 'N/A')}")
        print(f"   Inputs: {len(tx.get('vin', []))}")
        print(f"   Outputs: {len(tx.get('vout', []))}")

        # Try to broadcast
        print(f"\n📡 Broadcasting to network...")
        broadcast_result = self.rpc_call("sendrawtransaction", [raw_hex])

        if 'error' in broadcast_result:
            print(f"\n❌ Broadcast failed")
            print(f"   Error: {broadcast_result['error']}")
            print(f"\n💡 Common reasons:")
            print(f"   • Transaction already in blockchain")
            print(f"   • Invalid signatures")
            print(f"   • Insufficient fees")
            print(f"   • Spending already-spent outputs")
        else:
            txid = broadcast_result['result']
            print(f"\n✅ Transaction broadcast successfully!")
            print(f"   TXID: {txid}")
            print(f"\n🔗 Track it:")
            print(f"   https://mempool.space/testnet/tx/{txid}")

        print("\n" + "="*80)

    def rpc_call(self, method: str, params: list = None) -> Dict:
        """Make Bitcoin RPC call"""
        if params is None:
            params = []

        request_data = {
            "jsonrpc": "1.0",
            "id": "network_tool",
            "method": method,
            "params": params
        }

        curl_cmd = [
            'curl',
            '--silent',
            '--user', f'{self.rpc_user}:{self.rpc_password}',
            '--data-binary', json.dumps(request_data),
            '-H', 'content-type: text/plain;',
            self.rpc_url
        ]

        try:
            result = subprocess.run(
                curl_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return {'error': 'Connection failed'}

            response = json.loads(result.stdout)

            if 'error' in response and response['error']:
                return {'error': response['error']}

            return {'success': True, 'result': response.get('result')}

        except Exception as e:
            return {'error': str(e)}


def main():
    if len(sys.argv) < 2:
        print("Bitcoin Network Tool")
        print("="*80)
        print("\nUsage: python3 bitcoin_network_tool.py <data>")
        print("\nSupported formats:")
        print("  • Transaction ID (64 hex chars)")
        print("  • Raw transaction hex")
        print("  • Bitcoin address")
        print("  • Node address (pubkey@ip:port)")
        print("\nExamples:")
        print("  python3 bitcoin_network_tool.py a1b2c3d4...abcd")
        print("  python3 bitcoin_network_tool.py 02ccd07f...e24f@103.99.169.206:19735")
        print("  python3 bitcoin_network_tool.py tb1q...")
        sys.exit(1)

    data = sys.argv[1]
    tool = BitcoinNetworkTool()

    # Analyze input
    data_type, info = tool.analyze_input(data)

    # Handle based on type
    if data_type == 'lightning_node':
        tool.handle_lightning_node(info)
    elif data_type == 'node_address':
        tool.handle_node_address(info)
    elif data_type == 'txid':
        tool.track_transaction(info['txid'])
    elif data_type == 'raw_tx':
        tool.broadcast_transaction(info['hex'])
    elif data_type == 'address':
        print(f"\n💡 To check this address, use:")
        print(f"   bitcoin-cli getnewaddress")
        print(f"   Or search on block explorer")
    else:
        print(f"\n❓ Unknown format - cannot process")


if __name__ == "__main__":
    main()
