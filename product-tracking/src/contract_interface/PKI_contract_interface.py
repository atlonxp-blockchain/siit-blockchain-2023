from web3 import Web3
from web3.exceptions import ContractLogicError
from dateutil.relativedelta import relativedelta

# pkcs1_15 is used for signing
# pkcs1_OAEP is used for encryption and decryption

from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256, SHA1
from Crypto.PublicKey import RSA
from datetime import datetime
from json import dumps, loads, dump, load
from secrets import token_bytes
import datetime, os, random


# Retrieve ABI of our smart contract
with open("./smart_contract/abi_PKI.json", "r") as file:
    abi = file.read()

# Retrieve address of our smart contract
with open("./smart_contract/contract_address_PKI.txt", "r") as file:
    contract_address = file.read()


with open("./smart_contract/network_deploy.txt", "r") as f:
    blockchain_network = f.read()

# Connect to the blockchain network
w3 = Web3(Web3.HTTPProvider(blockchain_network))

# Make smart contract object
PKI_certificate = w3.eth.contract(address=contract_address, abi=abi)

# Import key for CA and AA
# This is just a simulation of CA and AA, just a mocking certificate

with open(f"./contract_interface/CA_private_key.pem", "r") as f:
    CA_private_key = pkcs1_15.new(RSA.import_key(f.read()))

with open(f"./contract_interface/CA_public_key.pem", "r") as f:
    CA_public_key = pkcs1_15.new(RSA.import_key(f.read()))

with open(f"./contract_interface/AA_private_key.pem", "r") as f:
    AA_private_key = pkcs1_15.new(RSA.import_key(f.read()))

with open(f"./contract_interface/AA_public_key.pem", "r") as f:
    AA_public_key = pkcs1_15.new(RSA.import_key(f.read()))

# For AES encryption in CBC mode


def AES_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    return (ciphertext, iv)


# For AES decryption in CBC mode
def AES_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext


# To generate string in form of Certificate serial number
# Ex. 00:D5:51:91:16:66:48:A2:01:0A:25:61:BF:AF:49:A0:E6
def generate_serial_number() -> str:
    random_bytes = token_bytes(16)
    hex_string = ":".join("{:02x}".format(b) for b in random_bytes)
    return hex_string.lower()


# All of our function will return in form of dictionary so that debugging will be easier and more efficient
# It comprises of "status code" and "message"
# status code < 0 mean error. Otherwise is a good sign
# Message can be the payload, just a warning or, an error message
# Interface for function to issue certificate in our smart contract


