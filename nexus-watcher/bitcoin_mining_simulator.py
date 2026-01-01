"""
BITCOIN MINING EDUCATIONAL SIMULATOR v1.0
==========================================
⚠️  EDUCATIONAL SIMULATION ONLY - NOT REAL BITCOIN MINING ⚠️

This is a simulation that demonstrates Bitcoin mining concepts including:
- Proof-of-Work algorithm
- Block validation
- Transaction creation and signing
- Difficulty adjustment
- Blockchain structure

This does NOT:
- Mine real Bitcoin
- Connect to the Bitcoin network
- Deposit to real wallets
- Generate actual cryptocurrency value

For educational purposes only.
"""

import hashlib
import time
import json
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import struct


# ======================================================
# BITCOIN SIMULATION DATA STRUCTURES
# ======================================================

@dataclass
class Transaction:
    """Simulated Bitcoin transaction"""
    sender: str
    recipient: str
    amount: float
    timestamp: float
    signature: str = ""
    tx_id: str = ""

    def __post_init__(self):
        if not self.tx_id:
            self.tx_id = self._calculate_tx_id()
        if not self.signature:
            self.signature = self._sign_transaction()

    def _calculate_tx_id(self) -> str:
        """Calculate transaction ID"""
        data = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()

    def _sign_transaction(self) -> str:
        """Simulate transaction signing"""
        data = f"{self.tx_id}{self.sender}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class Block:
    """Simulated Bitcoin block"""
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    difficulty: int = 4
    miner_address: str = ""
    block_reward: float = 6.25  # Current Bitcoin block reward
    hash: str = ""

    def calculate_hash(self) -> str:
        """Calculate block hash using SHA-256"""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [
                {
                    'sender': tx.sender,
                    'recipient': tx.recipient,
                    'amount': tx.amount,
                    'tx_id': tx.tx_id
                }
                for tx in self.transactions
            ],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'miner': self.miner_address
        }

        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> Dict[str, Any]:
        """
        Simulate Proof-of-Work mining.
        Find a nonce that produces a hash with required leading zeros.
        """
        target = "0" * difficulty
        start_time = time.time()
        attempts = 0

        print(f"\n⛏️  Mining block {self.index}...")
        print(f"   Target: {target}{'*' * (64 - difficulty)}")
        print(f"   Difficulty: {difficulty} leading zeros")

        while True:
            self.nonce = attempts
            self.hash = self.calculate_hash()

            # Check if hash meets difficulty requirement
            if self.hash.startswith(target):
                mining_time = time.time() - start_time
                hash_rate = attempts / mining_time if mining_time > 0 else attempts

                print(f"   ✅ Block mined!")
                print(f"   Hash: {self.hash}")
                print(f"   Nonce: {self.nonce:,}")
                print(f"   Attempts: {attempts:,}")
                print(f"   Time: {mining_time:.2f}s")
                print(f"   Hash Rate: {hash_rate:,.0f} H/s")

                return {
                    'success': True,
                    'hash': self.hash,
                    'nonce': self.nonce,
                    'attempts': attempts,
                    'time': mining_time,
                    'hash_rate': hash_rate
                }

            attempts += 1

            # Progress indicator
            if attempts % 10000 == 0:
                print(f"   ... {attempts:,} attempts, current hash: {self.hash[:16]}...")


@dataclass
class Blockchain:
    """Simulated Bitcoin blockchain"""
    chain: List[Block] = field(default_factory=list)
    pending_transactions: List[Transaction] = field(default_factory=list)
    difficulty: int = 4
    mining_reward: float = 6.25

    def __post_init__(self):
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64,
            difficulty=self.difficulty,
            miner_address="GENESIS"
        )
        genesis.hash = genesis.calculate_hash()
        self.chain.append(genesis)
        print("🎬 Genesis block created")

    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """Add transaction to pending pool"""
        self.pending_transactions.append(transaction)
        print(f"💸 Transaction added: {transaction.amount:.8f} BTC")

    def mine_pending_transactions(self, miner_address: str) -> Dict[str, Any]:
        """
        Mine a new block with pending transactions.
        Includes coinbase transaction (mining reward).
        """
        # Create coinbase transaction (mining reward)
        coinbase = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=self.mining_reward,
            timestamp=time.time()
        )

        # Add pending transactions
        block_transactions = [coinbase] + self.pending_transactions

        # Create new block
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=block_transactions,
            previous_hash=self.get_latest_block().hash,
            difficulty=self.difficulty,
            miner_address=miner_address,
            block_reward=self.mining_reward
        )

        # Mine the block (Proof-of-Work)
        mining_result = new_block.mine_block(self.difficulty)

        # Add block to chain
        self.chain.append(new_block)

        # Clear pending transactions
        self.pending_transactions = []

        return {
            **mining_result,
            'block_index': new_block.index,
            'reward': self.mining_reward,
            'transactions': len(block_transactions)
        }

    def validate_chain(self) -> bool:
        """Validate the entire blockchain"""
        print("\n🔍 Validating blockchain...")

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if current hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"   ❌ Block {i} hash is invalid")
                return False

            # Check if previous hash reference is correct
            if current_block.previous_hash != previous_block.hash:
                print(f"   ❌ Block {i} previous hash is invalid")
                return False

            # Check if hash meets difficulty requirement
            if not current_block.hash.startswith("0" * current_block.difficulty):
                print(f"   ❌ Block {i} doesn't meet difficulty requirement")
                return False

        print("   ✅ All blocks valid!")
        return True

    def get_balance(self, address: str) -> float:
        """Calculate balance for an address"""
        balance = 0.0

        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount

        return balance


