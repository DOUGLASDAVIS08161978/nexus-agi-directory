#!/usr/bin/env python3
"""
Bitcoin Core Offline Package Builder
Creates a complete offline package for transferring Bitcoin Core to restricted environments

This tool helps you prepare Bitcoin Core on a machine WITH network access,
then transfer it to a machine WITHOUT network access.

Authors: Douglas Shane Davis & Claude
Purpose: Legitimate workaround for network restrictions
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class OfflinePackageBuilder:
    """Build offline Bitcoin Core package"""

    def __init__(self):
        self.package_dir = "bitcoin_offline_package"
        self.instructions_file = "OFFLINE_INSTALLATION_INSTRUCTIONS.md"

    def create_package_structure(self):
        """Create package directory structure"""
        print("="*80)
        print(" 📦 BITCOIN OFFLINE PACKAGE BUILDER")
        print("="*80)
        print("\nThis tool creates a package you can download on another machine")
        print("and transfer to this restricted environment.")
        print()

        os.makedirs(self.package_dir, exist_ok=True)
        os.makedirs(f"{self.package_dir}/binaries", exist_ok=True)
        os.makedirs(f"{self.package_dir}/scripts", exist_ok=True)

        print(f"✅ Created package directory: {self.package_dir}/")

    def generate_download_script(self):
        """Generate script to run on machine with network access"""
        script = """#!/bin/bash
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
"""

        script_path = f"{self.package_dir}/download_bitcoin.sh"
        with open(script_path, 'w') as f:
            f.write(script)

        os.chmod(script_path, 0o755)
        print(f"✅ Created download script: {script_path}")

    def generate_installation_script(self):
        """Generate installation script for restricted environment"""
        script = """#!/bin/bash
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
"""

        script_path = f"{self.package_dir}/install_bitcoin.sh"
        with open(script_path, 'w') as f:
            f.write(script)

        os.chmod(script_path, 0o755)
        print(f"✅ Created installation script: {script_path}")

    def generate_instructions(self):
        """Generate complete instructions"""
        instructions = """# Bitcoin Core Offline Installation Guide

**Complete guide for installing Bitcoin Core in a network-restricted environment**

---

## 🎯 Overview

Since direct downloads are blocked, you'll:
1. Download Bitcoin Core on another machine (with network access)
2. Transfer the file to this environment
3. Install from the transferred file

---

## 📋 Prerequisites

**Machine WITH Network Access** (for downloading):
- Internet connection
- Linux, macOS, or Windows
- wget or web browser

**Machine WITHOUT Network Access** (restricted environment):
- This machine
- USB drive or file transfer capability
- sudo access (for installation)

---

## 🔄 Step-by-Step Process

### **PART 1: On Machine WITH Network Access**

#### Option A: Using the Download Script

```bash
# 1. Copy the download script to a machine with network access
# 2. Run it:
chmod +x download_bitcoin.sh
./download_bitcoin.sh
```

#### Option B: Manual Download

1. **Visit**: https://bitcoincore.org/en/download/
2. **Download**: Bitcoin Core 27.0 (x86_64-linux-gnu)
3. **File**: `bitcoin-27.0-x86_64-linux-gnu.tar.gz` (~26 MB)
4. **Also download**: SHA256SUMS (for verification)

#### Verify Download (Recommended)

```bash
sha256sum --ignore-missing --check SHA256SUMS
```

Expected output: `bitcoin-27.0-x86_64-linux-gnu.tar.gz: OK`

---

### **PART 2: Transfer to Restricted Environment**

#### Transfer Methods:

**USB Drive**:
```bash
# On source machine
cp bitcoin-27.0-x86_64-linux-gnu.tar.gz /media/usb/

# On restricted machine
cp /media/usb/bitcoin-27.0-x86_64-linux-gnu.tar.gz ~/
```

**SCP (if internal network allows)**:
```bash
scp bitcoin-27.0-x86_64-linux-gnu.tar.gz user@restricted-machine:~/
```

