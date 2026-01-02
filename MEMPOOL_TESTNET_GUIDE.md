# Mempool Testnet Explorer Setup Guide

**Local Bitcoin Testnet Block Explorer**

Integrate Mempool with the Bitcoin Testnet Learning System for visual blockchain exploration.

Authors: Douglas Shane Davis & Claude
Date: January 2, 2026

---

## 🎯 What is Mempool?

Mempool is a **self-hosted Bitcoin block explorer** that provides:
- Visual blockchain explorer
- Transaction tracking
- Block visualization
- Fee estimation
- Mempool statistics
- Address lookups

**Perfect for**: Viewing your testnet transactions with a professional UI!

---

## 📦 Files Provided

### 1. docker-compose-testnet.yml
**Testnet-optimized** Mempool configuration:
- Connects to Bitcoin Core on port **18332** (testnet)
- Uses credentials: `bitcoinrpc:testnet123`
- Runs frontend on port **8080**
- Includes MariaDB database
- Optimized for testnet operations

### 2. docker-compose.yml (Original)
**Mainnet** configuration:
- Connects to Bitcoin Core on port **8332** (mainnet)
- **⚠️ WARNING**: For mainnet use only!
- Uses different credentials

---

## 🚀 Quick Start

### Prerequisites

1. **Docker & Docker Compose installed**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Bitcoin Core running on testnet**
   ```bash
   bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123 -server
   ```

### Step 1: Create Data Directories

```bash
mkdir -p data mysql/data
chmod 1000:1000 data mysql/data
```

### Step 2: Start Mempool

```bash
# For testnet (recommended for learning)
docker-compose -f docker-compose-testnet.yml up -d

# Check status
docker-compose -f docker-compose-testnet.yml ps
```

### Step 3: Access Mempool

Open browser to: **http://localhost:8080**

You'll see:
- Testnet blockchain explorer
- Recent blocks
- Mempool transactions
- Network statistics

---

## 🔗 Integration with Bitcoin Testnet Learning System

### Complete Workflow

**1. Start Bitcoin Core**
```bash
bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123 -server
```

**2. Start Mempool Explorer**
```bash
docker-compose -f docker-compose-testnet.yml up -d
```

**3. Run Bitcoin Learning System**
```bash
python3 bitcoin_testnet_system.py
```

**4. Generate Address**
The system will create an address like:
```
📍 tb1q2s9k3mtxcwx5lu0ndhaefegjj7k0cwjh8vm5f2
```

**5. Get Testnet Coins**
- Visit: https://testnet-faucet.mempool.co/
- Paste your address
- Receive testnet bitcoins

**6. View Transaction in Local Mempool**
- Go to: http://localhost:8080
- Search for your address
- See transaction in real-time!

**7. Send Transaction**
```python
# Using the learning system
system.send_transaction("tb1q...", 0.001)
```

**8. Watch Confirmation**
- View in Mempool: http://localhost:8080
- See transaction enter mempool
- Watch confirmations increase
- Explore block details

---

## 📊 Configuration Details

### Testnet Configuration (docker-compose-testnet.yml)

```yaml
Key Settings:
  CORE_RPC_PORT: "18332"          # Testnet RPC port
  CORE_RPC_USERNAME: "bitcoinrpc"
  CORE_RPC_PASSWORD: "testnet123"
  MEMPOOL_NETWORK: "testnet"
  MEMPOOL_TESTNET_ENABLED: "true"
  Frontend Port: 8080
```

### Mainnet Configuration (docker-compose.yml)

```yaml
Key Settings:
  CORE_RPC_PORT: "8332"           # Mainnet RPC port
  CORE_RPC_USERNAME: "mempool"
  CORE_RPC_PASSWORD: "mempool"
  Frontend Port: 80
```

**⚠️ IMPORTANT**: Never confuse testnet and mainnet configurations!

---

## 🔧 Docker Compose Commands

### Start Services
```bash
# Testnet
docker-compose -f docker-compose-testnet.yml up -d

# Mainnet
docker-compose -f docker-compose.yml up -d
```

### Stop Services
```bash
# Testnet
docker-compose -f docker-compose-testnet.yml down

# Mainnet
docker-compose -f docker-compose.yml down
```

### View Logs
```bash
# All services
docker-compose -f docker-compose-testnet.yml logs -f

# Specific service
docker-compose -f docker-compose-testnet.yml logs -f api
docker-compose -f docker-compose-testnet.yml logs -f web
docker-compose -f docker-compose-testnet.yml logs -f db
```

### Check Status
```bash
docker-compose -f docker-compose-testnet.yml ps
```

### Restart Services
```bash
docker-compose -f docker-compose-testnet.yml restart
```

### Remove Everything (Including Data)
```bash
# Stop and remove containers
docker-compose -f docker-compose-testnet.yml down -v

# Remove data directories
rm -rf data mysql
```

