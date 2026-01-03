#!/usr/bin/env python3
"""
Bitcoin Testnet Toolkit - Complete Command Center
All-in-one tool for Bitcoin testnet operations

Authors: Douglas Shane Davis & Claude
Purpose: Unified interface for all Bitcoin testnet tools
"""

import subprocess
import sys

class BitcoinToolkit:
    """Unified Bitcoin toolkit interface"""

    def __init__(self):
        self.tools = {
            '1': {
                'name': 'Bitcoin Testnet System',
                'desc': 'Complete learning system with wallet, addresses, transactions',
                'cmd': 'python3 bitcoin_testnet_system.py'
            },
            '2': {
                'name': 'Bitcoin Demo Mode',
                'desc': 'Educational demonstration (no Bitcoin Core needed)',
                'cmd': 'python3 bitcoin_testnet_demo.py'
            },
            '3': {
                'name': 'Mock RPC Server',
                'desc': 'Simulate Bitcoin Core for testing',
                'cmd': 'python3 bitcoin_mock_server.py'
            },
            '4': {
                'name': 'Mine Testnet Coins',
                'desc': 'Automated testnet mining tool',
                'cmd': 'python3 mine_testnet_coins.py'
            },
            '5': {
                'name': 'Check Address Balance',
                'desc': 'Check any Bitcoin address balance',
                'cmd': 'python3 check_balance.py'
            },
            '6': {
                'name': 'Track Transaction',
                'desc': 'Track transaction by TXID',
                'cmd': 'python3 track_transaction.py'
            },
            '7': {
                'name': 'Network Analysis Tool',
                'desc': 'Analyze Lightning nodes, addresses, transactions',
                'cmd': 'python3 bitcoin_network_tool.py'
            },
            '8': {
                'name': 'Analyze Mining Results',
                'desc': 'Analyze proof-of-work mining results',
                'cmd': 'python3 analyze_mining.py'
            },
            '9': {
                'name': 'Create Offline Package',
                'desc': 'Build offline Bitcoin Core installation package',
                'cmd': 'python3 create_offline_package.py'
            }
        }

    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*80)
        print(" ⛓️  BITCOIN TESTNET TOOLKIT - COMMAND CENTER")
        print("="*80)
        print("\n📚 Available Tools:\n")

        for key in sorted(self.tools.keys()):
            tool = self.tools[key]
            print(f"  {key}. {tool['name']}")
            print(f"     {tool['desc']}")
            print()

        print("  0. Exit")
        print("\n" + "="*80)

    def run_tool(self, choice: str):
        """Run selected tool"""
        if choice == '0':
            print("\n👋 Goodbye!\n")
            return False

        if choice not in self.tools:
            print("\n❌ Invalid choice\n")
            return True

        tool = self.tools[choice]
        print(f"\n{'='*80}")
        print(f" 🚀 Running: {tool['name']}")
        print(f"{'='*80}\n")

        # For tools that need parameters
        if choice == '4':  # Mining
            blocks = input("Number of blocks to mine (default 10): ") or "10"
            cmd = f"{tool['cmd']} {blocks}"
        elif choice == '5':  # Balance check
            addr = input("Bitcoin address: ")
            if not addr:
                print("❌ Address required")
                return True
            cmd = f"{tool['cmd']} {addr}"
        elif choice == '6':  # Track transaction
            txid = input("Transaction ID: ")
            if not txid:
                print("❌ TXID required")
                return True
            cmd = f"{tool['cmd']} {txid}"
        elif choice == '7':  # Network tool
            data = input("Data to analyze (address/txid/node): ")
            if not data:
                print("❌ Data required")
                return True
            cmd = f"{tool['cmd']} {data}"
        elif choice == '8':  # Mining analysis
            print("Enter JSON mining result (or press Ctrl+C to cancel):")
            json_data = input()
            if not json_data:
                print("❌ JSON required")
                return True
            cmd = f"{tool['cmd']} '{json_data}'"
        else:
            cmd = tool['cmd']

        try:
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            print("\n\n⏹️  Tool stopped\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

        input("\nPress Enter to continue...")
        return True

    def show_quick_commands(self):
        """Show quick reference commands"""
        print("\n" + "="*80)
        print(" 📖 QUICK REFERENCE")
        print("="*80)
        print("\n🚀 Quick Commands:\n")

        print("Start mock server:")
        print("  python3 bitcoin_mock_server.py &\n")

        print("Run main system:")
        print("  python3 bitcoin_testnet_system.py\n")

        print("Mine 10 blocks:")
        print("  python3 mine_testnet_coins.py 10\n")

        print("Check balance:")
        print("  python3 check_balance.py <address>\n")

        print("Track transaction:")
        print("  python3 track_transaction.py <txid>\n")

        print("="*80 + "\n")

    def run(self):
        """Run toolkit"""
        while True:
            self.show_menu()
            choice = input("Select tool (0-9): ").strip()

            if not self.run_tool(choice):
                break


def main():
    """Main execution"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        toolkit = BitcoinToolkit()
        toolkit.show_quick_commands()
        return

    print("\n" + "="*80)
    print(" ⛓️  BITCOIN TESTNET TOOLKIT")
    print("="*80)
    print("\n Complete Bitcoin education and development toolkit")
    print(" All tools integrated in one interface")
    print("\n Testnet coins have NO VALUE - safe for learning!")
    print("\n" + "="*80)

    toolkit = BitcoinToolkit()
    toolkit.run()


if __name__ == "__main__":
    main()
