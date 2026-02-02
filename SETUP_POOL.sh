#!/bin/bash
# COMPLETE POOL SETUP - Single Command
# Checks balances, wraps ETH, approves tokens, creates pool, INITIALIZES pool, adds liquidity

echo "🚀 Starting complete pool setup..."
echo "This will:"
echo "  1. Check your TBTC balance (you have 1,000,000 TBTC!)"
echo "  2. Wrap ETH to WETH if needed"
echo "  3. Approve TBTC for Uniswap"
echo "  4. Approve WETH for Uniswap"
echo "  5. Create pool (if doesn't exist)"
echo "  6. INITIALIZE pool with Bitcoin price"
echo "  7. Add liquidity (1 TBTC = 20 ETH)"
echo ""

node setup_pool_complete.js
