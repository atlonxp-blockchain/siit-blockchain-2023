import contract_interface as contract
import random
from datetime import datetime, timedelta


with open("./smart_contract/account_address_list.txt","r") as f:
    account_list = f.read().split("\n")

account_list.remove('')


# Get the current timestamp
current_timestamp = datetime.now()
# Add one day to the current timestamp
one_day = timedelta(days=1)
new_timestamp = int((current_timestamp + one_day).timestamp())

for i in range(5):
    address = random.choice(account_list)
    contract.create_project(f"Topic {i}",f"Description for project {i}",10,new_timestamp,address)

for i in range(5):
    print(contract.get_project(i))