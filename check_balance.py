#!/usr/bin/env python3
"""
Bitcoin Address Balance Checker
Check balance of any Bitcoin address using RPC or block explorers

Usage: python3 check_balance.py <address>
"""

import sys
import json
import subprocess
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class AddressBalanceChecker:
    """Check Bitcoin address balances"""

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
            "id": "balance_check",
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
                return {'error': 'connection_failed'}

            response = json.loads(result.stdout)

            if 'error' in response and response['error']:
                return {'error': response['error']}

            return {'success': True, 'result': response.get('result')}

        except Exception as e:
            return {'error': str(e)}

    def identify_address_type(self, address: str) -> tuple:
        """Identify address type and network"""
        logger.info("="*80)
        logger.info(" 🔍 ADDRESS ANALYSIS")
        logger.info("="*80)
        logger.info(f"\nAddress: {address}")

        # Testnet bech32
        if address.startswith('tb1'):
            logger.info("Network: 🧪 TESTNET")
            logger.info("Type: Bech32 (SegWit)")
            logger.info("Prefix: tb1 (testnet bech32)")
            return 'testnet', 'bech32'

        # Mainnet bech32
        elif address.startswith('bc1'):
            logger.info("Network: 🔴 MAINNET")
            logger.info("Type: Bech32 (SegWit)")
            logger.info("Prefix: bc1 (mainnet bech32)")
            logger.info("\n⚠️  WARNING: This is a MAINNET address with REAL VALUE!")
            return 'mainnet', 'bech32'

        # Testnet P2PKH
        elif address.startswith('m') or address.startswith('n'):
            logger.info("Network: 🧪 TESTNET")
            logger.info("Type: P2PKH (Legacy)")
            logger.info("Prefix: m/n (testnet legacy)")
            return 'testnet', 'p2pkh'

        # Testnet P2SH
        elif address.startswith('2'):
            logger.info("Network: 🧪 TESTNET")
            logger.info("Type: P2SH (Script)")
            logger.info("Prefix: 2 (testnet script)")
            return 'testnet', 'p2sh'

        # Mainnet P2PKH
        elif address.startswith('1'):
            logger.info("Network: 🔴 MAINNET")
            logger.info("Type: P2PKH (Legacy)")
            logger.info("Prefix: 1 (mainnet legacy)")
            logger.info("\n⚠️  WARNING: This is a MAINNET address with REAL VALUE!")
            return 'mainnet', 'p2pkh'

        # Mainnet P2SH
        elif address.startswith('3'):
            logger.info("Network: 🔴 MAINNET")
            logger.info("Type: P2SH (Script)")
            logger.info("Prefix: 3 (mainnet script)")
            logger.info("\n⚠️  WARNING: This is a MAINNET address with REAL VALUE!")
            return 'mainnet', 'p2sh'

        else:
            logger.info("Network: ❓ UNKNOWN")
            logger.info("Type: ❓ UNKNOWN")
            return 'unknown', 'unknown'

    def check_balance_rpc(self, address: str) -> Optional[Dict]:
        """Check balance using RPC"""
        logger.info("\n" + "-"*80)
        logger.info(" 💰 CHECKING BALANCE (Local Node)")
        logger.info("-"*80)

        # Try scantxoutset (requires node with full UTXO set)
        logger.info("\n🔍 Scanning UTXO set...")

        result = self.rpc_call("scantxoutset", ["start", [f"addr({address})"]])

        if 'error' in result:
            logger.info("⚠️  Local node query failed")
            logger.info(f"   Reason: {result['error']}")
            logger.info("   Note: Node may not be running or not fully synced")
            return None

        data = result['result']

        logger.info("\n✅ Query successful!")
        logger.info(f"   Total Amount: {data.get('total_amount', 0):.8f} BTC")
        logger.info(f"   UTXOs Found: {len(data.get('unspents', []))}")

        if data.get('unspents'):
            logger.info("\n📊 Unspent Outputs (UTXOs):")
            for i, utxo in enumerate(data['unspents'], 1):
                logger.info(f"\n   UTXO #{i}:")
                logger.info(f"      TXID: {utxo.get('txid', 'N/A')}")
                logger.info(f"      Vout: {utxo.get('vout', 'N/A')}")
                logger.info(f"      Amount: {utxo.get('amount', 0):.8f} BTC")
                logger.info(f"      Height: {utxo.get('height', 'N/A')}")

        return data

    def show_block_explorer_links(self, address: str, network: str):
        """Show block explorer links"""
        logger.info("\n" + "-"*80)
        logger.info(" 🔗 BLOCK EXPLORER LINKS")
        logger.info("-"*80)

        if network == 'testnet':
            logger.info("\n🧪 Testnet Explorers:")
            logger.info(f"   • Mempool.space: https://mempool.space/testnet/address/{address}")
            logger.info(f"   • Blockstream: https://blockstream.info/testnet/address/{address}")
            logger.info(f"   • BlockCypher: https://live.blockcypher.com/btc-testnet/address/{address}/")
            logger.info(f"   • Local Mempool: http://localhost:8080/address/{address}")

        elif network == 'mainnet':
            logger.info("\n🔴 Mainnet Explorers:")
            logger.info(f"   • Mempool.space: https://mempool.space/address/{address}")
            logger.info(f"   • Blockstream: https://blockstream.info/address/{address}")
            logger.info(f"   • Blockchain.com: https://www.blockchain.com/btc/address/{address}")
            logger.info(f"   • BlockCypher: https://live.blockcypher.com/btc/address/{address}/")

    def check_address(self, address: str):
        """Complete address check"""
        # Identify address type
        network, addr_type = self.identify_address_type(address)

        # Try RPC balance check
        balance_data = self.check_balance_rpc(address)

        # Show explorer links
        self.show_block_explorer_links(address, network)

        # Summary
        logger.info("\n" + "="*80)
        logger.info(" 📊 SUMMARY")
        logger.info("="*80)

        if balance_data:
            total = balance_data.get('total_amount', 0)
            utxos = len(balance_data.get('unspents', []))

            logger.info(f"\n💰 Balance: {total:.8f} BTC")
            logger.info(f"📦 UTXOs: {utxos}")

            if total == 0:
                logger.info("\n📭 Address is empty (no funds)")
                logger.info("\n💡 To receive funds:")
                if network == 'testnet':
                    logger.info("   • Use testnet faucet: https://testnet-faucet.mempool.co/")
                    logger.info(f"   • Send testnet coins to: {address}")
                else:
                    logger.info("   • Use a Bitcoin wallet to send to this address")
                    logger.info("   ⚠️  MAINNET addresses hold REAL VALUE!")
            else:
                logger.info(f"\n✅ Address has funds: {total:.8f} BTC")

                # Convert to satoshis
                satoshis = int(total * 100000000)
                logger.info(f"   = {satoshis:,} satoshis")

                if network == 'testnet':
                    logger.info("   (Testnet coins - NO REAL VALUE)")
                else:
                    logger.info("   ⚠️  REAL MAINNET BITCOIN - HAS VALUE!")

        else:
            logger.info("\n⚠️  Could not query local node")
            logger.info("   Use block explorers above to check balance")

        logger.info("\n" + "="*80)


def main():
    if len(sys.argv) < 2:
        print("Bitcoin Address Balance Checker")
        print("="*80)
        print("\nUsage: python3 check_balance.py <address>")
        print("\nExamples:")
        print("  Testnet: python3 check_balance.py tb1q...")
        print("  Mainnet: python3 check_balance.py bc1q...")
        print("\nSupported formats:")
        print("  • Bech32: bc1... (mainnet), tb1... (testnet)")
        print("  • P2PKH: 1... (mainnet), m/n... (testnet)")
        print("  • P2SH: 3... (mainnet), 2... (testnet)")
        sys.exit(1)

    address = sys.argv[1]
    checker = AddressBalanceChecker()
    checker.check_address(address)


if __name__ == "__main__":
    main()
