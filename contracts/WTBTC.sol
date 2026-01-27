// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title WTBTC - Wrapped Testnet Bitcoin
 * @dev ERC20 Token for bridging Bitcoin Testnet to Ethereum
 * @notice Total Supply: 100,000,000 WTBTC
 *
 * Features:
 * - Mintable (only by bridge contract)
 * - Burnable (for bridging back to Bitcoin)
 * - Pausable (for emergency situations)
 * - Ownable (for access control)
 */

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WTBTC is ERC20, ERC20Burnable, Pausable, Ownable {
    // Maximum supply: 100 million WTBTC
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10**8; // 8 decimals like Bitcoin

    // Bridge contract address (can mint tokens)
    address public bridge;

    // Mapping to track Bitcoin addresses that received burned tokens
    mapping(bytes32 => BurnRecord) public burnRecords;

    struct BurnRecord {
        address burner;
        uint256 amount;
        string bitcoinAddress;
        uint256 timestamp;
        bool processed;
    }

    // Events
    event BridgeUpdated(address indexed oldBridge, address indexed newBridge);
    event TokensBurned(
        address indexed burner,
        uint256 amount,
        string bitcoinAddress,
        bytes32 burnId,
        uint256 timestamp
    );
    event BurnProcessed(bytes32 indexed burnId, string bitcoinTxHash);

    /**
     * @dev Constructor - Mints initial supply to deployer
     */
    constructor() ERC20("Wrapped Testnet Bitcoin", "WTBTC") {
        // Mint initial supply to contract deployer
        _mint(msg.sender, MAX_SUPPLY);
    }

    /**
     * @dev Returns 8 decimals to match Bitcoin
     */
    function decimals() public pure override returns (uint8) {
        return 8;
    }

    /**
     * @dev Set the bridge contract address
     * @param _bridge Address of the bridge contract
     */
    function setBridge(address _bridge) external onlyOwner {
        require(_bridge != address(0), "Bridge cannot be zero address");
        address oldBridge = bridge;
        bridge = _bridge;
        emit BridgeUpdated(oldBridge, _bridge);
    }

    /**
     * @dev Pause token transfers (emergency only)
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @dev Unpause token transfers
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @dev Burn tokens and bridge to Bitcoin address
     * @param amount Amount of WTBTC to burn
     * @param bitcoinAddress Bitcoin address to receive BTC
     * @return burnId Unique identifier for this burn
     */
    function burnAndBridge(uint256 amount, string memory bitcoinAddress)
        external
        whenNotPaused
        returns (bytes32 burnId)
    {
        require(amount > 0, "Amount must be greater than 0");
        require(bytes(bitcoinAddress).length > 0, "Bitcoin address required");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Generate unique burn ID
        burnId = keccak256(
            abi.encodePacked(
                msg.sender,
                amount,
                bitcoinAddress,
                block.timestamp,
                block.number
            )
        );

        // Burn the tokens
        _burn(msg.sender, amount);

        // Record the burn
        burnRecords[burnId] = BurnRecord({
            burner: msg.sender,
            amount: amount,
            bitcoinAddress: bitcoinAddress,
            timestamp: block.timestamp,
            processed: false
        });

        emit TokensBurned(
            msg.sender,
            amount,
            bitcoinAddress,
            burnId,
            block.timestamp
        );

        return burnId;
    }

    /**
     * @dev Mark a burn as processed (called by bridge after Bitcoin transfer)
     * @param burnId The burn identifier
     * @param bitcoinTxHash The Bitcoin transaction hash
     */
    function markBurnProcessed(bytes32 burnId, string memory bitcoinTxHash)
        external
    {
        require(
            msg.sender == bridge || msg.sender == owner(),
            "Only bridge or owner can mark processed"
        );
        require(burnRecords[burnId].amount > 0, "Burn record not found");
        require(!burnRecords[burnId].processed, "Already processed");

        burnRecords[burnId].processed = true;

        emit BurnProcessed(burnId, bitcoinTxHash);
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
            bool processed
        )
    {
        BurnRecord memory record = burnRecords[burnId];
        return (
            record.burner,
            record.amount,
            record.bitcoinAddress,
            record.timestamp,
            record.processed
        );
    }

    /**
     * @dev Mint new tokens (only bridge can call)
     * @param to Recipient address
     * @param amount Amount to mint
     */
    function mint(address to, uint256 amount) external {
        require(msg.sender == bridge, "Only bridge can mint");
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }

    /**
     * @dev Override transfer to add pausable functionality
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
}
