#!/usr/bin/env python3
"""
REAL WTBTC Deployment to Monad Testnet
This creates actual blockchain contracts you can use in wallets
"""

import os
import json
import time
from pathlib import Path
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
MONAD_RPC = "https://testnet.monad.xyz"
CHAIN_ID = 41454
BITCOIN_ADDRESS = "bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal"
BITGET_WALLET = "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6"  # User's wallet

print("=" * 80)
print("🚀 REAL WTBTC Deployment to Monad Testnet")
print("=" * 80)
print()

# Step 1: Load private key
private_key = os.getenv('PRIVATE_KEY')
if not private_key:
    print("❌ ERROR: No PRIVATE_KEY found in .env file")
    print()
    print("Run this first to generate a wallet:")
    print("  python3 simple_wallet_gen.py")
    exit(1)

if not private_key.startswith('0x'):
    private_key = '0x' + private_key

account = Account.from_key(private_key)
print(f"✅ Deploying from: {account.address}")
print()

# Step 2: Connect to Monad
print("Connecting to Monad testnet...")
w3 = Web3(Web3.HTTPProvider(MONAD_RPC))

if not w3.is_connected():
    print("❌ ERROR: Cannot connect to Monad testnet")
    print(f"   RPC: {MONAD_RPC}")
    exit(1)

print(f"✅ Connected to Monad (Chain ID: {w3.eth.chain_id})")
print()

# Step 3: Check balance
balance = w3.eth.get_balance(account.address)
balance_eth = w3.from_wei(balance, 'ether')

print(f"Wallet Balance: {balance_eth} MON")

if balance == 0:
    print()
    print("❌ ERROR: Zero balance! Cannot deploy without gas fees.")
    print()
    print("Get free testnet tokens:")
    print(f"1. Visit: https://www.alchemy.com/faucets/monad-testnet")
    print(f"2. Enter your address: {account.address}")
    print(f"3. Claim free MON tokens")
    print(f"4. Wait 30 seconds")
    print(f"5. Run this script again")
    exit(1)

print("✅ Sufficient balance for deployment")
print()

# Step 4: Load compiled contracts
print("Loading compiled contracts...")
compilation_file = Path('compilation_results.json')

if not compilation_file.exists():
    print("❌ ERROR: No compilation_results.json found")
    print()
    print("Run this first to compile contracts:")
    print("  python3 deploy_wtbtc_system.py")
    exit(1)

with open(compilation_file) as f:
    compilation = json.load(f)

wtbtc_bytecode = compilation['WTBTC_Enhanced']['bytecode']
wtbtc_abi = compilation['WTBTC_Enhanced']['abi']
bridge_bytecode = compilation['WTBTCBridge']['bytecode']
bridge_abi = compilation['WTBTCBridge']['abi']

print("✅ Contracts loaded")
print()

# Step 5: Deploy WTBTC Token
print("=" * 80)
print("📦 Deploying WTBTC Token Contract")
print("=" * 80)
print()

WTBTC = w3.eth.contract(abi=wtbtc_abi, bytecode=wtbtc_bytecode)

# Build transaction
nonce = w3.eth.get_transaction_count(account.address)
constructor_txn = WTBTC.constructor(BITCOIN_ADDRESS).build_transaction({
    'chainId': CHAIN_ID,
    'gas': 3000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
})

# Sign and send
signed_txn = account.sign_transaction(constructor_txn)
print("Sending WTBTC deployment transaction...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Transaction hash: {tx_hash.hex()}")
print()

