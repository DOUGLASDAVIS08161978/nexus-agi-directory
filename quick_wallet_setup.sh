#!/bin/bash
################################################################################
# WTBTC Quick Wallet Setup for Termux
# Automatically generates wallet without prompts
################################################################################

set -e

echo "================================================================================"
echo "🔑 WTBTC Wallet Setup (Automatic)"
echo "================================================================================"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install --quiet requests eth-account 2>/dev/null || pip3 install requests eth-account
echo "✅ Dependencies ready"
echo ""

# Generate wallet
python3 << 'PYEOF'
import json
import os
import time
from pathlib import Path

print("=" * 80)
print("🔑 Generating New Wallet")
print("=" * 80)
print("")

# Check if .env exists
if Path('.env').exists():
    print("✅ Wallet already exists in .env file")
    print("")
    with open('.env') as f:
        for line in f:
            if line.startswith('PRIVATE_KEY='):
                pk = line.strip().split('=')[1]
                print(f"Private Key: {pk[:10]}...{pk[-10:]}")

                # Load and show address
                from eth_account import Account
                if not pk.startswith('0x'):
                    pk = '0x' + pk
                account = Account.from_key(pk)
                print(f"Address: {account.address}")
else:
    from eth_account import Account
    import secrets

    # Generate new wallet
    print("Generating new Ethereum wallet...")
    private_key = "0x" + secrets.token_hex(32)
    account = Account.from_key(private_key)

    print("")
    print("=" * 80)
    print("✅ NEW WALLET CREATED!")
    print("=" * 80)
    print(f"Address: {account.address}")
    print(f"Private Key: {private_key}")
    print("=" * 80)
    print("")

    # Save to .env
    with open('.env', 'w') as f:
        f.write(f'PRIVATE_KEY={private_key[2:]}\n')

    print("✅ Saved to .env file")
    print("")

bitcoin_address = "bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal"

# Create deployment config
deployment = {
    "network": "monad",
    "chainId": 41454,
    "timestamp": int(time.time()),
    "bitcoinAddress": bitcoin_address,
    "status": "configured"
}

with open('wallet_config.json', 'w') as f:
    json.dump(deployment, f, indent=2)

print("=" * 80)
print("📝 NEXT STEPS: Get Free Testnet Tokens")
print("=" * 80)
print("")
print("1. Copy your address from above")
print("2. Visit: https://www.alchemy.com/faucets/monad-testnet")
print("3. Paste your address")
print("4. Click 'Send Me MON'")
print("5. Wait 30 seconds")
print("")
print("After getting tokens, you can:")
print("- Import to MetaMask")
print("- Use for testnet transactions")
print("- Deploy contracts (requires full environment)")
print("")
print("=" * 80)
print("✅ WALLET SETUP COMPLETE!")
print("=" * 80)
print("")
print(f"Your wallet is ready for Monad testnet!")
print(f"Configuration saved to: wallet_config.json")
print("")

PYEOF

echo ""
echo "================================================================================"
echo "✅ Done! Your wallet is ready."
echo "================================================================================"
echo ""
echo "To see your wallet info:"
echo "  cat .env"
echo ""
echo "To get testnet tokens:"
echo "  https://www.alchemy.com/faucets/monad-testnet"
echo ""