def issue_certificate(
    issue_to: str,
    version: str = "Version 1",
    issue_from: str = "Good CA Company",
    validity_period_in_months: int = 3,
    public_key_algorithm: str = "PKCS1_OAEP",
) -> dict:
    # Generate the certificate serial number
    serial_number = generate_serial_number()
    # Check if this serial number is taken (Ultimately low probability to occur collision, just for safety)

    if view_certificate(serial_number)["status_code"] > 0:
        return {"status_code": -1, "message": "Duplicate serial number"}

    # Select address for performing transaction
    transact_address = random.choice(w3.eth.accounts)

    # Pack issue_from and issue_to into single string by using dumps (json.dumps)
    issue = {"issue_from": issue_from, "issue_to": issue_to}
    issue = dumps(issue)

    # Pack valid after and valid before into single string by using dumps (json.dumps)
    # We use relativedelta to increase the value of timestamp according to the validity period
    # In our cases, we fix it into 3 months.

    valid_after = datetime.datetime.now().timestamp()
    valid_before = (
        datetime.datetime.fromtimestamp(valid_after)
        + relativedelta(months=validity_period_in_months)
    ).timestamp()

    validity = {"valid_after": str(valid_after), "valid_before": str(valid_before)}
    validity = dumps(validity)

    # Generate user key-pairs
    user_key_pair = RSA.generate(2048)

    # The public key will be stored to blockchain
    # This library return bytes, we need to transform it to string to match with contract policy
    # .decode() = byte to str

    user_public_key = user_key_pair.public_key().export_key("PEM").decode()

    # Pack all of certificate element using string concatenation
    # So that we can use this string for signing
    # .encode() = string to byte. pycryptodome usually working with byte instead of string

    certificate_body = (
        serial_number
        + version
        + issue
        + validity
        + public_key_algorithm
        + user_public_key
    ).encode()

    # Perform signing and hash (for fingerprint)
    signature_algorithm = "PKCS1_15 with SHA256"
    # Sign by CA private key
    signature = CA_private_key.sign(SHA256.new(certificate_body)).decode("latin-1")
    # Generate fingerprint using SHA1
    # .hexdigest() mean byte to string (in hex form)
    SHA1_fingerprint = SHA1.new(certificate_body).hexdigest()

    try:
        # Perform transaction = add to blockchain
        PKI_certificate.functions.issue_certificate(
            serial_number,
            version,
            issue,
            validity,
            public_key_algorithm,
            user_public_key,
            signature_algorithm,
            signature,
            SHA1_fingerprint,
        ).transact({"from": transact_address})

        print(f"Add PKI certificate {serial_number} successfully.")

        # This section is for generating local storage directory
        # This is used for simulation of user's directory in different device
        # We will store certificate data in the user's device using only serial number and owner
        # If someone want more information, must use serial number to retrieve from blockchain
        data = {"serial_number": serial_number, "owner": issue_to}
        data = dumps(data)

        # use os library to create new directory name user_local_storage
        if not os.path.exists(f"./{issue_to}_local_storage"):
            os.makedirs(f"./{issue_to}_local_storage")

        # store user's private key
        with open(f"./{issue_to}_local_storage/{issue_to}_private_key.pem", "wb") as f:
            f.write(user_key_pair.export_key("PEM"))

        print(f"Transfer private key to {issue_to} storage successfully.")
        # store user's certificate

        with open(f"./{issue_to}_local_storage/{issue_to}_certificate.json", "w") as f:
            f.write(data)

        print(f"Transfer certificate serial number to {issue_to} successfully.")
        # return status code and payload
        return {
            "status_code": 1,
            "message": f"Issue certificate for {serial_number} successfully",
            "serial_number": serial_number,
        }

    # For error that some of execution violate policy of smart contract
    # (Specified in require(condition) in .sol file)

    except ContractLogicError as e:
        return {"status_code": -1, "message": e}

    # For unknown error
    except Exception as e:
        return {"status_code": 0, "message": e}


# Interface of certificate revokation function
def revoke_certificate(
    serial_number: str,
    reason: str = "Just want to revoke",
    issuer: str = "Good CA Company",
) -> dict:
    # Check if the certification is already revoked or not
    if view_revoke_certificate(serial_number)["status_code"] > 0:
        return {"status_code": -1, "message": "The certificate is already revoked."}

    # Select an address to make the transaction
    transact_address = random.choice(w3.eth.accounts)

    # Set the revocation date to be now's timestamp
    revocation_date = str(datetime.datetime.now().timestamp())

    # Then, pack everything into single string so that we can sign it
    revocation_body = (serial_number + revocation_date + issuer + reason).encode()

    # Sign and generate fingerprint
    signature_algorithm = "PKCS1_15 with SHA256"
    signature = CA_private_key.sign(SHA256.new(revocation_body)).decode("latin-1")
    SHA1_fingerprint = SHA1.new(revocation_body).hexdigest()

    try:
        # Add to blockchain
        PKI_certificate.functions.revoke_certificate(
            serial_number,
            revocation_date,
            issuer,
            reason,
            signature_algorithm,
            signature,
            SHA1_fingerprint,
        ).transact({"from": transact_address})
        print(f"Add revocation list of {serial_number} successfully.")

        return {"status_code": 1, "message": f"Revoke {serial_number} successfully."}

    # for the case that we violate smart contract policy
    # specify in require(condition) in .sol file
    except ContractLogicError as e:
        return {"status_code": -1, "message": e}

    # for unknown error
    except Exception as e:
        return {"status_code": 0, "message": e}


# Function for view certificate in the blockchain
def view_certificate(serial_number: str) -> dict:
    # as we have said, .call() will be used for viewing function in .sol file
    # It will always return but for the cases of non-existing object, it returns blank
    # Check, if necessary data in the certificate is missing => mean no certificate for that serial number

    certificate = PKI_certificate.functions.view_certificate(serial_number).call()
    if certificate[0] == "" or certificate[1] == "":
        return {"status_code": -1, "message": "Certificate is not found"}

    # For the case we have found the certificate
    # unpack value and store into dictionary for easier management and debugging
    # loads mean string to dictionary because issue = issue_to + isseu_from
    # validty = validity after + validity before

    version = certificate[0]
    issue = loads(certificate[1])
    validity = loads(certificate[2])
    public_key_algorithm = certificate[3]
    public_key = certificate[4].encode()
    signature_algorithm = certificate[5]
    signature = certificate[6].encode("latin-1")
    SHA1_fingerprint = bytes.fromhex(certificate[7])

    certificate = {
        "serial_number": serial_number,
        "version": version,
        "issue_from": issue["issue_from"],
        "issue_to": issue["issue_to"],
        "valid_after": validity["valid_after"],
        "valid_before": validity["valid_before"],
        "public_key_algorithm": public_key_algorithm,
        "public_key": public_key,
        "signature_algorithm": signature_algorithm,
        "signature": signature,
        "SHA1_fingerprint": SHA1_fingerprint,
    }

    print(f"Retrieve {serial_number} certificate from blockchain successfully.")
    return {"status_code": 1, "message": certificate}


