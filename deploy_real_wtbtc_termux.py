#!/usr/bin/env python3
"""
REAL WTBTC Deployment to Monad Testnet - Termux Compatible
Uses only requests and eth-account (no web3.py needed)
"""

import os
import json
import time
from pathlib import Path
import requests
from eth_account import Account
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
MONAD_RPC = "https://testnet.monad.xyz"
CHAIN_ID = 41454
BITCOIN_ADDRESS = "bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal"
BITGET_WALLET = "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6"

print("=" * 80)
print("🚀 REAL WTBTC Deployment to Monad Testnet (Termux Edition)")
print("=" * 80)
print()

# Helper function for JSON-RPC calls
def rpc_call(method, params=[]):
    """Make JSON-RPC call to Monad"""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(MONAD_RPC, json=payload, timeout=30)
    result = response.json()
    if "error" in result:
        raise Exception(f"RPC Error: {result['error']}")
    return result.get("result")

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

# Step 2: Check connection
print("Connecting to Monad testnet...")
try:
    chain_id = rpc_call("eth_chainId")
    chain_id_int = int(chain_id, 16)
    if chain_id_int != CHAIN_ID:
        print(f"⚠️  Warning: Chain ID mismatch. Expected {CHAIN_ID}, got {chain_id_int}")
    print(f"✅ Connected to Monad (Chain ID: {chain_id_int})")
except Exception as e:
    print(f"❌ ERROR: Cannot connect to Monad testnet")
    print(f"   {e}")
    exit(1)

print()

