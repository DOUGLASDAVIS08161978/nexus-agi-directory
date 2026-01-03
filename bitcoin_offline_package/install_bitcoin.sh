#!/bin/bash
# Bitcoin Core Installation Script
# Run this in the restricted environment after transferring the binary

set -e

echo "=========================================="
echo " Bitcoin Core Offline Installation"
echo "=========================================="
echo ""

# Check for binary
FILENAME="bitcoin-27.0-x86_64-linux-gnu.tar.gz"

if [ ! -f "${FILENAME}" ]; then
    echo "❌ Error: ${FILENAME} not found"
    echo "   Please transfer the file to this directory first"
    exit 1
fi

echo "Found: ${FILENAME}"
echo ""

# Extract
echo "Extracting..."
tar -xzf "${FILENAME}"

if [ $? -eq 0 ]; then
    echo "✅ Extraction successful!"
    echo ""

    # Install
    echo "Installing binaries to /usr/local/bin..."
    sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-27.0/bin/*

    if [ $? -eq 0 ]; then
        echo "✅ Installation successful!"
        echo ""

        # Verify
        echo "Verifying installation..."
        bitcoind --version

        echo ""
        echo "✅ Bitcoin Core installed successfully!"
        echo ""
        echo "📋 Next steps:"
        echo "   1. Configure: nano ~/.bitcoin/bitcoin.conf"
        echo "   2. Start testnet: bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123"
        echo "   3. Run learning system: python3 bitcoin_testnet_system.py"
        echo ""
    else
        echo "❌ Installation failed (may need sudo)"
        exit 1
    fi
else
    echo "❌ Extraction failed"
    exit 1
fi
