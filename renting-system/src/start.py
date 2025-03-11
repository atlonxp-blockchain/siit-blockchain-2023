from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    url_for,
    session,
    redirect,
    flash,
    abort,
)

import interface
import json
import os

import web3
from flask import Flask
import threading
import time

def get_sender_address(transaction_hash):
  """Gets the Solidity sender address from a transaction hash.

  Args:
    transaction_hash: The hash of the transaction.

  Returns:
    The sender's address.
  """

  

  # Get the transaction receipt
  receipt = web3.eth.getTransactionReceipt(transaction_hash)

  # Get the sender's address
  sender_address = receipt.sender

  return sender_address

def getAccountAddress2(userName):
    address2 = None  # Assign a default value

    if os.path.exists(userName):
        with open(f"{userName}","r") as f:
            address2 = f.read()

    return address2




app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "secret_key"



@app.errorhandler(500)
def internal_server_error(error):
    error_message = error.description

    referrer = request.referrer
    if referrer:
        flash(f" {error_message}.or you probaly may incorrectly fill the form.")
        return redirect(referrer)
    else:
        flash(f"Internal Server Error: {error_message}. Please try again later.")
        return redirect(url_for("index"))

@app.errorhandler(400)
def internal_server_error(error):
    error_message = error.description

    referrer = request.referrer
    if referrer:
        flash(f" {error_message}.or you probaly may incorrectly fill the form.")
        return redirect(referrer)
    else:
        flash(f"Internal Server Error: {error_message}. Please try again later.")
        return redirect(url_for("index"))
    
@app.errorhandler(405)
def internal_server_error(error):
    error_message = error.description

    referrer = request.referrer
    if referrer:
        flash(f" {error_message}.or you probaly may incorrectly fill the form.")
        return redirect(referrer)
    else:
        flash(f"Internal Server Error: {error_message}. Please try again later.")
        return redirect(url_for("index"))

def autopay():
    interface.autopay()
    # Perform your desired actions here

def schedule_function():
    while True:
        
        autopay()
        time.sleep(1)



@app.route("/")
# @app.route("/index")
# def gotoindex():

#     return render_template("index.html")

@app.route("/newindex")
def gotoindex():

    return render_template("newindex.html")


@app.route("/listing")
def gotolisting():
    return render_template("listing.html",box=interface.create_boxes())

def get_information(username):
    attribute = interface.decrypt_attribute(username)
    return attribute["message"]


@app.route("/registerRenter")
def gotoRegisterRenter():
 
    return render_template(
        "registerRenter.html",
        
    )
@app.route("/registerLandlord")
def gotoRegisterLandlord():
    return render_template(
        "registerLandlord.html",
         
    )

@app.route("/login")
def gotologin():
    return render_template("login.html")

@app.route("/accountlandlord", methods=["POST"])
def gotoaccountlandlord():
    data = request.form
    print(data)
    
    if "value" in data:
        if data["value"] == "registerlandlord":
            print("landlord registered")
            interface.registerLandlord(data["dormName"], data["userName"])
            print(getAccountAddress2(data["userName"]))
            print(interface.getBalanceLandlord(data["userName"]))
            
        elif data["value"] == "Landlord Add room":
            print("landlord add room")
            interface.addRoom(data["userName"],data["dormName"],data["price"],data["deposit"])
            
        elif data["value"] == "Landlord withdraw":
            print("landlord withdraw")
            interface.withdrawRent(data["userName"],data["amount"])
        elif data["value"] == "landlord Terminate Contact":
            interface.terminateContractLandlord(data["UserName"],data["terminateAddress"])
            return render_template("accountlandlord.html",balance=interface.getBalanceLandlord(data["UserName"]))
        elif data["value"] == "Login Landlord":
            userName = data["userName"]+".txt"
            if os.path.exists(userName):
                print(interface.getBalanceLandlord(data["userName"]))
                return render_template("accountlandlord.html",balance=interface.getBalanceLandlord(data["userName"]))
            else :
                flash(f"Wrong username")
                return redirect("/login",message="Wrong username")
    
    return render_template("accountlandlord.html",balance=interface.getBalanceLandlord(data["userName"]))
    

