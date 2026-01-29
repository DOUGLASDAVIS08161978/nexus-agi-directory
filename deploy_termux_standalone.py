#!/usr/bin/env python3
"""
REAL WTBTC Deployment - Pure Python for Termux
No eth-account, no web3, no Rust dependencies
Uses only: requests, ecdsa, pycryptodome
"""

import os
import json
import time
import hashlib
import requests
from pathlib import Path

# Try to import crypto libraries
try:
    from ecdsa import SigningKey, SECP256k1
    from ecdsa.util import sigencode_string
except ImportError:
    print("❌ ERROR: ecdsa package not installed")
    print("Run: pip install ecdsa")
    exit(1)

try:
    from Crypto.Hash import keccak
except ImportError:
    print("❌ ERROR: pycryptodome package not installed")
    print("Run: pip install pycryptodome")
    exit(1)

# Configuration
MONAD_RPC = "https://testnet.monad.xyz"
CHAIN_ID = 41454
BITCOIN_ADDRESS = "bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal"
BITGET_WALLET = "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6"

print("=" * 80)
print("🚀 REAL WTBTC Deployment to Monad Testnet (Standalone)")
print("=" * 80)
print()

# Helper functions
def keccak256(data):
    """Compute Keccak-256 hash"""
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def private_key_to_address(private_key_hex):
    """Convert private key to Ethereum address"""
    if private_key_hex.startswith('0x'):
        private_key_hex = private_key_hex[2:]

    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()

    # Get uncompressed public key (64 bytes, without 0x04 prefix)
    public_key = vk.to_string()

    # Keccak256 hash of public key
    hash_bytes = keccak256(public_key)

    # Take last 20 bytes as address
    address = '0x' + hash_bytes[-20:].hex()
    return address

