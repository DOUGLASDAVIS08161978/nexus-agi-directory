#!/usr/bin/env python3
"""
Bitcoin Transaction Tracker
Track and display detailed information about Bitcoin transactions

Usage: python3 track_transaction.py <txid>
"""

import sys
import json
import subprocess
from typing import Dict, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class TransactionTracker:
    """Track Bitcoin transactions and display detailed information"""

    def __init__(self, rpc_url: str = "http://127.0.0.1:18332",
                 rpc_user: str = "bitcoinrpc",
                 rpc_password: str = "testnet123"):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password

    def rpc_call(self, method: str, params: list = None) -> Dict:
        """Make Bitcoin RPC call"""
        if params is None:
            params = []

        request_data = {
            "jsonrpc": "1.0",
            "id": "tracker",
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

    def get_transaction(self, txid: str) -> Optional[Dict]:
        """Get transaction details"""
        logger.info("\n" + "="*80)
        logger.info(f" 🔍 TRACKING TRANSACTION")
        logger.info("="*80)
        logger.info(f"\n📝 TXID: {txid}")
        logger.info(f"🔗 Testnet Explorer: https://mempool.space/testnet/tx/{txid}")
        logger.info(f"🔗 Local Mempool: http://localhost:8080/tx/{txid}")

        result = self.rpc_call("gettransaction", [txid])

        if 'error' in result:
            logger.info(f"\n⚠️  Transaction not found in local wallet")
            logger.info(f"   This may be a transaction to/from another wallet")
            logger.info(f"\n💡 To track this transaction:")
            logger.info(f"   1. View on public explorer: https://mempool.space/testnet/tx/{txid}")
            logger.info(f"   2. Or use getrawtransaction if it's in a block")
            return None

        tx = result['result']

        logger.info("\n" + "-"*80)
        logger.info(" TRANSACTION DETAILS")
        logger.info("-"*80)

        # Basic info
        logger.info(f"\n💰 Amount: {tx.get('amount', 0):.8f} BTC")
        logger.info(f"💵 Fee: {tx.get('fee', 0):.8f} BTC")
        logger.info(f"📊 Confirmations: {tx.get('confirmations', 0)}")

        # Status
        confirmations = tx.get('confirmations', 0)
        if confirmations == 0:
            logger.info(f"📍 Status: ⏳ UNCONFIRMED (in mempool)")
        elif confirmations < 6:
            logger.info(f"📍 Status: 🔄 CONFIRMING ({confirmations}/6)")
        else:
            logger.info(f"📍 Status: ✅ CONFIRMED ({confirmations} confirmations)")

        # Timestamps
        if 'time' in tx:
            from datetime import datetime
            timestamp = datetime.fromtimestamp(tx['time'])
            logger.info(f"🕐 Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        if 'blocktime' in tx:
            from datetime import datetime
            blocktime = datetime.fromtimestamp(tx['blocktime'])
            logger.info(f"📦 Block Time: {blocktime.strftime('%Y-%m-%d %H:%M:%S')}")

        # Block info
        if 'blockhash' in tx:
            logger.info(f"\n📦 Block Hash: {tx['blockhash']}")
            logger.info(f"🔗 View Block: https://mempool.space/testnet/block/{tx['blockhash']}")

        # Transaction details
        if 'details' in tx and tx['details']:
            logger.info("\n" + "-"*80)
            logger.info(" TRANSACTION INPUTS/OUTPUTS")
            logger.info("-"*80)

            for i, detail in enumerate(tx['details'], 1):
                logger.info(f"\n#{i}")
                logger.info(f"  Category: {detail.get('category', 'unknown')}")
                logger.info(f"  Amount: {detail.get('amount', 0):.8f} BTC")
                if 'address' in detail:
                    logger.info(f"  Address: {detail['address']}")
                if 'label' in detail:
                    logger.info(f"  Label: {detail['label']}")

        # Raw transaction (hex)
        if 'hex' in tx:
            logger.info("\n" + "-"*80)
            logger.info(" RAW TRANSACTION")
            logger.info("-"*80)
            logger.info(f"\nHex: {tx['hex'][:100]}...")
            logger.info(f"Size: {len(tx['hex']) // 2} bytes")

        logger.info("\n" + "="*80)

        return tx

    def get_raw_transaction(self, txid: str) -> Optional[Dict]:
        """Get raw transaction (works for any tx in blockchain)"""
        logger.info(f"\n🔍 Fetching raw transaction data...")

        result = self.rpc_call("getrawtransaction", [txid, True])

        if 'error' in result:
            logger.info(f"⚠️  Transaction not found in blockchain")
            return None

        tx = result['result']

        logger.info("\n" + "-"*80)
        logger.info(" RAW TRANSACTION DETAILS")
        logger.info("-"*80)

        logger.info(f"\n📝 TXID: {tx.get('txid', txid)}")
        logger.info(f"📏 Size: {tx.get('size', 0)} bytes")
        logger.info(f"⚖️  Weight: {tx.get('weight', 0)} WU")
        logger.info(f"🔢 Version: {tx.get('version', 0)}")
        logger.info(f"🔒 Locktime: {tx.get('locktime', 0)}")

        # Inputs
        if 'vin' in tx:
            logger.info(f"\n📥 INPUTS ({len(tx['vin'])})")
            for i, vin in enumerate(tx['vin'], 1):
                logger.info(f"\n  Input #{i}:")
                if 'coinbase' in vin:
                    logger.info(f"    Type: COINBASE (mining reward)")
                else:
                    logger.info(f"    Previous TX: {vin.get('txid', 'N/A')}")
                    logger.info(f"    Output Index: {vin.get('vout', 'N/A')}")
                if 'sequence' in vin:
                    logger.info(f"    Sequence: {vin['sequence']}")

        # Outputs
        if 'vout' in tx:
            logger.info(f"\n📤 OUTPUTS ({len(tx['vout'])})")
            total_out = 0
            for i, vout in enumerate(tx['vout'], 1):
                value = vout.get('value', 0)
                total_out += value
                logger.info(f"\n  Output #{i}:")
                logger.info(f"    Value: {value:.8f} BTC")
                if 'scriptPubKey' in vout:
                    spk = vout['scriptPubKey']
                    if 'address' in spk:
                        logger.info(f"    Address: {spk['address']}")
                    if 'type' in spk:
                        logger.info(f"    Type: {spk['type']}")

            logger.info(f"\n💰 Total Output: {total_out:.8f} BTC")

        # Confirmations
        confirmations = tx.get('confirmations', 0)
        logger.info(f"\n📊 Confirmations: {confirmations}")

        if confirmations > 0:
            logger.info(f"✅ Status: CONFIRMED")
        else:
            logger.info(f"⏳ Status: UNCONFIRMED")

        logger.info("\n" + "="*80)

        return tx

    def monitor_transaction(self, txid: str):
        """Monitor transaction until confirmed"""
        logger.info("\n" + "="*80)
        logger.info(" 📊 TRANSACTION MONITORING")
        logger.info("="*80)
        logger.info(f"\nMonitoring: {txid}")
        logger.info("\nPress Ctrl+C to stop\n")

        import time
        last_confirmations = -1

        try:
            while True:
                result = self.rpc_call("gettransaction", [txid])

                if 'error' not in result:
                    tx = result['result']
                    confirmations = tx.get('confirmations', 0)

                    if confirmations != last_confirmations:
                        timestamp = time.strftime('%H:%M:%S')

                        if confirmations == 0:
                            logger.info(f"[{timestamp}] ⏳ In mempool (0 confirmations)")
                        elif confirmations < 6:
                            logger.info(f"[{timestamp}] 🔄 Confirming... ({confirmations}/6)")
                        else:
                            logger.info(f"[{timestamp}] ✅ CONFIRMED! ({confirmations} confirmations)")
                            logger.info("\n🎉 Transaction fully confirmed!")
                            break

                        last_confirmations = confirmations

                time.sleep(10)  # Check every 10 seconds

        except KeyboardInterrupt:
            logger.info("\n\n⏹️  Monitoring stopped")


def main():
    """Main execution"""

    if len(sys.argv) < 2:
        print("Usage: python3 track_transaction.py <txid>")
        print("\nExample:")
        print("  python3 track_transaction.py a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd")
        sys.exit(1)

    txid = sys.argv[1]

    tracker = TransactionTracker()

    # Try to get transaction from wallet
    tx = tracker.get_transaction(txid)

    # If not in wallet, try raw transaction
    if tx is None:
        tracker.get_raw_transaction(txid)


if __name__ == "__main__":
    main()
