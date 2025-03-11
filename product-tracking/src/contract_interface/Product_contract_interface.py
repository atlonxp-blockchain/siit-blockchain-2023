from web3 import Web3
from web3.exceptions import ContractLogicError
from dateutil.relativedelta import relativedelta
from datetime import datetime
import secrets, string, random
import concurrent.futures

# Retrieve ABI of our smart contract
with open("./smart_contract/abi_Product.json", "r") as file:
    abi = file.read()

# Retrieve address of our smart contract
with open("./smart_contract/contract_address_Product.txt", "r") as file:
    contract_address = file.read()


with open("./smart_contract/network_deploy.txt", "r") as f:
    blockchain_network = f.read()

# Connect to the blockchain network
w3 = Web3(Web3.HTTPProvider(blockchain_network))

# Make smart contract object
Product = w3.eth.contract(address=contract_address, abi=abi)


def generate_product_ID():
    alphabet = string.ascii_letters + string.digits
    # Generate a random 128-character string
    random_string = "".join(secrets.choice(alphabet) for i in range(12))
    return random_string


def add_new_product(name, origin, manufacturer, product_info):
    transact_address = random.choice(w3.eth.accounts)

    product_ID = generate_product_ID()

    try:
        Product.functions.add_new_product(
            product_ID, name, origin, manufacturer, product_info, manufacturer
        ).transact({"from": transact_address})

        return {
            "status_code": 1,
            "message": "Add product sucessfully",
            "product_ID": product_ID,
        }

    except ContractLogicError as e:
        return {"status_code": -1, "message": "Product ID is duplicated"}

    except Exception as e:
        return {"status_code": -2, "message": "Unknown error"}


def list_product():
    return {"status_code": 1, "message": Product.functions.get_product_list().call()}


def get_last_product_record(product_ID):
    result = get_product_track_table(product_ID)["message"][0]
    return {"status_code": 1, "message": list(result)}


# This also sort the record
def get_product_track_table(product_ID):
    record = Product.functions.get_product_record(product_ID).call()
    list_record = []
    for item in record:
        timestamp = item[5]
        dt_object = datetime.fromtimestamp(timestamp)
        formatted_date = dt_object.strftime("%A, %d/%m/%Y, %H:%M:%S")
        new_record = item[:5] + (formatted_date,)
        list_record.append(new_record)

    list_record.sort(key=lambda x: x[5], reverse=True)
    return {"status_code": 1, "message": list_record}


def add_new_product_track(product_ID, new_owner, product_info):
    try:
        transact_address = random.choice(w3.eth.accounts)
        Product.functions.add_new_product_track(
            product_ID, new_owner, product_info
        ).transact({"from": transact_address})
        return {
            "status_code": 1,
            "message": f"transfer product to {new_owner} successfully.",
        }
    except ContractLogicError as e:
        return {"status_code": -1, "message": "The product ID does not exist."}

    except Exception as e:
        return {"status_code": -2, "message": "Unknown error"}


def is_my_product(product_id, username):
    if get_last_product_record(product_id)["message"][4] == username:
        return True
    else:
        return False


def get_my_product(username):
    list_product_ = list_product()["message"]
    my_product = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in list_product_:
            futures.append(executor.submit(is_my_product, i, username))
        for future, product_id in zip(futures, list_product_):
            if future.result():
                my_product.append(product_id)
    return my_product
