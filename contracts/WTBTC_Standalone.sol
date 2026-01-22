// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title WTBTC - Wrapped Testnet Bitcoin (Standalone)
 * @dev ERC20 Token for bridging Bitcoin Testnet to Ethereum
 * @notice Total Supply: 100,000,000 WTBTC
 * @notice This is a standalone version without external dependencies
 */

contract WTBTC {
    string public constant name = "Wrapped Testnet Bitcoin";
    string public constant symbol = "WTBTC";
    uint8 public constant decimals = 8; // Match Bitcoin decimals
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10**8; // 100 million WTBTC

    uint256 public totalSupply;
    address public owner;
    address public bridge;
    bool public paused;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    // Burn records for bridging back to Bitcoin
    struct BurnRecord {
        address burner;
        uint256 amount;
        string bitcoinAddress;
        uint256 timestamp;
        bool processed;
        string bitcoinTxHash;
    }

    mapping(bytes32 => BurnRecord) public burnRecords;
    bytes32[] public burnIds;

    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event TokensBurned(
        address indexed burner,
        uint256 amount,
        string bitcoinAddress,
        bytes32 indexed burnId,
        uint256 timestamp
    );
    event BurnProcessed(bytes32 indexed burnId, string bitcoinTxHash);
    event BridgeUpdated(address indexed newBridge);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    constructor() {
        owner = msg.sender;
        // Mint initial supply to deployer
        totalSupply = MAX_SUPPLY;
        balanceOf[msg.sender] = MAX_SUPPLY;
        emit Transfer(address(0), msg.sender, MAX_SUPPLY);
    }

    function transfer(address to, uint256 amount) public whenNotPaused returns (bool) {
        require(to != address(0), "Transfer to zero address");
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");

        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;

        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public whenNotPaused returns (bool) {
        require(to != address(0), "Transfer to zero address");
        require(balanceOf[from] >= amount, "Insufficient balance");
        require(allowance[from][msg.sender] >= amount, "Insufficient allowance");

        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        allowance[from][msg.sender] -= amount;

        emit Transfer(from, to, amount);
        return true;
    }

    /**
     * @dev Burn tokens and bridge to Bitcoin address
     * This is the KEY function for getting tokens to Bitcoin wallet
     */
    function burnAndBridge(uint256 amount, string memory bitcoinAddress)
        public
        whenNotPaused
        returns (bytes32)
    {
        require(amount > 0, "Amount must be greater than 0");
        require(bytes(bitcoinAddress).length > 0, "Bitcoin address required");
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");

        // Generate unique burn ID
        bytes32 burnId = keccak256(
            abi.encodePacked(
                msg.sender,
                amount,
                bitcoinAddress,
                block.timestamp,
                block.number,
                burnIds.length
            )
        );

        // Burn the tokens (reduce supply)
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;

        // Record the burn with Bitcoin address
        burnRecords[burnId] = BurnRecord({
            burner: msg.sender,
            amount: amount,
            bitcoinAddress: bitcoinAddress,
            timestamp: block.timestamp,
            processed: false,
            bitcoinTxHash: ""
        });

        burnIds.push(burnId);

        emit Transfer(msg.sender, address(0), amount);
        emit TokensBurned(msg.sender, amount, bitcoinAddress, burnId, block.timestamp);

        return burnId;
    }

    /**
     * @dev Mark burn as processed after Bitcoin transfer completed
     */
    function markBurnProcessed(bytes32 burnId, string memory bitcoinTxHash) public {
        require(
            msg.sender == bridge || msg.sender == owner,
            "Only bridge or owner"
        );
        require(burnRecords[burnId].amount > 0, "Burn not found");
        require(!burnRecords[burnId].processed, "Already processed");

        burnRecords[burnId].processed = true;
        burnRecords[burnId].bitcoinTxHash = bitcoinTxHash;

        emit BurnProcessed(burnId, bitcoinTxHash);
    }

    /**
     * @dev Get all pending burns (not yet processed)
     */
    function getPendingBurns() public view returns (bytes32[] memory) {
        uint256 pendingCount = 0;

        // Count pending burns
        for (uint256 i = 0; i < burnIds.length; i++) {
            if (!burnRecords[burnIds[i]].processed) {
                pendingCount++;
            }
        }

        // Create array of pending burn IDs
        bytes32[] memory pending = new bytes32[](pendingCount);
        uint256 index = 0;

        for (uint256 i = 0; i < burnIds.length; i++) {
            if (!burnRecords[burnIds[i]].processed) {
                pending[index] = burnIds[i];
                index++;
            }
        }

        return pending;
    }

    /**
     * @dev Get total number of burns
     */
    function getTotalBurns() public view returns (uint256) {
        return burnIds.length;
    }

    /**
     * @dev Set bridge contract
     */
    function setBridge(address _bridge) public onlyOwner {
        require(_bridge != address(0), "Invalid bridge address");
        bridge = _bridge;
        emit BridgeUpdated(_bridge);
    }

    /**
     * @dev Pause contract (emergency)
     */
    function pause() public onlyOwner {
        paused = true;
    }

    /**
     * @dev Unpause contract
     */
    function unpause() public onlyOwner {
        paused = false;
    }

    /**
     * @dev Transfer ownership
     */
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid new owner");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    /**
     * @dev Mint tokens (only bridge)
     */
    function mint(address to, uint256 amount) public {
        require(msg.sender == bridge, "Only bridge can mint");
        require(totalSupply + amount <= MAX_SUPPLY, "Exceeds max supply");

        totalSupply += amount;
        balanceOf[to] += amount;

        emit Transfer(address(0), to, amount);
    }
}
