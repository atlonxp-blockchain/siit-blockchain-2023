from web3 import Web3
from web3.exceptions import ContractLogicError
from hashlib import sha256
import random,string

with open("./smart_contract/account_address_list.txt","r") as f:
    account_list = f.read().split("\n")

account_list.remove('')

# Retrieve ABI of our smart contract
with open("./smart_contract/abi.json", "r") as file:
    abi = file.read()

# Retrieve address of our smart contract
with open("./smart_contract/contract_address.txt", "r") as file:
    contract_address = file.read()

# Retrieve ABI of our smart contract
with open("./smart_contract/authen_abi.json", "r") as file:
    authen_abi = file.read()

# Retrieve address of our smart contract
with open("./smart_contract/authen_contract_address.txt", "r") as file:
    authen_contract_address = file.read()

with open("./smart_contract/network_deploy.txt", "r") as f:
    blockchain_network = f.read()

# Connect to the blockchain network
w3 = Web3(Web3.HTTPProvider(blockchain_network))

project_contract = w3.eth.contract(address=contract_address, abi=abi)
authen_contract = w3.eth.contract(address=authen_contract_address,abi=authen_abi)

def create_project(topic,description,goal,deadline,owner_address):
    project_contract.functions.create_project(topic,description,w3.to_wei(goal,"ether"),deadline).transact({"from":owner_address})
    print("Add project successfully")       

def get_last_project_ID():
    return project_contract.functions.get_last_project_ID().call() - 1

def get_project(project_id):
    return project_contract.functions.get_project(project_id).call()

def fund_project(project_id,value,funder_address):
    try:
        print(project_id)
        print(value)
        print(funder_address)
        project_contract.functions.fund_project(project_id).transact({"from":funder_address,"value":w3.to_wei(value,"ether")})
        return {"status":1,"output":f"Fund project with {value} ETH successfully"}
    except ContractLogicError as e:
        if("terminated" in e):
            return {"status":-1,"output":"The funding is already terminated"}
        
        elif("expired" in e):
            return {"status":-2,"output":"The funding is expired"}
        
        elif("Insufficient" in e):
            return {"status":-3,"output":"Insufficient fund"}
        else:
            return {"status":0,"output":"Unknown error"}
        
def get_funder_list(project_id):
    return project_contract.functions.get_funder_list(project_id).call()

def register(username,password,name,surname):
    if(get_credential(username)[2] != 0):
        return {"status":-1,"output":"Duplicated username"}
    
    account_address = random.choice(account_list)
    password = sha256(password.encode()).hexdigest()
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    salt = sha256(salt.encode()).hexdigest()
    hash_password = sha256((password+salt).encode()).hexdigest()
    
    try:
        authen_contract.functions.register(username,hash_password,salt,account_address,name,surname).transact({"from":account_address})       
        account_list.remove(account_address)
        return {"status":1,"output":"register successfully."}
    
    except ContractLogicError as e:
        if("Duplicated" in e):
            return {"status":-1,"output":"Duplicated username"}
        return {"status":0,"output":"Unknown error"}

def get_credential(username):
    return authen_contract.functions.get_credential(username).call()

def get_user_info(username):
    return authen_contract.functions.get_info(username).call()

def credential_validation(username,password):
    if(get_credential(username)[2] == 0):
        return {"status":-1,"output":"Username does not exist"}
    
    password = sha256(password.encode()).hexdigest()
    pass_blockchain,salt_blockchain,status = get_credential(username)
    password = sha256((password+salt_blockchain).encode()).hexdigest()
    if password == pass_blockchain:
        return {"status":1,"output":"pass"}
    return {"status":-2,"output":"password is incorrect"}

def get_ETH(username):
    address = get_user_info(username)[0]
    return w3.from_wei(w3.eth.get_balance(address),"ether")