# Step 3: Check balance
print("Checking balance...")
balance_hex = rpc_call("eth_getBalance", [account.address, "latest"])
balance = int(balance_hex, 16)
balance_eth = balance / 10**18

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
    print("Compiling contracts now...")

    # Simple compilation using solc if available
    import subprocess
    try:
        result = subprocess.run(['python3', 'deploy_wtbtc_system.py'],
                              capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print("⚠️  Compilation may have issues, but continuing...")
    except:
        print("⚠️  Could not auto-compile. Please run: python3 deploy_wtbtc_system.py")
        exit(1)

# Reload after compilation
if not compilation_file.exists():
    print("❌ Still no compilation file. Exiting.")
    exit(1)

with open(compilation_file) as f:
    compilation = json.load(f)

wtbtc_bytecode = compilation['WTBTC_Enhanced']['bytecode']
wtbtc_abi = compilation['WTBTC_Enhanced']['abi']
bridge_bytecode = compilation['WTBTCBridge']['bytecode']
bridge_abi = compilation['WTBTCBridge']['abi']

print("✅ Contracts loaded")
print()

# Helper to encode constructor parameters
def encode_constructor_params(abi, bytecode, *args):
    """Encode constructor parameters and append to bytecode"""
    # For simple types, we'll do basic ABI encoding
    # This is a simplified version - for production use web3

    # Find constructor in ABI
    constructor = None
    for item in abi:
        if item.get('type') == 'constructor':
            constructor = item
            break

    if not constructor or not constructor.get('inputs'):
        return bytecode

    # Simple encoding for address and string types
    encoded_params = ""
    for i, param in enumerate(constructor['inputs']):
        param_type = param['type']
        value = args[i] if i < len(args) else None

        if param_type == 'address':
            # Encode address (remove 0x, pad to 32 bytes)
            addr = value.replace('0x', '').lower()
            encoded_params += addr.zfill(64)
        elif param_type == 'string':
            # Encode string (simplified)
            str_bytes = value.encode('utf-8').hex()
            offset = hex(32 * len(constructor['inputs']))[2:].zfill(64)
            length = hex(len(value))[2:].zfill(64)
            data = str_bytes.ljust(64, '0')
            encoded_params += offset + length + data

    return bytecode + encoded_params

# Get current nonce
nonce_hex = rpc_call("eth_getTransactionCount", [account.address, "latest"])
nonce = int(nonce_hex, 16)

# Get gas price
gas_price_hex = rpc_call("eth_gasPrice")
gas_price = int(gas_price_hex, 16)

print("=" * 80)
print("📦 Deploying WTBTC Token Contract")
print("=" * 80)
print()

# Prepare WTBTC deployment with constructor parameter
print("Encoding constructor parameters...")
wtbtc_data = encode_constructor_params(wtbtc_abi, wtbtc_bytecode, BITCOIN_ADDRESS)

# Build transaction
wtbtc_tx = {
    'nonce': nonce,
    'gasPrice': gas_price,
    'gas': 3000000,
    'to': '',  # Empty for contract creation
    'value': 0,
    'data': wtbtc_data if wtbtc_data.startswith('0x') else '0x' + wtbtc_data,
    'chainId': CHAIN_ID
}

# Sign transaction
signed_wtbtc = account.sign_transaction(wtbtc_tx)

# Send transaction
print("Sending WTBTC deployment transaction...")
try:
    tx_hash = rpc_call("eth_sendRawTransaction", [signed_wtbtc.rawTransaction.hex()])
    print(f"Transaction hash: {tx_hash}")
except Exception as e:
    print(f"❌ Failed to send transaction: {e}")
    print()
    print("This might be because:")
    print("  - Insufficient gas")
    print("  - Network congestion")
    print("  - Invalid transaction data")
    exit(1)

print()
print("Waiting for confirmation (this may take 1-2 minutes)...")

# Wait for receipt
wtbtc_receipt = None
for attempt in range(60):  # Wait up to 2 minutes
    try:
        receipt = rpc_call("eth_getTransactionReceipt", [tx_hash])
        if receipt:
            wtbtc_receipt = receipt
            break
    except:
        pass
    time.sleep(2)
    if attempt % 5 == 0:
        print(f"  Still waiting... ({attempt * 2}s)")

if not wtbtc_receipt:
    print("❌ Transaction timeout. Check status manually:")
    print(f"   https://explorer.testnet.monad.xyz/tx/{tx_hash}")
    exit(1)

# Check status
status = int(wtbtc_receipt.get('status', '0x0'), 16)
if status != 1:
    print("❌ Deployment failed!")
    print(f"   Explorer: https://explorer.testnet.monad.xyz/tx/{tx_hash}")
    exit(1)

wtbtc_address = wtbtc_receipt['contractAddress']
block_number = int(wtbtc_receipt['blockNumber'], 16)
gas_used = int(wtbtc_receipt['gasUsed'], 16)

print("✅ WTBTC Token deployed successfully!")
print(f"   Address: {wtbtc_address}")
print(f"   Block: {block_number}")
print(f"   Gas used: {gas_used}")
print()

# Step 6: Deploy Bridge Contract
print("=" * 80)
print("🌉 Deploying Bridge Contract")
print("=" * 80)
print()

nonce += 1

print("Encoding bridge constructor parameters...")
bridge_data = encode_constructor_params(
    bridge_abi,
    bridge_bytecode,
    wtbtc_address,
    BITCOIN_ADDRESS,
    account.address  # Oracle address
)

bridge_tx = {
    'nonce': nonce,
    'gasPrice': gas_price,
    'gas': 3000000,
    'to': '',
    'value': 0,
    'data': bridge_data if bridge_data.startswith('0x') else '0x' + bridge_data,
    'chainId': CHAIN_ID
}

signed_bridge = account.sign_transaction(bridge_tx)

print("Sending Bridge deployment transaction...")
try:
    tx_hash = rpc_call("eth_sendRawTransaction", [signed_bridge.rawTransaction.hex()])
    print(f"Transaction hash: {tx_hash}")
except Exception as e:
    print(f"❌ Failed to send transaction: {e}")
    exit(1)

print()
print("Waiting for confirmation...")

bridge_receipt = None
for attempt in range(60):
    try:
        receipt = rpc_call("eth_getTransactionReceipt", [tx_hash])
        if receipt:
            bridge_receipt = receipt
            break
    except:
        pass
    time.sleep(2)
    if attempt % 5 == 0:
        print(f"  Still waiting... ({attempt * 2}s)")

if not bridge_receipt or int(bridge_receipt.get('status', '0x0'), 16) != 1:
    print("❌ Bridge deployment failed!")
    exit(1)

bridge_address = bridge_receipt['contractAddress']
print("✅ Bridge deployed successfully!")
print(f"   Address: {bridge_address}")
print()

# Save deployment info
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
    "note": "Use web3 or MetaMask to interact with contracts (transfer, etc.)",
    "timestamp": int(time.time())
}

with open('real_wtbtc_deployment_termux.json', 'w') as f:
    json.dump(deployment_info, f, indent=2)

print("=" * 80)
print("✅ DEPLOYMENT COMPLETE!")
print("=" * 80)
print()
print("📍 Contract Addresses:")
print(f"   WTBTC Token: {wtbtc_address}")
print(f"   Bridge: {bridge_address}")
print()
print("🔗 Explorers:")
print(f"   WTBTC: https://explorer.testnet.monad.xyz/address/{wtbtc_address}")
print(f"   Bridge: https://explorer.testnet.monad.xyz/address/{bridge_address}")
print()
print("=" * 80)
print("📱 NEXT STEPS:")
print("=" * 80)
print()
print("The contracts are deployed! To transfer WTBTC to your Bitget wallet,")
print("you'll need to use MetaMask or a web3 interface because Termux")
print("can't easily call contract functions without web3.py.")
print()
print("Option 1: Use MetaMask")
print("  1. Import your private key to MetaMask")
print("  2. Add Monad Testnet network")
print("  3. Add WTBTC token:", wtbtc_address)
print("  4. Transfer to Bitget:", BITGET_WALLET)
print()
print("Option 2: Deploy from a computer (not Termux)")
print("  Run: python3 deploy_real_wtbtc.py")
print("  (This will auto-transfer to Bitget)")
print()
print("=" * 80)
print("✅ Contracts are REAL and on the blockchain!")
print("=" * 80)
print()
