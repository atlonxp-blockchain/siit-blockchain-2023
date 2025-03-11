from web3 import Web3
from web3.exceptions import ContractLogicError
from dateutil.relativedelta import relativedelta
from datetime import datetime
import secrets, string, random
import concurrent.futures
import os
import random
import base64
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


#get account address require userName
def getAccountAddress(userName):
    address = None 
    filename=userName+".txt"
    if os.path.exists(filename):
        with open(f"{filename}","r") as f:
            address=f.read()
    return address

def get_random_account():
    account_list = w3.eth.accounts.copy()
    selected_account = random.choice(account_list)
    account_list.remove(selected_account)
    return selected_account

def registerLandlord(dormName,userName):

    if not os.path.exists(userName):
        accountlist=w3.eth.accounts.copy()
        account=random.choice(accountlist)
        accountlist.remove(account)

        with open(f"{userName}.txt","w") as f:
            f.write(account)
    
        Product.functions.registerLandlord(dormName).transact({"from":account})
    
import os
import random

def registerRenter(userName, dormName, roomID, value):
    if not os.path.exists(userName):
        accountlist = w3.eth.accounts.copy()
        account = random.choice(accountlist)

        with open(f"{userName}.txt", "w") as f:
            f.write(account)

        try:
            Product.functions.registerRenter(dormName, int(roomID)).transact({"from": account, "value": int(value)})
        except Exception as e:
            # Delete the account.txt file if an error occurs
            os.remove(f"{userName}.txt")
            # Handle or log the error message
            print(f"Error: {str(e)}")


def getAllDormNames():
    return Product.functions.getAllDormNames().call()

def getAvailableRooms(dormName):
    return Product.functions.getAvailableRooms(dormName).call()


def getBalanceRenter(userName):
    return Product.functions.getBalanceRenter().call({"from":getAccountAddress(userName)})

def getBalanceLandlord(userName):
    return Product.functions.getBalanceLandlord().call({"from":getAccountAddress(userName)})

def addRoom(userName,dormName,price,deposit):
    Product.functions.addRoom(dormName,int(price),int(deposit)).transact({"from":getAccountAddress(userName)})

def getRoomPrice(dormName,roomId):
    return Product.functions.getRoomPrice(dormName,int(roomId)).call()


def depositRent(userName,value):
    Product.functions.depositRent().transact({"from":getAccountAddress(userName),"value":int(value)})
    return {"status":1,"output":f"Deposit{value} ETH successfully"}

#for landlord only
def withdrawRent(userName,value):
    return Product.functions.withdrawRent(int(value)).transact({"from":getAccountAddress(userName)})
#withdraw for renters
def withdrawBalance(userName,value):
    return Product.functions.withdrawBalance(int(value)).transact({"from":getAccountAddress(userName)})

def terminateContractRenter(userName):
   
    Product.functions.terminateContractRenter().transact({"from": getAccountAddress(userName)})
    alert_panel = '''
        <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    background-color: #f8d7da; padding: 10px; border: 1px solid #f5c6cb;
                    border-radius: 5px; text-align: center; font-weight: bold;">
            YOUR CONTRACT HAS BEEN TERMINATED
            <span style="position: absolute; top: 5px; right: 5px; cursor: pointer;"
                  onclick="this.parentNode.style.display = 'none';">X</span>
        </div>
    '''
    return {alert_panel}

   
def terminateContractLandlord(userName, termiAddress):
    Product.functions.terminateContractLandlord(Web3.to_checksum_address(termiAddress)).transact({"from": getAccountAddress(userName)})
    # alert_panel = '''
    #     <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
    #                 background-color: #f8d7da; padding: 10px; border: 1px solid #f5c6cb;
    #                 border-radius: 5px; text-align: center; font-weight: bold;">
    #         YOUR CONTRACT HAS BEEN TERMINATED
    #         <span style="position: absolute; top: 5px; right: 5px; cursor: pointer;"
    #               onclick="this.parentNode.style.display = 'none';">X</span>
    #     </div>
    # '''
    # return {alert_panel}

def getPendingTermination(userName):
    return Product.functions.getPendingTermination().call({"from":getAccountAddress(userName)})



def autopay():
    Product.functions.autopay().transact({'from': get_random_account()})



#terminateContractAuto doesnt need one it is auto just reminding




    