@app.route("/renterTerminateC")
def gotorenterTerminateC():
    
    return render_template("renterTerminateC.html")


@app.route("/landlordTerminateC")
def gotolandlordTerminateC():
    
    return render_template("landlordTerminateC.html")

@app.route("/accountrenter",methods=["POST"])
def gotoaccountrenter():
    data = request.form
    print(data)
    if "value" in data:
        if data["value"] == "renterregister":
            interface.registerRenter(data["userName"],data["dormName"],data["roomID"],int(data["deposit"]))
            return render_template("accountrenter.html",balance=interface.getBalanceRenter(data["userName"]))
        elif data["value"] == "deposit":
            try:
                interface.depositRent(data["userName"],data["amount"])
                
            except web3.exceptions.ContractLogicError as e:
                 error_message = str(e)
                 flash(f"Contract Error: {error_message}")
                 return redirect("/deposit")
            return render_template("accountrenter.html",balance=interface.getBalanceRenter(data["userName"]))
        elif data["value"] == "renter Terminate Contact":
            interface.terminateContractRenter(data["UserName"])
            return render_template("accountrenter.html",balance=interface.getBalanceRenter(data["UserName"]))
        elif data["value"] == "withdraw":
            interface.withdrawBalance(data["userName"],data["amount"])
            return render_template("accountrenter.html",balance=interface.getBalanceRenter(data["userName"]))
        elif data["value"] == "Login Renter":
                userName = data["userName"]+".txt"
                if os.path.exists(userName):
                    return render_template("accountrenter.html",balance=interface.getBalanceRenter(data["userName"]))
                else :
                    return render_template("login.html",balance=interface.getBalanceRenter(data["userName"]))         
    
    return redirect("/registerRenter",message="form error")

@app.route("/deposit")
def gotodeposit():
    
    return render_template("deposit.html")

@app.route("/withdrawrenter")
def gotowithdrawrenter():
    
    return render_template("withdrawrenter.html")   


@app.route("/withdrawlandlord")
def gotowithdrawlandlord():
    
    return render_template("withdrawlandlord.html")



@app.route("/getpending")
def gotogetpending():
    
    return render_template("getpending.html")


@app.route("/showpending",methods=["POST"])
def gotoshowpending():
    data = request.form
    print(data)
    if data["value"]== "landlord get pending":
        return render_template("showpending.html",pendinglist=interface.getPendingTermination(data["UserName"]))



@app.route("/afterpay", methods=["POST"])
def gotoafterpay():
    data = request.form
    print(data)
    if "value" in data:
        if data["value"] == "Renter Log in":
            interface.registerRenter(data["dormName"], data["userName"], data["roomId"])
    return render_template("accountrenter.html",username=data['userName'],dormName=data['dormName'])

@app.route("/addroom")
def gotoaddRoom():
    return render_template("addroom.html") 


@app.route("/getalldormnames")
def getalldormnames():
    return render_template("getalldormnames.html") 

@app.route("/getAvailableRoom")
def getAvailableRoom():
    
    return render_template("getAvailableRoom.html",alldormNames=interface.getAllDormNames())

@app.route("/getRoomprice", methods=["POST"])
def getRoomprice():
    data = request.form
    if "value" in data:
        if data["dormName"]!="":
                rooms = interface.getAvailableRooms(data["dormName"])
                print(rooms)
                return render_template("getRoomPrice.html", rooms=rooms)
        else:
                
                return redirect("/getalldormnames",message="dormitory did not exist")
    else:
        flash("Wrong username.")
        return redirect("/getalldormnames")

   
@app.route("/showroomprice", methods=["POST"])
def gotoshowroom():
    data = request.form
    roomprice,roomdeposit=interface.getRoomPrice(data["dormName"],data["roomID"])
    return render_template("showroomprice.html",roomprice=roomprice,roomdeposit=roomdeposit)





if __name__ == "__main__":
    # Start the scheduled function in a separate thread
    thread = threading.Thread(target=schedule_function)
    thread.start()






app.run("localhost", 5000)
