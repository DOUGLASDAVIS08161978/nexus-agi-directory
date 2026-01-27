// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title WTBTC Enhanced - Wrapped Testnet Bitcoin
 * @dev ERC-20 token representing Bitcoin with 1:1 peg
 * @notice This token bridges between Bitcoin and Ethereum networks
 *
 * Features:
 * - 1,000,000 initial supply (1M WTBTC = 1M BTC equivalent)
 * - 8 decimals (matching Bitcoin)
 * - Mintable by authorized bridge contracts
 * - Burnable for redemption back to Bitcoin
 * - Pausable for emergency situations
 * - 1:1 peg with BTC maintained by bridge collateral
 * - Cross-chain bridge support
 */
contract WTBTC_Enhanced is ERC20, ERC20Burnable, Ownable, Pausable {
    // 8 decimals to match Bitcoin precision
    uint8 private constant DECIMALS = 8;

    // Initial supply: 1,000,000 WTBTC (1M * 10^8)
    uint256 private constant INITIAL_SUPPLY = 1_000_000 * 10**8;

    // Mapping of authorized minters (bridge contracts)
    mapping(address => bool) public authorizedMinters;

    // Mapping of bridge addresses for cross-chain operations
    mapping(address => bool) public authorizedBridges;

    // Total BTC locked in the bridge (for 1:1 peg tracking)
    uint256 public totalBTCLocked;

    // Bitcoin address for deposits (stored as string for reference)
    string public bitcoinDepositAddress;

    // Burn records for tracking redemptions
    mapping(bytes32 => BurnRecord) public burnRecords;

    struct BurnRecord {
        address burner;
        uint256 amount;
        string bitcoinAddress;
        uint256 timestamp;
        bool processed;
        string btcTxHash;
    }

    // Events for bridge operations
    event Minted(address indexed to, uint256 amount, string btcTxHash);
    event Burned(address indexed from, uint256 amount, string btcAddress, bytes32 indexed burnId);
    event BridgeDeposit(address indexed user, uint256 amount, string btcTxHash);
    event BridgeWithdrawal(address indexed user, uint256 amount, string btcAddress, bytes32 indexed burnId);
    event BurnProcessed(bytes32 indexed burnId, string btcTxHash);
    event MinterAuthorized(address indexed minter);
    event MinterRevoked(address indexed minter);
    event BridgeAuthorized(address indexed bridge);
    event BridgeRevoked(address indexed bridge);
    event BTCLocked(uint256 amount, string btcTxHash);
    event BTCUnlocked(uint256 amount, string btcAddress);

    /**
     * @dev Constructor that mints initial supply to deployer
     * @param _bitcoinDepositAddress The Bitcoin address for receiving deposits
     */
    constructor(string memory _bitcoinDepositAddress) ERC20("Wrapped Testnet Bitcoin", "WTBTC") {
        bitcoinDepositAddress = _bitcoinDepositAddress;
        _mint(msg.sender, INITIAL_SUPPLY);

        // Authorize deployer as initial minter
        authorizedMinters[msg.sender] = true;
        authorizedBridges[msg.sender] = true;

        // Initial BTC locked equals initial supply (1:1 peg)
        totalBTCLocked = INITIAL_SUPPLY;

        emit MinterAuthorized(msg.sender);
        emit BridgeAuthorized(msg.sender);
    }

    /**
     * @dev Returns 8 decimals to match Bitcoin
     */
    function decimals() public pure override returns (uint8) {
        return DECIMALS;
    }

    /**
     * @dev Authorize a bridge contract to mint tokens
     * @param minter Address of the bridge contract
     */
    function authorizeMinter(address minter) external onlyOwner {
        require(minter != address(0), "WTBTC: zero address");
        require(!authorizedMinters[minter], "WTBTC: already authorized");

        authorizedMinters[minter] = true;
        emit MinterAuthorized(minter);
    }

    /**
     * @dev Revoke minting authorization
     * @param minter Address to revoke
     */
    function revokeMinter(address minter) external onlyOwner {
        require(authorizedMinters[minter], "WTBTC: not authorized");

        authorizedMinters[minter] = false;
        emit MinterRevoked(minter);
    }

    /**
     * @dev Authorize a bridge contract
     * @param bridge Address of the bridge contract
     */
    function authorizeBridge(address bridge) external onlyOwner {
        require(bridge != address(0), "WTBTC: zero address");
        require(!authorizedBridges[bridge], "WTBTC: already authorized");

        authorizedBridges[bridge] = true;
        emit BridgeAuthorized(bridge);
    }

    /**
     * @dev Revoke bridge authorization
     * @param bridge Address to revoke
     */
    function revokeBridge(address bridge) external onlyOwner {
        require(authorizedBridges[bridge], "WTBTC: not authorized");

        authorizedBridges[bridge] = false;
        emit BridgeRevoked(bridge);
    }

    /**
     * @dev Mint new WTBTC tokens (only by authorized bridges)
     * @param to Recipient address
     * @param amount Amount to mint
     * @param btcTxHash Bitcoin transaction hash proving BTC deposit
     */
    function mint(address to, uint256 amount, string memory btcTxHash) external whenNotPaused {
        require(authorizedMinters[msg.sender], "WTBTC: not authorized minter");
        require(to != address(0), "WTBTC: mint to zero address");
        require(amount > 0, "WTBTC: amount must be positive");

        // Update total BTC locked (maintaining 1:1 peg)
        totalBTCLocked += amount;

        _mint(to, amount);
        emit Minted(to, amount, btcTxHash);
        emit BTCLocked(amount, btcTxHash);
    }

    /**
     * @dev Burn WTBTC to redeem BTC on Bitcoin network
     * @param amount Amount to burn
     * @param btcAddress Bitcoin address to receive the BTC
     * @return burnId Unique identifier for this burn operation
     */
    function burnForBTC(uint256 amount, string memory btcAddress) external whenNotPaused returns (bytes32 burnId) {
        require(amount > 0, "WTBTC: amount must be positive");
        require(bytes(btcAddress).length > 0, "WTBTC: invalid BTC address");
        require(balanceOf(msg.sender) >= amount, "WTBTC: insufficient balance");

        // Generate unique burn ID
        burnId = keccak256(
            abi.encodePacked(
                msg.sender,
                amount,
                btcAddress,
                block.timestamp,
                block.number
            )
        );

        // Update total BTC locked
        totalBTCLocked -= amount;

        // Burn the tokens
        _burn(msg.sender, amount);

        // Record the burn
        burnRecords[burnId] = BurnRecord({
            burner: msg.sender,
            amount: amount,
            bitcoinAddress: btcAddress,
            timestamp: block.timestamp,
            processed: false,
            btcTxHash: ""
        });

        emit Burned(msg.sender, amount, btcAddress, burnId);
        emit BTCUnlocked(amount, btcAddress);
        emit BridgeWithdrawal(msg.sender, amount, btcAddress, burnId);

        return burnId;
    }

    /**
     * @dev Mark burn as processed after BTC is sent
     * @param burnId The burn identifier
     * @param btcTxHash Bitcoin transaction hash
     */
    function markBurnProcessed(bytes32 burnId, string memory btcTxHash) external {
        require(
            authorizedBridges[msg.sender] || msg.sender == owner(),
            "WTBTC: not authorized"
        );
        require(burnRecords[burnId].amount > 0, "WTBTC: burn not found");
        require(!burnRecords[burnId].processed, "WTBTC: already processed");

        burnRecords[burnId].processed = true;
        burnRecords[burnId].btcTxHash = btcTxHash;

        emit BurnProcessed(burnId, btcTxHash);
    }

    /**
     * @dev Bridge deposit from Bitcoin (called by bridge backend)
     * @param user User's Ethereum address
     * @param amount Amount of BTC deposited
     * @param btcTxHash Bitcoin transaction hash
     */
    function bridgeDeposit(address user, uint256 amount, string memory btcTxHash)
        external
        whenNotPaused
    {
        require(authorizedBridges[msg.sender], "WTBTC: not authorized bridge");
        require(user != address(0), "WTBTC: invalid user address");
        require(amount > 0, "WTBTC: amount must be positive");

        // Mint WTBTC to user (1:1 with deposited BTC)
        totalBTCLocked += amount;
        _mint(user, amount);

        emit BridgeDeposit(user, amount, btcTxHash);
        emit Minted(user, amount, btcTxHash);
        emit BTCLocked(amount, btcTxHash);
    }

    /**
     * @dev Get burn record details
     * @param burnId The burn identifier
     */
    function getBurnRecord(bytes32 burnId)
        external
        view
        returns (
            address burner,
            uint256 amount,
            string memory bitcoinAddress,
            uint256 timestamp,
            bool processed,
            string memory btcTxHash
        )
    {
        BurnRecord memory record = burnRecords[burnId];
        return (
            record.burner,
            record.amount,
            record.bitcoinAddress,
            record.timestamp,
            record.processed,
            record.btcTxHash
        );
    }

    /**
     * @dev Get the current 1:1 peg ratio
     * @return ratio The peg ratio (should always be 1:1)
     */
    function getPegRatio() external view returns (uint256 ratio) {
        uint256 supply = totalSupply();
        if (supply == 0) return 1e18; // 1:1 ratio

        // Calculate ratio: totalBTCLocked / totalSupply
        // Should always be 1:1 (represented as 1e18 for precision)
        ratio = (totalBTCLocked * 1e18) / supply;
        return ratio;
    }

    /**
     * @dev Update Bitcoin deposit address
     * @param newAddress New Bitcoin address for deposits
     */
    function updateBitcoinAddress(string memory newAddress) external onlyOwner {
        require(bytes(newAddress).length > 0, "WTBTC: invalid address");
        bitcoinDepositAddress = newAddress;
    }

    /**
     * @dev Pause contract (emergency only)
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @dev Unpause contract
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @dev Override transfer to add pause functionality
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }

    /**
     * @dev Get contract information
     */
    function getInfo() external view returns (
        string memory name,
        string memory symbol,
        uint8 tokenDecimals,
        uint256 supply,
        uint256 btcLocked,
        string memory btcAddress,
        bool paused
    ) {
        return (
            name(),
            symbol(),
            decimals(),
            totalSupply(),
            totalBTCLocked,
            bitcoinDepositAddress,
            paused()
        );
    }
}
