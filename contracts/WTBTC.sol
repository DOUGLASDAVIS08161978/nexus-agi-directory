// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WTBTC {
    string public constant name = "Wrapped Test BTC";
    string public constant symbol = "WTBTC";
    uint8 public constant decimals = 8;
    uint256 public constant totalSupply = 1000000 * 10**8;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor() {
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }
}
