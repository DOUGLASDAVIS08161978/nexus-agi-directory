#!/bin/bash
################################################################################
# ONE-COMMAND WTBTC DEPLOYMENT TO BITGET
# Fully autonomous deployment that sends tokens to your Bitget wallet
################################################################################

set -e

echo "================================================================================"
echo "🚀 Deploying WTBTC and Sending to Your Bitget Wallet"
echo "================================================================================"
echo ""

BITGET_WALLET="0xD34beE1C52D05798BD1925318dF8d3292d0e49E6"

echo "Target Bitget Wallet: $BITGET_WALLET"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Step 1: Check Python
echo "Step 1: Checking Python..."
echo "────────────────────────────────────────────────────────────────────────────────"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 installed: $(python3 --version)${NC}"
else
    echo -e "${RED}❌ Python3 not found${NC}"
    if [ -n "$TERMUX_VERSION" ]; then
        echo "Installing Python in Termux..."
        pkg install python -y
    else
        echo "Please install Python3"
        exit 1
    fi
fi
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
echo "────────────────────────────────────────────────────────────────────────────────"
# Only install pure Python packages (no Rust compilation needed)
pip3 install --quiet ecdsa pycryptodome requests 2>/dev/null || {
    echo "Installing packages..."
    pip3 install ecdsa pycryptodome requests
}
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Step 3: Generate wallet if needed
echo "Step 3: Checking for wallet..."
echo "────────────────────────────────────────────────────────────────────────────────"
if [ ! -f .env ] || ! grep -q "PRIVATE_KEY" .env; then
    echo -e "${YELLOW}⚠️  No wallet found, generating new one...${NC}"
    python3 simple_wallet_gen.py

    # Extract wallet address
    WALLET_ADDRESS=$(grep "WALLET_ADDRESS=" .env | cut -d'=' -f2)

    echo ""
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANT: GET TESTNET TOKENS BEFORE CONTINUING${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Your deployer wallet: $WALLET_ADDRESS"
    echo ""
    echo "You need free Monad testnet tokens (MON) to deploy contracts."
    echo ""
    echo "1. Visit: https://www.alchemy.com/faucets/monad-testnet"
    echo "2. Enter: $WALLET_ADDRESS"
    echo "3. Click 'Send Me MON'"
    echo "4. Wait 30 seconds"
    echo ""
    read -p "Press Enter after getting testnet tokens from faucet..."
else
    echo -e "${GREEN}✅ Wallet found in .env${NC}"
fi
echo ""

# Step 4: Deploy WTBTC
echo "Step 4: Deploying WTBTC to Monad testnet..."
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

# Use standalone version (pure Python, no problematic dependencies)
python3 deploy_termux_standalone.py

# Check if deployment succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo -e "${GREEN}✅ SUCCESS! WTBTC DEPLOYED AND SENT TO YOUR BITGET WALLET!${NC}"
    echo "================================================================================"
    echo ""

    # Show deployment summary
    if [ -f real_wtbtc_deployment_termux.json ]; then
        echo "📊 Deployment Summary:"
        python3 << 'PYEOF'
import json
with open('real_wtbtc_deployment_termux.json') as f:
    d = json.load(f)
    print(f"\n📍 Contract Addresses:")
    print(f"   WTBTC Token: {d['contracts']['WTBTC']['address']}")
    print(f"   Bridge: {d['contracts']['Bridge']['address']}")
    print(f"\n🔗 Block Explorer:")
    print(f"   {d['contracts']['WTBTC']['explorer']}")
PYEOF

        echo ""
        echo "════════════════════════════════════════════════════════════════════════════════"
        echo "📱 IMPORT TO BITGET APP:"
        echo "════════════════════════════════════════════════════════════════════════════════"
        echo ""
        echo "1. Open Bitget app"
        echo "2. Tap 'Assets' → 'Deposit'"
        echo "3. Add Monad Testnet network:"
        echo "   - Network: Monad Testnet"
        echo "   - RPC: https://testnet.monad.xyz"
        echo "   - Chain ID: 41454"
        echo "   - Symbol: MON"
        echo ""
        echo "4. Add Custom Token:"

        python3 << 'PYEOF'
import json
with open('real_wtbtc_deployment_termux.json') as f:
    d = json.load(f)
    print(f"   - Contract: {d['contracts']['WTBTC']['address']}")
    print(f"   - Symbol: WTBTC")
    print(f"   - Decimals: 8")
PYEOF

        echo ""
        echo "════════════════════════════════════════════════════════════════════════════════"
        echo ""
        echo "✅ Deployment complete! Check DEPOSIT_TO_BITGET.md for detailed instructions."
        echo ""
    fi
else
    echo ""
    echo -e "${RED}❌ Deployment failed${NC}"
    echo "Check errors above. Common issues:"
    echo "  - No MON tokens (get from faucet)"
    echo "  - Network connection"
    echo "  - Already deployed (check real_wtbtc_deployment_termux.json)"
    exit 1
fi
