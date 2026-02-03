#!/bin/bash
#
# ALL-IN-ONE: Deploy Token + Create Uniswap Pool + Add Liquidity
# For Termux - Single Copy-Paste Command
#

set -e

echo "🚀 INSTALLING DEPENDENCIES..."
pip install --quiet ecdsa pycryptodome requests 2>/dev/null || {
    echo "Installing dependencies..."
    pip install ecdsa pycryptodome requests
}

echo ""
echo "🚀 DEPLOYING TOKEN AND CREATING UNISWAP POOL..."
echo ""

# Run the all-in-one Python script
python3 deploy_and_pool_all_in_one.py

echo ""
echo "✅ COMPLETE!"
