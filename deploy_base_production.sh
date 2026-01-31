#!/bin/bash
# WTBTC Deployment for Base Sepolia
# Deployer & Recipient: 0x9fe74d9d6f1ae0ce1fb3b51d4a82c05b74e280f3

pip3 install -q web3 solcx 2>/dev/null; python3 << 'DEPLOY_SCRIPT'
from web3 import Web3
from solcx import compile_source, install_solc
import sys

# Configuration
PRIVATE_KEY = "0x0eee6f45b0af8f5a6a24744a1a978346d5bd66b41c64dc30bd18a32e246515cd"
BASE_RPC = "https://sepolia.base.org"
CHAIN_ID = 84532

print("="*80)
print("🚀 WTBTC DEPLOYMENT TO BASE SEPOLIA")
print("="*80 + "\n")

# Connect to Base Sepolia
w3 = Web3(Web3.HTTPProvider(BASE_RPC))
if not w3.is_connected():
    print("❌ Cannot connect to Base Sepolia")
    sys.exit(1)

account = w3.eth.account.from_key(PRIVATE_KEY)
addr = account.address

print(f"Deployer: {addr}")

# Check balance
balance = w3.eth.get_balance(addr)
balance_eth = w3.from_wei(balance, 'ether')
print(f"Balance: {balance_eth:.6f} ETH\n")

if balance < w3.to_wei(0.001, 'ether'):
    print("⚠️  Need more ETH for deployment")
    print(f"Get testnet ETH: https://www.alchemy.com/faucets/base-sepolia")
    print(f"Send to: {addr}")
    sys.exit(1)

# Solidity contract
source_code = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WTBTC {
    string public constant name = "Wrapped Test BTC";
    string public constant symbol = "WTBTC";
    uint8 public constant decimals = 8;
    uint256 public constant totalSupply = 1000000 * 10**8;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor() {
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }
}
'''

print("Compiling contract...")
try:
    install_solc('0.8.19', show_progress=False)
except:
    pass

compiled = compile_source(source_code, solc_version='0.8.19')
contract_interface = compiled['<stdin>:WTBTC']
bytecode = contract_interface['bin']

print(f"Contract compiled ({len(bytecode)} bytes)\n")

# Deploy
print("Deploying to Base Sepolia...")
tx = {
    'from': addr,
    'nonce': w3.eth.get_transaction_count(addr),
    'gas': 800000,
    'gasPrice': w3.eth.gas_price,
    'data': '0x' + bytecode,
    'chainId': CHAIN_ID
}

signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

print(f"✅ Transaction sent!")
print(f"TX Hash: {tx_hash.hex()}")
print(f"🔍 BaseScan: https://sepolia.basescan.org/tx/{tx_hash.hex()}\n")

print("⏳ Waiting for confirmation (may take 1-2 minutes)...")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)

if receipt['status'] == 1:
    contract_address = receipt['contractAddress']
    gas_used = receipt['gasUsed']

    print("\n" + "="*80)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("="*80)
    print(f"\n📊 Contract Details:")
    print(f"   Address: {contract_address}")
    print(f"   Symbol: WTBTC")
    print(f"   Decimals: 8")
    print(f"   Total Supply: 1,000,000 WTBTC")
    print(f"   Owner: {addr}")
    print(f"   Gas Used: {gas_used:,}")

    print(f"\n🔗 View on BaseScan:")
    print(f"   https://sepolia.basescan.org/address/{contract_address}")

    print(f"\n✅ All 1,000,000 WTBTC minted to: {addr}")
    print(f"\n📝 Contract is deployed and ready to use!")
else:
    print(f"\n❌ Deployment failed")
    print(f"Gas used: {receipt['gasUsed']:,}")
    sys.exit(1)
DEPLOY_SCRIPT