# Interface for issuing attribute
def issue_attribute(
    holder: str,
    attributes: dict,
    validity_period_in_months: int = 3,
    version: str = "Version 1",
    issuer: str = "Good AA Company",
) -> dict:
    # Generate serial number for attribute certification
    serial_number = generate_serial_number()
    # Check if the serial number is taken by another attribute certificate
    if view_attribute(serial_number)["status_code"] > 0:
        return {"status_code": -1, "message": "serial number is duplicated"}

    # Check if the holder is existed?
    # You cannot generate attribute without generating PKI certificate first
    if view_certificate(holder)["status_code"] < 0:
        return {"status_code": -2, "message": "must obtain certificate first"}

    # Select an address to perform transaction
    transact_address = random.choice(w3.eth.accounts)

    # Pack validity data (validity after + validity before)
    valid_after = datetime.datetime.now().timestamp()
    valid_before = (
        datetime.datetime.fromtimestamp(valid_after)
        + relativedelta(months=validity_period_in_months)
    ).timestamp()

    validity = {"valid_after": str(valid_after), "valid_before": str(valid_before)}
    validity = dumps(validity)

    # Attributes can be many values such as age, role, workplace, country
    # We will pack all of them into one string because .sol file has degisned to recieve string input only
    # dumpes = dictionary to string
    holder_public_key = view_certificate(holder)["message"]["public_key"]
    holder_public_key = RSA.import_key(holder_public_key)
    holder_public_key = PKCS1_OAEP.new(holder_public_key)

    attributes_key = os.urandom(16)

    attributes = dumps(attributes).encode()
    attributes, iv = AES_encrypt(attributes, attributes_key)

    attributes = attributes.decode("latin-1")
    attributes_key = holder_public_key.encrypt(attributes_key).decode("latin-1")
    iv = holder_public_key.encrypt(iv).decode("latin-1")

    store_attribute_key(serial_number, attributes_key, iv)

    # Pack everything so that we can sign and create fingerprint
    # .encode() = string to type. pycryptodome usually work with byte rather than string
    attribute_body = (
        serial_number + version + issuer + holder + validity + attributes
    ).encode()

    # Then, we can sign and generate fingerprint
    signature_algorithm = "PKCS1_15 with SHA256"
    signature = AA_private_key.sign(SHA256.new(attribute_body)).decode("latin-1")
    SHA1_fingerprint = SHA1.new(attribute_body).hexdigest()

    try:
        # Add to the blockchain
        PKI_certificate.functions.issue_attribute(
            serial_number,
            version,
            issuer,
            holder,
            validity,
            attributes,
            signature_algorithm,
            signature,
            SHA1_fingerprint,
        ).transact({"from": transact_address})

        print(
            f"Add new attribute certificate number {serial_number} for {holder} successfully."
        )

        # Prepare data for making local certificate store in user's local storage
        # It will comprises of attribute certificate serial number, and holder (serial number of holder's PKI certificate)
        # Get user's PKI certificate serial number
        issue_to = view_certificate(holder)["message"]["issue_to"]
        # Transform it into string so that we can write it as a .json file
        data = {"serial_number": serial_number, "holder": holder}
        data = dumps(data)

        # Generate attribute certificate file on user's local storage
        # If someone want more information about attribute, just use this serial number and retrieve it from blockchain
        with open(
            f"./{issue_to}_local_storage/{issue_to}_attribute_certificate.json", "w"
        ) as f:
            f.write(data)
        print(
            f"Transfer attribute ceritifcate serial number to {issue_to} successfully."
        )

        return {
            "status_code": 1,
            "message": f"Issue attribute for {holder} successfully",
            "serial_number": serial_number,
        }

    # In cases we violate the condition of smart comtract
    # Specified in "require(condition)" in .sol file
    except ContractLogicError as e:
        return {"status_code": -1, "message": e}

    # For unknown error
    except Exception as e:
        return {"status_code": 0, "message": e}


