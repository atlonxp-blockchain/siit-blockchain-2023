from solcx import compile_standard, install_solc
from web3 import Web3
from json import dump
from random import choice
from os import chdir


chdir("./smart_contract")
# Set the version of solidity compiler

install_solc("0.8.19")

# Currently, we use Ganache or localhost blockchain network for operating.
# However, you can change it into productive URL blockchain network for further deployment.
# Ganache is using Proof of Work
# We suggest that we should rely on Proof of Authority for speed and reliability
# However, even testnet, it is now force us to have ETH in wallet

blockchain_network = 'HTTP://127.0.0.1:7545'

w3 = Web3(Web3.HTTPProvider(blockchain_network))

# Retrieve target solidity file to compile and deploy to the blockchain network.
with open("RentalAgreement.sol", "r") as file:
    RentalAgreement = file.read()

# Then, we can finally compile our smart contract.
# solc_version must match with install_solc in the 7 line.

complied_RentalAgreement = compile_standard(
    {
        "language": "Solidity",
        "sources": {"RentalAgreement.sol": {"content": RentalAgreement}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.19",
)



# After we compile our code, there will be many components stored in dictionary form.
# We will retrieve only its bytecode and abi for deploying our contract to the blockchain network
# Retrieve bytecode (Mostly, assembly)

bytecode_PKI = complied_RentalAgreement["contracts"]["RentalAgreement.sol"]["RentalAgreement"][ "evm"]["bytecode"]["object"]


# Retrieve ABI (Application Binary Interface)

abi_PKI = complied_RentalAgreement["contracts"]["RentalAgreement.sol"]["RentalAgreement"]["abi"]


# Save our complied smart contract into json file
# This enable other Python files to interact and interface with our contract
# Just read the compiled file, and then retriving only bytecode and APIzzzzz

with open("complied_RentalAgreement.json", "w") as file:
    dump(complied_RentalAgreement, file)



# save abi file for futher use
with open("abi_PKI.json", "w") as file:
    dump(abi_PKI, file)



# Random the account to deploy the contract. However, you can set a specific one if you want

deploy_address1 = choice(w3.eth.accounts)


# Create contract object by pipeline the ABI and bytecode from the above

Rental_Agreement_Cer = w3.eth.contract(abi=abi_PKI, bytecode=bytecode_PKI)


# Transact the contract to the blockchain

transaction_PKI = Rental_Agreement_Cer.constructor().transact({"from": deploy_address1})
contract_address_PKI = w3.eth.wait_for_transaction_receipt(transaction_PKI)



# Store the address to the file so that other Python files can access the address automatically by reading this file

with open("contract_address_PKI.txt", "w") as file:
    file.write(contract_address_PKI.contractAddress)

chdir("..")