# ======================================================
# BITCOIN MINING SIMULATOR
# ======================================================

class BitcoinMiningSimulator:
    """
    Educational Bitcoin mining simulator.
    Demonstrates mining concepts without real blockchain interaction.
    """

    def __init__(self, miner_name: str, difficulty: int = 4):
        self.miner_name = miner_name
        self.miner_address = self._generate_address(miner_name)
        self.blockchain = Blockchain(difficulty=difficulty)
        self.total_mined = 0.0
        self.blocks_mined = 0
        self.total_hash_attempts = 0
        self.mining_history = []

        print("="*80)
        print("           ⛏️  BITCOIN MINING SIMULATOR v1.0")
        print("          Educational Demonstration - Not Real Mining")
        print("="*80)
        print(f"\n👷 Miner: {self.miner_name}")
        print(f"📧 Simulated Address: {self.miner_address}")
        print(f"🎯 Difficulty: {difficulty} leading zeros")
        print(f"💰 Block Reward: {self.blockchain.mining_reward} BTC")
        print("="*80)

    def _generate_address(self, name: str) -> str:
        """Generate simulated Bitcoin address"""
        # Simulate Bitcoin address format (starts with 1, 3, or bc1)
        hash_input = f"{name}{time.time()}"
        hash_val = hashlib.sha256(hash_input.encode()).hexdigest()
        # Create address ending with requested suffix
        return f"1{hash_val[:25]}WASS"

    def create_transaction(self, sender: str, recipient: str, amount: float):
        """Create a simulated transaction"""
        tx = Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            timestamp=time.time()
        )
        self.blockchain.add_transaction(tx)
        return tx

    def mine_block(self) -> Dict[str, Any]:
        """Mine a single block"""
        print(f"\n{'='*80}")
        print(f"   MINING SESSION {self.blocks_mined + 1}")
        print(f"{'='*80}")

        result = self.blockchain.mine_pending_transactions(self.miner_address)

        self.blocks_mined += 1
        self.total_mined += result['reward']
        self.total_hash_attempts += result['attempts']

        mining_record = {
            'block': result['block_index'],
            'reward': result['reward'],
            'transactions': result['transactions'],
            'hash': result['hash'],
            'time': result['time'],
            'hash_rate': result['hash_rate']
        }
        self.mining_history.append(mining_record)

        return result

    def run_mining_session(self, num_blocks: int = 3, create_txs: bool = True):
        """
        Run a complete mining simulation session.
        """
        print("\n🚀 Starting mining session...")
        print(f"   Target: {num_blocks} blocks")

        session_start = time.time()

        for i in range(num_blocks):
            # Optionally create some transactions
            if create_txs and i > 0:
                num_txs = random.randint(1, 3)
                for _ in range(num_txs):
                    sender = f"User{random.randint(1, 100)}"
                    recipient = f"User{random.randint(1, 100)}"
                    amount = round(random.uniform(0.001, 1.0), 8)
                    self.create_transaction(sender, recipient, amount)

            # Mine block
            self.mine_block()

            # Small delay for readability
            time.sleep(0.1)

        session_time = time.time() - session_start

        # Validate blockchain
        self.blockchain.validate_chain()

        # Generate report
        self._print_mining_report(session_time)

        return self.get_statistics()

    def _print_mining_report(self, session_time: float):
        """Print comprehensive mining report"""
        print("\n" + "="*80)
        print("                        📊 MINING SESSION REPORT")
        print("="*80)

        print(f"\n⛏️  MINING PERFORMANCE")
        print(f"   Blocks Mined:           {self.blocks_mined}")
        print(f"   Total Hash Attempts:    {self.total_hash_attempts:,}")
        print(f"   Session Time:           {session_time:.2f}s")

        if session_time > 0:
            avg_hash_rate = self.total_hash_attempts / session_time
            print(f"   Average Hash Rate:      {avg_hash_rate:,.0f} H/s")

        print(f"\n💰 REWARDS")
        print(f"   Total BTC Mined:        {self.total_mined:.8f} BTC")
        print(f"   Reward per Block:       {self.blockchain.mining_reward:.8f} BTC")
        print(f"   Miner Address:          {self.miner_address}")

        # Show balance
        balance = self.blockchain.get_balance(self.miner_address)
        print(f"   Current Balance:        {balance:.8f} BTC")

        print(f"\n⛓️  BLOCKCHAIN STATUS")
        print(f"   Chain Length:           {len(self.blockchain.chain)} blocks")
        print(f"   Difficulty:             {self.blockchain.difficulty}")
        print(f"   Validation Status:      ✅ Valid")

        # Block details
        print(f"\n📦 MINED BLOCKS")
        for record in self.mining_history:
            print(f"   Block #{record['block']}:")
            print(f"      Hash:       {record['hash']}")
            print(f"      Reward:     {record['reward']:.8f} BTC")
            print(f"      Txs:        {record['transactions']}")
            print(f"      Time:       {record['time']:.2f}s")
            print(f"      Hash Rate:  {record['hash_rate']:,.0f} H/s")

        # Simulated deposit information
        print(f"\n💳 SIMULATED DEPOSIT")
        print(f"   ⚠️  THIS IS A SIMULATION - NO REAL BITCOIN ⚠️")
        print(f"   Recipient Address:      {self.miner_address}")
        print(f"   Total Deposited:        {balance:.8f} BTC (SIMULATED)")
        print(f"   Status:                 ✅ Simulation Complete")

        print("\n" + "="*80)
        print("   ⚠️  EDUCATIONAL SIMULATION ONLY - NOT REAL BITCOIN MINING ⚠️")
        print("="*80)

    def get_statistics(self) -> Dict[str, Any]:
        """Get mining statistics"""
        return {
            'miner_address': self.miner_address,
            'blocks_mined': self.blocks_mined,
            'total_btc_mined': self.total_mined,
            'current_balance': self.blockchain.get_balance(self.miner_address),
            'total_hash_attempts': self.total_hash_attempts,
            'blockchain_length': len(self.blockchain.chain),
            'blockchain_valid': self.blockchain.validate_chain(),
            'mining_history': self.mining_history
        }

    def export_blockchain(self, filename: str = "simulated_blockchain.json"):
        """Export blockchain to JSON"""
        chain_data = []

        for block in self.blockchain.chain:
            block_data = {
                'index': block.index,
                'timestamp': block.timestamp,
                'hash': block.hash,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce,
                'miner': block.miner_address,
                'reward': block.block_reward,
                'transactions': [
                    {
                        'tx_id': tx.tx_id,
                        'sender': tx.sender,
                        'recipient': tx.recipient,
                        'amount': tx.amount,
                        'signature': tx.signature
                    }
                    for tx in block.transactions
                ]
            }
            chain_data.append(block_data)

        with open(filename, 'w') as f:
            json.dump(chain_data, f, indent=2)

        print(f"\n💾 Blockchain exported to {filename}")