---

## 🌐 Network Configuration

### Docker Network Setup

The testnet configuration creates an isolated network:
```yaml
networks:
  mempool-testnet:
    driver: bridge
```

### Accessing Bitcoin Core from Docker

Bitcoin Core runs on host at: `172.27.0.1:18332`

This IP allows Docker containers to access services on the host.

### Port Mapping

| Service | Container Port | Host Port | Purpose |
|---------|---------------|-----------|---------|
| Frontend | 8080 | 8080 | Web interface |
| API | - | - | Internal only |
| Database | 3306 | - | Internal only |

---

## 📱 Using the Mempool Interface

### Homepage
- **Recent Blocks**: Latest testnet blocks
- **Mempool Stats**: Unconfirmed transactions
- **Fee Rates**: Current network fees

### Search Features
- **Address**: `tb1q...` (testnet address)
- **Transaction**: Full TXID
- **Block**: Block hash or height

### Transaction View
- Input/Output details
- Confirmations
- Fee information
- Block inclusion
- Raw transaction data

### Block View
- Block header details
- All transactions in block
- Miner information
- Block hash and height

### Address View
- Balance
- Transaction history
- Received/Sent amounts
- UTXO list

---

## 🔍 Example Usage Scenario

### Complete Testnet Workflow

**1. Setup**
```bash
# Start Bitcoin Core
bitcoind -testnet -daemon -rpcuser=bitcoinrpc -rpcpassword=testnet123

# Wait for initial sync
bitcoin-cli -testnet getblockchaininfo

# Start Mempool
docker-compose -f docker-compose-testnet.yml up -d

# Wait for Mempool to sync
# Check: http://localhost:8080
```

**2. Generate Address**
```bash
python3 bitcoin_testnet_system.py
# Note the address: tb1q...
```

**3. Get Testnet Coins**
```bash
# Visit faucet: https://testnet-faucet.mempool.co/
# Send 0.01 tBTC to your address
```

**4. View in Mempool**
```bash
# Go to: http://localhost:8080
# Search for your address
# See incoming transaction!
```

**5. Send Transaction**
```python
# Create transaction
txid = system.send_transaction("tb1qrecipient...", 0.005)
print(f"TXID: {txid}")
```

**6. Track in Mempool**
```bash
# Go to: http://localhost:8080/tx/{txid}
# Watch it:
# - Enter mempool (0 confirmations)
# - Get included in block (1 confirmation)
# - Gain more confirmations (2, 3, 4...)
```

---

## 🛠️ Troubleshooting

### Mempool Won't Start

**Check Docker**
```bash
docker ps
docker-compose -f docker-compose-testnet.yml logs
```

**Common Issues**:
- Port 8080 already in use
- Docker not running
- Insufficient permissions

### Can't Connect to Bitcoin Core

**Verify Bitcoin Core Running**
```bash
bitcoin-cli -testnet getblockchaininfo
```

**Check RPC Settings**
```bash
# In bitcoin.conf or command line:
server=1
rpcuser=bitcoinrpc
rpcpassword=testnet123
rpcallowip=127.0.0.1
```

**Test RPC Connection**
```bash
curl --user bitcoinrpc:testnet123 \
  --data-binary '{"jsonrpc":"1.0","id":"test","method":"getblockchaininfo","params":[]}' \
  http://127.0.0.1:18332/
```

### Mempool Shows No Data

**Wait for Sync**
- Mempool needs to sync with Bitcoin Core
- Check logs: `docker-compose -f docker-compose-testnet.yml logs -f api`
- Initial sync can take 10-30 minutes

**Verify Database**
```bash
# Check database container
docker-compose -f docker-compose-testnet.yml logs db

# Restart if needed
docker-compose -f docker-compose-testnet.yml restart db
```

### Frontend Won't Load

**Check Web Container**
```bash
docker-compose -f docker-compose-testnet.yml logs web
```

**Verify Port**
```bash
netstat -tlnp | grep 8080
```

**Try Different Port**
Edit `docker-compose-testnet.yml`:
```yaml
ports:
  - 8081:8080  # Use port 8081 instead
```

### Permission Issues

**Fix Data Directory Permissions**
```bash
sudo chown -R 1000:1000 data mysql
```

---

## 🔒 Security Considerations

### Testnet Security
- ✅ Safe for learning (no real value)
- ✅ RPC credentials in clear text is OK for testnet
- ✅ Local-only access is fine

### Mainnet Security
If using mainnet configuration:
- ⚠️ Use strong RPC passwords
- ⚠️ Never expose RPC to internet
- ⚠️ Use firewall rules
- ⚠️ Consider VPN for remote access
- ⚠️ Encrypt wallet
- ⚠️ Regular backups

---

## 📊 Resource Usage

### Disk Space
- MariaDB: ~100-500 MB (depends on usage)
- Mempool cache: ~50-200 MB
- Docker images: ~500 MB

