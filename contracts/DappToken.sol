// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DAPP is ERC20 {
    constructor() ERC20("DappToken", "DAPP") {
        _mint(msg.sender, 10*(10**18));
    }
}