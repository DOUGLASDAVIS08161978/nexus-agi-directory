#!/usr/bin/env python3
"""
================================================================================
NEXUS AGI UNIFIED SYSTEM DEMONSTRATION
Comprehensive demonstration of all Nexus AGI systems
================================================================================

This script demonstrates three advanced systems:
1. Bitcoin Autonomous Mining System
2. Web Automation Suite
3. Quantum Superintelligence Simulation

Author: Douglas Davis
Version: 1.0
================================================================================
"""

import subprocess
import sys
import time
from datetime import datetime


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(title, char="=", width=80):
    print("\n" + char * width)
    print(title.center(width))
    print(char * width + "\n")


def run_system(name, script, args=[], timeout=60):
    """Run a system and capture output"""
    print_header(f"RUNNING: {name}", "=")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ['python3', script] + args,
            capture_output=False,
            text=True,
            timeout=timeout
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n{Colors.OKGREEN}✓ {name} completed successfully{Colors.ENDC}")
            print(f"  Execution time: {elapsed:.2f}s")
            return True
        else:
            print(f"\n{Colors.FAIL}✗ {name} failed with code {result.returncode}{Colors.ENDC}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n{Colors.WARNING}⚠ {name} timed out after {timeout}s{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ {name} error: {e}{Colors.ENDC}")
        return False


def main():
    """Main demonstration function"""
    
    print_header("NEXUS AGI UNIFIED SYSTEM DEMONSTRATION", "=")
    print(f"Demonstration started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis demonstration includes:")
    print("  1. Bitcoin Autonomous Mining System (simulation mode)")
    print("  2. Nexus AGI Web Automation Suite")
    print("  3. Quantum Superintelligence Simulation")
    print("\nTotal estimated time: 2-3 minutes")
    print("=" * 80)
    
    input("\nPress Enter to begin demonstration...")
    
    results = {}
    
    # System 1: Bitcoin Autonomous Mining
    print("\n\n")
    results['bitcoin'] = run_system(
        "Bitcoin Autonomous Mining System",
        "bitcoin_autonomous_mining_system.py",
        ['--simulate', '--blocks', '2'],
        timeout=60
    )
    
    time.sleep(2)
    
    # System 2: Web Automation
    print("\n\n")
    results['web'] = run_system(
        "Web Automation Suite",
        "nexus_web_automation_suite.py",
        [],
        timeout=60
    )
    
    time.sleep(2)
    
    # System 3: Quantum Superintelligence
    print("\n\n")
    results['quantum'] = run_system(
        "Quantum Superintelligence",
        "nexus_quantum_superintelligence.py",
        [],
        timeout=120
    )
    
    # Final Summary
    print_header("DEMONSTRATION COMPLETE", "=")
    
    print("System Results:")
    print("-" * 80)
    
    for system, success in results.items():
        status = f"{Colors.OKGREEN}✓ PASSED{Colors.ENDC}" if success else f"{Colors.FAIL}✗ FAILED{Colors.ENDC}"
        print(f"  {system.upper():30s} {status}")
    
    print("-" * 80)
    
    total_passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nTotal: {total_passed}/{total} systems completed successfully")
    print(f"Success Rate: {total_passed/total*100:.1f}%")
    
    print(f"\nDemonstration ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 80)
    print("Thank you for exploring Nexus AGI Systems!")
    print("=" * 80 + "\n")
    
    print(f"{Colors.OKCYAN}Next Steps:{Colors.ENDC}")
    print("  • Read NEXUS_SYSTEMS_README.md for detailed documentation")
    print("  • Explore individual scripts for specific use cases")
    print("  • Modify and extend systems for your needs")
    print("  • Contribute improvements to the project")
    print("\n" + "=" * 80 + "\n")
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠ Demonstration interrupted by user{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}✗ Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
