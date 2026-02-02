#!/bin/bash
# Create Uniswap V3 Pool for TBTC/WETH on Base Sepolia

echo "🚀 Installing dependencies..."
npm install --silent ethers 2>/dev/null || { echo "❌ npm install failed"; exit 1; }

echo "🔄 Creating Uniswap V3 Pool..."
node send_pool_transactions_FIXED.js
