# How to Deploy WTBTC for Real (Get Real Contract Addresses)

## Current Status
The deployments we ran are **simulations** - they show you how the system works without actually deploying to the blockchain.

**Simulated addresses:** `0xAAAA...` and `0xBBBB...`

To get **REAL** contract addresses you can import into MetaMask or other wallets, you need to deploy to an actual blockchain.

## Steps to Deploy for Real

### Option 1: Deploy to Sepolia Testnet (FREE - Recommended)

#### Step 1: Get an Ethereum Wallet
```bash
# If you don't have one:
# 1. Install MetaMask: https://metamask.io
# 2. Create a new wallet
# 3. SAVE your seed phrase securely
# 4. Copy your Ethereum address
```

#### Step 2: Get Free Testnet ETH
```bash
# Visit Sepolia faucet:
https://sepoliafaucet.com

# Enter your Ethereum address
# Wait ~30 seconds
# You'll receive 0.5 Sepolia ETH (FREE)
```

#### Step 3: Export Your Private Key
```bash
# In MetaMask:
# 1. Click the 3 dots menu
# 2. Account Details
# 3. Export Private Key
# 4. Enter your password
# 5. Copy the private key
```

⚠️ **SECURITY WARNING:**
- Never share your private key
- Never commit it to git
- Store it ONLY in .env file

#### Step 4: Create .env File
```bash
cat > .env << 'EOF'
PRIVATE_KEY=your_private_key_here_without_0x
SEPOLIA_RPC=https://rpc.sepolia.org
EOF
```

#### Step 5: Install Hardhat (for real deployment)
```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
# Choose: Create a JavaScript project
```

#### Step 6: Create Real Deployment Script
Save this as `real_deploy_sepolia.js`:

```javascript
const hre = require("hardhat");
const fs = require("fs");

async function main() {
  console.log("Deploying WTBTC to Sepolia testnet...");

  const bitcoinAddress = "bc1qyhkq7usdfhhhynkjksdqfx32u3rmv94y0htsal";

  // Deploy WTBTC Token
  console.log("\nDeploying WTBTC Token...");
  const WTBTC = await hre.ethers.getContractFactory("WTBTC_Enhanced");
  const wtbtc = await WTBTC.deploy(bitcoinAddress);
  await wtbtc.waitForDeployment();

  const wtbtcAddress = await wtbtc.getAddress();
  console.log("✅ WTBTC Token deployed to:", wtbtcAddress);

  // Deploy Bridge
  console.log("\nDeploying Bridge Contract...");
  const Bridge = await hre.ethers.getContractFactory("WTBTCBridge");
  const [deployer] = await hre.ethers.getSigners();
  const bridge = await Bridge.deploy(
    wtbtcAddress,
    bitcoinAddress,
    deployer.address
  );
  await bridge.waitForDeployment();

  const bridgeAddress = await bridge.getAddress();
  console.log("✅ Bridge deployed to:", bridgeAddress);

  // Save deployment info
  const deployment = {
    network: "sepolia",
    chainId: 11155111,
    wtbtcToken: wtbtcAddress,
    bridge: bridgeAddress,
    bitcoinAddress: bitcoinAddress,
    deployer: deployer.address,
    timestamp: Date.now()
  };

  fs.writeFileSync(
    'real_deployment_sepolia.json',
    JSON.stringify(deployment, null, 2)
  );

  console.log("\n" + "=".repeat(80));
  console.log("✅ REAL DEPLOYMENT COMPLETE!");
  console.log("=".repeat(80));
  console.log("WTBTC Token:", wtbtcAddress);
  console.log("Bridge:", bridgeAddress);
  console.log("Network: Sepolia");
  console.log("Explorer:", `https://sepolia.etherscan.io/address/${wtbtcAddress}`);
  console.log("=".repeat(80));
  console.log("\n💡 Import to MetaMask:");
  console.log("   1. Open MetaMask");
  console.log("   2. Switch to Sepolia network");
  console.log("   3. Click 'Import tokens'");
  console.log("   4. Paste token address:", wtbtcAddress);
  console.log("   5. Symbol: WTBTC");
  console.log("   6. Decimals: 8");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

