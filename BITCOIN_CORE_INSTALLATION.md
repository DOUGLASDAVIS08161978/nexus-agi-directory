# Bitcoin Core Installation Guide

## Overview
This guide shows how to install Bitcoin Core on Ubuntu 24.04 for testnet operations.

## Installation Methods

### Method 1: Download Official Binary (Recommended)

```bash
# Download Bitcoin Core 27.0
cd /tmp
wget https://bitcoincore.org/bin/bitcoin-core-27.0/bitcoin-27.0-x86_64-linux-gnu.tar.gz

# Verify the download (optional but recommended)
wget https://bitcoincore.org/bin/bitcoin-core-27.0/SHA256SUMS
sha256sum --ignore-missing --check SHA256SUMS

# Extract the archive
tar -xzf bitcoin-27.0-x86_64-linux-gnu.tar.gz

# Install to /usr/local/bin
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-27.0/bin/*

# Verify installation
bitcoind --version
bitcoin-cli --version
```

### Method 2: Using Snap Package

```bash
# Install via snap (if available)
sudo snap install bitcoin-core

# Snap binaries are accessed via:
bitcoin-core.daemon
bitcoin-core.cli
```

### Method 3: Build from Source

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential libtool autotools-dev automake \
    pkg-config bsdmainutils python3 libevent-dev libboost-dev \
    libsqlite3-dev libminiupnpc-dev libnatpmp-dev libzmq3-dev \
    systemtap-sdt-dev

# Clone repository
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin

# Build
./autogen.sh
./configure --without-gui
make -j$(nproc)
sudo make install
```

## Configuration

### Create Bitcoin Data Directory

```bash
mkdir -p ~/.bitcoin
```

### Create Configuration File

Create `~/.bitcoin/bitcoin.conf`:

```ini
# Bitcoin Core Testnet Configuration
# Network
testnet=1
server=1

# RPC Settings
rpcuser=bitcoinrpc
rpcpassword=testnet123
rpcallowip=127.0.0.1
rpcbind=127.0.0.1:18332

# Wallet
wallet=learning_wallet

# Performance
dbcache=450
maxmempool=300

# Logging
debug=0
```

### Alternative: Command Line Configuration

Instead of a config file, you can start bitcoind with parameters:

```bash
bitcoind -testnet \
    -daemon \
    -server \
    -rpcuser=bitcoinrpc \
    -rpcpassword=testnet123 \
    -rpcallowip=127.0.0.1 \
    -rpcbind=127.0.0.1:18332
```

## Starting Bitcoin Core

### Start the Daemon

```bash
# Using config file
bitcoind -testnet -daemon

# Or with command line parameters
bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123 -server
```

### Check if Running

```bash
# Check process
ps aux | grep bitcoind

# Test RPC connection
bitcoin-cli -testnet -rpcuser=bitcoinrpc -rpcpassword=testnet123 getblockchaininfo
```

### Monitor Sync Progress

```bash
# Watch sync progress
watch -n 5 'bitcoin-cli -testnet -rpcuser=bitcoinrpc -rpcpassword=testnet123 getblockchaininfo | grep -E "blocks|headers|verificationprogress"'
```

## Initial Sync

The first time you run Bitcoin Core on testnet, it will sync the blockchain:

- **Testnet blockchain size**: ~30-40 GB
- **Sync time**: 2-6 hours (depending on connection)
- **You can use the node before 100% sync** for basic operations

## Stopping Bitcoin Core

```bash
bitcoin-cli -testnet -rpcuser=bitcoinrpc -rpcpassword=testnet123 stop
```

## Firewall Configuration (Optional)

If you want to accept incoming connections:

```bash
# Testnet P2P port
sudo ufw allow 18333/tcp

# Testnet RPC port (only if needed remotely)
sudo ufw allow 18332/tcp
```

## Useful Commands

```bash
# Get blockchain info
bitcoin-cli -testnet getblockchaininfo

# Create wallet
bitcoin-cli -testnet createwallet "my_wallet"

# Get new address
bitcoin-cli -testnet getnewaddress

# Get balance
bitcoin-cli -testnet getbalance

# List wallets
bitcoin-cli -testnet listwallets

# Get mining info
bitcoin-cli -testnet getmininginfo

# Generate blocks (regtest/testnet with low difficulty)
bitcoin-cli -testnet generatetoaddress 1 <your-address>
```

## Testnet Resources

### Faucets (Get Free Testnet Coins)
- https://testnet-faucet.mempool.co/
- https://bitcoinfaucet.uo1.net/
- https://testnet.help/

### Block Explorers
- https://mempool.space/testnet
- https://blockstream.info/testnet/
- https://live.blockcypher.com/btc-testnet/

## Troubleshooting

### Connection Issues
```bash
# Check if daemon is running
ps aux | grep bitcoind

# Check RPC connection
curl --user bitcoinrpc:testnet123 \
    --data-binary '{"jsonrpc":"1.0","id":"test","method":"getblockchaininfo","params":[]}' \
    -H 'content-type: text/plain;' \
    http://127.0.0.1:18332/
```

### Logs
```bash
# View debug log
tail -f ~/.bitcoin/testnet3/debug.log
```

### Reset/Resync
```bash
# Stop daemon
bitcoin-cli -testnet stop

# Remove blockchain data (keeps wallet)
rm -rf ~/.bitcoin/testnet3/blocks
rm -rf ~/.bitcoin/testnet3/chainstate

# Restart
bitcoind -testnet -daemon
```

## Security Notes

⚠️ **TESTNET ONLY**: The configuration above is for testnet (no real value)

For mainnet:
- Use strong RPC passwords
- Restrict RPC access
- Encrypt wallet
- Backup wallet regularly
- Never expose RPC to internet

## Next Steps

After Bitcoin Core is running:

1. Wait for initial sync to start
2. Create a wallet
3. Generate addresses
4. Get testnet coins from faucet
5. Practice transactions
6. Run the Python learning system!

```bash
python3 bitcoin_testnet_system.py
```
