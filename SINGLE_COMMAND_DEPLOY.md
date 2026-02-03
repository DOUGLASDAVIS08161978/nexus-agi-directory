# 🚀 SINGLE COMMAND DEPLOYMENT

Deploy your ERC-20 token + Create Uniswap pool + Add liquidity - **ALL IN ONE COMMAND**

## For Termux (Copy-Paste This):

```bash
export PRIVATE_KEY="YOUR_PRIVATE_KEY_HERE" && pip install -q ecdsa pycryptodome requests && python3 deploy_and_pool_all_in_one.py
```

### Replace `YOUR_PRIVATE_KEY_HERE` with your actual private key!

---

## What This Does:

1. ✅ Deploys **tBTC** token (21M supply, 8 decimals) to Base Sepolia
2. ✅ Wraps 0.0005 ETH to WETH
3. ✅ Approves tBTC for Uniswap
4. ✅ Approves WETH for Uniswap
5. ✅ Creates Uniswap V3 pool (0.3% fee)
6. ✅ Initializes pool at **20 ETH per tBTC** (Bitcoin peg)
7. ✅ Adds initial liquidity

---

## Token Details:

- **Name**: Test Bitcoin
- **Symbol**: tBTC
- **Decimals**: 8
- **Total Supply**: 21,000,000 tBTC
- **Pool Price**: 1 tBTC = 20 ETH
- **Network**: Base Sepolia

---

## Requirements:

- At least **0.002 ETH** on Base Sepolia for gas fees
- Termux or any Linux terminal
- Python 3.6+

---

## Get Testnet ETH:

https://www.alchemy.com/faucets/base-sepolia

---

## Customize Token (Optional):

Edit `deploy_and_pool_all_in_one.py`:

```python
TOKEN_NAME = "Your Token Name"
TOKEN_SYMBOL = "SYMBOL"
TOKEN_DECIMALS = 18
TOKEN_SUPPLY = 1000000
POOL_PRICE = 0.001  # 1 token = 0.001 ETH
```

---

## Alternative: Using Shell Script

```bash
export PRIVATE_KEY="YOUR_PRIVATE_KEY_HERE" && ./DEPLOY_EVERYTHING.sh
```

---

**⚠️ NEVER share your private key with anyone!**

The script stores it temporarily in an environment variable and uses it to sign transactions. It's never saved to disk.
