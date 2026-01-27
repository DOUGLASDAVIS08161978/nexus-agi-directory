#!/usr/bin/env python3
"""
================================================================================
MONAD TESTNET FAUCET GUIDE & SIMULATOR
Get testnet MON tokens for testing
================================================================================
"""

import json
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


def load_wallet():
    """Load wallet from .env"""
    import os
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if 'RECEIVING_ADDRESS' in line:
                    return line.split('=')[1].strip()
    return "0x24f6b1ce11c57d40b542f91ac85fa9eb61f78771"


def display_monad_info():
    """Display Monad network information"""
    print(f"\n{'='*80}")
    print(f"{Colors.HEADER}{Colors.BOLD}🌟 MONAD BLOCKCHAIN{Colors.ENDC}")
    print(f"{'='*80}\n")

    print(f"{Colors.BOLD}Network Information:{Colors.ENDC}")
    print(f"  Network Name: {Colors.OKCYAN}Monad Testnet{Colors.ENDC}")
    print(f"  Chain ID: {Colors.OKGREEN}41454{Colors.ENDC}")
    print(f"  Currency: MON")
    print(f"  Type: EVM-Compatible Blockchain")
    print(f"  Focus: High-performance, low-latency transactions\n")


def display_faucets(wallet_address):
    """Display all available Monad faucets"""
    print(f"{'='*80}")
    print(f"{Colors.HEADER}{Colors.BOLD}💧 MONAD TESTNET FAUCETS{Colors.ENDC}")
    print(f"{'='*80}\n")

    print(f"Your Wallet Address:")
    print(f"  {Colors.OKGREEN}{wallet_address}{Colors.ENDC}\n")

    faucets = [
        {
            'name': '1. Alchemy Faucet (Recommended)',
            'url': 'https://www.alchemy.com/faucets/monad-testnet',
            'amount': '0.5 MON',
            'cooldown': '24 hours',
            'requirements': 'None - Just enter your address',
            'instructions': [
                'Visit the URL above',
                'Enter your wallet address',
                'Click "Send Me MON"',
                'Wait for transaction confirmation'
            ]
        },
        {
            'name': '2. Official Monad Faucet',
            'url': 'https://faucet.monad.xyz/',
            'amount': 'Varies',
            'cooldown': '24 hours',
            'requirements': 'Connect wallet',
            'instructions': [
                'Visit faucet.monad.xyz',
                'Connect your Web3 wallet',
                'Click request tokens',
                'Approve transaction'
            ]
        },
        {
            'name': '3. QuickNode Faucet',
            'url': 'https://faucet.quicknode.com/monad/testnet',
            'amount': 'Varies',
            'cooldown': '24 hours',
            'requirements': '0.001 ETH on Ethereum mainnet',
            'instructions': [
                'Visit QuickNode faucet',
                'Connect wallet (must have 0.001 ETH on mainnet)',
                'Request MON tokens',
                'Receive tokens in ~1 minute'
            ]
        },
        {
            'name': '4. Chainstack Faucet',
            'url': 'https://chainstack.com/how-to-get-monad-testnet-tokens/',
            'amount': '0.5 MON',
            'cooldown': '24 hours',
            'requirements': 'Twitter auth (optional)',
            'instructions': [
                'Visit Chainstack',
                'Enter wallet address',
                'Complete captcha',
                'Receive 0.5 MON'
            ]
        }
    ]

    for faucet in faucets:
        print(f"{Colors.BOLD}{faucet['name']}{Colors.ENDC}")
        print(f"  URL: {Colors.OKCYAN}{faucet['url']}{Colors.ENDC}")
        print(f"  Amount: {Colors.OKGREEN}{faucet['amount']}{Colors.ENDC}")
        print(f"  Cooldown: {faucet['cooldown']}")
        print(f"  Requirements: {faucet['requirements']}")
        print(f"\n  {Colors.BOLD}How to use:{Colors.ENDC}")
        for i, step in enumerate(faucet['instructions'], 1):
            print(f"    {i}. {step}")
        print()


