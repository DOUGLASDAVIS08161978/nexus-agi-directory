#!/bin/bash
# Bitcoin Core Download Script
# Run this on a machine WITH network access

set -e

echo "=========================================="
echo " Bitcoin Core Offline Download Script"
echo "=========================================="
echo ""

# Bitcoin Core version
VERSION="27.0"
ARCH="x86_64-linux-gnu"
FILENAME="bitcoin-${VERSION}-${ARCH}.tar.gz"
URL="https://bitcoincore.org/bin/bitcoin-core-${VERSION}/${FILENAME}"

echo "Downloading Bitcoin Core ${VERSION}..."
echo "URL: ${URL}"
echo ""

# Download binary
wget -O "${FILENAME}" "${URL}"

if [ $? -eq 0 ]; then
    echo "✅ Download successful!"
    echo ""

    # Download checksums
    echo "Downloading checksums..."
    wget -O "SHA256SUMS" "https://bitcoincore.org/bin/bitcoin-core-${VERSION}/SHA256SUMS"

    # Verify
    echo ""
    echo "Verifying download..."
    sha256sum --ignore-missing --check SHA256SUMS

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Verification successful!"
        echo ""
        echo "📦 Package ready for transfer:"
        echo "   ${FILENAME}"
        echo ""
        echo "📋 Next steps:"
        echo "   1. Transfer ${FILENAME} to the restricted environment"
        echo "   2. Run the installation script"
        echo ""
    else
        echo "❌ Verification failed!"
        exit 1
    fi
else
    echo "❌ Download failed!"
    exit 1
fi
