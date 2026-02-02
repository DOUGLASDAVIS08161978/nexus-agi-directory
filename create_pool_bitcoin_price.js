const { ethers } = require('ethers');
const fs = require('fs');

// Base Sepolia Configuration
const BASE_RPC = "https://sepolia.base.org";
const CHAIN_ID = 84532;

// Addresses
const WETH = "0x4200000000000000000000000000000000000006";
const UNISWAP_V3_FACTORY = "0x4752ba5dbc23f44d87826276bf6fd6b1c372ad24";
const NONFUNGIBLE_POSITION_MANAGER = "0x27F971cb582BF9E50F397e4d29a5C7A34f11faA2";

async function main() {
  console.log("\n🚀 CREATING UNISWAP V3 POOL - BITCOIN PRICE (1 TBTC = ~20 ETH)\n");

  // Read config
  const config = JSON.parse(fs.readFileSync('pool_config.json', 'utf8'));
  const { token0, token1, price, wallet, privateKey } = config;

  console.log(`Wallet: ${wallet}`);
  console.log(`Token0 (WETH): ${token0}`);
  console.log(`Token1 (TBTC): ${token1}`);
  console.log(`Price: ${price} ETH per TBTC (Bitcoin peg)\n`);

  // Setup provider and signer
  const provider = new ethers.JsonRpcProvider(BASE_RPC);
  const signer = new ethers.Wallet(privateKey, provider);

  // Check WETH balance
  const wethAbi = ["function balanceOf(address) view returns (uint256)"];
  const wethContract = new ethers.Contract(WETH, wethAbi, provider);
  const wethBalance = await wethContract.balanceOf(wallet);

  console.log(`Current WETH balance: ${ethers.formatEther(wethBalance)} WETH`);

  // ====================================================================
  // STEP 1: WRAP MORE ETH IF NEEDED
  // ====================================================================
  if (wethBalance < ethers.parseEther("0.1")) {
    console.log("\n" + "═".repeat(60));
    console.log("STEP 1: WRAP ETH TO WETH");
    console.log("═".repeat(60));

    try {
      console.log("\nWrapping 0.1 ETH to WETH for liquidity...");

      const wrapTx = await signer.sendTransaction({
        to: WETH,
        value: ethers.parseEther("0.1"),
        gasLimit: 50000
      });

      console.log(`TX: ${wrapTx.hash}`);
      console.log("Waiting for confirmation...");
      const wrapReceipt = await wrapTx.wait();

      if (wrapReceipt.status === 1) {
        console.log("✅ Successfully wrapped ETH to WETH!");
      } else {
        throw new Error("Wrap transaction failed");
      }
    } catch (error) {
      console.error("\n❌ Error:", error.message);
      process.exit(1);
    }
  } else {
    console.log("✅ Already have enough WETH, skipping wrap step\n");
  }

  // ====================================================================
  // STEP 2: APPROVE TBTC
  // ====================================================================
  console.log("═".repeat(60));
  console.log("STEP 2: APPROVE TBTC FOR UNISWAP");
  console.log("═".repeat(60));

  try {
    const erc20Abi = [
      "function approve(address spender, uint256 amount) returns (bool)",
      "function allowance(address owner, address spender) view returns (uint256)"
    ];
    const tbtcContract = new ethers.Contract(token1, erc20Abi, signer);

    // Check current allowance
    const tbtcAllowance = await tbtcContract.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);

    if (tbtcAllowance < ethers.parseUnits("100", 8)) {
      console.log("\nApproving TBTC...");
      const approveTx1 = await tbtcContract.approve(
        NONFUNGIBLE_POSITION_MANAGER,
        ethers.MaxUint256,
        { gasLimit: 100000 }
      );

      console.log(`TX: ${approveTx1.hash}`);
      console.log("Waiting for confirmation...");
      await approveTx1.wait();
      console.log("✅ TBTC approved!");
    } else {
      console.log("✅ TBTC already approved!");
    }
  } catch (error) {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  }

  // ====================================================================
  // STEP 3: APPROVE WETH
  // ====================================================================
  console.log("\n" + "═".repeat(60));
  console.log("STEP 3: APPROVE WETH FOR UNISWAP");
  console.log("═".repeat(60));

  try {
    const erc20Abi = [
      "function approve(address spender, uint256 amount) returns (bool)",
      "function allowance(address owner, address spender) view returns (uint256)"
    ];
    const wethContract = new ethers.Contract(WETH, erc20Abi, signer);

    // Check current allowance
    const wethAllowance = await wethContract.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);

    if (wethAllowance < ethers.parseEther("1")) {
      console.log("\nApproving WETH...");
      const approveTx2 = await wethContract.approve(
        NONFUNGIBLE_POSITION_MANAGER,
        ethers.MaxUint256,
        { gasLimit: 100000 }
      );

      console.log(`TX: ${approveTx2.hash}`);
      console.log("Waiting for confirmation...");
      await approveTx2.wait();
      console.log("✅ WETH approved!");
    } else {
      console.log("✅ WETH already approved!");
    }
  } catch (error) {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  }

  // ====================================================================
  // STEP 4: CREATE POOL
  // ====================================================================
  console.log("\n" + "═".repeat(60));
  console.log("STEP 4: CREATE POOL");
  console.log("═".repeat(60));

  try {
    const factoryAbi = [
      "function createPool(address tokenA, address tokenB, uint24 fee) external returns (address pool)",
      "function getPool(address tokenA, address tokenB, uint24 fee) view returns (address)"
    ];
    const factory = new ethers.Contract(UNISWAP_V3_FACTORY, factoryAbi, provider);

    // Check if pool exists
    const existingPool = await factory.getPool(token0, token1, 3000);

    if (existingPool === "0x0000000000000000000000000000000000000000") {
      console.log("\nCreating pool with 0.3% fee...");
      const createPoolTx = await factory.connect(signer).createPool(token0, token1, 3000, { gasLimit: 5000000 });

      console.log(`TX: ${createPoolTx.hash}`);
      console.log("Waiting for confirmation...");
      await createPoolTx.wait();
      console.log("✅ Pool created!");
    } else {
      console.log(`✅ Pool already exists at: ${existingPool}`);
    }
  } catch (error) {
    if (error.message.includes("Already exists")) {
      console.log("ℹ️  Pool already exists, continuing...");
    } else {
      console.error("\n❌ Error:", error.message);
      process.exit(1);
    }
  }

  // ====================================================================
  // STEP 5: INITIALIZE POOL & ADD LIQUIDITY
  // ====================================================================
  console.log("\n" + "═".repeat(60));
  console.log("STEP 5: INITIALIZE & ADD LIQUIDITY");
  console.log("═".repeat(60));

  try {
    // Calculate sqrtPriceX96 for price = 20 ETH per TBTC
    // sqrtPriceX96 = sqrt(price) * 2^96
    const sqrtPriceX96 = BigInt(Math.floor(Math.sqrt(price) * (2 ** 96)));

    console.log(`\nInitializing pool with price: ${price} ETH per TBTC`);
    console.log(`sqrtPriceX96: ${sqrtPriceX96.toString()}`);

    const positionManagerAbi = [
      "function mint(tuple(address token0, address token1, uint24 fee, int24 tickLower, int24 tickUpper, uint256 amount0Desired, uint256 amount1Desired, uint256 amount0Min, uint256 amount1Min, address recipient, uint256 deadline)) external returns (uint256 tokenId, uint128 liquidity, uint256 amount0, uint256 amount1)"
    ];
    const positionManager = new ethers.Contract(NONFUNGIBLE_POSITION_MANAGER, positionManagerAbi, signer);

    const params = {
      token0: token0,
      token1: token1,
      fee: 3000,
      tickLower: -887220,  // Full range
      tickUpper: 887220,
      amount0Desired: ethers.parseEther("0.02"),  // 0.02 WETH
      amount1Desired: ethers.parseUnits("0.001", 8),  // 0.001 TBTC
      amount0Min: 0,
      amount1Min: 0,
      recipient: wallet,
      deadline: Math.floor(Date.now() / 1000) + 3600
    };

    console.log("\nAdding liquidity:");
    console.log(`  WETH: ${ethers.formatEther(params.amount0Desired)}`);
    console.log(`  TBTC: ${ethers.formatUnits(params.amount1Desired, 8)}`);

    const mintTx = await positionManager.mint(params, { gasLimit: 5000000 });

    console.log(`TX: ${mintTx.hash}`);
    console.log("Waiting for confirmation...");
    await mintTx.wait();
    console.log("✅ Liquidity added!");

    console.log("\n" + "═".repeat(60));
    console.log("🎉 POOL CREATION COMPLETE!");
    console.log("═".repeat(60));
    console.log("\n✅ Your TBTC/WETH pool is now live on Base Sepolia!");
    console.log(`✅ Price: 1 TBTC = ${price} ETH (Bitcoin peg)`);
  } catch (error) {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  }
}

main().catch(console.error);