# Interface with attribute revocation function
def revoke_attribute(
    serial_number: str,
    reason: str = "Just want to revoke",
    issuer: str = "Good CA Company",
) -> dict:
    # Check if this attribute is already revoked or not
    if view_revoke_attribute(serial_number)["status_code"] > 0:
        return {"status_code": -1, "message": "The attribute is already revoked"}

    # Select an address to make the transaction
    transact_address = random.choice(w3.eth.accounts)

    # Stamp the revocation date to be now's timestamp
    revocation_date = str(datetime.datetime.now().timestamp())

    # Pack everything into single string so that we can sign and generate fingerprint
    revocation_body = (serial_number + revocation_date + issuer + reason).encode()

    # Sign
    signature_algorithm = "PKCS1_15 with SHA256"
    signature = CA_private_key.sign(SHA256.new(revocation_body)).decode("latin-1")

    # Generate fingerprint
    SHA1_fingerprint = SHA1.new(revocation_body).hexdigest()

    try:
        # add to blockchain
        PKI_certificate.functions.revoke_attribute(
            serial_number,
            revocation_date,
            issuer,
            reason,
            signature_algorithm,
            signature,
            SHA1_fingerprint,
        ).transact({"from": transact_address})

        print(f"Revoke attribute certificate {serial_number} successfully.")
        return {"status_code": 1, "message": f"Revoke {serial_number} successfully"}

    # In cases we violate smart contract condition
    except ContractLogicError as e:
        return {"status_code": -1, "message": e}

    # For unknown error
    except Exception as e:
        return {"status_code": 0, "message": e}


# Interface with function view attribute
def view_attribute(serial_number: str) -> dict:
    attribute = PKI_certificate.functions.view_attribute(serial_number).call()

    # Check if some of the neccessary attribute certificate's components are blank
    # Then, it will mean that the attribute certificate does not exist
    # Solidty will try to return event there is no certificate match with the serial number (in form of blank list)
    if attribute[0] == "" or attribute[1] == "":
        return {"status_code": -1, "message": "Attribute is not found"}

    # Unpack everything into dictionary for easier mantainance and debugging
    version = attribute[0]
    issuer = attribute[1]
    holder = attribute[2]
    validity = loads(attribute[3])
    attributes = attribute[4]
    signature_algorithm = attribute[5]
    signature = attribute[6].encode("latin-1")
    SHA1_fingerprint = bytes.fromhex(attribute[7])

    attribute = {
        "serial_number": serial_number,
        "version": version,
        "issuer": issuer,
        "holder": holder,
        "valid_after": validity["valid_after"],
        "valid_before": validity["valid_before"],
        "attributes": attributes,
        "signature_algorithm": signature_algorithm,
        "signature": signature,
        "SHA1_fingerprint": SHA1_fingerprint,
    }

    print(
        f"Retrieve attribute certificate {serial_number} from blockchain successfully"
    )
    return {"status_code": 1, "message": attribute}


# Interface with CRL view function
def view_revoke_certificate(serial_number: str) -> dict:
    # Check if the revocation does exist
    revocation = PKI_certificate.functions.view_revocation(serial_number).call()
    if revocation[0] == "" or revocation[1] == "":
        return {"status_code": -1, "message": "Revocation is not found"}

    # Unpack everything into Python dictionary
    revocation_date = revocation[0]
    issuer = revocation[1]
    reason = revocation[2]
    signature_algorithm = revocation[3]
    signature = revocation[4].encode("latin-1")
    SHA1_fingerprint = bytes.fromhex(revocation[5])

    revocation = {
        "revocation_date": revocation_date,
        "issuer": issuer,
        "reason": reason,
        "signature_algorithm": signature_algorithm,
        "signature": signature,
        "SHA1_fingerprint": SHA1_fingerprint,
    }

    print(
        f"Retrieve certification revocation information of {serial_number} successfully."
    )
    return {"status_code": 1, "message": revocation}


# Interface with function viewing revocation of attribute certificate


