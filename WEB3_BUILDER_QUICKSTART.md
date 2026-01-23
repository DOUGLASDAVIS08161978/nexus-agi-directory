# Autonomous Web3 Builder - Quick Start Guide

Get started building smart contracts with AI in under 5 minutes.

## Prerequisites

- Python 3.8+
- Node.js 16+ (optional, for Hardhat)
- 8GB RAM minimum
- Linux, macOS, or WSL2 on Windows

## Installation (5 minutes)

### Step 1: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama (keep this terminal open)
ollama serve
```

### Step 2: Download AI Model (in a new terminal)

```bash
# Download the model (this may take a few minutes)
ollama pull llama3.2

# Verify it's working
ollama run llama3.2 "Say hello"
```

### Step 3: Install Python Dependencies

```bash
cd nexus-agi-directory

# Install required packages
pip install requests web3 eth-account python-dotenv
```

### Step 4: Configure Environment

```bash
# Create .env file
cat > .env << EOF
PRIVATE_KEY=your_private_key_here_without_0x
SEPOLIA_RPC=https://rpc.sepolia.org
MONAD_RPC=https://testnet.monad.xyz
EOF
```

To get testnet tokens:
- **Sepolia ETH**: https://sepoliafaucet.com
- **Monad MON**: https://www.alchemy.com/faucets/monad-testnet

## Your First Smart Contract (2 minutes)

### Example 1: Simple ERC-20 Token

Create a file `my_first_token.py`:

```python
import asyncio
from autonomous_web3_builder import AutonomousWeb3Builder

async def main():
    # Initialize the builder
    builder = AutonomousWeb3Builder()

    # Check if system is ready
    initialized = await builder.initialize()
    if not initialized:
        print("Error: Make sure Ollama is running (ollama serve)")
        return

    # Define your goal in plain English
    goal = """
    Create a simple ERC-20 token:
    - Name: MyFirstToken
    - Symbol: MFT
    - Total supply: 1,000,000 tokens
    - 18 decimals
    - No special features
    """

    # Let AI build and deploy it
    result = await builder.autonomous_build(
        user_goal=goal,
        deploy_networks=["sepolia"]  # Deploy to Sepolia testnet
    )

    # Show results
    if result['status'] == 'success':
        print(f"\n✅ Token deployed successfully!")
        print(f"📍 Address: {result['deployments'][0]['address']}")
        print(f"🔗 Explorer: {result['deployments'][0]['explorer_url']}")
    else:
        print(f"\n❌ Deployment failed: {result['error']}")

# Run it
asyncio.run(main())
```

Run it:

```bash
python3 my_first_token.py
```

## Example 2: NFT Collection

```python
goal = """
Create an NFT collection:
- Name: MyNFTs
- Symbol: MNFT
- Max supply: 1000
- Public minting: 0.01 ETH per NFT
- Owner can mint for free
"""

result = await builder.autonomous_build(goal, ["sepolia"])
```

## Example 3: Staking Contract

```python
goal = """
Create a staking contract:
- Users stake ERC-20 tokens
- Earn 10% APY
- Minimum lock period: 7 days
- Withdraw rewards anytime
"""

result = await builder.autonomous_build(goal, ["sepolia"])
```

## Troubleshooting

### "Connection refused to localhost:11434"
**Problem**: Ollama is not running
**Solution**: Run `ollama serve` in a separate terminal

### "Model 'llama3.2' not found"
**Problem**: Model not downloaded
**Solution**: Run `ollama pull llama3.2`

### "Insufficient funds for gas"
**Problem**: No testnet ETH in wallet
**Solution**: Get testnet ETH from https://sepoliafaucet.com

## More Examples & Full Documentation

See [AUTONOMOUS_WEB3_BUILDER_README.md](AUTONOMOUS_WEB3_BUILDER_README.md) for:
- Complete architecture explanation
- Advanced usage examples
- Cross-chain bridging
- Security best practices
- Troubleshooting guide

**Happy building!** ✨
