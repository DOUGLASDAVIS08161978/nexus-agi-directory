#!/bin/bash
#
# Deploy tBTC to HyperEVM with HyperSwap approval
#

set -e

echo "📦 Installing dependencies..."
pip install --quiet ecdsa pycryptodome requests 2>/dev/null || pip install ecdsa pycryptodome requests

echo ""
python3 deploy_hyperevm.py