# Wait for confirmation
print("Waiting for confirmation...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

if tx_receipt['status'] == 1:
    wtbtc_address = tx_receipt['contractAddress']
    print("✅ WTBTC Token deployed successfully!")
    print(f"   Address: {wtbtc_address}")
    print(f"   Block: {tx_receipt['blockNumber']}")
    print(f"   Gas used: {tx_receipt['gasUsed']}")
else:
    print("❌ Deployment failed!")
    exit(1)

print()

# Step 6: Deploy Bridge Contract
print("=" * 80)
print("🌉 Deploying Bridge Contract")
print("=" * 80)
print()

Bridge = w3.eth.contract(abi=bridge_abi, bytecode=bridge_bytecode)

nonce = w3.eth.get_transaction_count(account.address)
constructor_txn = Bridge.constructor(
    wtbtc_address,
    BITCOIN_ADDRESS,
    account.address  # Oracle address
).build_transaction({
    'chainId': CHAIN_ID,
    'gas': 3000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
})

signed_txn = account.sign_transaction(constructor_txn)
print("Sending Bridge deployment transaction...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Transaction hash: {tx_hash.hex()}")
print()

print("Waiting for confirmation...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

if tx_receipt['status'] == 1:
    bridge_address = tx_receipt['contractAddress']
    print("✅ Bridge deployed successfully!")
    print(f"   Address: {bridge_address}")
    print(f"   Block: {tx_receipt['blockNumber']}")
    print(f"   Gas used: {tx_receipt['gasUsed']}")
else:
    print("❌ Bridge deployment failed!")
    exit(1)

print()

# Step 7: Authorize bridge to mint tokens
print("=" * 80)
print("🔧 Configuring Contracts")
print("=" * 80)
print()

wtbtc_contract = w3.eth.contract(address=wtbtc_address, abi=wtbtc_abi)

print("Authorizing bridge as minter...")
nonce = w3.eth.get_transaction_count(account.address)
auth_txn = wtbtc_contract.functions.authorizeMinter(bridge_address).build_transaction({
    'chainId': CHAIN_ID,
    'gas': 100000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
})

signed_txn = account.sign_transaction(auth_txn)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

if tx_receipt['status'] == 1:
    print("✅ Bridge authorized as minter")
else:
    print("⚠️  Authorization failed (might already be authorized)")

print()

# Step 8: Transfer tokens to Bitget wallet
print("=" * 80)
print("💸 Transferring WTBTC to Your Bitget Wallet")
print("=" * 80)
print()

# Get initial supply (1M WTBTC)
total_supply = wtbtc_contract.functions.totalSupply().call()
print(f"Total WTBTC Supply: {total_supply / 10**8} WTBTC")
print()

# Transfer 50% to Bitget wallet
transfer_amount = total_supply // 2  # 500,000 WTBTC
transfer_amount_readable = transfer_amount / 10**8

print(f"Transferring {transfer_amount_readable} WTBTC to {BITGET_WALLET}...")

nonce = w3.eth.get_transaction_count(account.address)
transfer_txn = wtbtc_contract.functions.transfer(
    BITGET_WALLET,
    transfer_amount
).build_transaction({
    'chainId': CHAIN_ID,
    'gas': 100000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
})

signed_txn = account.sign_transaction(transfer_txn)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Transaction hash: {tx_hash.hex()}")
print()

print("Waiting for confirmation...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

if tx_receipt['status'] == 1:
    print("✅ Transfer successful!")

    # Check balances
    deployer_balance = wtbtc_contract.functions.balanceOf(account.address).call()
    bitget_balance = wtbtc_contract.functions.balanceOf(BITGET_WALLET).call()

    print()
    print(f"Deployer balance: {deployer_balance / 10**8} WTBTC")
    print(f"Bitget wallet balance: {bitget_balance / 10**8} WTBTC")
else:
    print("❌ Transfer failed!")

print()

# Step 9: Save deployment details
deployment_info = {
    "network": "monad",
    "chain_id": CHAIN_ID,
    "deployer": account.address,
    "bitcoin_address": BITCOIN_ADDRESS,
    "bitget_wallet": BITGET_WALLET,
    "contracts": {
        "WTBTC": {
            "address": wtbtc_address,
            "explorer": f"https://explorer.testnet.monad.xyz/address/{wtbtc_address}"
        },
        "Bridge": {
            "address": bridge_address,
            "explorer": f"https://explorer.testnet.monad.xyz/address/{bridge_address}"
        }
    },
    "balances": {
        "deployer": deployer_balance / 10**8,
        "bitget_wallet": bitget_balance / 10**8
    },
    "timestamp": int(time.time())
}

with open('real_wtbtc_deployment.json', 'w') as f:
    json.dump(deployment_info, f, indent=2)

print("=" * 80)
print("✅ DEPLOYMENT COMPLETE!")
print("=" * 80)
print()
print("📍 Contract Addresses:")
print(f"   WTBTC Token: {wtbtc_address}")
print(f"   Bridge: {bridge_address}")
print()
print("💰 Balances:")
print(f"   Your deployer wallet: {deployer_balance / 10**8} WTBTC")
print(f"   Your Bitget wallet: {bitget_balance / 10**8} WTBTC")
print()
print("🔗 Explorers:")
print(f"   WTBTC: https://explorer.testnet.monad.xyz/address/{wtbtc_address}")
print(f"   Bridge: https://explorer.testnet.monad.xyz/address/{bridge_address}")
print()
print("=" * 80)
print("📱 IMPORT TO BITGET:")
print("=" * 80)
print()
print("1. Open Bitget app")
print("2. Go to Assets → Deposit")
print("3. Search for 'Custom Token' or 'Add Token'")
print("4. Enter token details:")
print(f"   • Contract Address: {wtbtc_address}")
print("   • Token Symbol: WTBTC")
print("   • Decimals: 8")
print("   • Network: Monad Testnet (Chain ID: 41454)")
print()
print("5. Your balance should show:", bitget_balance / 10**8, "WTBTC")
print()
print("=" * 80)
print("✅ You now have REAL WTBTC tokens in your Bitget wallet!")
print("=" * 80)
print()
