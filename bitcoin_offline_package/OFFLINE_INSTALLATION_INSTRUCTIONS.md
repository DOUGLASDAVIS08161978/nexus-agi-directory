# Bitcoin Core Offline Installation Guide

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
