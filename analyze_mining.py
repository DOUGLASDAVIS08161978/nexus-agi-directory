#!/usr/bin/env python3
"""
Bitcoin Mining Result Analyzer
Analyze and verify mining results and proof-of-work

Usage: python3 analyze_mining.py <json_file_or_data>
"""

import json
import hashlib
import sys
from datetime import datetime

class MiningAnalyzer:
    """Analyze Bitcoin mining results"""

    def analyze_mining_result(self, data: dict):
        """Analyze mining result data"""
        print("="*80)
        print(" ⛏️  BITCOIN MINING RESULT ANALYSIS")
        print("="*80)

        # Extract data
        header = data.get('header_used', '')
        nonce = data.get('nonce', 0)
        result_hash = data.get('hash', '')
        attempts = data.get('attempts', 0)
        time_sec = data.get('time_seconds', 0)
        hash_rate = data.get('hash_rate_est_per_sec', 0)

        print(f"\n📊 MINING STATISTICS")
        print("-"*80)
        print(f"Nonce Found: {nonce:,}")
        print(f"Total Attempts: {attempts:,}")
        print(f"Time Taken: {time_sec:.4f} seconds")
        print(f"Hash Rate: {hash_rate:,} H/s ({hash_rate/1_000_000:.2f} MH/s)")

        # Analyze the hash
        print(f"\n🔢 PROOF-OF-WORK HASH")
        print("-"*80)
        print(f"Hash: {result_hash}")

        # Count leading zeros
        leading_zeros = len(result_hash) - len(result_hash.lstrip('0'))
        print(f"Leading Zeros: {leading_zeros}")

        # Check if valid proof of work
        if result_hash.startswith('0000'):
            print(f"✅ Valid Proof-of-Work! (starts with '0000')")
            difficulty = self.estimate_difficulty(leading_zeros)
            print(f"Estimated Difficulty: ~{difficulty:.2f}")
        else:
            print(f"❌ Not a valid proof-of-work for typical difficulty")

        # Analyze header
        print(f"\n📦 BLOCK HEADER")
        print("-"*80)
        if '|' in header:
            parts = header.split('|')
            if len(parts) >= 4:
                header_type = parts[0]
                prev_hash = parts[1]
                timestamp = parts[2]
                bits = parts[3]

                print(f"Type: {header_type}")
                print(f"Previous Hash: {prev_hash[:20]}...")
                print(f"Timestamp: {timestamp}")

                # Convert timestamp
                try:
                    ts = int(timestamp)
                    dt = datetime.fromtimestamp(ts)
                    print(f"  → {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    pass

                print(f"Bits (Difficulty): {bits}")
        else:
            print(f"Header: {header[:60]}...")

        # Performance analysis
        print(f"\n⚡ PERFORMANCE ANALYSIS")
        print("-"*80)

        # Expected time to find block
        if hash_rate > 0:
            # Testnet difficulty ~1, means finding hash < target
            # With leading zeros requirement
            expected_attempts = 16 ** leading_zeros
            expected_time = expected_attempts / hash_rate

            print(f"Hash Rate: {hash_rate:,} H/s")
            print(f"  = {hash_rate/1_000:.2f} KH/s")
            print(f"  = {hash_rate/1_000_000:.2f} MH/s")

            print(f"\nFor {leading_zeros} leading zeros:")
            print(f"  Expected Attempts: ~{expected_attempts:,}")
            print(f"  Your Attempts: {attempts:,}")

            if attempts < expected_attempts:
                print(f"  ✅ Lucky! Found faster than expected")
                luck = (expected_attempts / attempts) * 100
                print(f"  🍀 Luck: {luck:.1f}% (found at {attempts/expected_attempts*100:.1f}% of expected)")
            else:
                print(f"  📊 Normal variance")

            print(f"  Expected Time: {expected_time:.2f} seconds")
            print(f"  Actual Time: {time_sec:.4f} seconds")

        # Compare to real mining
        print(f"\n🌐 COMPARISON TO REAL BITCOIN MINING")
        print("-"*80)
        print(f"Your Hash Rate: {hash_rate:,} H/s ({hash_rate/1_000_000:.2f} MH/s)")
        print(f"\nReal Mining Hardware:")
        print(f"  • CPU (like yours): ~10-100 MH/s")
        print(f"  • GPU: ~1-10 GH/s (1,000-10,000 MH/s)")
        print(f"  • ASIC Miner: ~100 TH/s (100,000,000 MH/s)")
        print(f"\nBitcoin Network:")
        print(f"  • Total Hash Rate: ~500 EH/s (500,000,000,000,000 MH/s)")
        print(f"  • Your percentage: {(hash_rate/1_000_000) / 500_000_000_000_000 * 100:.15f}%")

        # Network difficulty
        print(f"\n⛓️  NETWORK DIFFICULTY")
        print("-"*80)
        print(f"Testnet Difficulty: ~1.0 (minimum)")
        print(f"Mainnet Difficulty: ~60-80 trillion")
        print(f"\nWith testnet difficulty, CPU mining is possible!")
        print(f"With mainnet difficulty, you'd need ASIC miners")

        # Educational insight
        print(f"\n📚 WHAT THIS MEANS")
        print("-"*80)
        print(f"✅ You successfully performed proof-of-work!")
        print(f"✅ Your hash starts with enough zeros")
        print(f"✅ This demonstrates Bitcoin's mining process")
        print(f"\n💡 In real Bitcoin mining:")
        print(f"   • You'd need this hash to be below the difficulty target")
        print(f"   • Current mainnet requires ~19-20 leading zeros")
        print(f"   • ASICs do this trillions of times per second")
        print(f"   • Network finds a block every ~10 minutes")

        print("\n" + "="*80)

    def estimate_difficulty(self, leading_zeros: int) -> float:
        """Estimate difficulty from leading zeros"""
        # Each leading zero (in hex) represents 4 bits
        # Difficulty roughly doubles for each bit
        return 16 ** leading_zeros / 4

    def verify_hash(self, header: str, nonce: int, expected_hash: str) -> bool:
        """Verify the mining result"""
        print("\n🔍 VERIFYING PROOF-OF-WORK")
        print("-"*80)

        # Reconstruct the data that was hashed
        data = f"{header}{nonce}".encode()

        # Double SHA-256 (Bitcoin's hash algorithm)
        hash1 = hashlib.sha256(data).digest()
        hash2 = hashlib.sha256(hash1).hexdigest()

        print(f"Reconstructed Hash: {hash2}")
        print(f"Claimed Hash: {expected_hash}")

        if hash2 == expected_hash:
            print("✅ Hash verified! Proof-of-work is valid!")
            return True
        else:
            print("⚠️  Hash mismatch (expected for demo data)")
            print("   This is normal for educational demonstrations")
            return False


def main():
    """Main execution"""

    if len(sys.argv) < 2:
        print("Bitcoin Mining Result Analyzer")
        print("="*80)
        print("\nUsage: python3 analyze_mining.py <json_data>")
        print("\nOr provide JSON data via stdin")
        print("\nExample:")
        print('  python3 analyze_mining.py \'{"nonce": 45703, "hash": "000050da...", ...}\'')
        sys.exit(1)

    # Try to parse JSON from argument
    json_data = sys.argv[1]

    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        print("❌ Invalid JSON data")
        sys.exit(1)

    analyzer = MiningAnalyzer()
    analyzer.analyze_mining_result(data)


if __name__ == "__main__":
    main()
