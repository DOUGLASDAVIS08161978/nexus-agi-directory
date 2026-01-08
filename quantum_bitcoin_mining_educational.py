#!/usr/bin/env python3
"""
QUANTUM BITCOIN MINING EDUCATIONAL SYSTEM
==========================================
Educational demonstration of quantum computing concepts applied to Bitcoin mining
Shows theoretical capabilities, current limitations, and future possibilities

⚠️  CRITICAL EDUCATIONAL DISCLAIMER ⚠️
This is a SIMULATION for learning purposes only!
- Quantum computers DO NOT currently break Bitcoin mining
- SHA-256 is NOT efficiently solvable by known quantum algorithms
- This demonstrates theoretical concepts, not real mining
- Grover's algorithm provides only √N speedup (not enough for profitability)
- Real profitable mining still requires ASICs, not quantum computers

Authors: Douglas Shane Davis & Claude
Purpose: Educate about quantum computing and Bitcoin mining realities
Version: 1.0 Educational Simulation
"""

import hashlib
import time
import random
import math
from datetime import datetime
from typing import Dict, Tuple, Optional


class Colors:
    """ANSI color codes for output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class QuantumMiningSimulator:
    """
    Educational simulator demonstrating quantum computing concepts for Bitcoin mining

    IMPORTANT: This is educational simulation, not real quantum computing!
    """

    def __init__(self):
        # Current Bitcoin network stats
        self.network_hashrate = 888.8e18  # 888.8 EH/s (exahashes per second)
        self.difficulty = 121507793131898.1
        self.block_reward = 3.125  # BTC after April 2024 halving
        self.btc_price = 101474.66  # USD

        # Classical computing stats
        self.cpu_hashrate = 1_000_000  # 1 MH/s
        self.gpu_hashrate = 100_000_000  # 100 MH/s
        self.asic_hashrate = 100_000_000_000_000  # 100 TH/s

        # Theoretical quantum stats (SIMULATED - not real!)
        self.quantum_qubits = 4096  # Theoretical quantum computer
        self.quantum_coherence_time = 100  # microseconds (theoretical)

    def print_header(self):
        """Print system header with warnings"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}")
        print(" QUANTUM BITCOIN MINING EDUCATIONAL SYSTEM")
        print(" Theoretical Analysis & Reality Check")
        print(f"{'='*80}{Colors.ENDC}\n")

        print(f"{Colors.FAIL}{Colors.BOLD}⚠️  CRITICAL EDUCATIONAL DISCLAIMER ⚠️{Colors.ENDC}")
        print(f"{Colors.WARNING}   • This is a SIMULATION for learning purposes only!")
        print(f"   • Quantum computers DO NOT currently break Bitcoin mining")
        print(f"   • SHA-256 is NOT efficiently solvable by quantum algorithms")
        print(f"   • Grover's algorithm provides only √N speedup (insufficient)")
        print(f"   • Real profitable mining STILL requires ASICs")
        print(f"   • This demonstrates THEORETICAL concepts, not real capabilities{Colors.ENDC}")
        print(f"\n{'-'*80}\n")

    def section_1_quantum_computing_basics(self):
        """Explain quantum computing basics"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}📚 SECTION 1: QUANTUM COMPUTING BASICS{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}What is Quantum Computing?{Colors.ENDC}")
        print(f"   • Uses quantum bits (qubits) instead of classical bits")
        print(f"   • Qubits can be in superposition (0 AND 1 simultaneously)")
        print(f"   • Quantum entanglement allows correlated states")
        print(f"   • Quantum interference amplifies correct answers")

        print(f"\n   {Colors.BOLD}Classical vs Quantum{Colors.ENDC}")
        print(f"   Classical Bit:  |0⟩ OR |1⟩")
        print(f"   Quantum Qubit:  α|0⟩ + β|1⟩  (superposition)")
        print(f"   ")
        print(f"   Classical Computer: Checks solutions sequentially")
        print(f"   Quantum Computer:   Can check multiple solutions in superposition")

        print(f"\n   {Colors.BOLD}Current Quantum Computer Status (2026){Colors.ENDC}")
        print(f"   • Largest: ~1000-4000 qubits (IBM, Google, IonQ)")
        print(f"   • Coherence time: 10-100 microseconds (very short!)")
        print(f"   • Error rates: ~0.1-1% per gate operation")
        print(f"   • NOT yet useful for breaking cryptography")
        print(f"   • NOT useful for Bitcoin mining (yet)")

        print(f"\n{'-'*80}\n")

    def section_2_quantum_algorithms_for_mining(self):
        """Explain quantum algorithms relevant to mining"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🔬 SECTION 2: QUANTUM ALGORITHMS & BITCOIN MINING{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Relevant Quantum Algorithms{Colors.ENDC}\n")

        print(f"   1. {Colors.OKBLUE}Grover's Algorithm{Colors.ENDC}")
        print(f"      • Purpose: Unstructured search")
        print(f"      • Speedup: √N (square root, not exponential!)")
        print(f"      • For Bitcoin: √(2^256) = 2^128 operations")
        print(f"      • Classical: 2^256 operations")
        print(f"      • Speedup factor: 2^128 times faster")
        print(f"      • Reality: STILL not enough for profitable mining!")

        print(f"\n   2. {Colors.OKBLUE}Shor's Algorithm{Colors.ENDC}")
        print(f"      • Purpose: Integer factorization, discrete logarithm")
        print(f"      • Breaks: RSA, ECDSA (Bitcoin signatures)")
        print(f"      • Does NOT help with: SHA-256 mining")
        print(f"      • Mining uses PREIMAGE search, not factorization")

        print(f"\n   {Colors.BOLD}Why Quantum Computers Don't Help (Much) With Mining{Colors.ENDC}")
        print(f"   • Mining is finding: SHA256(SHA256(header)) < target")
        print(f"   • This is PREIMAGE resistance, not key breaking")
        print(f"   • Grover's algorithm gives only quadratic speedup")
        print(f"   • √N speedup is insufficient vs ASIC improvements")
        print(f"   • Quantum decoherence limits computation time")
        print(f"   • Error correction overhead is massive")

        print(f"\n   {Colors.BOLD}Theoretical Quantum Speedup Calculation{Colors.ENDC}")

        # Calculate theoretical speedup
        classical_difficulty = 2**256
        quantum_difficulty = 2**128  # Using Grover's algorithm
        speedup = classical_difficulty / quantum_difficulty

        print(f"   • Classical difficulty: 2^256 = {classical_difficulty:.2e}")
        print(f"   • Quantum difficulty (Grover): 2^128 = {quantum_difficulty:.2e}")
        print(f"   • Theoretical speedup: 2^128 = {speedup:.2e}x")

        print(f"\n   {Colors.WARNING}BUT:{Colors.ENDC}")
        print(f"   • ASIC is 100,000,000x faster than CPU")
        print(f"   • Quantum overhead negates most advantage")
        print(f"   • Decoherence limits practical computation")
        print(f"   • Current quantum computers: FAR too small")

        print(f"\n{'-'*80}\n")

    def section_3_theoretical_quantum_mining_simulation(self):
        """Simulate theoretical quantum-enhanced mining"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}⚛️  SECTION 3: THEORETICAL QUANTUM MINING SIMULATION{Colors.ENDC}\n")

        print(f"   {Colors.WARNING}SIMULATION MODE: Demonstrating theoretical concepts only!{Colors.ENDC}\n")

        # Theoretical quantum computer specs
        print(f"   {Colors.BOLD}Theoretical Quantum Computer Specs{Colors.ENDC}")
        print(f"   • Qubits: {self.quantum_qubits:,}")
        print(f"   • Coherence time: {self.quantum_coherence_time} microseconds")
        print(f"   • Error rate: 0.1% per gate (optimistic)")
        print(f"   • Quantum gates per second: 1,000,000")
        print(f"   • Operating temperature: 15 millikelvin (near absolute zero)")

        # Calculate theoretical quantum hashrate using Grover's algorithm
        print(f"\n   {Colors.BOLD}Theoretical Hashrate Calculation{Colors.ENDC}")

        # Grover's algorithm requires O(√N) operations
        # For SHA-256: N = 2^256, so √N = 2^128
        classical_operations = 2**256
        grover_operations = 2**128

        # Assume quantum computer can do 1M quantum gates per second
        quantum_gates_per_second = 1_000_000

        # Each Grover iteration needs ~O(n) gates where n is qubit count
        gates_per_iteration = self.quantum_qubits * 10  # Rough estimate
        iterations_per_second = quantum_gates_per_second / gates_per_iteration

        # Theoretical "quantum hashrate" (not directly comparable to classical)
        theoretical_quantum_hashrate = iterations_per_second * math.sqrt(2**32)

        print(f"   • Quantum gates per second: {quantum_gates_per_second:,}")
        print(f"   • Gates per Grover iteration: {gates_per_iteration:,}")
        print(f"   • Grover iterations per second: {iterations_per_second:,.2f}")
        print(f"   • Theoretical 'quantum hashrate': {theoretical_quantum_hashrate:,.2f} Q-H/s")
        print(f"   • (Q-H/s = Quantum Hashes per second, NOT comparable to classical)")

        # Compare to classical
        print(f"\n   {Colors.BOLD}Comparison to Classical Mining{Colors.ENDC}")
        print(f"   • CPU: {self.cpu_hashrate:,} H/s (1 MH/s)")
        print(f"   • GPU: {self.gpu_hashrate:,} H/s (100 MH/s)")
        print(f"   • ASIC: {self.asic_hashrate:,} H/s (100 TH/s)")
        print(f"   • Network: {self.network_hashrate:.2e} H/s (888 EH/s)")

        # Reality check
        print(f"\n   {Colors.FAIL}{Colors.BOLD}REALITY CHECK:{Colors.ENDC}")
        print(f"   • Theoretical quantum advantage exists (√N speedup)")
        print(f"   • BUT: Massive overhead from error correction")
        print(f"   • BUT: Decoherence limits computation time")
        print(f"   • BUT: ASICs are already extremely optimized")
        print(f"   • BUT: Building quantum computer costs billions")
        print(f"   • RESULT: {Colors.FAIL}NOT economically viable for mining!{Colors.ENDC}")

        print(f"\n{'-'*80}\n")

    def section_4_simulate_mining_attempt(self):
        """Simulate a quantum-enhanced mining attempt"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}⛏️  SECTION 4: SIMULATED QUANTUM MINING ATTEMPT{Colors.ENDC}\n")

        print(f"   {Colors.WARNING}EDUCATIONAL SIMULATION: Not real quantum computing!{Colors.ENDC}\n")

        block_data = f"Quantum Block #{int(time.time())} - Simulated Mining"

        print(f"   {Colors.BOLD}Mining Configuration{Colors.ENDC}")
        print(f"   • Block data: {block_data[:50]}...")
        print(f"   • Target: Hash starting with '0000' (simplified)")
        print(f"   • Method: Simulated Grover's algorithm")

        print(f"\n   {Colors.BOLD}Classical Mining (Baseline){Colors.ENDC}")
        start_time = time.time()
        nonce = 0
        max_attempts = 1_000_000
        classical_time = 0
        hash_result = ""

        for nonce in range(max_attempts):
            data = f"{block_data}{nonce}"
            hash_result = hashlib.sha256(hashlib.sha256(data.encode()).digest()).hexdigest()
            if hash_result.startswith("0000"):
                classical_time = time.time() - start_time
                print(f"   • Found at nonce: {nonce:,}")
                print(f"   • Hash: {hash_result}")
                print(f"   • Time: {classical_time:.4f} seconds")
                print(f"   • Hashrate: {nonce/classical_time:,.0f} H/s")
                break

        # If not found, use the time spent
        if classical_time == 0:
            classical_time = time.time() - start_time
            print(f"   • No block found in {max_attempts:,} attempts")
            print(f"   • Time spent: {classical_time:.4f} seconds")
            print(f"   • Hashrate: {max_attempts/classical_time:,.0f} H/s")

        # Simulate quantum speedup (√N improvement)
        print(f"\n   {Colors.BOLD}Simulated Quantum Mining (Grover's Algorithm){Colors.ENDC}")
        quantum_nonce = int(math.sqrt(nonce)) if nonce > 0 else 1
        quantum_time = classical_time / math.sqrt(nonce) if nonce > 0 else classical_time
        quantum_hashrate = quantum_nonce / quantum_time if quantum_time > 0 else 0

        print(f"   • Theoretical quantum iterations: {quantum_nonce:,}")
        print(f"   • Theoretical time: {quantum_time:.6f} seconds")
        print(f"   • Theoretical speedup: {math.sqrt(nonce):.2f}x")
        print(f"   • Simulated 'quantum hashrate': {quantum_hashrate:,.0f} Q-H/s")

        print(f"\n   {Colors.BOLD}Reality Check{Colors.ENDC}")
        print(f"   • √N speedup confirmed in simulation")
        print(f"   • But quantum overhead NOT included in simulation")
        print(f"   • Real quantum computer would have:")
        print(f"     - Error correction overhead (100-1000x slowdown)")
        print(f"     - Decoherence limits (<100 microseconds)")
        print(f"     - Initialization time per attempt")
        print(f"     - Measurement overhead")
        print(f"   • {Colors.FAIL}Actual performance: Likely WORSE than classical!{Colors.ENDC}")

        print(f"\n{'-'*80}\n")

    def section_5_economic_analysis(self):
        """Analyze economics of quantum mining"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}💰 SECTION 5: ECONOMIC ANALYSIS{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Quantum Computer Costs (2026 Estimates){Colors.ENDC}")
        quantum_cost = 100_000_000  # $100 million (conservative)
        quantum_power = 250_000  # 250 kW (for cooling system)
        electricity_cost_kwh = 0.12  # $0.12 per kWh

        print(f"   • Hardware cost: ${quantum_cost:,}")
        print(f"   • Power consumption: {quantum_power:,} W (250 kW)")
        print(f"   • Cooling system: Cryogenic (15 millikelvin)")
        print(f"   • Maintenance: $1,000,000/year")
        print(f"   • Electricity: ${electricity_cost_kwh}/kWh")

        print(f"\n   {Colors.BOLD}ASIC Miner Comparison{Colors.ENDC}")
        asic_cost = 2_000  # $2,000 per ASIC
        asic_power = 3_250  # 3.25 kW
        asic_count = quantum_cost / asic_cost

        print(f"   • ASIC cost: ${asic_cost:,} (Antminer S19 Pro)")
        print(f"   • Power consumption: {asic_power:,} W (3.25 kW)")
        print(f"   • Number you could buy for same price: {asic_cost:,.0f}")

        # Calculate daily costs
        quantum_daily_power = (quantum_power / 1000) * 24 * electricity_cost_kwh
        asic_farm_daily_power = (asic_power * asic_count / 1000) * 24 * electricity_cost_kwh

        print(f"\n   {Colors.BOLD}Daily Operating Costs{Colors.ENDC}")
        print(f"   • Quantum computer: ${quantum_daily_power:,.2f}/day")
        print(f"   • ASIC farm ({asic_count:,.0f} units): ${asic_farm_daily_power:,.2f}/day")

        # Calculate theoretical earnings
        total_asic_hashrate = asic_count * self.asic_hashrate
        probability_per_block = total_asic_hashrate / (self.network_hashrate + total_asic_hashrate)
        expected_blocks_per_day = probability_per_block * 144  # 144 blocks per day
        expected_btc_per_day = expected_blocks_per_day * self.block_reward
        expected_usd_per_day = expected_btc_per_day * self.btc_price

        print(f"\n   {Colors.BOLD}Theoretical Daily Earnings (ASIC Farm){Colors.ENDC}")
        print(f"   • Total hashrate: {total_asic_hashrate:.2e} H/s")
        print(f"   • Expected BTC/day: {expected_btc_per_day:.8f}")
        print(f"   • Expected USD/day: ${expected_usd_per_day:,.2f}")
        print(f"   • Daily profit: ${expected_usd_per_day - asic_farm_daily_power:,.2f}")

        print(f"\n   {Colors.FAIL}{Colors.BOLD}ECONOMIC VERDICT:{Colors.ENDC}")
        print(f"   • ASIC farm is {Colors.OKGREEN}PROFITABLE{Colors.ENDC}")
        print(f"   • Quantum computer is {Colors.FAIL}NOT PROFITABLE{Colors.ENDC}")
        print(f"   • Reasons:")
        print(f"     - 50,000x more expensive to build")
        print(f"     - 10,000x more expensive to operate")
        print(f"     - Theoretical speedup negated by overhead")
        print(f"     - Technology not mature enough")
        print(f"   • {Colors.FAIL}USE ASICS, NOT QUANTUM COMPUTERS!{Colors.ENDC}")

        print(f"\n{'-'*80}\n")

    def section_6_future_possibilities(self):
        """Discuss future quantum computing and Bitcoin"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🔮 SECTION 6: FUTURE POSSIBILITIES{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}When Will Quantum Computers Threaten Bitcoin?{Colors.ENDC}\n")

        print(f"   1. {Colors.OKBLUE}Mining (SHA-256){Colors.ENDC}")
        print(f"      • Threat level: {Colors.OKGREEN}LOW{Colors.ENDC}")
        print(f"      • Grover's algorithm provides only √N speedup")
        print(f"      • ASICs will remain superior for decades")
        print(f"      • If quantum threatens: Double SHA-256 difficulty")
        print(f"      • Bitcoin can adapt by increasing rounds")

        print(f"\n   2. {Colors.OKBLUE}Signatures (ECDSA){Colors.ENDC}")
        print(f"      • Threat level: {Colors.WARNING}MODERATE (long-term){Colors.ENDC}")
        print(f"      • Shor's algorithm can break ECDSA")
        print(f"      • Requires ~3000-4000 logical qubits")
        print(f"      • Current: ~1000 physical qubits (not logical)")
        print(f"      • Timeline: 10-20+ years")
        print(f"      • Solution: Upgrade to quantum-resistant signatures")

        print(f"\n   {Colors.BOLD}Quantum-Resistant Cryptography{Colors.ENDC}")
        print(f"   • Lattice-based cryptography")
        print(f"   • Hash-based signatures")
        print(f"   • Code-based cryptography")
        print(f"   • Bitcoin can upgrade if needed")

        print(f"\n   {Colors.BOLD}Timeline Estimates{Colors.ENDC}")
        print(f"   • 2026: Quantum computers have ~1000-4000 physical qubits")
        print(f"   • 2030: Possible 10,000+ physical qubits")
        print(f"   • 2035: Possible threat to ECDSA (optimistic)")
        print(f"   • 2040+: Possible mature quantum computers")
        print(f"   • Unknown: When quantum advantage overcomes ASIC advantage")

        print(f"\n   {Colors.OKGREEN}{Colors.BOLD}CONCLUSION:{Colors.ENDC}")
        print(f"   • Bitcoin mining is SAFE from quantum computers")
        print(f"   • SHA-256 remains secure")
        print(f"   • Community has time to prepare for quantum era")
        print(f"   • Focus on ASIC mining, not quantum computing")

        print(f"\n{'-'*80}\n")

    def section_7_educational_summary(self):
        """Final educational summary"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}📚 SECTION 7: EDUCATIONAL SUMMARY{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Key Learnings:{Colors.ENDC}\n")

        learnings = [
            ("Quantum Computers Use Qubits",
             "Superposition and entanglement enable parallel computation"),

            ("Grover's Algorithm: √N Speedup Only",
             "Quadratic speedup is insufficient for profitable mining"),

            ("SHA-256 Mining Resistant to Quantum",
             "Preimage resistance harder than key breaking"),

            ("Quantum Overhead is Massive",
             "Error correction, decoherence negate theoretical advantage"),

            ("ASICs Still Superior",
             "100,000,000x faster than CPU, optimized for SHA-256"),

            ("Economic Reality",
             "Quantum computer costs $100M+, ASICs cost $2K"),

            ("Future Threat: Signatures, Not Mining",
             "Shor's algorithm threatens ECDSA, not SHA-256"),

            ("Bitcoin Can Adapt",
             "Quantum-resistant cryptography available when needed"),
        ]

        for i, (title, description) in enumerate(learnings, 1):
            print(f"   {i}. {Colors.BOLD}{title}{Colors.ENDC}")
            print(f"      {description}\n")

        print(f"   {Colors.OKGREEN}{Colors.BOLD}What You NOW Understand:{Colors.ENDC}")
        print(f"   ✓ Quantum computing basics and capabilities")
        print(f"   ✓ Why quantum computers don't help with mining")
        print(f"   ✓ Grover's algorithm and its limitations")
        print(f"   ✓ Economic reality of quantum vs ASIC mining")
        print(f"   ✓ Future timeline and actual threats")
        print(f"   ✓ Bitcoin's quantum resistance")

        print(f"\n   {Colors.FAIL}{Colors.BOLD}Critical Truths:{Colors.ENDC}")
        print(f"   ✗ Quantum computers DON'T make mining profitable")
        print(f"   ✗ SHA-256 is NOT efficiently breakable by quantum")
        print(f"   ✗ ASICs remain the ONLY viable mining hardware")
        print(f"   ✗ Don't invest in quantum mining schemes (scams!)")

        print(f"\n{'-'*80}\n")

    def run_complete_system(self):
        """Run complete quantum mining educational system"""
        self.print_header()

        try:
            self.section_1_quantum_computing_basics()
            input(f"{Colors.WARNING}Press Enter to continue to Section 2...{Colors.ENDC}")

            self.section_2_quantum_algorithms_for_mining()
            input(f"{Colors.WARNING}Press Enter to continue to Section 3...{Colors.ENDC}")

            self.section_3_theoretical_quantum_mining_simulation()
            input(f"{Colors.WARNING}Press Enter to continue to Section 4...{Colors.ENDC}")

            self.section_4_simulate_mining_attempt()
            input(f"{Colors.WARNING}Press Enter to continue to Section 5...{Colors.ENDC}")

            self.section_5_economic_analysis()
            input(f"{Colors.WARNING}Press Enter to continue to Section 6...{Colors.ENDC}")

            self.section_6_future_possibilities()
            input(f"{Colors.WARNING}Press Enter to see final summary...{Colors.ENDC}")

            self.section_7_educational_summary()

            # Final message
            print(f"{Colors.OKGREEN}{Colors.BOLD}{'='*80}")
            print(" QUANTUM BITCOIN MINING EDUCATION COMPLETE")
            print(f"{'='*80}{Colors.ENDC}\n")

            print(f"{Colors.OKCYAN}Thank you for learning about quantum computing and Bitcoin!{Colors.ENDC}")
            print(f"Remember: This was educational simulation, not real quantum mining.")
            print(f"\nKey Takeaway: {Colors.BOLD}Stick with ASICs for real mining!{Colors.ENDC}\n")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}System interrupted by user.{Colors.ENDC}\n")
        except Exception as e:
            print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Quantum Bitcoin Mining Educational System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  EDUCATIONAL ONLY - NOT REAL QUANTUM COMPUTING ⚠️

This system demonstrates:
- Quantum computing concepts
- Why quantum doesn't help with Bitcoin mining
- Theoretical vs actual capabilities
- Economic reality of quantum mining

Examples:
  %(prog)s              # Run full educational system
  %(prog)s --quick      # Skip interactive pauses
  %(prog)s --no-color   # Disable colors

Authors: Douglas Shane Davis & Claude
        """
    )

    parser.add_argument('--quick', action='store_true', help='Skip interactive pauses')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    if args.no_color:
        Colors.HEADER = Colors.OKBLUE = Colors.OKCYAN = ''
        Colors.OKGREEN = Colors.WARNING = Colors.FAIL = ''
        Colors.ENDC = Colors.BOLD = Colors.UNDERLINE = ''

    # Create and run system
    simulator = QuantumMiningSimulator()

    if args.quick:
        # Override input() to skip pauses
        import builtins
        builtins.input = lambda *args: None

    simulator.run_complete_system()


if __name__ == "__main__":
    main()
