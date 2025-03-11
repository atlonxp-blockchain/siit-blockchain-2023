from web3 import Web3
from web3.exceptions import ContractLogicError
from dateutil.relativedelta import relativedelta
from datetime import datetime
import secrets, string, random
import concurrent.futures

# Retrieve ABI of our smart contract
with open("./smart_contract/abi_PKI.json", "r") as file:
    abi = file.read()

# Retrieve address of our smart contract
with open("./smart_contract/contract_address_PKI.txt", "r") as file:
    contract_address = file.read()



blockchain_network = 'HTTP://127.0.0.1:7545'

# Connect to the blockchain network
w3 = Web3(Web3.HTTPProvider(blockchain_network))

# Make smart contract object
Product = w3.eth.contract(address=contract_address, abi=abi)

username="peem"

accountlist=w3.eth.accounts.copy()

account=random.choice(accountlist)

accountlist.remove(account)


with open(f"{username}-address","w") as f:
    f.write(account)

with open(f"{username}-address","r") as f:
    a=f.read()

username="keem"



account=random.choice(accountlist)

accountlist.remove(account)


with open(f"{username}-address","w") as f:
    f.write(account)

with open(f"{username}-address","r") as f:
    a=f.read()
