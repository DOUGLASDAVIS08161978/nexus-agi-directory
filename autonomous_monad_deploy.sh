#!/bin/bash
################################################################################
# WTBTC Autonomous Deployment to Monad Testnet
# This script deploys WTBTC contracts to Monad blockchain
#
# REQUIREMENTS:
# 1. Ethereum private key (for signing transactions)
# 2. Monad testnet tokens (for gas fees - get from faucet)
# 3. Internet connection
#
# NOTE: Claude API key is NOT needed for blockchain deployment!
################################################################################

set -e  # Exit on any error

echo "================================================================================"
echo "🚀 WTBTC Autonomous Deployment to Monad Testnet"
echo "================================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in Termux
if [ -n "$TERMUX_VERSION" ]; then
    echo "✅ Detected Termux environment"
    TERMUX=true
else
    echo "ℹ️  Running in standard Linux environment"
    TERMUX=false
fi

# Step 1: Check dependencies
echo ""
echo "Step 1: Checking dependencies..."
echo "────────────────────────────────────────────────────────────────────────────────"

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 installed: $(python3 --version)"
else
    echo "❌ Python3 not found"
    if [ "$TERMUX" = true ]; then
        echo "Installing Python in Termux..."
        pkg install python -y
    else
        echo "Please install Python3: apt install python3"
        exit 1
    fi
fi

# Check pip packages
echo ""
echo "Checking Python packages..."
pip3 install --quiet web3 eth-account python-dotenv requests 2>/dev/null || {
    echo "Installing required packages..."
    pip3 install web3 eth-account python-dotenv requests
}
echo "✅ All Python packages installed"

# Step 2: Check for private key
echo ""
echo "Step 2: Checking for Ethereum private key..."
echo "────────────────────────────────────────────────────────────────────────────────"

if [ -f .env ] && grep -q "PRIVATE_KEY" .env; then
    echo "✅ Found .env file with PRIVATE_KEY"
else
    echo ""
    echo "${YELLOW}⚠️  WARNING: No Ethereum private key found!${NC}"
    echo ""
    echo "You need an Ethereum private key to deploy contracts."
    echo ""
    echo "Options:"
    echo "1. If you have MetaMask:"
    echo "   - Export your private key from MetaMask"
    echo "   - Create .env file: echo 'PRIVATE_KEY=your_key_here' > .env"
    echo ""
    echo "2. Generate a new wallet (for testing only):"
    read -p "Generate a new test wallet? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 << 'PYEOF'
from eth_account import Account
import secrets
# Generate new account
private_key = "0x" + secrets.token_hex(32)
account = Account.from_key(private_key)
print(f"\n{'='*80}")
print("🔑 NEW WALLET GENERATED (TESTNET ONLY)")
print(f"{'='*80}")
print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
print(f"{'='*80}")
print("\n⚠️  SAVE THIS PRIVATE KEY SECURELY!")
print("Writing to .env file...")
with open('.env', 'w') as f:
    f.write(f'PRIVATE_KEY={private_key[2:]}\n')
print("✅ Saved to .env")
print("\n📝 Next step: Get Monad testnet tokens")
print(f"   1. Go to: https://www.alchemy.com/faucets/monad-testnet")
print(f"   2. Enter address: {account.address}")
print(f"   3. Claim free MON tokens")
print(f"   4. Wait 30 seconds")
print(f"   5. Re-run this script")
PYEOF
        echo ""
        read -p "Press Enter after getting testnet tokens from faucet..."
    else
        echo ""
        echo "Please create .env file with your PRIVATE_KEY and re-run this script."
        exit 1
    fi
fi

# Step 3: Check Monad testnet balance
echo ""
echo "Step 3: Checking Monad testnet balance..."
echo "────────────────────────────────────────────────────────────────────────────────"

python3 << 'PYEOF'
from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv('PRIVATE_KEY')
if not private_key:
    print("❌ No PRIVATE_KEY in .env")
    exit(1)

if not private_key.startswith('0x'):
    private_key = '0x' + private_key

account = Account.from_key(private_key)
w3 = Web3(Web3.HTTPProvider('https://testnet.monad.xyz'))

try:
    balance = w3.eth.get_balance(account.address)
    balance_eth = w3.from_wei(balance, 'ether')

    print(f"Wallet Address: {account.address}")
    print(f"MON Balance: {balance_eth} MON")

    if balance == 0:
        print("\n⚠️  WARNING: Zero balance!")
        print(f"\nGet free testnet tokens:")
        print(f"1. Visit: https://www.alchemy.com/faucets/monad-testnet")
        print(f"2. Enter: {account.address}")
        print(f"3. Claim tokens")
        print(f"4. Wait 30 seconds")
        print(f"5. Re-run this script")
        exit(1)
    else:
        print("✅ Sufficient balance for deployment")
except Exception as e:
    print(f"⚠️  Could not check balance: {e}")
    print("Proceeding anyway...")
PYEOF

if [ $? -ne 0 ]; then
    echo ""
    echo "${RED}Exiting: Please get testnet tokens first${NC}"
    exit 1
fi

# Step 4: Deploy to Monad
echo ""
echo "Step 4: Deploying WTBTC to Monad testnet..."
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

# Run the deployment
python3 deploy_to_monad.py

# Check if deployment succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
    echo "================================================================================"
    echo ""

    # Show deployment details
    if [ -f wtbtc_monad_deployment.json ]; then
        echo "📄 Deployment Details:"
        python3 -c "import json; d=json.load(open('wtbtc_monad_deployment.json')); print(f\"WTBTC Token: {d['contracts']['WTBTC']['address']}\"); print(f\"Bridge: {d['contracts']['Bridge']['address']}\"); print(f\"Explorer: {d['contracts']['WTBTC']['explorer_url']}\")"
    fi

    echo ""
    echo "🎉 Your WTBTC is now live on Monad testnet!"
    echo ""
    echo "Next steps:"
    echo "1. Import token to MetaMask:"
    echo "   - Network: Monad Testnet"
    echo "   - Add network if needed (Chain ID: 41454)"
    echo "   - Import token with address from above"
    echo "   - Symbol: WTBTC"
    echo "   - Decimals: 8"
    echo ""
    echo "2. Send BTC to: bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal"
    echo "   - Receive WTBTC on Monad at 1:1 ratio"
    echo ""
else
    echo ""
    echo "${RED}❌ Deployment failed${NC}"
    echo "Check errors above and try again"
    exit 1
fi
