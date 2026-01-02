"""
BITCOIN TESTNET LEARNING SYSTEM
================================
Complete Bitcoin testnet mining, wallet management, and transaction system
Educational system for learning Bitcoin mechanics with real blockchain

Network: Testnet (public test blockchain)
Mining: Real proof-of-work (adjusted difficulty)
Transactions: Real propagation across network
Coins: NO VALUE - for learning only

Authors: Douglas Shane Davis & Claude
Purpose: Complete Bitcoin education through hands-on mining and transactions
"""

import subprocess
import json
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class BitcoinTestnetSystem:
    """
    Complete Bitcoin Testnet Learning System

    Features:
    - CPU mining on testnet
    - Wallet creation and management
    - Address generation
    - Transaction creation
    - Block exploration
    - Balance tracking
    """

    def __init__(self, rpc_url: str = "http://127.0.0.1:18332",
                 rpc_user: str = "bitcoinrpc",
                 rpc_password: str = "testnet123"):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password

        # Mining stats
        self.blocks_found = 0
        self.mining_attempts = 0
        self.wallets = {}
        self.addresses = {}

        logger.info("🎓 Bitcoin Testnet Learning System initialized")
        logger.info(f"   RPC URL: {self.rpc_url}")
        logger.info(f"   Network: TESTNET (real blockchain, no value)")

    def rpc_call(self, method: str, params: List = None) -> Dict:
        """Make Bitcoin RPC call using curl"""
        if params is None:
            params = []

        request_data = {
            "jsonrpc": "1.0",
            "id": "learning",
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
                return {
                    'error': 'curl_failed',
                    'stderr': result.stderr,
                    'method': method
                }

            response = json.loads(result.stdout)

            if 'error' in response and response['error']:
                return {'error': response['error'], 'method': method}

            return {'success': True, 'result': response.get('result')}

        except Exception as e:
            logger.error(f"   ❌ RPC Error ({method}): {e}")
            return {'error': str(e), 'method': method}

    def check_connection(self) -> bool:
        """Check Bitcoin Core connection"""
        logger.info("\n🔌 Checking Bitcoin Core connection...")

        result = self.rpc_call("getblockchaininfo")

        if 'error' in result:
            logger.error("   ❌ Cannot connect to Bitcoin Core")
            logger.error("\n   💡 START BITCOIN CORE TESTNET:")
            logger.error("      bitcoind -testnet -daemon \\")
            logger.error("               -rpcuser=bitcoinrpc \\")
            logger.error("               -rpcpassword=testnet123 \\")
            logger.error("               -server")
            return False

        info = result['result']
        chain = info.get('chain', 'unknown')
        blocks = info.get('blocks', 0)
        headers = info.get('headers', 0)
        sync_progress = info.get('verificationprogress', 0) * 100

        logger.info(f"   ✅ Connected to Bitcoin Core")
        logger.info(f"   Chain: {chain}")
        logger.info(f"   Blocks: {blocks:,}")
        logger.info(f"   Headers: {headers:,}")
        logger.info(f"   Sync: {sync_progress:.2f}%")

        if sync_progress < 99.9:
            logger.warning(f"   ⚠️  Node still syncing...")
            logger.info(f"   Syncing from network - this may take time")

        return True

    def create_wallet(self, wallet_name: str) -> bool:
        """Create new wallet"""
        logger.info(f"\n👛 Creating wallet: {wallet_name}")

        result = self.rpc_call("createwallet", [wallet_name, False, False, "", False, True])

        if 'error' in result:
            # Try to load if exists
            result = self.rpc_call("loadwallet", [wallet_name])
            if 'error' in result:
                logger.error(f"   ❌ Could not create/load wallet")
                return False
            logger.info(f"   ✅ Wallet loaded: {wallet_name}")
        else:
            logger.info(f"   ✅ Wallet created: {wallet_name}")

        self.wallets[wallet_name] = {'created': datetime.now(), 'addresses': []}
        return True

    def generate_address(self, label: str = "mining") -> Optional[str]:
        """Generate new address"""
        logger.info(f"\n📬 Generating new address (label: {label})...")

        result = self.rpc_call("getnewaddress", [label, "bech32"])

        if 'error' in result:
            logger.error("   ❌ Could not generate address")
            return None

        address = result['result']
        logger.info(f"   ✅ Address generated!")
        logger.info(f"   📍 {address}")

        self.addresses[address] = {
            'label': label,
            'created': datetime.now(),
            'type': 'bech32'
        }

        return address

    def get_balance(self) -> Dict:
        """Get wallet balance"""
        result = self.rpc_call("getbalances")

        if 'error' in result:
            return {'total': 0, 'confirmed': 0, 'unconfirmed': 0}

        balances = result['result']
        mine = balances.get('mine', {})

        return {
            'total': mine.get('trusted', 0) + mine.get('untrusted_pending', 0),
            'confirmed': mine.get('trusted', 0),
            'unconfirmed': mine.get('untrusted_pending', 0),
            'immature': mine.get('immature', 0)
        }

    def get_mining_info(self) -> Dict:
        """Get mining information"""
        result = self.rpc_call("getmininginfo")

        if 'error' in result:
            return {}

        return result['result']

    def start_cpu_mining(self, num_threads: int = 1) -> bool:
        """
        Start CPU mining
        WARNING: Testnet mining is HARD - may take hours/days to find a block
        """
        logger.info(f"\n⛏️  Starting CPU mining...")
        logger.info(f"   Threads: {num_threads}")
        logger.info(f"   ⚠️  WARNING: Testnet mining uses real proof-of-work")
        logger.info(f"   ⚠️  Finding blocks may take HOURS or DAYS")

        # Generate mining address if needed
        if not self.addresses:
            self.generate_address("cpu_mining")

        result = self.rpc_call("generatetoaddress", [1, list(self.addresses.keys())[0]])

        if 'error' in result:
            logger.error("   ❌ Mining failed to start")
            return False

        logger.info("   ✅ Mining command sent")
        return True

    def mine_blocks(self, num_blocks: int, address: str) -> bool:
        """
        Attempt to mine blocks
        Note: On testnet, this is REAL mining with proof-of-work
        """
        logger.info(f"\n⛏️  Attempting to mine {num_blocks} block(s)...")
        logger.info(f"   Address: {address[:20]}...")
        logger.info(f"   🔄 This may take considerable time...")

        self.mining_attempts += num_blocks

        result = self.rpc_call("generatetoaddress", [num_blocks, address])

        if 'error' in result:
            logger.error("   ❌ Mining failed")
            return False

        block_hashes = result['result']
        self.blocks_found += len(block_hashes)

        logger.info(f"   ✅ Successfully mined {len(block_hashes)} block(s)!")
        for i, hash in enumerate(block_hashes):
            logger.info(f"   📦 Block {i+1}: {hash[:20]}...")

        return True

    def send_transaction(self, to_address: str, amount: float,
                        subtract_fee: bool = False) -> Optional[str]:
        """Send transaction"""
        logger.info(f"\n💸 Creating transaction...")
        logger.info(f"   To: {to_address[:20]}...")
        logger.info(f"   Amount: {amount} tBTC")
        logger.info(f"   Subtract fee from amount: {subtract_fee}")

        result = self.rpc_call("sendtoaddress", [to_address, amount, "", "", subtract_fee])

        if 'error' in result:
            logger.error(f"   ❌ Transaction failed: {result.get('error')}")
            return None

        txid = result['result']
        logger.info(f"   ✅ Transaction created!")
        logger.info(f"   📝 TXID: {txid}")
        logger.info(f"   ⏳ Transaction in mempool, waiting for confirmation...")

        return txid

    def get_transaction(self, txid: str) -> Dict:
        """Get transaction details"""
        result = self.rpc_call("gettransaction", [txid])

        if 'error' in result:
            return {}

        return result['result']

    def list_transactions(self, count: int = 10) -> List[Dict]:
        """List recent transactions"""
        result = self.rpc_call("listtransactions", ["*", count])

        if 'error' in result:
            return []

        return result['result']

    def explain_testnet(self):
        """Educational explanation of testnet"""
        logger.info("\n" + "="*70)
        logger.info(" 📚 BITCOIN TESTNET - EDUCATIONAL GUIDE")
        logger.info("="*70)

        logger.info("\n🌐 WHAT IS TESTNET?")
        logger.info("   • Public Bitcoin test blockchain")
        logger.info("   • Real proof-of-work mining")
        logger.info("   • Real transaction propagation")
        logger.info("   • Coins have ZERO value")
        logger.info("   • Perfect for learning!")

        logger.info("\n⛏️  TESTNET MINING:")
        logger.info("   • Uses same algorithm as mainnet (SHA-256)")
        logger.info("   • Difficulty adjusts based on network hashrate")
        logger.info("   • Block reward: 50 tBTC (testnet coins)")
        logger.info("   • Block time: ~10 minutes target")
        logger.info("   • CPU mining: Possible but slow")
        logger.info("   • May take hours/days to find blocks")

        logger.info("\n💰 GETTING TESTNET COINS:")
        logger.info("   Option 1: Mine blocks (slow)")
        logger.info("   Option 2: Use testnet faucets (fast)")
        logger.info("   • https://testnet-faucet.mempool.co/")
        logger.info("   • https://bitcoinfaucet.uo1.net/")
        logger.info("   • https://testnet.help/")

        logger.info("\n📝 TRANSACTIONS:")
        logger.info("   • Work exactly like mainnet")
        logger.info("   • Broadcast to real P2P network")
        logger.info("   • Confirmed by miners")
        logger.info("   • Visible on testnet block explorers")

        logger.info("\n🔍 BLOCK EXPLORERS:")
        logger.info("   • https://mempool.space/testnet")
        logger.info("   • https://blockstream.info/testnet/")
        logger.info("   • Use these to view your transactions!")

        logger.info("\n" + "="*70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution - connects to real Bitcoin testnet"""
    system = BitcoinTestnetSystem()

    # Show educational info
    system.explain_testnet()

    # Check connection to Bitcoin Core
    if not system.check_connection():
        logger.error("\n❌ Bitcoin Core not running!")
        logger.error("   Please start Bitcoin Core first:")
        logger.error("   bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123 -server")
        return

    # Create wallet
    if not system.create_wallet("learning_wallet"):
        logger.error("❌ Failed to create wallet")
        return

    # Generate address
    address = system.generate_address("testnet_learning")
    if not address:
        logger.error("❌ Failed to generate address")
        return

    # Check balance
    logger.info("\n💰 Checking wallet balance...")
    balance = system.get_balance()
    logger.info(f"   Confirmed: {balance['confirmed']:.8f} tBTC")
    logger.info(f"   Unconfirmed: {balance['unconfirmed']:.8f} tBTC")
    logger.info(f"   Immature: {balance['immature']:.8f} tBTC")
    logger.info(f"   Total: {balance['total']:.8f} tBTC")

    # Get mining info
    logger.info("\n⛏️  Getting mining information...")
    mining_info = system.get_mining_info()
    if mining_info:
        logger.info(f"   Network difficulty: {mining_info.get('difficulty', 'N/A')}")
        logger.info(f"   Network hashrate: {mining_info.get('networkhashps', 0) / 1e12:.2f} TH/s")
        logger.info(f"   Blocks: {mining_info.get('blocks', 'N/A')}")

    # List recent transactions
    logger.info("\n📝 Recent transactions:")
    transactions = system.list_transactions(5)
    if transactions:
        for i, tx in enumerate(transactions[:5], 1):
            logger.info(f"   {i}. {tx.get('category', 'unknown')}: {tx.get('amount', 0):.8f} tBTC")
    else:
        logger.info("   No transactions yet")

    logger.info("\n" + "="*70)
    logger.info(" ✅ BITCOIN TESTNET SYSTEM READY!")
    logger.info("="*70)
    logger.info("\n💡 NEXT STEPS:")
    logger.info("   1. Get testnet coins from faucet:")
    logger.info(f"      https://testnet-faucet.mempool.co/")
    logger.info(f"      Your address: {address}")
    logger.info("\n   2. Try sending a transaction:")
    logger.info("      system.send_transaction(<recipient_address>, 0.001)")
    logger.info("\n   3. Try mining (will take time!):")
    logger.info(f"      system.mine_blocks(1, '{address}')")
    logger.info("\n")


if __name__ == "__main__":
    main()
