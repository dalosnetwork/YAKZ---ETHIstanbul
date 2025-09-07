// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title TradingSignalContract
 * @dev Smart contract for emitting trading signals that trigger automated trading
 * @author Your Name
 */
contract TradingSignalContract {
    
    // ===========================================
    // EVENTS
    // ===========================================
    
    /**
     * @dev Emitted when a trading signal is generated
     * @param exType Exchange type (cex or dex)
     * @param quantity Amount to trade (in wei, 18 decimals)
     * @param expectedPrice Expected price (in wei, 18 decimals)
     * @param pair Trading pair symbol
     * @param side Buy or sell
     */
    event TradingSignal(
        string indexed exType,
        uint256 quantity,
        uint256 expectedPrice,
        string pair,
        string side
    );
    
    // ===========================================
    // STATE VARIABLES
    // ===========================================
    
    address public owner;
    mapping(address => bool) public authorizedCallers;
    
    // Trading limits
    uint256 public maxTradeAmount = 1000 ether; // 1000 tokens max
    uint256 public minTradeAmount = 0.001 ether; // 0.001 tokens min
    
    // ===========================================
    // MODIFIERS
    // ===========================================
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyAuthorized() {
        require(
            authorizedCallers[msg.sender] || msg.sender == owner,
            "Only authorized callers can emit signals"
        );
        _;
    }
    
    modifier validAmount(uint256 amount) {
        require(amount >= minTradeAmount, "Amount too small");
        require(amount <= maxTradeAmount, "Amount too large");
        _;
    }
    
    // ===========================================
    // CONSTRUCTOR
    // ===========================================
    
    constructor() {
        owner = msg.sender;
        authorizedCallers[msg.sender] = true;
    }
    
    // ===========================================
    // MAIN FUNCTIONS
    // ===========================================
    
    /**
     * @dev Emit a CEX trading signal
     * @param quantity Amount to trade (in wei)
     * @param expectedPrice Expected price (in wei)
     * @param pair Trading pair symbol
     * @param side Buy or sell
     */
    function emitCexSignal(
        uint256 quantity,
        uint256 expectedPrice,
        string calldata pair,
        string calldata side
    ) external onlyAuthorized validAmount(quantity) {
        emit TradingSignal("cex", quantity, expectedPrice, pair, side);
    }
    
    /**
     * @dev Emit a DEX trading signal
     * @param quantity Amount to trade (in wei)
     * @param expectedPrice Expected price (in wei)
     * @param pair Trading pair symbol
     * @param side Buy or sell
     */
    function emitDexSignal(
        uint256 quantity,
        uint256 expectedPrice,
        string calldata pair,
        string calldata side
    ) external onlyAuthorized validAmount(quantity) {
        emit TradingSignal("dex", quantity, expectedPrice, pair, side);
    }
    
    /**
     * @dev Emit a custom trading signal
     * @param exType Exchange type
     * @param quantity Amount to trade (in wei)
     * @param expectedPrice Expected price (in wei)
     * @param pair Trading pair symbol
     * @param side Buy or sell
     */
    function emitCustomSignal(
        string calldata exType,
        uint256 quantity,
        uint256 expectedPrice,
        string calldata pair,
        string calldata side
    ) external onlyAuthorized validAmount(quantity) {
        require(
            keccak256(bytes(exType)) == keccak256(bytes("cex")) ||
            keccak256(bytes(exType)) == keccak256(bytes("dex")),
            "Invalid exchange type"
        );
        require(
            keccak256(bytes(side)) == keccak256(bytes("buy")) ||
            keccak256(bytes(side)) == keccak256(bytes("sell")),
            "Invalid side"
        );
        
        emit TradingSignal(exType, quantity, expectedPrice, pair, side);
    }
    
    // ===========================================
    // ADMIN FUNCTIONS
    // ===========================================
    
    /**
     * @dev Add authorized caller
     * @param caller Address to authorize
     */
    function addAuthorizedCaller(address caller) external onlyOwner {
        authorizedCallers[caller] = true;
    }
    
    /**
     * @dev Remove authorized caller
     * @param caller Address to remove
     */
    function removeAuthorizedCaller(address caller) external onlyOwner {
        authorizedCallers[caller] = false;
    }
    
    /**
     * @dev Update trading limits
     * @param _minTradeAmount New minimum trade amount
     * @param _maxTradeAmount New maximum trade amount
     */
    function updateTradingLimits(
        uint256 _minTradeAmount,
        uint256 _maxTradeAmount
    ) external onlyOwner {
        require(_minTradeAmount < _maxTradeAmount, "Invalid limits");
        minTradeAmount = _minTradeAmount;
        maxTradeAmount = _maxTradeAmount;
    }
    
    /**
     * @dev Transfer ownership
     * @param newOwner New owner address
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid new owner");
        owner = newOwner;
    }
    
    // ===========================================
    // VIEW FUNCTIONS
    // ===========================================
    
    /**
     * @dev Check if address is authorized
     * @param caller Address to check
     * @return bool True if authorized
     */
    function isAuthorized(address caller) external view returns (bool) {
        return authorizedCallers[caller] || caller == owner;
    }
    
    /**
     * @dev Get contract info
     * @return _owner Contract owner
     * @return _minTradeAmount Minimum trade amount
     * @return _maxTradeAmount Maximum trade amount
     */
    function getContractInfo() external view returns (
        address _owner,
        uint256 _minTradeAmount,
        uint256 _maxTradeAmount
    ) {
        return (owner, minTradeAmount, maxTradeAmount);
    }
}