### Memory
- Frontend: ~50-100 MB
- API: ~200-500 MB
- Database: ~200-400 MB
- **Total**: ~500 MB - 1 GB

### CPU
- Low during normal operation
- Higher during initial sync
- Spikes when processing blocks

---

## 🎓 Educational Value

### What You Learn

**Docker & Containers**
- Docker Compose orchestration
- Multi-container applications
- Container networking
- Volume management

**Bitcoin Operations**
- Block explorer functionality
- Transaction visualization
- Mempool mechanics
- Block confirmation process

**Web Services**
- Frontend/Backend architecture
- API communication
- Database integration
- Nginx configuration

---

## 🔗 Integration Points

### With Bitcoin Testnet Learning System

The Mempool explorer enhances the learning system:

**Before Mempool**:
- Text-based transaction IDs
- Command-line output only
- No visual feedback

**With Mempool**:
- ✅ Visual transaction explorer
- ✅ Real-time confirmation tracking
- ✅ Professional block explorer
- ✅ Address history visualization
- ✅ Fee estimation tools

### Workflow Integration

```python
# In bitcoin_testnet_system.py
def send_transaction(self, to_address, amount):
    txid = self.rpc_call("sendtoaddress", [to_address, amount])

    print(f"✅ Transaction created!")
    print(f"📝 TXID: {txid}")
    print(f"🔗 View in Mempool: http://localhost:8080/tx/{txid}")

    return txid
```

---

## 📈 Advanced Configuration

### Custom Network Settings

Edit `docker-compose-testnet.yml`:

```yaml
api:
  environment:
    # Enable additional features
    MEMPOOL_AUDIT_ENABLED: "true"
    MEMPOOL_INDEXING_ENABLED: "true"
    MEMPOOL_BISQ_ENABLED: "false"

    # Performance tuning
    MEMPOOL_CACHE_DIR: "/backend/cache"
    MEMPOOL_CLEAR_PROTECTION_MINUTES: "20"
```

### Database Optimization

```yaml
db:
  environment:
    # Performance settings
    MYSQL_MAX_CONNECTIONS: "100"
    MYSQL_INNODB_BUFFER_POOL_SIZE: "256M"
```

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Start
docker-compose -f docker-compose-testnet.yml up -d

# Stop
docker-compose -f docker-compose-testnet.yml down

# Logs
docker-compose -f docker-compose-testnet.yml logs -f

# Restart
docker-compose -f docker-compose-testnet.yml restart

# Status
docker-compose -f docker-compose-testnet.yml ps
```

### Essential URLs

- **Mempool UI**: http://localhost:8080
- **API Health**: http://localhost:8080/api/v1/health
- **Public Testnet Mempool**: https://mempool.space/testnet

### Essential Ports

- **18332**: Bitcoin Core RPC (testnet)
- **8080**: Mempool frontend
- **3306**: MariaDB (internal)

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Docker installed and running
- [ ] Bitcoin Core running on testnet
- [ ] RPC credentials match in both configs
- [ ] Data directories created with correct permissions
- [ ] Docker Compose starts without errors
- [ ] Mempool accessible at http://localhost:8080
- [ ] Can search for testnet address
- [ ] API shows blockchain data
- [ ] Database connected and syncing

---

## 🎉 Success Indicators

You know it's working when:

✅ Mempool homepage shows testnet blocks
✅ Search works for testnet addresses (tb1...)
✅ Recent transactions appear
✅ Block height matches Bitcoin Core
✅ No errors in docker logs
✅ Transactions from learning system appear in Mempool

---

## 📚 Additional Resources

### Mempool Documentation
- https://github.com/mempool/mempool
- https://mempool.space/docs

### Docker Documentation
- https://docs.docker.com/
- https://docs.docker.com/compose/

### Bitcoin Core RPC
- https://developer.bitcoin.org/reference/rpc/

---

## 🎓 Learning Path

### Beginner
1. Start Mempool with Docker Compose
2. Explore testnet blocks
3. Search for addresses
4. View transactions

### Intermediate
1. Integrate with learning system
2. Track your transactions
3. Understand mempool mechanics
4. Monitor confirmations

### Advanced
1. Customize Mempool configuration
2. Set up for mainnet
3. Deploy remotely
4. Optimize performance

---

## 🌟 Summary

**Mempool + Bitcoin Testnet Learning System = Complete Bitcoin Education Platform**

You get:
- ✅ Command-line Bitcoin operations (learning system)
- ✅ Visual blockchain explorer (Mempool)
- ✅ Real testnet interaction
- ✅ Professional development environment
- ✅ Zero financial risk

Perfect for learning Bitcoin development! 🎓⛓️

---

**Authors**: Douglas Shane Davis & Claude
**Date**: January 2, 2026
**Purpose**: Integrate Mempool with Bitcoin testnet learning system