def simulate_faucet_claim(wallet_address):
    """Simulate the faucet claiming process"""
    print(f"{'='*80}")
    print(f"{Colors.HEADER}{Colors.BOLD}💧 SIMULATING FAUCET CLAIM{Colors.ENDC}")
    print(f"{'='*80}\n")

    print(f"Simulating claim for wallet: {Colors.OKGREEN}{wallet_address}{Colors.ENDC}\n")

    steps = [
        ("Opening Alchemy Faucet page", 0.5),
        ("Entering wallet address", 0.4),
        ("Verifying address format", 0.3),
        ("Checking cooldown period", 0.5),
        ("Requesting 0.5 MON from faucet", 0.8),
        ("Creating faucet transaction", 1.0),
        ("Broadcasting to Monad testnet", 0.7),
        ("Waiting for confirmation", 1.2),
        ("Transaction confirmed!", 0.5)
    ]

    for step, delay in steps:
        print(f"{Colors.OKCYAN}⏳ {step}...{Colors.ENDC}")
        time.sleep(delay)
        print(f"{Colors.OKGREEN}✓ {step}{Colors.ENDC}\n")

    # Simulate transaction
    import hashlib
    tx_hash = '0x' + hashlib.sha256(f"monad_faucet_{wallet_address}_{time.time()}".encode()).hexdigest()

    print(f"{'='*80}")
    print(f"{Colors.OKGREEN}{Colors.BOLD}✅ FAUCET CLAIM SUCCESSFUL!{Colors.ENDC}")
    print(f"{'='*80}\n")

    result = {
        'success': True,
        'network': 'Monad Testnet',
        'wallet': wallet_address,
        'amount': 0.5,
        'token': 'MON',
        'tx_hash': tx_hash,
        'block': 12345678,
        'timestamp': datetime.now().isoformat(),
        'faucet': 'Alchemy',
        'next_claim': '24 hours'
    }

    print(f"Transaction Details:")
    print(f"  Network: {Colors.OKCYAN}Monad Testnet{Colors.ENDC}")
    print(f"  Amount Received: {Colors.OKGREEN}0.5 MON{Colors.ENDC}")
    print(f"  TX Hash: {tx_hash[:32]}...")
    print(f"  Block: {result['block']:,}")
    print(f"  Status: {Colors.OKGREEN}Confirmed ✓{Colors.ENDC}")
    print(f"\n  Next claim available in: {Colors.WARNING}24 hours{Colors.ENDC}\n")

    return result


def display_test_scenarios():
    """Display test scenarios you can run"""
    print(f"{'='*80}")
    print(f"{Colors.HEADER}{Colors.BOLD}🧪 TEST SCENARIOS WITH MON TOKENS{Colors.ENDC}")
    print(f"{'='*80}\n")

    scenarios = [
        {
            'name': 'Basic Transfer Test',
            'description': 'Send MON between addresses',
            'required_mon': '0.1 MON',
            'steps': [
                'Get 0.5 MON from faucet',
                'Send 0.1 MON to test address',
                'Verify transaction on explorer',
                'Check both wallet balances'
            ]
        },
        {
            'name': 'Smart Contract Deployment',
            'description': 'Deploy WTBTC contract to Monad',
            'required_mon': '0.2 MON',
            'steps': [
                'Compile WTBTC contract',
                'Estimate deployment gas',
                'Deploy to Monad testnet',
                'Verify contract on explorer'
            ]
        },
        {
            'name': 'Token Minting Test',
            'description': 'Mint and transfer tokens',
            'required_mon': '0.15 MON',
            'steps': [
                'Deploy token contract',
                'Mint 1000 tokens',
                'Transfer tokens to another address',
                'Verify balances'
            ]
        },
        {
            'name': 'Multi-chain Bridge Test',
            'description': 'Test bridging to Monad',
            'required_mon': '0.3 MON',
            'steps': [
                'Setup bridge contracts',
                'Lock tokens on source chain',
                'Mint on Monad',
                'Test reverse bridge'
            ]
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"{Colors.BOLD}{i}. {scenario['name']}{Colors.ENDC}")
        print(f"   Description: {scenario['description']}")
        print(f"   Required MON: {Colors.OKGREEN}{scenario['required_mon']}{Colors.ENDC}")
        print(f"   Steps:")
        for j, step in enumerate(scenario['steps'], 1):
            print(f"     {j}. {step}")
        print()


def save_faucet_results(results):
    """Save results to file"""
    with open('monad_faucet_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"{Colors.OKGREEN}📁 Results saved: monad_faucet_results.json{Colors.ENDC}\n")


def main():
    """Main execution"""
    wallet = load_wallet()

    print(f"\n{Colors.WARNING}{'='*80}{Colors.ENDC}")
    print(f"{Colors.WARNING}MONAD TESTNET FAUCET GUIDE{Colors.ENDC}")
    print(f"{Colors.WARNING}{'='*80}{Colors.ENDC}\n")

    time.sleep(1)

    # Display info
    display_monad_info()
    time.sleep(0.5)

    # Display faucets
    display_faucets(wallet)
    time.sleep(0.5)

    # Simulate claim
    result = simulate_faucet_claim(wallet)
    time.sleep(0.5)

    # Display test scenarios
    display_test_scenarios()
    time.sleep(0.5)

    # Save results
    save_faucet_results(result)

    print(f"{'='*80}")
    print(f"{Colors.OKGREEN}{Colors.BOLD}✨ READY FOR MONAD TESTING! ✨{Colors.ENDC}")
    print(f"{'='*80}\n")

    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"  1. Visit one of the faucet URLs above")
    print(f"  2. Enter your wallet: {Colors.OKGREEN}{wallet}{Colors.ENDC}")
    print(f"  3. Claim 0.5 MON tokens")
    print(f"  4. Start testing on Monad testnet!")
    print()


if __name__ == "__main__":
    main()
