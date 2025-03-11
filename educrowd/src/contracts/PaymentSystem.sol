// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract PaymentSystem {
    function makePayment(uint256 _amount, address _recipant) public payable {
        require(msg.value == _amount, "Invalid Payment");
        (bool success, ) = _recipant.call{value: _amount}("");
        require(success, "Payment failed");
    }
}