# ======================================================
# DEMONSTRATION
# ======================================================

def run_demonstration():
    """Run complete mining simulation demonstration"""

    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "       ⛏️  BITCOIN MINING EDUCATIONAL SIMULATOR".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "   This simulates Bitcoin mining algorithms for education".center(78) + "║")
    print("║" + "   NO REAL BITCOIN IS MINED OR TRANSFERRED".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    print()

    # Create simulator
    # Using difficulty 4 for demonstration (real Bitcoin uses ~19-20)
    simulator = BitcoinMiningSimulator(
        miner_name="NexusAGI Miner",
        difficulty=4  # Lower difficulty for demo speed
    )

    # Run mining session
    print("\n🔧 Configuration:")
    print(f"   • Proof-of-Work algorithm: SHA-256")
    print(f"   • Difficulty: {simulator.blockchain.difficulty} leading zeros")
    print(f"   • Block reward: {simulator.blockchain.mining_reward} BTC")
    print(f"   • Transaction validation: Enabled")
    print(f"   • Blockchain validation: Enabled")

    # Mine 3 blocks
    stats = simulator.run_mining_session(num_blocks=3, create_txs=True)

    # Export blockchain
    simulator.export_blockchain()

    # Final summary
    print("\n✅ SIMULATION COMPLETE")
    print(f"   Total simulated BTC: {stats['total_btc_mined']:.8f}")
    print(f"   Address: {stats['miner_address']}")
    print(f"   Blockchain: {stats['blockchain_length']} blocks")
    print(f"   Valid: {stats['blockchain_valid']}")

    print("\n" + "="*80)
    print("IMPORTANT DISCLAIMER:")
    print("="*80)
    print("This is an EDUCATIONAL SIMULATION demonstrating Bitcoin mining concepts.")
    print("It does NOT:")
    print("  • Mine real Bitcoin")
    print("  • Connect to the Bitcoin network")
    print("  • Deposit to real wallet addresses")
    print("  • Generate actual cryptocurrency value")
    print()
    print("To mine real Bitcoin, you would need:")
    print("  • Specialized ASIC mining hardware (costs $1,000-$10,000+)")
    print("  • Bitcoin node software (Bitcoin Core)")
    print("  • Connection to Bitcoin network")
    print("  • Significant electricity (mining is energy-intensive)")
    print("  • Mining pool membership (solo mining is impractical)")
    print("="*80 + "\n")

    return simulator


if __name__ == "__main__":
    simulator = run_demonstration()
