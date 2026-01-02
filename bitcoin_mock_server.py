#!/usr/bin/env python3
"""
Bitcoin Core Mock RPC Server
=============================
Simulates Bitcoin Core RPC responses for testing the learning system
Run this alongside bitcoin_testnet_system.py for full testing

Authors: Douglas Shane Davis & Claude
Purpose: Local testing without Bitcoin Core installation
"""

import json
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from base64 import b64decode
import threading

class BitcoinMockRPC(BaseHTTPRequestHandler):
    """Mock Bitcoin Core RPC server for testing"""

    # Mock blockchain state
    blockchain_height = 2547823
    wallet_balance = 0.0
    addresses = []
    transactions = []
    wallets = set()

    def do_POST(self):
        """Handle RPC POST requests"""
        # Check authentication
        auth_header = self.headers.get('Authorization')
        if not auth_header or not self.check_auth(auth_header):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="jsonrpc"')
            self.end_headers()
            return

        # Read request
        content_length = int(self.headers.get('Content-Length', 0))
        request_data = self.rfile.read(content_length)

        try:
            request = json.loads(request_data.decode())
            method = request.get('method')
            params = request.get('params', [])

            # Route to appropriate handler
            response = self.handle_method(method, params)

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            result = {
                "result": response,
                "error": None,
                "id": request.get('id')
            }

            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_error(500, str(e))

    def check_auth(self, auth_header):
        """Verify RPC authentication"""
        try:
            auth_type, auth_string = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                return False

            decoded = b64decode(auth_string).decode()
            username, password = decoded.split(':', 1)

            # Check credentials
            return username == 'bitcoinrpc' and password == 'testnet123'
        except:
            return False

    def handle_method(self, method, params):
        """Route RPC method to handler"""
        handlers = {
            'getblockchaininfo': self.getblockchaininfo,
            'createwallet': self.createwallet,
            'loadwallet': self.loadwallet,
            'getnewaddress': self.getnewaddress,
            'getbalances': self.getbalances,
            'getbalance': self.getbalance,
            'sendtoaddress': self.sendtoaddress,
            'gettransaction': self.gettransaction,
            'listtransactions': self.listtransactions,
            'getmininginfo': self.getmininginfo,
            'generatetoaddress': self.generatetoaddress,
        }

        handler = handlers.get(method)
        if handler:
            return handler(params)
        else:
            raise Exception(f"Method not found: {method}")

    def getblockchaininfo(self, params):
        """Return blockchain info"""
        return {
            "chain": "test",
            "blocks": self.blockchain_height,
            "headers": self.blockchain_height,
            "bestblockhash": "00000000000000" + ''.join(random.choices('0123456789abcdef', k=50)),
            "difficulty": 1.0,
            "mediantime": int(time.time()) - 600,
            "verificationprogress": 0.9999999,
            "initialblockdownload": False,
            "chainwork": "0000000000000000000000000000000000000000000000" + ''.join(random.choices('0123456789abcdef', k=16)),
            "size_on_disk": 35000000000,
            "pruned": False
        }

    def createwallet(self, params):
        """Create wallet"""
        wallet_name = params[0] if params else "default"
        self.wallets.add(wallet_name)
        return {
            "name": wallet_name,
            "warning": ""
        }

    def loadwallet(self, params):
        """Load wallet"""
        wallet_name = params[0] if params else "default"
        if wallet_name in self.wallets:
            return {
                "name": wallet_name,
                "warning": ""
            }
        else:
            raise Exception(f"Wallet {wallet_name} not found")

    def getnewaddress(self, params):
        """Generate new address"""
        label = params[0] if params else ""
        address_type = params[1] if len(params) > 1 else "bech32"

        # Generate realistic testnet bech32 address
        address = "tb1q" + ''.join(random.choices('023456789acdefghjklmnpqrstuvwxyz', k=38))

        self.addresses.append({
            'address': address,
            'label': label,
            'type': address_type
        })

        return address

    def getbalances(self, params):
        """Get wallet balances"""
        return {
            "mine": {
                "trusted": self.wallet_balance,
                "untrusted_pending": 0.0,
                "immature": 0.0
            }
        }

    def getbalance(self, params):
        """Get wallet balance (legacy)"""
        return self.wallet_balance

    def sendtoaddress(self, params):
        """Send transaction"""
        to_address = params[0]
        amount = float(params[1])

        if amount > self.wallet_balance:
            raise Exception("Insufficient funds")

        # Generate TXID
        txid = ''.join(random.choices('0123456789abcdef', k=64))

        # Update balance
        self.wallet_balance -= (amount + 0.00001)  # Include fee

        # Store transaction
        self.transactions.append({
            'txid': txid,
            'address': to_address,
            'amount': -amount,
            'fee': -0.00001,
            'confirmations': 0,
            'time': int(time.time()),
            'category': 'send'
        })

        return txid

    def gettransaction(self, params):
        """Get transaction details"""
        txid = params[0]

        # Find transaction
        for tx in self.transactions:
            if tx['txid'] == txid:
                return {
                    'amount': tx['amount'],
                    'fee': tx.get('fee', 0),
                    'confirmations': tx['confirmations'],
                    'txid': txid,
                    'time': tx['time'],
                    'timereceived': tx['time'],
                    'details': [{
                        'category': tx['category'],
                        'amount': tx['amount']
                    }]
                }

        raise Exception("Transaction not found")

    def listtransactions(self, params):
        """List recent transactions"""
        label = params[0] if params else "*"
        count = params[1] if len(params) > 1 else 10

        return self.transactions[-count:]

    def getmininginfo(self, params):
        """Get mining information"""
        return {
            "blocks": self.blockchain_height,
            "difficulty": 1.0,
            "networkhashps": 1200000000000,  # 1.2 TH/s
            "pooledtx": 50,
            "chain": "test",
            "warnings": ""
        }

    def generatetoaddress(self, params):
        """Generate blocks (mine)"""
        num_blocks = params[0]
        address = params[1]

        block_hashes = []
        for _ in range(num_blocks):
            # Generate block hash
            block_hash = "00000" + ''.join(random.choices('0123456789abcdef', k=59))
            block_hashes.append(block_hash)

            # Update blockchain height
            self.blockchain_height += 1

            # Add mining reward (50 tBTC, immature for 100 blocks)
            self.transactions.append({
                'txid': ''.join(random.choices('0123456789abcdef', k=64)),
                'address': address,
                'amount': 50.0,
                'confirmations': 1,
                'time': int(time.time()),
                'category': 'immature'
            })

        return block_hashes

    def log_message(self, format, *args):
        """Log requests"""
        print(f"[Mock RPC] {format % args}")


def run_mock_server(port=18332):
    """Run mock Bitcoin Core RPC server"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, BitcoinMockRPC)

    print("=" * 80)
    print("🎓 BITCOIN CORE MOCK RPC SERVER")
    print("=" * 80)
    print(f"   Listening on: http://127.0.0.1:{port}")
    print(f"   RPC User: bitcoinrpc")
    print(f"   RPC Password: testnet123")
    print()
    print("   This mock server simulates Bitcoin Core RPC responses")
    print("   Use it to test bitcoin_testnet_system.py without Bitcoin Core")
    print()
    print("   To test:")
    print(f"   1. Keep this server running")
    print(f"   2. In another terminal: python3 bitcoin_testnet_system.py")
    print()
    print("   Press Ctrl+C to stop")
    print("=" * 80)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down mock server...")
        httpd.shutdown()


if __name__ == "__main__":
    run_mock_server()
