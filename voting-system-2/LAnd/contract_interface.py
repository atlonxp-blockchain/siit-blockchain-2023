from web3 import Web3
from web3.exceptions import ContractLogicError

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

def start_vote(msg_address):
    try:
        contract.functions.startVote().transact({"from":msg_address})
        print("Vote is start")
    except ContractLogicError as e:
        print(f"Error: {e}")

def end_vote(msg_address):
   
    contract.functions.endVote().transact({"from":msg_address})
       

def add_candidate(id,name,party,campaign,msg_address):
    contract.functions.addCandidate(id,name,party,campaign).transact({"from":msg_address})
    print("Add candidate succesfully")

def vote_for_candidate(candidate,msg_address):
    try:
        contract.functions.voteForCandidate(candidate).transact({"from":msg_address})
        print(f"Vote for {candidate} successfully")
        return (True,"OK")
    except ContractLogicError as e:
        print(f"Error: {e}")
        e = str(e)
        if "started" in e:
            return (False,"Vote has not started or has ended")
        elif "Already" in e:
            return (False,"You have already voted")
        elif "Invalid" in e:
            return (False,"Invalid candidate")
        else:
            return (False,"Unknown error")

def get_vote_counts_for_all_candidates():
    try:
        return contract.functions.getVoteCountsForAllCandidates().call()
    except ContractLogicError as e:
        print(f"Error: {e}")

def get_candidate():
    return contract.functions.getCandidate().call()

def get_candidate_info():
    return contract.functions.getCandidateInfo().call()

def get_deploy_address():
    return w3.eth.accounts[0]

def registerUser(username, password , firstname,lastname,msg_address):
    contract.functions.registerUser(username,password,firstname,lastname).transact({"from":msg_address})

def get_user_info(Usename):
    return contract.functions.get_user_info(Usename).call()
    



