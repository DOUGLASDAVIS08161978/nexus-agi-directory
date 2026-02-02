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
  console.log("\n🚀 COMPLETE UNISWAP V3 POOL SETUP\n");
  console.log("═".repeat(70));

  // Read config
  const config = JSON.parse(fs.readFileSync('pool_config.json', 'utf8'));
  const { wallet, privateKey, price } = config;

  // Setup provider and signer
  const provider = new ethers.JsonRpcProvider(BASE_RPC);
  const signer = new ethers.Wallet(privateKey, provider);

  console.log(`Wallet: ${wallet}`);
  console.log(`Target Price: 1 TBTC = ${price} ETH\n`);

  // ====================================================================
  // STEP 1: CHECK BALANCES
  // ====================================================================
  console.log("═".repeat(70));
  console.log("STEP 1: CHECKING BALANCES");
  console.log("═".repeat(70));

  const ethBalance = await provider.getBalance(wallet);
  console.log(`ETH: ${ethers.formatEther(ethBalance)} ETH`);

  const erc20Abi = ["function balanceOf(address) view returns (uint256)"];

  const wethContract = new ethers.Contract(WETH, erc20Abi, provider);
  const wethBalance = await wethContract.balanceOf(wallet);
  console.log(`WETH: ${ethers.formatEther(wethBalance)} WETH`);

  const tbtcContract = new ethers.Contract(TBTC, erc20Abi, provider);
  const tbtcBalance = await tbtcContract.balanceOf(wallet);
  console.log(`TBTC: ${ethers.formatUnits(tbtcBalance, 8)} TBTC\n`);

  if (tbtcBalance === 0n) {
    console.log("❌ No TBTC! You need TBTC from contract 0x5B060693a0eB04e8ea43E5aDfC99FE5B7B92d53e");
    process.exit(1);
  }

  // ====================================================================
  // STEP 2: WRAP ETH IF NEEDED
  // ====================================================================
  console.log("═".repeat(70));
  console.log("STEP 2: WRAP ETH TO WETH");
  console.log("═".repeat(70));

  if (wethBalance < ethers.parseEther("0.001")) {
    try {
      console.log("\nWrapping 0.0004 ETH...");
      const wrapTx = await signer.sendTransaction({
        to: WETH,
        value: ethers.parseEther("0.0004"),
        gasLimit: 50000
      });
      console.log(`TX: ${wrapTx.hash}`);
      await wrapTx.wait();
      console.log("✅ Wrapped!");
      await sleep(2000);
    } catch (error) {
      console.error(`❌ Error: ${error.message}`);
      process.exit(1);
    }
  } else {
    console.log("\n✅ Already have WETH");
  }

  // ====================================================================
  // STEP 3: APPROVE TOKENS
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 3: APPROVING TOKENS");
  console.log("═".repeat(70));

  const approveAbi = [
    "function approve(address spender, uint256 amount) returns (bool)",
    "function allowance(address owner, address spender) view returns (uint256)"
  ];

  // Approve TBTC
  try {
    const tbtcWithSigner = new ethers.Contract(TBTC, approveAbi, signer);
    const tbtcAllowance = await tbtcWithSigner.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);

    if (tbtcAllowance < ethers.parseUnits("1", 8)) {
      console.log("\nApproving TBTC...");
      const tx = await tbtcWithSigner.approve(NONFUNGIBLE_POSITION_MANAGER, ethers.MaxUint256, { gasLimit: 100000 });
      await tx.wait();
      console.log("✅ TBTC approved");
      await sleep(2000);
    } else {
      console.log("\n✅ TBTC already approved");
    }
  } catch (error) {
    console.error(`❌ TBTC approval error: ${error.message}`);
    process.exit(1);
  }

  // Approve WETH
  try {
    const wethWithSigner = new ethers.Contract(WETH, approveAbi, signer);
    const wethAllowance = await wethWithSigner.allowance(wallet, NONFUNGIBLE_POSITION_MANAGER);

    if (wethAllowance < ethers.parseEther("0.001")) {
      console.log("\nApproving WETH...");
      const tx = await wethWithSigner.approve(NONFUNGIBLE_POSITION_MANAGER, ethers.MaxUint256, { gasLimit: 100000 });
      await tx.wait();
      console.log("✅ WETH approved");
      await sleep(2000);
    } else {
      console.log("✅ WETH already approved");
    }
  } catch (error) {
    console.error(`❌ WETH approval error: ${error.message}`);
    process.exit(1);
  }

  // ====================================================================
  // STEP 4: GET OR CREATE POOL
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 4: GET OR CREATE POOL");
  console.log("═".repeat(70));

  const factoryAbi = [
    "function getPool(address tokenA, address tokenB, uint24 fee) view returns (address)",
    "function createPool(address tokenA, address tokenB, uint24 fee) external returns (address pool)"
  ];
  const factory = new ethers.Contract(UNISWAP_V3_FACTORY, factoryAbi, provider);

  let poolAddress = await factory.getPool(WETH, TBTC, 3000);

  if (poolAddress === "0x0000000000000000000000000000000000000000") {
    try {
      console.log("\nCreating pool...");
      const tx = await factory.connect(signer).createPool(WETH, TBTC, 3000, { gasLimit: 5000000 });
      const receipt = await tx.wait();
      console.log(`✅ Pool created! TX: ${tx.hash}`);
      await sleep(2000);

      // Get pool address again
      poolAddress = await factory.getPool(WETH, TBTC, 3000);
    } catch (error) {
      if (error.message.includes("Already exists")) {
        console.log("✅ Pool already exists");
        poolAddress = await factory.getPool(WETH, TBTC, 3000);
      } else {
        console.error(`❌ Error: ${error.message}`);
        process.exit(1);
      }
    }
  } else {
    console.log(`✅ Pool exists at: ${poolAddress}`);
  }

  // ====================================================================
  // STEP 5: INITIALIZE POOL
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 5: INITIALIZE POOL WITH PRICE");
  console.log("═".repeat(70));

  const poolAbi = [
    "function initialize(uint160 sqrtPriceX96) external",
    "function slot0() external view returns (uint160 sqrtPriceX96, int24 tick, uint16 observationIndex, uint16 observationCardinality, uint16 observationCardinalityNext, uint8 feeProtocol, bool unlocked)"
  ];
  const pool = new ethers.Contract(poolAddress, poolAbi, signer);

  try {
    const slot0 = await pool.slot0();

    if (slot0.sqrtPriceX96 === 0n) {
      // Pool not initialized
      const sqrtPriceX96 = BigInt(Math.floor(Math.sqrt(price) * (2 ** 96)));
      console.log(`\nInitializing pool with price ${price} ETH per TBTC`);
      console.log(`sqrtPriceX96: ${sqrtPriceX96.toString()}`);

      const initTx = await pool.initialize(sqrtPriceX96, { gasLimit: 500000 });
      console.log(`TX: ${initTx.hash}`);
      await initTx.wait();
      console.log("✅ Pool initialized!");
      await sleep(3000);
    } else {
      console.log("\n✅ Pool already initialized");
      console.log(`Current sqrtPriceX96: ${slot0.sqrtPriceX96.toString()}`);
      console.log(`Current tick: ${slot0.tick}`);
    }
  } catch (error) {
    if (error.message.includes("Already initialized")) {
      console.log("✅ Pool already initialized");
    } else {
      console.error(`❌ Error: ${error.message}`);
      process.exit(1);
    }
  }

  // ====================================================================
  // STEP 6: ADD LIQUIDITY
  // ====================================================================
  console.log("\n" + "═".repeat(70));
  console.log("STEP 6: ADD LIQUIDITY");
  console.log("═".repeat(70));

  try {
    const positionManagerAbi = [
      "function mint(tuple(address token0, address token1, uint24 fee, int24 tickLower, int24 tickUpper, uint256 amount0Desired, uint256 amount1Desired, uint256 amount0Min, uint256 amount1Min, address recipient, uint256 deadline)) external returns (uint256 tokenId, uint128 liquidity, uint256 amount0, uint256 amount1)"
    ];
    const positionManager = new ethers.Contract(NONFUNGIBLE_POSITION_MANAGER, positionManagerAbi, signer);

    const params = {
      token0: WETH,
      token1: TBTC,
      fee: 3000,
      tickLower: -887220,
      tickUpper: 887220,
      amount0Desired: ethers.parseEther("0.0002"),
      amount1Desired: ethers.parseUnits("0.00001", 8),
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

    const receipt = await mintTx.wait();
    console.log("✅ Liquidity added!");

    console.log("\n" + "═".repeat(70));
    console.log("🎉 SUCCESS! POOL IS LIVE!");
    console.log("═".repeat(70));
    console.log(`\nPool: ${poolAddress}`);
    console.log(`Price: 1 TBTC = ${price} ETH`);
    console.log(`\n🔍 View on BaseScan:`);
    console.log(`https://sepolia.basescan.org/address/${poolAddress}`);
  } catch (error) {
    console.error(`\n❌ Error adding liquidity: ${error.message}`);
    console.error("This might mean the price ratio doesn't match the pool's current price.");
    console.error("Try adjusting the amounts in the mint parameters.");
    process.exit(1);
  }
}

main().catch(console.error);