**File Share**:
- Copy to shared network drive
- Access from restricted machine

---

### **PART 3: Install on Restricted Machine**

#### Option A: Using Installation Script

```bash
# 1. Copy install_bitcoin.sh to same directory as the .tar.gz file
# 2. Run:
chmod +x install_bitcoin.sh
./install_bitcoin.sh
```

#### Option B: Manual Installation

```bash
# 1. Extract
tar -xzf bitcoin-27.0-x86_64-linux-gnu.tar.gz

# 2. Install binaries
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-27.0/bin/*

# 3. Verify
bitcoind --version
```

Expected output: `Bitcoin Core version v27.0.0`

---

## ⚙️ Configuration

### Create Configuration File

```bash
mkdir -p ~/.bitcoin
nano ~/.bitcoin/bitcoin.conf
```

### Configuration Content:

```ini
# Bitcoin Testnet Configuration
testnet=1
server=1

# RPC Settings
rpcuser=bitcoinrpc
rpcpassword=testnet123
rpcallowip=127.0.0.1
rpcbind=127.0.0.1:18332

# Performance
dbcache=450
maxmempool=300
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

---

## 🚀 Start Bitcoin Core

```bash
# Start testnet daemon
bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123 -server

# Check status
bitcoin-cli -testnet getblockchaininfo

# View logs
tail -f ~/.bitcoin/testnet3/debug.log
```

---

## 🎓 Run Learning System

Once Bitcoin Core is running:

```bash
python3 bitcoin_testnet_system.py
```

Expected output:
```
✅ Connected to Bitcoin Core
Chain: test
Blocks: 2,XXX,XXX
Sync: XX.XX%
```

---

## 🔍 Verification Checklist

- [ ] Binary downloaded successfully
- [ ] SHA256 checksum verified
- [ ] File transferred to restricted machine
- [ ] Binaries extracted and installed
- [ ] `bitcoind --version` shows v27.0.0
- [ ] Configuration file created
- [ ] Daemon starts without errors
- [ ] RPC connection works
- [ ] Learning system connects successfully

---

## 🐛 Troubleshooting

### Binary Not Found After Installation

```bash
# Check if installed
which bitcoind

# If not found, add to PATH
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Permission Denied

```bash
# Installation needs sudo
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-27.0/bin/*
```

### RPC Connection Failed

```bash
# Check if daemon is running
ps aux | grep bitcoind

# Test RPC
bitcoin-cli -testnet -rpcuser=bitcoinrpc -rpcpassword=testnet123 getblockchaininfo
```

---

## 📦 File Sizes

- Binary: ~26 MB (compressed)
- Extracted: ~70 MB
- Blockchain (testnet): ~30-40 GB (will sync over time)

---

## ⏱️ Time Estimates

- Download: 1-5 minutes (depending on connection)
- Transfer: Varies (USB: minutes, Network: seconds to minutes)
- Installation: < 1 minute
- Initial sync: 2-6 hours (first time only)

---

## 🔒 Security Notes

### Verify Downloads

**Always verify** the SHA256 checksum:
```bash
sha256sum --ignore-missing --check SHA256SUMS
```

This ensures the download wasn't tampered with.

### Testnet vs Mainnet

- ✅ **Testnet**: Safe for learning (coins have no value)
- ⚠️ **Mainnet**: Real Bitcoin (has actual value)

Make sure you're using testnet for learning!

---

## 💡 Alternative: Use Mock Server

If transferring files is too complex, you can use the mock server:

```bash
# Already available, no download needed
python3 bitcoin_mock_server.py
```

This provides the same learning experience without needing Bitcoin Core!

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review Bitcoin Core logs: `~/.bitcoin/testnet3/debug.log`
3. Verify RPC configuration
4. Ensure sufficient disk space

---

## ✅ Success Indicators

You know it's working when:
- `bitcoind --version` shows version
- Daemon starts without errors
- RPC responds to commands
- Learning system connects successfully
- Blockchain starts syncing

---

