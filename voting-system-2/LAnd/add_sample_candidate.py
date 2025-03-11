from web3 import Web3
from web3.exceptions import ContractLogicError
import contract_interface

# Retrieve ABI of our smart contract
with open("./smart_contract/abi.json", "r") as file:
    abi = file.read()

# Retrieve address of our smart contract
with open("./smart_contract/contract_address.txt", "r") as file:
    contract_address = file.read()

with open("./smart_contract/network_deploy.txt", "r") as f:
    blockchain_network = f.read()

w3 = Web3(Web3.HTTPProvider(blockchain_network))
contract = w3.eth.contract(address=contract_address, abi=abi)

deploy_address = w3.eth.accounts[0]

contract_interface.add_candidate(1,"A1","Party A","Good Very good",deploy_address)
contract_interface.add_candidate(2,"A2","Party B","Very Well",deploy_address)
contract_interface.add_candidate(3,"A3","Party C","Good",deploy_address)
contract_interface.add_candidate(4,"A4","Party D","OK!",deploy_address)