#### Step 7: Update hardhat.config.js
```javascript
require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC || "https://rpc.sepolia.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 11155111
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};
```

#### Step 8: Deploy for Real!
```bash
# Copy contracts to Hardhat directory
cp contracts/WTBTC_Enhanced.sol contracts/
cp contracts/WTBTCBridge.sol contracts/

# Deploy to Sepolia
npx hardhat run real_deploy_sepolia.js --network sepolia
```

#### Step 9: Get Your Real Address!
```bash
# After deployment completes, check the output:
cat real_deployment_sepolia.json

# You'll see REAL addresses like:
# "wtbtcToken": "0x1234567890abcdef..."
# "bridge": "0xabcdef1234567890..."
```

### Option 2: Deploy to Monad Testnet (FREE)

#### Step 1: Get Monad Testnet Tokens
```bash
# Visit Monad faucet:
https://www.alchemy.com/faucets/monad-testnet

# Enter your Ethereum address
# Receive free MON tokens
```

#### Step 2: Add Monad to MetaMask
```bash
Network Name: Monad Testnet
RPC URL: https://testnet.monad.xyz
Chain ID: 41454
Currency Symbol: MON
Explorer: https://explorer.testnet.monad.xyz
```

#### Step 3: Deploy (same process as Sepolia)
```bash
# Update hardhat.config.js with Monad network
# Run deployment script
```

## Import Token to MetaMask

Once you have REAL contract addresses:

### Method 1: MetaMask Desktop/Extension
1. Open MetaMask
2. Switch to the network you deployed to (Sepolia or Monad)
3. Scroll down and click **"Import tokens"**
4. Click **"Custom token"** tab
5. Enter:
   - **Token Contract Address**: `0x...` (your real address)
   - **Token Symbol**: `WTBTC`
   - **Token Decimals**: `8`
6. Click **"Add Custom Token"**
7. Click **"Import Tokens"**
8. Done! Your WTBTC balance will appear

### Method 2: MetaMask Mobile
1. Open MetaMask app
2. Tap hamburger menu (≡)
3. Tap **"Import Tokens"**
4. Paste your token contract address
5. Symbol and decimals auto-fill
6. Tap **"Import"**

### Method 3: Direct Link (After Real Deployment)
```bash
# For Sepolia
https://sepolia.etherscan.io/token/YOUR_REAL_ADDRESS

# For Monad
https://explorer.testnet.monad.xyz/token/YOUR_REAL_ADDRESS
```

## Quick Command Reference

```bash
# Get testnet ETH
https://sepoliafaucet.com

# Get Monad tokens
https://www.alchemy.com/faucets/monad-testnet

# Deploy to Sepolia
npx hardhat run real_deploy_sepolia.js --network sepolia

# View deployment
cat real_deployment_sepolia.json

# Import to MetaMask
# Token Address: [from deployment output]
# Symbol: WTBTC
# Decimals: 8
```

## Costs

### Testnet (Sepolia/Monad)
- **Deployment Cost**: FREE (testnet tokens)
- **Transaction Fees**: FREE (testnet tokens)
- **Faucet Tokens**: FREE

### Mainnet (Real Ethereum)
- **Deployment Cost**: ~$50-200 in ETH (gas fees)
- **Transaction Fees**: Variable (depends on gas prices)
- **Risk**: Real money involved

## Why Current Addresses Don't Work

The addresses `0xAAAA...` and `0xBBBB...` are:
- ❌ Not real blockchain contracts
- ❌ Won't show in block explorers
- ❌ Can't be imported to wallets
- ❌ Are placeholder/simulation addresses

To get addresses that:
- ✅ Show in block explorers
- ✅ Can be imported to MetaMask
- ✅ Actually hold tokens
- ✅ Can be transferred/traded

You **must deploy for real** following the steps above.

## Need Help?

If you want to deploy for real:
1. Get testnet ETH from the faucet (FREE)
2. Run the deployment script
3. I'll help you through any errors
4. You'll get real contract addresses!

Would you like me to help you deploy for real right now?
