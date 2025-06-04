// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MyToken {
    string public name = "MyCustomToken";
    string public symbol = "MCT";
    uint8 public decimals = 18;
    uint public totalSupply;

    address public owner;

    mapping(address => uint) public balances;
    mapping(address => mapping(address => uint)) public allowances;

    constructor(uint _initialSupply) {
        owner = msg.sender;
        totalSupply = _initialSupply * (10 ** uint(decimals));
        balances[msg.sender] = totalSupply;
    }

    // Transfert direct de tokens
    function transfer(address _to, uint _amount) external returns (bool) {
        require(balances[msg.sender] >= _amount, "Solde insuffisant");
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
        return true;
    }

    // Autoriser un tiers à dépenser
    function approve(address _spender, uint _amount) external returns (bool) {
        allowances[msg.sender][_spender] = _amount;
        return true;
    }

    // Transfert depuis un compte autorisé
    function transferFrom(address _from, address _to, uint _amount) external returns (bool) {
        require(balances[_from] >= _amount, "Solde insuffisant");
        require(allowances[_from][msg.sender] >= _amount, "Autorisation insuffisante");

        balances[_from] -= _amount;
        balances[_to] += _amount;
        allowances[_from][msg.sender] -= _amount;
        return true;
    }

    // Solde d’un compte
    function balanceOf(address _account) external view returns (uint) {
        return balances[_account];
    }

    // Autorisation restante
    function allowance(address _owner, address _spender) external view returns (uint) {
        return allowances[_owner][_spender];
    }
}