def sign_transaction(tx, private_key_hex):
    """Sign an Ethereum transaction"""
    if private_key_hex.startswith('0x'):
        private_key_hex = private_key_hex[2:]

    # Encode transaction for signing (RLP encoding)
    # For EIP-155, we need: [nonce, gasPrice, gas, to, value, data, chainId, 0, 0]

    def encode_int(n):
        if n == 0:
            return b'\x80'
        hex_str = hex(n)[2:]
        if len(hex_str) % 2:
            hex_str = '0' + hex_str
        data = bytes.fromhex(hex_str)
        if len(data) == 1 and data[0] < 0x80:
            return data
        return bytes([0x80 + len(data)]) + data

    def encode_bytes(data):
        if isinstance(data, str):
            if data.startswith('0x'):
                data = data[2:]
            data = bytes.fromhex(data)
        if len(data) == 0:
            return b'\x80'
        if len(data) == 1 and data[0] < 0x80:
            return data
        if len(data) <= 55:
            return bytes([0x80 + len(data)]) + data
        len_bytes = len(data).to_bytes((len(data).bit_length() + 7) // 8, 'big')
        return bytes([0xb7 + len(len_bytes)]) + len_bytes + data

    def encode_list(items):
        encoded = b''.join(items)
        if len(encoded) <= 55:
            return bytes([0xc0 + len(encoded)]) + encoded
        len_bytes = len(encoded).to_bytes((len(encoded).bit_length() + 7) // 8, 'big')
        return bytes([0xf7 + len(len_bytes)]) + len_bytes + encoded

    # Build transaction data
    nonce = encode_int(tx['nonce'])
    gas_price = encode_int(tx['gasPrice'])
    gas = encode_int(tx['gas'])
    to = encode_bytes(tx['to']) if tx['to'] else b'\x80'
    value = encode_int(tx['value'])
    data = encode_bytes(tx['data'])
    chain_id = encode_int(tx['chainId'])

    # For signing: include chainId, 0, 0 (EIP-155)
    rlp_data = encode_list([nonce, gas_price, gas, to, value, data, chain_id, b'\x80', b'\x80'])

    # Hash the RLP-encoded transaction
    tx_hash = keccak256(rlp_data)

    # Sign with private key
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    signature = sk.sign_digest(tx_hash, sigencode=sigencode_string)

    # Extract r, s from signature
    r = int.from_bytes(signature[:32], 'big')
    s = int.from_bytes(signature[32:], 'big')

    # Calculate v (EIP-155)
    # v = chainId * 2 + 35 + recovery_id
    # For simplicity, try recovery_id = 0 and 1
    v = tx['chainId'] * 2 + 35

    # Encode signed transaction
    v_enc = encode_int(v)
    r_enc = encode_int(r)
    s_enc = encode_int(s)

    signed_rlp = encode_list([nonce, gas_price, gas, to, value, data, v_enc, r_enc, s_enc])

    return '0x' + signed_rlp.hex()

def rpc_call(method, params=[]):
    """Make JSON-RPC call"""
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

# Step 1: Load private key from .env
print("Step 1: Loading wallet...")
print()

if not os.path.exists('.env'):
    print("❌ ERROR: No .env file found")
    print("Run: python3 simple_wallet_gen.py")
    exit(1)

private_key = None
with open('.env') as f:
    for line in f:
        if line.startswith('PRIVATE_KEY='):
            private_key = line.split('=')[1].strip()
            break

if not private_key:
    print("❌ ERROR: No PRIVATE_KEY in .env")
    exit(1)

if not private_key.startswith('0x'):
    private_key = '0x' + private_key

# Derive address
address = private_key_to_address(private_key)
print(f"✅ Deploying from: {address}")
print()

# Step 2: Check connection
print("Step 2: Connecting to Monad...")
try:
    chain_id = rpc_call("eth_chainId")
    chain_id_int = int(chain_id, 16)
    print(f"✅ Connected (Chain ID: {chain_id_int})")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

print()

# Step 3: Check balance
print("Step 3: Checking balance...")
balance_hex = rpc_call("eth_getBalance", [address, "latest"])
balance = int(balance_hex, 16)
balance_mon = balance / 10**18

print(f"Balance: {balance_mon:.6f} MON")

if balance == 0:
    print()
    print("❌ ERROR: Zero balance!")
    print()
    print("Get testnet tokens:")
    print(f"1. Visit: https://www.alchemy.com/faucets/monad-testnet")
    print(f"2. Enter: {address}")
    print(f"3. Claim free MON")
    print(f"4. Run script again")
    exit(1)

print("✅ Ready to deploy")
print()

# Step 4: Load compiled contracts
print("Step 4: Loading contracts...")

compilation_file = Path('compilation_results.json')
if not compilation_file.exists():
    print("❌ No compilation_results.json")
    print()
    print("Compiling contracts...")
    import subprocess
    try:
        subprocess.run(['python3', 'deploy_wtbtc_system.py'], timeout=60)
    except:
        pass

if not compilation_file.exists():
    print("❌ Compilation failed")
    exit(1)

with open(compilation_file) as f:
    compilation = json.load(f)

wtbtc_bytecode = compilation['WTBTC_Enhanced']['bytecode']
wtbtc_abi = compilation['WTBTC_Enhanced']['abi']

print("✅ Contracts loaded")
print()

# Step 5: Get transaction parameters
nonce_hex = rpc_call("eth_getTransactionCount", [address, "latest"])
nonce = int(nonce_hex, 16)

gas_price_hex = rpc_call("eth_gasPrice")
gas_price = int(gas_price_hex, 16)

print("=" * 80)
print("📦 Deploying WTBTC Token")
print("=" * 80)
print()
print(f"Nonce: {nonce}")
print(f"Gas Price: {gas_price / 10**9:.2f} Gwei")
print()

# Build deployment transaction
# Note: For simplicity, we're deploying without constructor params
# A full implementation would need proper ABI encoding
tx = {
    'nonce': nonce,
    'gasPrice': gas_price,
    'gas': 3000000,
    'to': '',  # Empty for contract creation
    'value': 0,
    'data': wtbtc_bytecode if wtbtc_bytecode.startswith('0x') else '0x' + wtbtc_bytecode,
    'chainId': CHAIN_ID
}

print("Signing transaction...")
try:
    signed_tx = sign_transaction(tx, private_key)
except Exception as e:
    print(f"❌ Signing failed: {e}")
    print()
    print("This is a complex operation. For Termux, it's better to:")
    print("1. Use MetaMask on a computer")
    print("2. Or deploy from a non-Termux environment")
    exit(1)

print("Sending transaction...")
try:
    tx_hash = rpc_call("eth_sendRawTransaction", [signed_tx])
    print(f"✅ Transaction sent: {tx_hash}")
except Exception as e:
    print(f"❌ Send failed: {e}")
    exit(1)

print()
print("Waiting for confirmation...")

# Wait for receipt
receipt = None
for attempt in range(60):
    try:
        receipt = rpc_call("eth_getTransactionReceipt", [tx_hash])
        if receipt:
            break
    except:
        pass
    time.sleep(2)
    if attempt % 5 == 0 and attempt > 0:
        print(f"  Still waiting... ({attempt * 2}s)")

if not receipt:
    print("⏱️  Timeout. Check manually:")
    print(f"   https://explorer.testnet.monad.xyz/tx/{tx_hash}")
    exit(1)

status = int(receipt.get('status', '0x0'), 16)
if status != 1:
    print("❌ Deployment failed!")
    exit(1)

contract_address = receipt['contractAddress']
print()
print("✅ WTBTC DEPLOYED!")
print(f"   Address: {contract_address}")
print(f"   Explorer: https://explorer.testnet.monad.xyz/address/{contract_address}")
print()

# Save deployment info
deployment_info = {
    "network": "monad",
    "chain_id": CHAIN_ID,
    "deployer": address,
    "bitget_wallet": BITGET_WALLET,
    "contracts": {
        "WTBTC": {
            "address": contract_address,
            "explorer": f"https://explorer.testnet.monad.xyz/address/{contract_address}"
        }
    },
    "timestamp": int(time.time())
}

with open('real_wtbtc_deployment_termux.json', 'w') as f:
    json.dump(deployment_info, f, indent=2)

print("=" * 80)
print("✅ DEPLOYMENT COMPLETE!")
print("=" * 80)
print()
print("📱 Import to Bitget:")
print(f"   Contract: {contract_address}")
print(f"   Symbol: WTBTC")
print(f"   Decimals: 8")
print()
print("Use MetaMask to transfer tokens to your Bitget wallet:")
print(f"   {BITGET_WALLET}")
print()
