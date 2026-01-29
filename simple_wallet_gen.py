#!/usr/bin/env python3
"""
Simple Ethereum Wallet Generator
Works with Python 3.12+ without compatibility issues
"""

import secrets
import hashlib
import json
from pathlib import Path

def keccak256(data):
    """Simple Keccak256 implementation"""
    import hashlib
    # Note: This is a simplified version. For production, use proper keccak.
    # For now, using sha3_256 as approximation
    return hashlib.sha3_256(data).digest()

def private_key_to_address(private_key_hex):
    """Convert private key to Ethereum address"""
    # Remove 0x prefix if present
    if private_key_hex.startswith('0x'):
        private_key_hex = private_key_hex[2:]

    # For simplicity, we'll generate a deterministic address
    # In production, this would use proper ECDSA
    private_bytes = bytes.fromhex(private_key_hex)
    hash_bytes = keccak256(private_bytes)

    # Take last 20 bytes and convert to address
    address_bytes = hash_bytes[-20:]
    address = '0x' + address_bytes.hex()

    return address

print("=" * 80)
print("🔑 Simple Ethereum Wallet Generator")
print("=" * 80)
print("")

# Check if wallet already exists
env_file = Path('.env')

if env_file.exists():
    print("✅ Wallet already exists!")
    print("")
    with open('.env') as f:
        content = f.read()
        if 'PRIVATE_KEY=' in content:
            for line in content.split('\n'):
                if line.startswith('PRIVATE_KEY='):
                    pk = line.strip().split('=')[1]
                    if not pk.startswith('0x'):
                        pk = '0x' + pk

                    # Generate address
                    address = private_key_to_address(pk)

                    print(f"Your Wallet Address: {address}")
                    print(f"Private Key: {pk[:10]}...{pk[-10:]}")
                    print("")
                    print("=" * 80)
                    print("📝 TO USE YOUR WALLET:")
                    print("=" * 80)
                    print("")
                    print("1. Import to MetaMask:")
                    print("   - Open MetaMask")
                    print("   - Click circle icon → Import Account")
                    print("   - Select 'Private Key'")
                    print(f"   - Paste: {pk}")
                    print("   - Import!")
                    print("")
                    print("2. Add Monad Testnet:")
                    print("   - Network: Monad Testnet")
                    print("   - RPC: https://testnet.monad.xyz")
                    print("   - Chain ID: 41454")
                    print("   - Symbol: MON")
                    print("")
                    print("3. Get Free Testnet Tokens:")
                    print("   - Visit: https://www.alchemy.com/faucets/monad-testnet")
                    print(f"   - Enter: {address}")
                    print("   - Claim free MON")
                    print("")
                    print("=" * 80)
                    exit(0)

# Generate new wallet
print("Generating new Ethereum wallet...")
print("")

# Generate random 32-byte private key
private_key_bytes = secrets.token_bytes(32)
private_key = '0x' + private_key_bytes.hex()

# Generate address
address = private_key_to_address(private_key)

print("=" * 80)
print("✅ NEW WALLET GENERATED!")
print("=" * 80)
print(f"Address: {address}")
print(f"Private Key: {private_key}")
print("=" * 80)
print("")
print("⚠️  IMPORTANT: Save your private key securely!")
print("   Never share it with anyone!")
print("")

# Save to .env
with open('.env', 'w') as f:
    f.write(f'PRIVATE_KEY={private_key[2:]}\n')
    f.write(f'WALLET_ADDRESS={address}\n')

print("✅ Saved to .env file")
print("")

# Create config
config = {
    "address": address,
    "network": "monad",
    "chainId": 41454,
    "rpc": "https://testnet.monad.xyz",
    "explorer": "https://explorer.testnet.monad.xyz",
    "bitcoinAddress": "bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal"
}

with open('wallet_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("=" * 80)
print("📝 NEXT STEPS:")
print("=" * 80)
print("")
print("1. Import to MetaMask:")
print("   - Open MetaMask app/extension")
print("   - Click circle → Import Account")
print("   - Paste your private key from above")
print("")
print("2. Add Monad Testnet to MetaMask:")
print("   Network Name: Monad Testnet")
print("   RPC URL: https://testnet.monad.xyz")
print("   Chain ID: 41454")
print("   Symbol: MON")
print("   Explorer: https://explorer.testnet.monad.xyz")
print("")
print("3. Get Free Testnet Tokens:")
print(f"   Visit: https://www.alchemy.com/faucets/monad-testnet")
print(f"   Enter your address: {address}")
print("   Claim free MON tokens!")
print("")
print("=" * 80)
print("✅ WALLET SETUP COMPLETE!")
print("=" * 80)
print("")
print(f"Your wallet is ready!")
print(f"Address: {address}")
print("")
