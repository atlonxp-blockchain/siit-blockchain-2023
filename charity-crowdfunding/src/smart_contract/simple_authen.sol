//SPDX-License-Identifier: MITchange
pragma solidity ^0.8.5; //Use complier version 0.8.5 above

contract authentication {
    struct credential {
        string password;
        string salt;
        int status;
    }

    struct info {
        address payable account_address;
        string name;
        string surname;
    }

    mapping(string => credential) username_to_credential;
    mapping(string => info) username_to_info;

    function register(
        string memory username,
        string memory password,
        string memory salt,
        address payable account_address,
        string memory name,
        string memory surname
    ) public {
        require(
            username_to_credential[username].status == 0,
            "Duplicated Username"
        );

        username_to_credential[username].password = password;
        username_to_credential[username].salt = salt;
        username_to_credential[username].status = 1;
        username_to_info[username].account_address = account_address;
        username_to_info[username].name = name;
        username_to_info[username].surname = surname;
    }

    function get_credential(
        string memory username
    ) public view returns (credential memory) {
        return username_to_credential[username];
    }

    function get_info(
        string memory username
    ) public view returns (info memory) {
        return username_to_info[username];
    }
}
