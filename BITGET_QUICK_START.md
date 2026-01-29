# WTBTC to Bitget - Quick Start Guide

## Your Bitget Wallet
**Address:** `0xD34beE1C52D05798BD1925318dF8d3292d0e49E6`

---

## The Problem

Current deployment uses **simulated/placeholder addresses** that won't work in Bitget:
- ❌ `0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (fake)
- ❌ `0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB` (fake)

These addresses are NOT real blockchain contracts.

---

## The Solution

Deploy **REAL WTBTC** to Monad blockchain and automatically send tokens to your Bitget wallet.

---

## ONE-COMMAND DEPLOYMENT

Run this single command to do everything automatically:

```bash
bash deploy_to_bitget.sh
```

### What It Does:

1. ✅ Generates Ethereum wallet (if needed)
2. ✅ Checks dependencies
3. ⏸️  Pauses for you to get free testnet tokens
4. ✅ Deploys WTBTC token contract to Monad
5. ✅ Deploys Bridge contract
6. ✅ Configures everything
7. ✅ **Sends 500,000 WTBTC to your Bitget wallet automatically!**
8. ✅ Shows you contract addresses and instructions

**Total time:** 5-7 minutes (including faucet wait)

---

## Step-by-Step

### 1. Run Deployment Script

```bash
bash deploy_to_bitget.sh
```

### 2. Get Free Testnet Tokens

The script will pause and ask you to get tokens:

1. Visit: https://www.alchemy.com/faucets/monad-testnet
2. Enter the wallet address shown
3. Click "Send Me MON"
4. Wait 30 seconds
5. Press Enter to continue

### 3. Wait for Deployment

The script will:
- Deploy WTBTC contract → Get real address
- Deploy Bridge contract → Get real address
- Transfer 500K WTBTC to your Bitget wallet

### 4. Import to Bitget

After deployment completes, import the token:

**In Bitget App:**
1. Tap "Assets" → "Deposit"
2. Add network: Monad Testnet
   - RPC: `https://testnet.monad.xyz`
   - Chain ID: `41454`
3. Add custom token with contract address from output
4. Symbol: `WTBTC`, Decimals: `8`
5. Done! Balance shows 500,000 WTBTC

---

## Alternative: Manual Deployment

If you want more control, deploy manually:

```bash
# 1. Generate wallet
python3 simple_wallet_gen.py

# 2. Get testnet tokens (browser):
#    https://www.alchemy.com/faucets/monad-testnet

# 3. Deploy and send to Bitget
python3 deploy_real_wtbtc.py
```

---

## What You Get

After deployment:

✅ **Real WTBTC token contract** on Monad blockchain
✅ **Real Bridge contract** for Bitcoin ↔ Monad
✅ **500,000 WTBTC** in your Bitget wallet automatically
✅ **Real contract addresses** you can verify on block explorer
✅ **Tradeable tokens** you can transfer/use

---

## Files Created

- `deploy_to_bitget.sh` - One-command deployment script
- `deploy_real_wtbtc.py` - Python deployment script
- `DEPOSIT_TO_BITGET.md` - Detailed guide with screenshots
- `real_wtbtc_deployment.json` - Deployment results and addresses

---

## Cost

**Total: $0.00 (FREE)**

- Wallet generation: FREE
- Testnet tokens: FREE (from faucet)
- Contract deployment: FREE (uses testnet MON)
- Transfer to Bitget: FREE (uses testnet MON)

Everything is free because we're using Monad testnet!

---

## Troubleshooting

**"No PRIVATE_KEY in .env"**
→ Script will generate one automatically

**"Zero balance"**
→ Get MON from: https://www.alchemy.com/faucets/monad-testnet

**"Cannot connect to Monad"**
→ Check internet, wait 1 minute, try again

**"Token not in Bitget"**
→ Make sure to add Monad network first, then import token

---

## Verification

Check your deployment worked:

```bash
# View deployment details
cat real_wtbtc_deployment.json

# Check on block explorer
# (Visit URL shown in deployment output)
```

Your Bitget wallet should have 500,000 WTBTC!

---

## Security

- ✅ Private key stored in `.env` (git-ignored)
- ✅ Testnet only (no real money)
- ✅ Safe to experiment
- ⚠️  Never share private key

---

## Ready?

Run this now:

```bash
bash deploy_to_bitget.sh
```

You'll have real WTBTC in your Bitget wallet in 5 minutes!