**Authors**: Douglas Shane Davis & Claude
**Date**: January 2026
**Purpose**: Legitimate workaround for network-restricted environments
"""

        instructions_path = f"{self.package_dir}/{self.instructions_file}"
        with open(instructions_path, 'w') as f:
            f.write(instructions)

        print(f"✅ Created instructions: {instructions_path}")

    def create_transfer_checklist(self):
        """Create checklist for file transfer"""
        checklist = """# Transfer Checklist

## Files to Transfer

- [ ] bitcoin-27.0-x86_64-linux-gnu.tar.gz (~26 MB)
- [ ] install_bitcoin.sh (installation script)
- [ ] OFFLINE_INSTALLATION_INSTRUCTIONS.md (this guide)

## Transfer Methods

### USB Drive
- [ ] Copy files to USB
- [ ] Safely eject USB
- [ ] Transfer to restricted machine
- [ ] Verify file integrity (check file size)

### Network Share
- [ ] Copy to shared drive
- [ ] Access from restricted machine
- [ ] Copy to local directory
- [ ] Verify file integrity

### SCP/SFTP
- [ ] Verify internal network access
- [ ] Use scp or sftp to transfer
- [ ] Verify transfer completed
- [ ] Check file permissions

## After Transfer

- [ ] Verify file size matches
- [ ] Check SHA256 if possible
- [ ] Make install script executable
- [ ] Run installation
- [ ] Test bitcoind --version

## Notes

File size: bitcoin-27.0-x86_64-linux-gnu.tar.gz should be ~26 MB
If size differs significantly, re-transfer the file.
"""

        checklist_path = f"{self.package_dir}/TRANSFER_CHECKLIST.md"
        with open(checklist_path, 'w') as f:
            f.write(checklist)

        print(f"✅ Created checklist: {checklist_path}")

    def generate_summary(self):
        """Generate package summary"""
        print("\n" + "="*80)
        print(" 📦 OFFLINE PACKAGE CREATED")
        print("="*80)
        print(f"\nPackage directory: {self.package_dir}/")
        print("\nContents:")
        print("  📄 download_bitcoin.sh - Run on machine WITH network")
        print("  📄 install_bitcoin.sh - Run on THIS machine after transfer")
        print("  📄 OFFLINE_INSTALLATION_INSTRUCTIONS.md - Complete guide")
        print("  📄 TRANSFER_CHECKLIST.md - Transfer verification")

        print("\n" + "-"*80)
        print(" QUICK START")
        print("-"*80)
        print("\n1. On a machine WITH network access:")
        print(f"   cd {self.package_dir}")
        print("   ./download_bitcoin.sh")

        print("\n2. Transfer bitcoin-27.0-x86_64-linux-gnu.tar.gz to this machine")

        print("\n3. On this machine:")
        print(f"   cd {self.package_dir}")
        print("   ./install_bitcoin.sh")

        print("\n4. Configure and start:")
        print("   nano ~/.bitcoin/bitcoin.conf")
        print("   bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123")

        print("\n5. Run learning system:")
        print("   python3 bitcoin_testnet_system.py")

        print("\n" + "="*80)
        print("\n💡 Alternative: If file transfer is difficult, use the mock server:")
        print("   python3 bitcoin_mock_server.py")
        print("\n")

    def build(self):
        """Build complete offline package"""
        self.create_package_structure()
        self.generate_download_script()
        self.generate_installation_script()
        self.generate_instructions()
        self.create_transfer_checklist()
        self.generate_summary()


def main():
    print("\n" + "="*80)
    print(" 🔧 BITCOIN OFFLINE PACKAGE BUILDER")
    print("="*80)
    print("\nThis creates tools for LEGITIMATE workarounds to network restrictions.")
    print("It does NOT bypass security - it uses proper file transfer methods.")
    print("\n" + "="*80 + "\n")

    builder = OfflinePackageBuilder()
    builder.build()

    print("✅ Package ready!")
    print(f"\nRead: {builder.package_dir}/{builder.instructions_file}")
    print("\n")


if __name__ == "__main__":
    main()
