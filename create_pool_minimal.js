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
  console.log("\n🚀 CREATING UNISWAP V3 POOL - MINIMAL LIQUIDITY VERSION\n");

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

  // Check balances
  const ethBalance = await provider.getBalance(wallet);
  console.log(`ETH Balance: ${ethers.formatEther(ethBalance)} ETH`);

  const wethAbi = ["function balanceOf(address) view returns (uint256)"];
  const wethContract = new ethers.Contract(WETH, wethAbi, provider);
  const wethBalance = await wethContract.balanceOf(wallet);
  console.log(`WETH Balance: ${ethers.formatEther(wethBalance)} WETH`);

  const tbtcAbi = ["function balanceOf(address) view returns (uint256)"];
  const tbtcContract = new ethers.Contract(token1, tbtcAbi, provider);
  const tbtcBalance = await tbtcContract.balanceOf(wallet);
  console.log(`TBTC Balance: ${ethers.formatUnits(tbtcBalance, 8)} TBTC\n`);

  if (ethBalance < ethers.parseEther("0.0005")) {
    console.log("❌ Insufficient ETH for gas fees!");
    console.log("Need at least 0.001 ETH for gas");
    console.log("Get testnet ETH from: https://www.alchemy.com/faucets/base-sepolia");
    process.exit(1);
  }

  if (tbtcBalance < ethers.parseUnits("0.0001", 8)) {
    console.log("❌ Insufficient TBTC balance!");
    console.log(`You need at least 0.0001 TBTC, but have ${ethers.formatUnits(tbtcBalance, 8)} TBTC`);
    process.exit(1);
  }

  // ====================================================================
  // STEP 1: WRAP MINIMAL ETH TO WETH (skip if we have enough)
  // ====================================================================
  const neededWeth = ethers.parseEther("0.002"); // Minimal 0.002 WETH needed

  if (wethBalance < neededWeth) {
    console.log("═".repeat(60));
    console.log("STEP 1: WRAP ETH TO WETH");
    console.log("═".repeat(60));

    // Wrap a small amount, leaving room for gas
    const wrapAmount = ethers.parseEther("0.0003");

    try {
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
        console.log("✅ Successfully wrapped ETH to WETH!");
      } else {
        throw new Error("Wrap transaction failed");
      }
    } catch (error) {
      console.error("\n❌ Error:", error.message);
      process.exit(1);
    }
  } else {
    console.log("✅ Already have enough WETH\n");
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
    const tbtcContractWithSigner = new ethers.Contract(token1, erc20Abi, signer);

    const tbtcAllowance = await tbtcContractWithSigner.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);

    if (tbtcAllowance < ethers.parseUnits("0.0001", 8)) {
      console.log("\nApproving TBTC...");
      const approveTx = await tbtcContractWithSigner.approve(
        NONFUNGIBLE_POSITION_MANAGER,
        ethers.MaxUint256,
        { gasLimit: 100000 }
      );

      console.log(`TX: ${approveTx.hash}`);
      console.log("Waiting for confirmation...");
      await approveTx.wait();
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
    const wethContractWithSigner = new ethers.Contract(WETH, erc20Abi, signer);

    const wethAllowance = await wethContractWithSigner.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);

    if (wethAllowance < ethers.parseEther("0.001")) {
      console.log("\nApproving WETH...");
      const approveTx = await wethContractWithSigner.approve(
        NONFUNGIBLE_POSITION_MANAGER,
        ethers.MaxUint256,
        { gasLimit: 100000 }
      );

      console.log(`TX: ${approveTx.hash}`);
      console.log("Waiting for confirmation...");
      await approveTx.wait();
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
    const sqrtPriceX96 = BigInt(Math.floor(Math.sqrt(price) * (2 ** 96)));

    console.log(`\nInitializing pool with price: ${price} ETH per TBTC`);
    console.log(`sqrtPriceX96: ${sqrtPriceX96.toString()}`);

    const positionManagerAbi = [
      "function mint(tuple(address token0, address token1, uint24 fee, int24 tickLower, int24 tickUpper, uint256 amount0Desired, uint256 amount1Desired, uint256 amount0Min, uint256 amount1Min, address recipient, uint256 deadline)) external returns (uint256 tokenId, uint128 liquidity, uint256 amount0, uint256 amount1)"
    ];
    const positionManager = new ethers.Contract(NONFUNGIBLE_POSITION_MANAGER, positionManagerAbi, signer);

    // Use minimal amounts that we actually have
    const params = {
      token0: token0,
      token1: token1,
      fee: 3000,
      tickLower: -887220,
      tickUpper: 887220,
      amount0Desired: ethers.parseEther("0.0002"),     // Tiny WETH amount
      amount1Desired: ethers.parseUnits("0.00001", 8), // Tiny TBTC amount (0.00001 BTC)
      amount0Min: 0,
      amount1Min: 0,
      recipient: wallet,
      deadline: Math.floor(Date.now() / 1000) + 3600
    };

    console.log("\nAdding minimal liquidity:");
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
    console.log("\n💡 You can add more liquidity once you get more testnet ETH!");
  } catch (error) {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  }
}

main().catch(console.error);
