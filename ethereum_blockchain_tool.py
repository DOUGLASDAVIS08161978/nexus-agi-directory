#!/usr/bin/env python3
"""
================================================================================
ETHEREUM BLOCKCHAIN INTERACTION TOOL
Connect to Ethereum Blockchain and Interact with Smart Contracts
================================================================================

🔗 FEATURES:
- Connect to Ethereum Mainnet/Testnets
- Check wallet balances (ETH and ERC20 tokens)
- Query blocks and transactions
- Interact with smart contracts
- Get gas prices and estimates
- WBTC contract interaction
- Full Web3 integration

Author: Douglas Shane Davis & Claude AI
Version: 1.0 PRODUCTION
================================================================================
"""

import json
import time
import os
import sys
import hashlib
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class EthereumRPCClient:
    """Ethereum RPC Client for blockchain interaction"""

    def __init__(self, rpc_url: str = None):
        self.rpc_url = rpc_url or "https://eth-mainnet.g.alchemy.com/v2/demo"
        self.session = requests.Session()
        self.request_id = 0

    def _make_request(self, method: str, params: List = None) -> Dict:
        """Make JSON-RPC request to Ethereum node"""
        self.request_id += 1

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": self.request_id
        }

        try:
            response = self.session.post(
                self.rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if "error" in result:
                logger.error(f"RPC Error: {result['error']}")
                return None

            return result.get("result")

        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    def get_block_number(self) -> int:
        """Get latest block number"""
        result = self._make_request("eth_blockNumber")
        if result:
            return int(result, 16)
        return 0

    def get_balance(self, address: str) -> float:
        """Get ETH balance for address"""
        result = self._make_request("eth_getBalance", [address, "latest"])
        if result:
            wei = int(result, 16)
            eth = wei / 1e18
            return eth
        return 0.0

    def get_block(self, block_number: int = None) -> Dict:
        """Get block by number"""
        block_param = hex(block_number) if block_number else "latest"
        result = self._make_request("eth_getBlockByNumber", [block_param, False])
        return result

    def get_transaction(self, tx_hash: str) -> Dict:
        """Get transaction by hash"""
        result = self._make_request("eth_getTransactionByHash", [tx_hash])
        return result

    def get_gas_price(self) -> float:
        """Get current gas price in Gwei"""
        result = self._make_request("eth_gasPrice")
        if result:
            wei = int(result, 16)
            gwei = wei / 1e9
            return gwei
        return 0.0

    def call_contract(self, to_address: str, data: str) -> str:
        """Call smart contract function"""
        params = {
            "to": to_address,
            "data": data
        }
        result = self._make_request("eth_call", [params, "latest"])
        return result


class EthereumBlockchainTool:
    """Complete Ethereum Blockchain Interaction Tool"""

    def __init__(self):
        self.client = None
        self.config = self.load_config()
        self.wbtc_contract = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"

    def load_config(self) -> Dict:
        """Load configuration from .env file"""
        config = {}
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        return config

    def connect(self, network: str = "mainnet") -> bool:
        """Connect to Ethereum network"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}🔗 CONNECTING TO ETHEREUM BLOCKCHAIN{Colors.ENDC}")
        print(f"{'='*80}\n")

        # Network RPC endpoints with fallbacks
        networks = {
            "mainnet": [
                "https://cloudflare-eth.com",
                "https://ethereum.publicnode.com",
                "https://rpc.ankr.com/eth",
                "https://eth-mainnet.g.alchemy.com/v2/demo"
            ],
            "sepolia": [
                "https://ethereum-sepolia.publicnode.com",
                "https://rpc.sepolia.org",
                "https://eth-sepolia.g.alchemy.com/v2/demo"
            ],
            "goerli": [
                "https://ethereum-goerli.publicnode.com",
                "https://rpc.ankr.com/eth_goerli",
                "https://eth-goerli.g.alchemy.com/v2/demo"
            ]
        }

        rpc_urls = networks.get(network, networks["mainnet"])

        logger.info(f"   Network: {Colors.OKCYAN}{network.upper()}{Colors.ENDC}")
        logger.info(f"   Trying {len(rpc_urls)} RPC endpoints...")

        time.sleep(0.3)

        # Try each endpoint until one works
        for i, rpc_url in enumerate(rpc_urls, 1):
            logger.info(f"\n   Attempt {i}/{len(rpc_urls)}: {rpc_url[:50]}...")

            self.client = EthereumRPCClient(rpc_url)

            # Test connection
            block_number = self.client.get_block_number()

            if block_number > 0:
                logger.info(f"{Colors.OKGREEN}✓ Connected successfully!{Colors.ENDC}")
                logger.info(f"{Colors.OKGREEN}✓ Latest block: {block_number:,}{Colors.ENDC}")
                logger.info(f"{Colors.OKGREEN}✓ RPC: {rpc_url}{Colors.ENDC}\n")
                return True
            else:
                logger.warning(f"{Colors.WARNING}✗ Connection failed, trying next...{Colors.ENDC}")

        logger.error(f"\n{Colors.FAIL}✗ All connection attempts failed{Colors.ENDC}\n")
        return False

    def get_network_info(self) -> Dict:
        """Get current network information"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}📊 NETWORK INFORMATION{Colors.ENDC}")
        print(f"{'='*80}\n")

        if not self.client:
            logger.error(f"{Colors.FAIL}Not connected to network{Colors.ENDC}")
            return {}

        block_number = self.client.get_block_number()
        gas_price = self.client.get_gas_price()
        block_data = self.client.get_block()

        info = {
            'block_number': block_number,
            'gas_price_gwei': round(gas_price, 2),
            'timestamp': datetime.now().isoformat()
        }

        if block_data:
            info['block_hash'] = block_data.get('hash', 'N/A')
            info['transactions'] = len(block_data.get('transactions', []))

        logger.info(f"   Latest Block: {Colors.OKGREEN}{info['block_number']:,}{Colors.ENDC}")
        logger.info(f"   Gas Price: {Colors.OKGREEN}{info['gas_price_gwei']} Gwei{Colors.ENDC}")
        logger.info(f"   Block Hash: {info.get('block_hash', 'N/A')[:32]}...")
        logger.info(f"   Transactions: {info.get('transactions', 0)}")

        print(f"\n{Colors.OKGREEN}✓ Network info retrieved{Colors.ENDC}\n")

        return info

    def check_wallet_balance(self, address: str) -> Dict:
        """Check ETH balance for wallet"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}💰 CHECKING WALLET BALANCE{Colors.ENDC}")
        print(f"{'='*80}\n")

        if not self.client:
            logger.error(f"{Colors.FAIL}Not connected to network{Colors.ENDC}")
            return {}

        logger.info(f"   Address: {Colors.OKCYAN}{address}{Colors.ENDC}")

        time.sleep(0.5)

        balance_eth = self.client.get_balance(address)

        balance_info = {
            'address': address,
            'balance_eth': balance_eth,
            'balance_wei': int(balance_eth * 1e18),
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"\n{Colors.OKGREEN}✓ Balance: {balance_eth:.6f} ETH{Colors.ENDC}")
        logger.info(f"{Colors.OKGREEN}✓ Wei: {balance_info['balance_wei']:,}{Colors.ENDC}\n")

        return balance_info

    def check_wbtc_balance(self, wallet_address: str) -> Dict:
        """Check WBTC token balance"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}🪙  CHECKING WBTC BALANCE{Colors.ENDC}")
        print(f"{'='*80}\n")

        if not self.client:
            logger.error(f"{Colors.FAIL}Not connected to network{Colors.ENDC}")
            return {}

        logger.info(f"   Wallet: {Colors.OKCYAN}{wallet_address}{Colors.ENDC}")
        logger.info(f"   WBTC Contract: {Colors.OKCYAN}{self.wbtc_contract}{Colors.ENDC}")

        # ERC20 balanceOf function signature
        # balanceOf(address) = 0x70a08231
        function_sig = "0x70a08231"
        # Pad address to 32 bytes
        padded_address = wallet_address[2:].zfill(64)
        data = function_sig + padded_address

        time.sleep(0.5)

        result = self.client.call_contract(self.wbtc_contract, data)

        wbtc_balance = 0.0
        if result:
            # WBTC has 8 decimals
            balance_raw = int(result, 16)
            wbtc_balance = balance_raw / 1e8

        balance_info = {
            'wallet': wallet_address,
            'contract': self.wbtc_contract,
            'balance_wbtc': wbtc_balance,
            'balance_satoshis': int(wbtc_balance * 1e8),
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"\n{Colors.OKGREEN}✓ WBTC Balance: {wbtc_balance:.8f} WBTC{Colors.ENDC}")
        logger.info(f"{Colors.OKGREEN}✓ Satoshis: {balance_info['balance_satoshis']:,}{Colors.ENDC}\n")

        return balance_info

    def get_block_info(self, block_number: int = None) -> Dict:
        """Get detailed block information"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}🔲 BLOCK INFORMATION{Colors.ENDC}")
        print(f"{'='*80}\n")

        if not self.client:
            logger.error(f"{Colors.FAIL}Not connected to network{Colors.ENDC}")
            return {}

        block_data = self.client.get_block(block_number)

        if not block_data:
            logger.error(f"{Colors.FAIL}Failed to retrieve block{Colors.ENDC}")
            return {}

        block_info = {
            'number': int(block_data.get('number', '0x0'), 16),
            'hash': block_data.get('hash', 'N/A'),
            'timestamp': int(block_data.get('timestamp', '0x0'), 16),
            'transactions': len(block_data.get('transactions', [])),
            'miner': block_data.get('miner', 'N/A'),
            'gas_used': int(block_data.get('gasUsed', '0x0'), 16),
            'gas_limit': int(block_data.get('gasLimit', '0x0'), 16)
        }

        block_time = datetime.fromtimestamp(block_info['timestamp'])

        logger.info(f"   Block Number: {Colors.OKGREEN}{block_info['number']:,}{Colors.ENDC}")
        logger.info(f"   Block Hash: {block_info['hash'][:32]}...")
        logger.info(f"   Timestamp: {block_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"   Transactions: {Colors.OKGREEN}{block_info['transactions']}{Colors.ENDC}")
        logger.info(f"   Miner: {block_info['miner'][:20]}...")
        logger.info(f"   Gas Used: {block_info['gas_used']:,} / {block_info['gas_limit']:,}")

        print(f"\n{Colors.OKGREEN}✓ Block info retrieved{Colors.ENDC}\n")

        return block_info

    def get_transaction_info(self, tx_hash: str) -> Dict:
        """Get transaction information"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}📝 TRANSACTION INFORMATION{Colors.ENDC}")
        print(f"{'='*80}\n")

        if not self.client:
            logger.error(f"{Colors.FAIL}Not connected to network{Colors.ENDC}")
            return {}

        logger.info(f"   TX Hash: {Colors.OKCYAN}{tx_hash[:32]}...{Colors.ENDC}")

        time.sleep(0.5)

        tx_data = self.client.get_transaction(tx_hash)

        if not tx_data:
            logger.error(f"\n{Colors.FAIL}Transaction not found{Colors.ENDC}\n")
            return {}

        tx_info = {
            'hash': tx_data.get('hash', 'N/A'),
            'from': tx_data.get('from', 'N/A'),
            'to': tx_data.get('to', 'N/A'),
            'value': int(tx_data.get('value', '0x0'), 16) / 1e18,
            'gas': int(tx_data.get('gas', '0x0'), 16),
            'gas_price': int(tx_data.get('gasPrice', '0x0'), 16) / 1e9,
            'block_number': int(tx_data.get('blockNumber', '0x0'), 16) if tx_data.get('blockNumber') else 'Pending'
        }

        logger.info(f"\n   From: {Colors.OKCYAN}{tx_info['from']}{Colors.ENDC}")
        logger.info(f"   To: {Colors.OKCYAN}{tx_info['to']}{Colors.ENDC}")
        logger.info(f"   Value: {Colors.OKGREEN}{tx_info['value']:.6f} ETH{Colors.ENDC}")
        logger.info(f"   Gas Price: {tx_info['gas_price']:.2f} Gwei")
        logger.info(f"   Block: {tx_info['block_number']}")

        print(f"\n{Colors.OKGREEN}✓ Transaction info retrieved{Colors.ENDC}\n")

        return tx_info

    def interactive_menu(self):
        """Interactive menu for blockchain interaction"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}ETHEREUM BLOCKCHAIN INTERACTION TOOL{Colors.ENDC}")
        print(f"{'='*80}\n")

        while True:
            print(f"\n{Colors.BOLD}Available Commands:{Colors.ENDC}")
            print(f"  1. Connect to Network")
            print(f"  2. Get Network Info")
            print(f"  3. Check ETH Balance")
            print(f"  4. Check WBTC Balance")
            print(f"  5. Get Block Info")
            print(f"  6. Get Transaction Info")
            print(f"  7. Run Full Test Suite")
            print(f"  8. Exit")

            choice = input(f"\n{Colors.OKCYAN}Enter choice (1-8): {Colors.ENDC}").strip()

            if choice == "1":
                network = input(f"{Colors.OKCYAN}Enter network (mainnet/sepolia/goerli): {Colors.ENDC}").strip() or "mainnet"
                self.connect(network)

            elif choice == "2":
                self.get_network_info()

            elif choice == "3":
                address = input(f"{Colors.OKCYAN}Enter wallet address: {Colors.ENDC}").strip()
                if address:
                    self.check_wallet_balance(address)

            elif choice == "4":
                address = input(f"{Colors.OKCYAN}Enter wallet address: {Colors.ENDC}").strip()
                if address:
                    self.check_wbtc_balance(address)

            elif choice == "5":
                block_input = input(f"{Colors.OKCYAN}Enter block number (or press Enter for latest): {Colors.ENDC}").strip()
                block_num = int(block_input) if block_input else None
                self.get_block_info(block_num)

            elif choice == "6":
                tx_hash = input(f"{Colors.OKCYAN}Enter transaction hash: {Colors.ENDC}").strip()
                if tx_hash:
                    self.get_transaction_info(tx_hash)

            elif choice == "7":
                self.run_test_suite()

            elif choice == "8":
                print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}\n")
                break

            else:
                print(f"{Colors.FAIL}Invalid choice{Colors.ENDC}")

    def run_test_suite(self):
        """Run complete test suite"""
        print(f"\n{'='*80}")
        print(f"{Colors.HEADER}{Colors.BOLD}🧪 RUNNING FULL TEST SUITE{Colors.ENDC}")
        print(f"{'='*80}\n")

        # Test 1: Connect to mainnet
        print(f"{Colors.BOLD}TEST 1: Connecting to Ethereum Mainnet{Colors.ENDC}")
        success = self.connect("mainnet")

        if not success:
            print(f"{Colors.FAIL}Test suite aborted - connection failed{Colors.ENDC}")
            return

        time.sleep(1)

        # Test 2: Network info
        print(f"{Colors.BOLD}TEST 2: Getting Network Information{Colors.ENDC}")
        self.get_network_info()
        time.sleep(1)

        # Test 3: Check wallet balance
        print(f"{Colors.BOLD}TEST 3: Checking Wallet Balance{Colors.ENDC}")
        test_address = self.config.get('RECEIVING_ADDRESS', '0x24f6b1ce11c57d40b542f91ac85fa9eb61f78771')
        self.check_wallet_balance(test_address)
        time.sleep(1)

        # Test 4: Check WBTC balance
        print(f"{Colors.BOLD}TEST 4: Checking WBTC Token Balance{Colors.ENDC}")
        self.check_wbtc_balance(test_address)
        time.sleep(1)

        # Test 5: Get block info
        print(f"{Colors.BOLD}TEST 5: Getting Block Information{Colors.ENDC}")
        self.get_block_info()
        time.sleep(1)

        # Test 6: Get transaction info (sample WBTC transaction)
        print(f"{Colors.BOLD}TEST 6: Getting Transaction Information{Colors.ENDC}")
        sample_tx = "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060"
        self.get_transaction_info(sample_tx)

        print(f"\n{'='*80}")
        print(f"{Colors.OKGREEN}{Colors.BOLD}✅ ALL TESTS COMPLETED!{Colors.ENDC}")
        print(f"{'='*80}\n")

        # Save results
        results = {
            'test_suite': 'ethereum_blockchain_tool',
            'network': 'mainnet',
            'test_address': test_address,
            'wbtc_contract': self.wbtc_contract,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }

        with open('ethereum_tool_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        print(f"{Colors.OKGREEN}📁 Results saved: ethereum_tool_test_results.json{Colors.ENDC}\n")


def main():
    """Main execution"""
    tool = EthereumBlockchainTool()

    # Check if running with --test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        tool.run_test_suite()
    else:
        tool.interactive_menu()


if __name__ == "__main__":
    main()