def view_revoke_attribute(serial_number: str) -> dict:
    revocation = PKI_certificate.functions.view_revocation_attribute(
        serial_number
    ).call()

    # Check if the revocation does exists
    if revocation[0] == "" or revocation[1] == "":
        return {"status_code": -1, "message": "Revocation is not found"}

    # Unpack everything into Python dictionary
    revocation_date = revocation[0]
    issuer = revocation[1]
    reason = revocation[2]
    signature_algorithm = revocation[3]
    signature = revocation[4].encode("latin-1")
    SHA1_fingerprint = bytes.fromhex(revocation[5])

    revocation = {
        "revocation_date": revocation_date,
        "issuer": issuer,
        "reason": reason,
        "signature_algorithm": signature_algorithm,
        "signature": signature,
        "SHA1_fingerprint": SHA1_fingerprint,
    }

    print(f"Retrieve attribute certificate revocation of {serial_number} successfully.")
    return {"status_code": 1, "message": revocation}


# For store credential (user's password)


def store_credential(username: str, credential: str, algorith: str = "SHA256") -> dict:
    # Select an address to make the transaction
    transact_address = random.choice(w3.eth.accounts)
    # Must store in SHA256 form instead of clear data
    credential = SHA256.new(credential.encode()).hexdigest()
    algorithm = "SHA256"

    # Add to blockchain
    try:
        PKI_certificate.functions.store_credential(
            username, credential, algorithm
        ).transact({"from": transact_address})

        print(f"Store credential for {username} successfully.")
        return {"status_code": 1, "messsage": "Store credential successfully"}
    except ContractLogicError as e:
        return {"status_code": -1, "messsage": "duplicate username"}
    except Exception as e:
        return {"status_code": 0, "messsage": e}


# For retriving credential (in Hash form)
def get_credential(username: str) -> dict:
    try:
        credential = PKI_certificate.functions.get_credential(username).call()
        credential = {
            "credential": credential[0],
            "algorithm": credential[1],
        }

        print(f"Retrieve credential of {username} from blockchain successfully")
        return {"status_code": 1, "message": credential}
    except:
        return {"status_code": -1, "message": "username does not exist"}


def credential_validation(username: str, password: str) -> dict:
    password = SHA256.new(password.encode()).hexdigest()
    password_blockchain = get_credential(username)["message"]
    if "credential" in password_blockchain:
        password_blockchain = password_blockchain["credential"]
    if password == password_blockchain:
        return {"status_code": 1, "message": "password match."}
    else:
        return {"status_code": -1, "message": "password does not match."}


# For validation of certificate


def certificate_validation(serial_number: str):
    # Get certificate's information from blockchain
    result = view_certificate(serial_number)
    status_code = result["status_code"]
    certificate = result["message"]

    # Check if the certificate does exists
    if status_code < 0:
        return {"status_code": -1, "message": "The certificate is not found"}

    print("Finish checking for certificate existence: PASS")
    # Check if the certificate is expired
    if float(certificate["valid_before"]) - datetime.datetime.now().timestamp() < 0:
        return {"status_code": -2, "message": "The certificate is expired"}

    print("Finish checking for certificate expiration: PASS")
    # Check if the certificate is revoked
    result = view_revoke_certificate(serial_number)
    status_code = result["status_code"]

    print("Finish checking for revocation list: PASS")
    if status_code > 0:
        return {"status_code": -3, "message": "The user is revoked"}

    # Otherwise, we will check for signature
    # Pack every necessary information of certificate into single string
    # So that we can use this string to check signature

    version = certificate["version"]
    issue = dumps(
        {"issue_from": certificate["issue_from"], "issue_to": certificate["issue_to"]}
    )
    validity = dumps(
        {
            "valid_after": certificate["valid_after"],
            "valid_before": certificate["valid_before"],
        }
    )

    # Get user's public key and then transform into object of pycryptodome so that we can use it for decryption
    public_key_algorithm = certificate["public_key_algorithm"]
    user_public_key = RSA.import_key(certificate["public_key"])
    user_public_key = user_public_key.public_key().export_key("PEM").decode()

    # Now, all of necessary components of certificate is packed
    certificate_body = (
        serial_number
        + version
        + issue
        + validity
        + public_key_algorithm
        + user_public_key
    ).encode()

    # Check signature

    try:
        CA_public_key.verify(SHA256.new(certificate_body), certificate["signature"])
        print("Finish checking for signature: PASS")
        return {"status_code": 1, "message": "Certificate is valid"}

    # For the case that signature does not match
    except ValueError as e:
        return {"status_code": -3, "message": e}

    # For unknown error
    except Exception as e:
        return {"status_code": 0, "message": e}


