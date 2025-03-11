// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract UserRegistration {
    struct User {
        uint256 id;
        string name;
        string email;
        address user_address;
    }

    mapping(address => User) public users;

    event UserRegistered(address indexed userAddress, uint256 indexed userId);

    uint256 public userIdCounter;

    function registerUser(string memory _name, string memory _email) public {
        require(msg.sender != address(0), "Invalid user address");
        require(users[msg.sender].id == 0, "User already registered");
        require(bytes(_name).length > 0, "Name is required");
        require(bytes(_email).length > 0, "Email is required");
        userIdCounter++;
        users[msg.sender] = User({
            id: userIdCounter,
            name: _name,
            email: _email,
            user_address: msg.sender
        });
        emit UserRegistered(msg.sender, userIdCounter);
    }

    function getUserAddress() public view returns (address) {
        return msg.sender;
    }

    function isRegistered() public view returns (bool) {
        return users[msg.sender].id != 0;
    }
}
