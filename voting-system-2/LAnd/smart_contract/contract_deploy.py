from solcx import compile_standard, install_solc
from web3 import Web3
from json import dump
from random import choice
from os import chdir

chdir("./smart_contract")
# Set the version of solidity compiler

install_solc("0.8.5")

with open("network_deploy.txt","r") as f:
    blockchain_network = f.read()

w3 = Web3(Web3.HTTPProvider(blockchain_network))
with open("contract.sol", "r") as file:
    contract = file.read()

complied_contract = compile_standard(
    {
        "language": "Solidity",
        "sources": {"contract.sol": {"content": contract}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.5",
)

bytecode = complied_contract["contracts"]["contract.sol"]["Poll"]["evm"]["bytecode"]["object"]
abi = complied_contract["contracts"]["contract.sol"]["Poll"]["abi"]

with open("complied_contract.json", "w") as file:
    dump(complied_contract, file)

with open("abi.json", "w") as file:
    dump(abi, file)

deploy_address = w3.eth.accounts[0]

poll_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
transaction = poll_contract.constructor().transact({"from": deploy_address})
contract_address = w3.eth.wait_for_transaction_receipt(transaction)

with open("contract_address.txt", "w") as file:
    file.write(contract_address.contractAddress)