# Similar to PKI certificate validation
def attribute_validation(serial_number: str):
    result = view_attribute(serial_number)
    status_code = result["status_code"]
    attribute = result["message"]

    # Check if certificate is existed
    if status_code < 0:
        return {"status_code": -1, "message": "The attribute is not found"}

    print("Finish checking for attribute existence: PASS")
    # Check expiration
    if float(attribute["valid_before"]) - datetime.datetime.now().timestamp() < 0:
        return {"status_code": -2, "message": "The attribute is expired"}

    print("Finish checking for attribute expiration: PASS")
    result = view_revoke_attribute(serial_number)
    status_code = result["status_code"]

    if status_code > 0:
        return {"status_code": -3, "message": "The attribute is revoked"}

    print("Finish checking for attribute revocation: PASS")
    version = attribute["version"]
    validity = dumps(
        {
            "valid_after": attribute["valid_after"],
            "valid_before": attribute["valid_before"],
        }
    )

    attributes = dumps(attribute["attributes"])
    attribute_body = (
        serial_number
        + version
        + attribute["issuer"]
        + attribute["holder"]
        + validity
        + attributes
    ).encode()
    # Check signature

    try:
        AA_public_key.verify(SHA256.new(attribute_body), attribute["signature"])
        print("Finish checking for attribute signature: PASS")
        return {"status_code": 1, "message": "Attribute is valid"}

    except ValueError as e:
        return {"status_code": -3, "message": e}

    except Exception as e:
        return {"status_code": 0, "message": e}


def store_attribute_key(serial_number, key, iv):
    transact_address = random.choice(w3.eth.accounts)
    PKI_certificate.functions.store_attribute_key(serial_number, key, iv).transact(
        {"from": transact_address}
    )
    print(f"Store key for attribute:{serial_number} in blockchain successfully.")


# Get key for the file according to the file's name
def get_attribute_key(serial_number):
    result = PKI_certificate.functions.get_attribute_key(serial_number).call()
    print(f"Retrieve key for attribute{serial_number} from blockchain successfully.")
    return {"key": result[0], "iv": result[1]}


def register(username: str, password: str, attributes: dict):
    try:
        PKI_credential = store_credential(username, password)
        print(PKI_credential)
        if PKI_credential["status_code"] < 0:
            return {"status_code": -1, "message": "User already exists"}

        PKI_certificate = issue_certificate(username)["serial_number"]
        attribute_certificate = issue_attribute(PKI_certificate, attributes)[
            "serial_number"
        ]
        return {
            "status_code": 1,
            "message": "Register complete",
            "PKI_certificate": PKI_certificate,
            "attribute_certificate": attribute_certificate,
        }

    except:
        return {"status_code": 0, "message": "unable to register"}


def decrypt_attribute(username):
    if get_credential(username)["status_code"] < 1:
        return {"status_code": -1, "message": "username does not exist"}

    with open(
        f"./{username}_local_storage/{username}_attribute_certificate.json", "r"
    ) as f:
        atttribute_serial = load(f)["serial_number"]

    with open(f"./{username}_local_storage/{username}_private_key.pem", "r") as f:
        private_key = PKCS1_OAEP.new(RSA.import_key(f.read()))

    attribute_key = get_attribute_key(atttribute_serial)
    attribute_key, attribute_iv = attribute_key["key"].encode("latin-1"), attribute_key[
        "iv"
    ].encode("latin-1")
    try:
        attribute_key = private_key.decrypt(attribute_key)
        attribute_iv = private_key.decrypt(attribute_iv)

    except:
        return {"status_code": -2, "message": "you are not the owner"}

    try:
        attribute = view_attribute(atttribute_serial)["message"]["attributes"].encode(
            "latin-1"
        )
        attribute = AES_decrypt(attribute, attribute_key, attribute_iv).decode()

    except:
        return {"status_code": -3, "message": "incorrect serial number"}

    return {"status_code": 1, "message": loads(attribute)}


"""
key = get_attribute_key("cc:8c:4c:e6:d9:43:21:d9:44:b9:ae:3e:c3:27:c5:ac")
AES_key, iv = key['key'].encode("latin-1"),key['iv'].encode("latin-1")

with open("./Blue_local_storage/Blue_private_key.pem","r") as f:
    private_key = PKCS1_OAEP.new(RSA.import_key(f.read()))

AES_key = private_key.decrypt(AES_key)
iv = private_key.decrypt(iv)

attributes = view_attribute("cc:8c:4c:e6:d9:43:21:d9:44:b9:ae:3e:c3:27:c5:ac")["message"]["attributes"]
attributes = attributes.encode("latin-1")
attributes = AES_decrypt(attributes,AES_key,iv).decode()
"""
