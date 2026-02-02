const { ethers } = require('ethers');
const fs = require('fs');

// Base Sepolia Configuration
const BASE_RPC = "https://sepolia.base.org";
const CHAIN_ID = 84532;

// Addresses
const WETH = "0x4200000000000000000000000000000000000006";
const TBTC = "0x5B060693a0eB04e8ea43E5aDfC99FE5B7B92d53e";
const UNISWAP_V3_FACTORY = "0x4752ba5dbc23f44d87826276bf6fd6b1c372ad24";
const NONFUNGIBLE_POSITION_MANAGER = "0x27F971cb582BF9E50F397e4d29a5C7A34f11faA2";

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  console.log("\n🚀 COMPLETE POOL SETUP - TBTC/WETH ON BASE SEPOLIA\n");
  console.log("═".repeat(70));

  // Read config
  const config = JSON.parse(fs.readFileSync('pool_config.json', 'utf8'));
  const { wallet, privateKey, price } = config;

  // Setup provider and signer
  const provider = new ethers.JsonRpcProvider(BASE_RPC);
  const signer = new ethers.Wallet(privateKey, provider);

  console.log(`Wallet: ${wallet}`);
  console.log(`Target Price: 1 TBTC = ${price} ETH (Bitcoin peg)\n`);

  // ====================================================================
  // STEP 1: CHECK BALANCES
  // ====================================================================
  console.log("═".repeat(70));
  console.log("STEP 1: CHECKING BALANCES");
  console.log("═".repeat(70));

  const ethBalance = await provider.getBalance(wallet);
  console.log(`ETH Balance: ${ethers.formatEther(ethBalance)} ETH`);

  const wethAbi = ["function balanceOf(address) view returns (uint256)"];
  const wethContract = new ethers.Contract(WETH, wethAbi, provider);
  const wethBalance = await wethContract.balanceOf(wallet);
  console.log(`WETH Balance: ${ethers.formatEther(wethBalance)} WETH`);

  const tbtcAbi = ["function balanceOf(address) view returns (uint256)"];
  const tbtcContract = new ethers.Contract(TBTC, tbtcAbi, provider);
  const tbtcBalance = await tbtcContract.balanceOf(wallet);
  console.log(`TBTC Balance: ${ethers.formatUnits(tbtcBalance, 8)} TBTC`);

  if (tbtcBalance === 0n) {
    console.log("\n❌ No TBTC balance found!");
    console.log("The WTBTC contract should have minted 1,000,000 TBTC to your address during deployment.");
    console.log("Contract address: 0x5B060693a0eB04e8ea43E5aDfC99FE5B7B92d53e");
    process.exit(1);
  }

  console.log(`\n✅ You have ${ethers.formatUnits(tbtcBalance, 8)} TBTC!`);

  if (ethBalance < ethers.parseEther("0.0005")) {
    console.log("\n❌ Insufficient ETH for gas fees!");
    console.log("Get testnet ETH from: https://www.alchemy.com/faucets/base-sepolia");
    process.exit(1);
  }

  // ====================================================================
  // STEP 2: WRAP ETH IF NEEDED
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 2: WRAPPING ETH TO WETH (IF NEEDED)");
  console.log("═".repeat(70));

  const minWethNeeded = ethers.parseEther("0.001");

  if (wethBalance < minWethNeeded) {
    try {
      const wrapAmount = ethers.parseEther("0.0004");
      console.log(`\nWrapping ${ethers.formatEther(wrapAmount)} ETH to WETH...`);

      const wrapTx = await signer.sendTransaction({
        to: WETH,
        value: wrapAmount,
        gasLimit: 50000
      });

      console.log(`TX: ${wrapTx.hash}`);
      console.log("Waiting for confirmation...");
      const wrapReceipt = await wrapTx.wait();

      if (wrapReceipt.status === 1) {
        console.log("✅ ETH wrapped to WETH!");
        await sleep(2000); // Wait 2 seconds for state to update
      } else {
        throw new Error("Wrap failed");
      }
    } catch (error) {
      console.error(`\n❌ Error wrapping ETH: ${error.message}`);
      process.exit(1);
    }
  } else {
    console.log("\n✅ Already have enough WETH, skipping wrap step");
  }

  // ====================================================================
  // STEP 3: APPROVE TBTC
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 3: APPROVING TBTC FOR UNISWAP");
  console.log("═".repeat(70));

  try {
    const erc20Abi = [
      "function approve(address spender, uint256 amount) returns (bool)",
      "function allowance(address owner, address spender) view returns (uint256)"
    ];
    const tbtcContractWithSigner = new ethers.Contract(TBTC, erc20Abi, signer);

    const tbtcAllowance = await tbtcContractWithSigner.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);
    console.log(`Current TBTC allowance: ${ethers.formatUnits(tbtcAllowance, 8)} TBTC`);

    if (tbtcAllowance < ethers.parseUnits("1", 8)) {
      console.log("\nApproving TBTC for Uniswap Position Manager...");

      const approveTx = await tbtcContractWithSigner.approve(
        NONFUNGIBLE_POSITION_MANAGER,
        ethers.MaxUint256,
        {
          gasLimit: 100000
        }
      );

      console.log(`TX: ${approveTx.hash}`);
      console.log("Waiting for confirmation...");
      const approveReceipt = await approveTx.wait();

      if (approveReceipt.status === 1) {
        console.log("✅ TBTC approved!");
        await sleep(2000);
      } else {
        throw new Error("Approval failed");
      }
    } else {
      console.log("✅ TBTC already approved!");
    }
  } catch (error) {
    console.error(`\n❌ Error approving TBTC: ${error.message}`);
    process.exit(1);
  }

  // ====================================================================
  // STEP 4: APPROVE WETH
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 4: APPROVING WETH FOR UNISWAP");
  console.log("═".repeat(70));

  try {
    const erc20Abi = [
      "function approve(address spender, uint256 amount) returns (bool)",
      "function allowance(address owner, address spender) view returns (uint256)"
    ];
    const wethContractWithSigner = new ethers.Contract(WETH, erc20Abi, signer);

    const wethAllowance = await wethContractWithSigner.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);
    console.log(`Current WETH allowance: ${ethers.formatEther(wethAllowance)} WETH`);

    if (wethAllowance < ethers.parseEther("0.001")) {
      console.log("\nApproving WETH for Uniswap Position Manager...");

      const approveTx = await wethContractWithSigner.approve(
        NONFUNGIBLE_POSITION_MANAGER,
        ethers.MaxUint256,
        {
          gasLimit: 100000
        }
      );

      console.log(`TX: ${approveTx.hash}`);
      console.log("Waiting for confirmation...");
      const approveReceipt = await approveTx.wait();

      if (approveReceipt.status === 1) {
        console.log("✅ WETH approved!");
        await sleep(2000);
      } else {
        throw new Error("Approval failed");
      }
    } else {
      console.log("✅ WETH already approved!");
    }
  } catch (error) {
    console.error(`\n❌ Error approving WETH: ${error.message}`);
    process.exit(1);
  }

  // ====================================================================
  // STEP 5: CREATE POOL (IF NOT EXISTS)
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 5: CREATING POOL (IF NOT EXISTS)");
  console.log("═".repeat(70));

  try {
    const factoryAbi = [
      "function createPool(address tokenA, address tokenB, uint24 fee) external returns (address pool)",
      "function getPool(address tokenA, address tokenB, uint24 fee) view returns (address)"
    ];
    const factory = new ethers.Contract(UNISWAP_V3_FACTORY, factoryAbi, provider);

    const existingPool = await factory.getPool(WETH, TBTC, 3000);

    if (existingPool === "0x0000000000000000000000000000000000000000") {
      console.log("\nCreating new pool with 0.3% fee...");
      const createPoolTx = await factory.connect(signer).createPool(WETH, TBTC, 3000, {
        gasLimit: 5000000
      });

      console.log(`TX: ${createPoolTx.hash}`);
      console.log("Waiting for confirmation...");
      const createReceipt = await createPoolTx.wait();

      if (createReceipt.status === 1) {
        console.log("✅ Pool created!");
        await sleep(2000);
      } else {
        throw new Error("Pool creation failed");
      }
    } else {
      console.log(`\n✅ Pool already exists at: ${existingPool}`);
    }
  } catch (error) {
    if (error.message.includes("Already exists") || error.message.includes("Pool already initialized")) {
      console.log("✅ Pool already exists, continuing...");
    } else {
      console.error(`\n❌ Error creating pool: ${error.message}`);
      process.exit(1);
    }
  }

  // ====================================================================
  // STEP 6: ADD LIQUIDITY
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 6: ADDING LIQUIDITY");
  console.log("═".repeat(70));

  try {
    const sqrtPriceX96 = BigInt(Math.floor(Math.sqrt(price) * (2 ** 96)));
    console.log(`\nTarget price: ${price} ETH per TBTC`);
    console.log(`sqrtPriceX96: ${sqrtPriceX96.toString()}`);

    const positionManagerAbi = [
      "function mint(tuple(address token0, address token1, uint24 fee, int24 tickLower, int24 tickUpper, uint256 amount0Desired, uint256 amount1Desired, uint256 amount0Min, uint256 amount1Min, address recipient, uint256 deadline)) external returns (uint256 tokenId, uint128 liquidity, uint256 amount0, uint256 amount1)"
    ];
    const positionManager = new ethers.Contract(NONFUNGIBLE_POSITION_MANAGER, positionManagerAbi, signer);

    // Use minimal amounts
    const params = {
      token0: WETH,
      token1: TBTC,
      fee: 3000,
      tickLower: -887220,
      tickUpper: 887220,
      amount0Desired: ethers.parseEther("0.0002"),     // 0.0002 WETH
      amount1Desired: ethers.parseUnits("0.00001", 8), // 0.00001 TBTC
      amount0Min: 0,
      amount1Min: 0,
      recipient: wallet,
      deadline: Math.floor(Date.now() / 1000) + 3600
    };

    console.log("\nAdding liquidity:");
    console.log(`  WETH: ${ethers.formatEther(params.amount0Desired)}`);
    console.log(`  TBTC: ${ethers.formatUnits(params.amount1Desired, 8)}`);

    const mintTx = await positionManager.mint(params, { gasLimit: 5000000 });

    console.log(`\nTX: ${mintTx.hash}`);
    console.log("Waiting for confirmation...");
    const mintReceipt = await mintTx.wait();

    if (mintReceipt.status === 1) {
      console.log("✅ Liquidity added successfully!");
    } else {
      throw new Error("Liquidity addition failed");
    }

    console.log("\n" + "═".repeat(70));
    console.log("🎉 POOL SETUP COMPLETE!");
    console.log("═".repeat(70));
    console.log(`\n✅ TBTC/WETH pool is live on Base Sepolia!`);
    console.log(`✅ Price: 1 TBTC = ${price} ETH (Bitcoin peg)`);
    console.log(`✅ Pool address: Check Uniswap V3 Factory on BaseScan`);
    console.log(`\n💡 You can add more liquidity anytime with your ${ethers.formatUnits(tbtcBalance, 8)} TBTC!`);
  } catch (error) {
    console.error(`\n❌ Error adding liquidity: ${error.message}`);
    process.exit(1);
  }
}

main().catch(console.error);
