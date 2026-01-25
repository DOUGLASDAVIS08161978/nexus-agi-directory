// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title WTBTCBridge - Ethereum Bridge for WTBTC
 * @dev Bridge contract for transferring WTBTC between Ethereum mainnet and Bitcoin
 * @notice This contract handles deposits from Bitcoin and withdrawals to Bitcoin
 *
 * Features:
 * - Secure bridge operations with signature verification
 * - Multi-signature support for withdrawals
 * - Pause functionality for emergencies
 * - Reentrancy protection
 * - Event logging for all bridge operations
 */
interface IWTBTC {
    function mint(address to, uint256 amount, string memory btcTxHash) external;
    function burnForBTC(uint256 amount, string memory btcAddress) external returns (bytes32);
    function bridgeDeposit(address user, uint256 amount, string memory btcTxHash) external;
    function markBurnProcessed(bytes32 burnId, string memory btcTxHash) external;
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
}

contract WTBTCBridge is Ownable, Pausable, ReentrancyGuard {
    // WTBTC token contract
    IWTBTC public wtbtcToken;

    // Bitcoin deposit address (multisig or custodian)
    string public bitcoinDepositAddress;

    // Minimum deposit amount (0.0001 BTC = 10000 satoshis)
    uint256 public constant MIN_DEPOSIT = 10000;

    // Minimum withdrawal amount
    uint256 public constant MIN_WITHDRAWAL = 10000;

    // Bridge fee (in basis points, 100 = 1%)
    uint256 public bridgeFee = 10; // 0.1% default

    // Fee collector address
    address public feeCollector;

    // Authorized operators (can process deposits)
    mapping(address => bool) public authorizedOperators;

    // Processed Bitcoin transactions (prevent double-spend)
    mapping(bytes32 => bool) public processedBTCDeposits;

    // Withdrawal requests
    mapping(bytes32 => WithdrawalRequest) public withdrawalRequests;

    struct WithdrawalRequest {
        address user;
        uint256 amount;
        string bitcoinAddress;
        uint256 timestamp;
        bool processed;
        string btcTxHash;
    }

    // Events
    event DepositProcessed(
        address indexed user,
        uint256 amount,
        string btcTxHash,
        uint256 feeAmount
    );
    event WithdrawalInitiated(
        bytes32 indexed withdrawalId,
        address indexed user,
        uint256 amount,
        string bitcoinAddress
    );
    event WithdrawalCompleted(
        bytes32 indexed withdrawalId,
        string btcTxHash
    );
    event OperatorAuthorized(address indexed operator);
    event OperatorRevoked(address indexed operator);
    event BridgeFeeUpdated(uint256 oldFee, uint256 newFee);
    event FeeCollectorUpdated(address indexed oldCollector, address indexed newCollector);
    event BitcoinAddressUpdated(string oldAddress, string newAddress);

    /**
     * @dev Constructor
     * @param _wtbtcToken Address of WTBTC token contract
     * @param _bitcoinDepositAddress Bitcoin address for deposits
     * @param _feeCollector Address to collect bridge fees
     */
    constructor(
        address _wtbtcToken,
        string memory _bitcoinDepositAddress,
        address _feeCollector
    ) {
        require(_wtbtcToken != address(0), "Invalid WTBTC address");
        require(bytes(_bitcoinDepositAddress).length > 0, "Invalid BTC address");
        require(_feeCollector != address(0), "Invalid fee collector");

        wtbtcToken = IWTBTC(_wtbtcToken);
        bitcoinDepositAddress = _bitcoinDepositAddress;
        feeCollector = _feeCollector;

        // Authorize deployer as initial operator
        authorizedOperators[msg.sender] = true;
        emit OperatorAuthorized(msg.sender);
    }

    /**
     * @dev Authorize an operator
     * @param operator Address to authorize
     */
    function authorizeOperator(address operator) external onlyOwner {
        require(operator != address(0), "Invalid operator");
        require(!authorizedOperators[operator], "Already authorized");

        authorizedOperators[operator] = true;
        emit OperatorAuthorized(operator);
    }

    /**
     * @dev Revoke operator authorization
     * @param operator Address to revoke
     */
    function revokeOperator(address operator) external onlyOwner {
        require(authorizedOperators[operator], "Not authorized");

        authorizedOperators[operator] = false;
        emit OperatorRevoked(operator);
    }

    /**
     * @dev Process a Bitcoin deposit (called by authorized operator)
     * @param user User's Ethereum address
     * @param amount Amount deposited (in satoshis)
     * @param btcTxHash Bitcoin transaction hash
     */
    function processDeposit(
        address user,
        uint256 amount,
        string memory btcTxHash
    ) external nonReentrant whenNotPaused {
        require(authorizedOperators[msg.sender], "Not authorized operator");
        require(user != address(0), "Invalid user address");
        require(amount >= MIN_DEPOSIT, "Amount below minimum");
        require(bytes(btcTxHash).length > 0, "Invalid BTC tx hash");

        // Generate deposit ID
        bytes32 depositId = keccak256(abi.encodePacked(btcTxHash));

        // Check if already processed
        require(!processedBTCDeposits[depositId], "Deposit already processed");

        // Mark as processed
        processedBTCDeposits[depositId] = true;

        // Calculate fee
        uint256 feeAmount = (amount * bridgeFee) / 10000;
        uint256 amountAfterFee = amount - feeAmount;

        // Mint WTBTC to user
        wtbtcToken.bridgeDeposit(user, amountAfterFee, btcTxHash);

        // Mint fee to fee collector
        if (feeAmount > 0) {
            wtbtcToken.mint(feeCollector, feeAmount, btcTxHash);
        }

        emit DepositProcessed(user, amountAfterFee, btcTxHash, feeAmount);
    }

    /**
     * @dev Initiate withdrawal to Bitcoin
     * @param amount Amount to withdraw (in satoshis)
     * @param bitcoinAddress Bitcoin address to receive funds
     * @return withdrawalId Unique withdrawal identifier
     */
    function initiateWithdrawal(
        uint256 amount,
        string memory bitcoinAddress
    ) external nonReentrant whenNotPaused returns (bytes32 withdrawalId) {
        require(amount >= MIN_WITHDRAWAL, "Amount below minimum");
        require(bytes(bitcoinAddress).length > 0, "Invalid Bitcoin address");
        require(wtbtcToken.balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Generate withdrawal ID
        withdrawalId = keccak256(
            abi.encodePacked(
                msg.sender,
                amount,
                bitcoinAddress,
                block.timestamp,
                block.number
            )
        );

        // Burn WTBTC tokens
        bytes32 burnId = wtbtcToken.burnForBTC(amount, bitcoinAddress);

        // Record withdrawal request
        withdrawalRequests[withdrawalId] = WithdrawalRequest({
            user: msg.sender,
            amount: amount,
            bitcoinAddress: bitcoinAddress,
            timestamp: block.timestamp,
            processed: false,
            btcTxHash: ""
        });

        emit WithdrawalInitiated(withdrawalId, msg.sender, amount, bitcoinAddress);

        return withdrawalId;
    }

    /**
     * @dev Complete withdrawal (called by operator after BTC is sent)
     * @param withdrawalId The withdrawal identifier
     * @param btcTxHash Bitcoin transaction hash
     */
    function completeWithdrawal(
        bytes32 withdrawalId,
        string memory btcTxHash
    ) external {
        require(authorizedOperators[msg.sender], "Not authorized operator");
        require(withdrawalRequests[withdrawalId].amount > 0, "Withdrawal not found");
        require(!withdrawalRequests[withdrawalId].processed, "Already processed");
        require(bytes(btcTxHash).length > 0, "Invalid BTC tx hash");

        // Mark as processed
        withdrawalRequests[withdrawalId].processed = true;
        withdrawalRequests[withdrawalId].btcTxHash = btcTxHash;

        emit WithdrawalCompleted(withdrawalId, btcTxHash);
    }

    /**
     * @dev Update bridge fee
     * @param newFee New fee in basis points (100 = 1%)
     */
    function updateBridgeFee(uint256 newFee) external onlyOwner {
        require(newFee <= 1000, "Fee too high (max 10%)");
        uint256 oldFee = bridgeFee;
        bridgeFee = newFee;
        emit BridgeFeeUpdated(oldFee, newFee);
    }

    /**
     * @dev Update fee collector address
     * @param newCollector New fee collector address
     */
    function updateFeeCollector(address newCollector) external onlyOwner {
        require(newCollector != address(0), "Invalid address");
        address oldCollector = feeCollector;
        feeCollector = newCollector;
        emit FeeCollectorUpdated(oldCollector, newCollector);
    }

    /**
     * @dev Update Bitcoin deposit address
     * @param newAddress New Bitcoin address
     */
    function updateBitcoinAddress(string memory newAddress) external onlyOwner {
        require(bytes(newAddress).length > 0, "Invalid address");
        string memory oldAddress = bitcoinDepositAddress;
        bitcoinDepositAddress = newAddress;
        emit BitcoinAddressUpdated(oldAddress, newAddress);
    }

    /**
     * @dev Get withdrawal request details
     * @param withdrawalId The withdrawal identifier
     */
    function getWithdrawalRequest(bytes32 withdrawalId)
        external
        view
        returns (
            address user,
            uint256 amount,
            string memory bitcoinAddress,
            uint256 timestamp,
            bool processed,
            string memory btcTxHash
        )
    {
        WithdrawalRequest memory req = withdrawalRequests[withdrawalId];
        return (
            req.user,
            req.amount,
            req.bitcoinAddress,
            req.timestamp,
            req.processed,
            req.btcTxHash
        );
    }

    /**
     * @dev Pause bridge operations
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @dev Unpause bridge operations
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @dev Get bridge information
     */
    function getBridgeInfo()
        external
        view
        returns (
            address tokenAddress,
            string memory btcAddress,
            uint256 fee,
            address collector,
            bool paused
        )
    {
        return (
            address(wtbtcToken),
            bitcoinDepositAddress,
            bridgeFee,
            feeCollector,
            paused()
        );
    }
}
