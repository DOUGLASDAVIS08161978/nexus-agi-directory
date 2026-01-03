#!/usr/bin/env python3
"""
Testnet Coin Miner
Automated testnet mining tool for the Bitcoin learning system

Authors: Douglas Shane Davis & Claude
Purpose: Mine testnet coins for educational purposes
"""

import subprocess
import json
import time
import sys
from typing import Dict

class TestnetMiner:
    """Mine testnet coins"""

    def __init__(self, rpc_url: str = "http://127.0.0.1:18332",
                 rpc_user: str = "bitcoinrpc",
                 rpc_password: str = "testnet123"):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.blocks_mined = 0
        self.total_reward = 0.0

    def rpc_call(self, method: str, params: list = None) -> Dict:
        """Make RPC call"""
        if params is None:
            params = []

        request_data = {
            "jsonrpc": "1.0",
            "id": "miner",
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

    def get_or_create_address(self) -> str:
        """Get mining address"""
        print("📬 Getting mining address...")

        # Try to get existing address
        result = self.rpc_call("getnewaddress", ["mining", "bech32"])

        if 'error' in result:
            print(f"   ❌ Could not generate address: {result['error']}")
            return None

        address = result['result']
        print(f"   ✅ Mining address: {address}")
        return address

    def mine_blocks(self, num_blocks: int, address: str):
        """Mine blocks to address"""
        print(f"\n⛏️  Mining {num_blocks} block(s)...")
        print(f"   Address: {address[:30]}...")
        print(f"   ⏳ Mining in progress...")

        start_time = time.time()

        result = self.rpc_call("generatetoaddress", [num_blocks, address])

        if 'error' in result:
            print(f"   ❌ Mining failed: {result['error']}")
            return False

        end_time = time.time()
        duration = end_time - start_time

        block_hashes = result['result']
        self.blocks_mined += len(block_hashes)
        reward = len(block_hashes) * 50.0  # 50 tBTC per block
        self.total_reward += reward

        print(f"   ✅ Successfully mined {len(block_hashes)} block(s)!")
        print(f"   ⏱️  Time: {duration:.2f} seconds")
        print(f"   💰 Reward: {reward:.8f} tBTC")
        print(f"   📦 Block hashes:")

        for i, hash in enumerate(block_hashes, 1):
            print(f"      {i}. {hash[:20]}...{hash[-20:]}")

        return True

    def check_balance(self) -> float:
        """Check wallet balance"""
        result = self.rpc_call("getbalances")

        if 'error' in result:
            return 0.0

        balances = result['result']
        mine = balances.get('mine', {})

        return mine.get('immature', 0.0)

    def show_stats(self):
        """Show mining statistics"""
        print(f"\n📊 MINING STATISTICS")
        print("="*60)
        print(f"   Blocks Mined: {self.blocks_mined}")
        print(f"   Total Reward: {self.total_reward:.8f} tBTC")
        print(f"   Average per Block: 50.00000000 tBTC")

        balance = self.check_balance()
        print(f"\n💰 WALLET BALANCE")
        print(f"   Immature: {balance:.8f} tBTC")
        print(f"   (Spendable after 100 confirmations)")

        print("="*60)

    def mine_session(self, total_blocks: int = 10, batch_size: int = 1):
        """Run a mining session"""
        print("="*80)
        print(" ⛏️  TESTNET MINING SESSION")
        print("="*80)
        print(f"\nTarget: Mine {total_blocks} blocks")
        print(f"Batch size: {batch_size} block(s) at a time")
        print()

        # Get mining address
        address = self.get_or_create_address()
        if not address:
            print("❌ Cannot proceed without address")
            return

        # Mine in batches
        blocks_remaining = total_blocks
        batch_num = 0

        while blocks_remaining > 0:
            batch_num += 1
            blocks_this_batch = min(batch_size, blocks_remaining)

            print(f"\n{'='*60}")
            print(f" Batch #{batch_num}")
            print(f"{'='*60}")

            if self.mine_blocks(blocks_this_batch, address):
                blocks_remaining -= blocks_this_batch
            else:
                print("⚠️  Mining failed, stopping session")
                break

            if blocks_remaining > 0:
                print(f"\n   📊 Progress: {total_blocks - blocks_remaining}/{total_blocks} blocks")
                time.sleep(1)  # Brief pause between batches

        # Final statistics
        print(f"\n{'='*80}")
        print(" ✅ MINING SESSION COMPLETE")
        print(f"{'='*80}")
        self.show_stats()

        print(f"\n💡 NEXT STEPS:")
        print(f"   • Blocks must mature (100 confirmations)")
        print(f"   • Then you can spend the coins")
        print(f"   • Use: check_balance.py to monitor")
        print()


def main():
    """Main execution"""

    # Parse arguments
    total_blocks = 10
    batch_size = 1

    if len(sys.argv) > 1:
        try:
            total_blocks = int(sys.argv[1])
        except:
            pass

    if len(sys.argv) > 2:
        try:
            batch_size = int(sys.argv[2])
        except:
            pass

    print("\n" + "="*80)
    print(" ⛏️  BITCOIN TESTNET MINER")
    print("="*80)
    print("\nMine testnet coins for educational purposes")
    print("Testnet coins have NO VALUE - safe for learning!")
    print()
    print("Usage: python3 mine_testnet_coins.py [total_blocks] [batch_size]")
    print(f"\nMining: {total_blocks} blocks in batches of {batch_size}")
    print("="*80 + "\n")

    miner = TestnetMiner()
    miner.mine_session(total_blocks, batch_size)


if __name__ == "__main__":
    main()
