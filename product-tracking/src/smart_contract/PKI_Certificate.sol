//SPDX-License-Identifier: MIT

pragma solidity 0.8.19; // Use complier version 0.8.19

// Begin contract section

contract PKI_certificate {
    // For dealing with password or any form of credential

    struct Credential {
        string credential;
        string algorithm;
    }

    // Sketch the struct of certificate

    // We must pack some value together to prevent "stack to deep" exception

    struct Certificate {
        // --- Certificate information start here --- //

        string version;
        // issue = issue from + issue to

        string issue;
        // validity = valid before + valid after

        string validity;
        string public_key_algorithm;
        string public_key;
        // --- Certificate information end here --- //

        // We will sign the entire certificate's information above with CA private key

        string signature_algorithm;
        string signature;
        // We will also hash the entire certificate's information above

        string SHA1_fingerprint;
    }

    // Sketch the struct of revokation certificate

    struct Revocation {
        // --- Revocation information start here --- //

        string revocation_date;
        // issuer = who revoke that certificate

        string issuer;
        string reason;
        // -- Revocation information end here --- //

        // We will sign the entire revocation's information above with CA private key

        string signature_algorithm;
        string signature;
        // Unique identifier

        string SHA1_fingerprint;
    }

    // Sketch the struct of attribute certificate

    struct Attribute {
        // --- Attribute information start here --- //

        string version;
        string issuer;
        string holder;
        string validity;
        string attributes;
        // -- Attribute information end here --- //

        // We will sign the entire revocation's information above with AA private key

        string signature_algorithm;
        string signature;
        // Unique identifier

        string SHA1_fingerprint;
    }

    struct Attribute_Revocation {
        // --- Revocation information start here --- //

        string revocation_date;
        // issuer = who revoke that certificate

        string issuer;
        string reason;
        // -- Revocation information end here --- //

        // We will sign the entire revocation's information above with CA private key

        string signature_algorithm;
        string signature;
        // Unique identifier

        string SHA1_fingerprint;
    }

    struct Attribute_Key {
        string key;
        string iv;
    }

    // Struct hash table to map from serial number to the instances above

    // Hash table O(1), Array O(n) for searching algorithm

    mapping(string => Credential) username_to_credential;
    mapping(string => Certificate) serial_number_to_certificate;
    mapping(string => Revocation) serial_number_to_revocation;
    mapping(string => Attribute) serial_number_to_attribute;
    mapping(string => Attribute_Revocation) serial_number_to_revocation_attribute;
    mapping(string => string) file_name_to_temp_AES_key;
    mapping(string => string) file_name_to_temp_iv;
    mapping(string => string[]) file_name_to_log;
    mapping(string => Attribute_Key) serial_number_to_attribute_key;

    function store_attribute_key(
        string memory serial_number,
        string memory key,
        string memory iv
    ) public {
        serial_number_to_attribute_key[serial_number].key = key;
        serial_number_to_attribute_key[serial_number].iv = iv;
    }

    function get_attribute_key(
        string memory serial_number
    ) public view returns (Attribute_Key memory) {
        return serial_number_to_attribute_key[serial_number];
    }

    // function to register certificate

    // We will not implement random, hash, sign function in the contract because

    // it will increase gas fee dramatically

    // Let's burden that works to the externals

    function issue_certificate(
        string memory serial_number,
        string memory version,
        string memory issue,
        string memory validity,
        string memory public_key_algorithm,
        string memory public_key,
        string memory signature_algorithm,
        string memory signature,
        string memory SHA1_fingerprint
    ) public returns (int256) {
        // Check if the serial_number is duplicated

        require(
            bytes(serial_number_to_certificate[serial_number].version).length ==
                0,
            "Duplicated serial number"
        );

        // Add some key,value to serial_number_to_certificate

        serial_number_to_certificate[serial_number].version = version;
        serial_number_to_certificate[serial_number].issue = issue;
        serial_number_to_certificate[serial_number].validity = validity;
        serial_number_to_certificate[serial_number]
            .public_key_algorithm = public_key_algorithm;
        serial_number_to_certificate[serial_number].public_key = public_key;
        serial_number_to_certificate[serial_number]
            .signature_algorithm = signature_algorithm;
        serial_number_to_certificate[serial_number].signature = signature;
        serial_number_to_certificate[serial_number]
            .SHA1_fingerprint = SHA1_fingerprint;

        // return 1 to indicate register successfully
        return 1;
    }

    // Implement view function

    // view function won't cost any gas fee

    function view_certificate(
        string memory serial_number
    ) public view returns (Certificate memory) {
        return serial_number_to_certificate[serial_number];
    }

    // function to revoke the certificate

    function revoke_certificate(
        string memory serial_number,
        string memory revocation_date,
        string memory issuer,
        string memory reason,
        string memory signature_algorithm,
        string memory signature,
        string memory SHA1_fingerprint
    ) public returns (int256) {
        // Check if the certificate is existed

        require(
            bytes(serial_number_to_certificate[serial_number].version).length >
                0,
            "Certificate is not found"
        );

        // Check if the certificate is already revoked

        require(
            bytes(serial_number_to_revocation[serial_number].reason).length ==
                0,
            "The certificate is already revoked"
        );

        serial_number_to_revocation[serial_number]
            .revocation_date = revocation_date;
        serial_number_to_revocation[serial_number].issuer = issuer;
        serial_number_to_revocation[serial_number].reason = reason;
        serial_number_to_revocation[serial_number]
            .signature_algorithm = signature_algorithm;
        serial_number_to_revocation[serial_number].signature = signature;
        serial_number_to_revocation[serial_number]
            .SHA1_fingerprint = SHA1_fingerprint;
        return 1;
    }

    function view_revocation(
        string memory serial_number
    ) public view returns (Revocation memory) {
        return serial_number_to_revocation[serial_number];
    }

    function issue_attribute(
        string memory serial_number,
        string memory version,
        string memory issuer,
        string memory holder,
        string memory validity,
        string memory attributes,
        string memory signature_algorithm,
        string memory signature,
        string memory SHA1_fingerprint
    ) public returns (int256) {
        // Check if the serial_number is duplicated

        require(
            bytes(serial_number_to_attribute[serial_number].version).length ==
                0,
            "duplicate serial number"
        );

        require(
            bytes(serial_number_to_certificate[holder].version).length > 0,
            "Must obtain digital certificate"
        );

        serial_number_to_attribute[serial_number].version = version;
        serial_number_to_attribute[serial_number].issuer = issuer;
        serial_number_to_attribute[serial_number].holder = holder;
        serial_number_to_attribute[serial_number].validity = validity;
        serial_number_to_attribute[serial_number].attributes = attributes;
        serial_number_to_attribute[serial_number]
            .signature_algorithm = signature_algorithm;
        serial_number_to_attribute[serial_number].signature = signature;
        serial_number_to_attribute[serial_number]
            .SHA1_fingerprint = SHA1_fingerprint;

        return 1;
    }

    function view_attribute(
        string memory serial_number
    ) public view returns (Attribute memory) {
        return serial_number_to_attribute[serial_number];
    }

    function revoke_attribute(
        string memory serial_number,
        string memory revocation_date,
        string memory issuer,
        string memory reason,
        string memory signature_algorithm,
        string memory signature,
        string memory SHA1_fingerprint
    ) public returns (int256) {
        // Check if the attribute is existed

        require(
            bytes(serial_number_to_attribute[serial_number].version).length > 0,
            "Attribute is not found"
        );

        // Check if the attribute is already revoked

        require(
            bytes(serial_number_to_revocation_attribute[serial_number].reason)
                .length == 0,
            "The attribute is already revoked"
        );

        serial_number_to_revocation_attribute[serial_number]
            .revocation_date = revocation_date;

        serial_number_to_revocation_attribute[serial_number].issuer = issuer;
        serial_number_to_revocation_attribute[serial_number].reason = reason;
        serial_number_to_revocation_attribute[serial_number]
            .signature_algorithm = signature_algorithm;
        serial_number_to_revocation_attribute[serial_number]
            .signature = signature;
        serial_number_to_revocation_attribute[serial_number]
            .SHA1_fingerprint = SHA1_fingerprint;

        return 1;
    }

    function view_revocation_attribute(
        string memory serial_number
    ) public view returns (Attribute_Revocation memory) {
        return serial_number_to_revocation_attribute[serial_number];
    }

    function store_credential(
        string memory username,
        string memory credential,
        string memory algorithm
    ) public returns (int256) {
        require(
            bytes(username_to_credential[username].credential).length == 0,
            "duplicate username"
        );
        username_to_credential[username].credential = credential;
        username_to_credential[username].algorithm = algorithm;

        return 1;
    }

    function get_credential(
        string memory username
    ) public view returns (Credential memory) {
        require(
            bytes(username_to_credential[username].credential).length != 0,
            "username does not exist"
        );
        return username_to_credential[username];
    }
}
