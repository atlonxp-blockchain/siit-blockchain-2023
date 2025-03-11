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

with open("simple_authen.sol","r") as file:
    authen_contract = file.read()

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

complied_authen_contract = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simple_authen.sol": {"content": authen_contract}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.5",
)

bytecode = complied_contract["contracts"]["contract.sol"]["project_fund"][ "evm"]["bytecode"]["object"]
abi = complied_contract["contracts"]["contract.sol"]["project_fund"]["abi"]

authen_bytecode = complied_authen_contract["contracts"]["simple_authen.sol"]["authentication"][ "evm"]["bytecode"]["object"]
authen_abi = complied_authen_contract["contracts"]["simple_authen.sol"]["authentication"]["abi"]

with open("complied_contract.json", "w") as file:
    dump(complied_contract, file)

with open("abi.json", "w") as file:
    dump(abi, file)

with open("complied_authen_contract.json", "w") as file:
    dump(complied_authen_contract, file)

with open("authen_abi.json", "w") as file:
    dump(authen_abi, file)

deploy_address = w3.eth.accounts[0]

project_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
transaction_project = project_contract.constructor().transact({"from": deploy_address})
contract_address = w3.eth.wait_for_transaction_receipt(transaction_project)

with open("contract_address.txt", "w") as file:
    file.write(contract_address.contractAddress)

authen_contract = w3.eth.contract(abi=authen_abi, bytecode=authen_bytecode)
transaction_authen = authen_contract.constructor().transact({"from": deploy_address})
authen_contract_address = w3.eth.wait_for_transaction_receipt(transaction_authen)

with open("authen_contract_address.txt", "w") as file:
    file.write(authen_contract_address.contractAddress)

with open("account_address_list.txt","w") as file:
    for account in w3.eth.accounts:
        file.write(account+"\n")