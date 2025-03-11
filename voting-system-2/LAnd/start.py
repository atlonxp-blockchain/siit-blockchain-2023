from web3 import Web3
from flask import redirect 
import random
import requests 
from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    flash,
)

import contract_interface

with open("./smart_contract/network_deploy.txt", "r") as f:
    blockchain_network = f.read()

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "secret_key"
w3 = Web3(Web3.HTTPProvider(blockchain_network))


@app.route("/vote", methods=["POST","Get"])
def vote():
    info = contract_interface.get_candidate_info()
    return render_template("vote.html", info=info)


@app.route("/add_candidate")
def add_candidate():
    return render_template("add_candidate.html")


@app.route("/add_new_candidate", methods=["POST"])
def add_new_candidate():
    data = request.form
    contract_interface.add_candidate(
        int(data["id"]),
        data["name"],
        data["party"],
        data["campaign"],
        contract_interface.get_deploy_address(),
    )
    return redirect("/add_candidate") 




@app.route("/start")
def start():
    contract_interface.start_vote(contract_interface.get_deploy_address())
    return  redirect("/vote") 
 
    


@app.route("/end")
def end():
    contract_interface.end_vote(contract_interface.get_deploy_address())
    return redirect("/result")


@app.route("/register", methods=["POST"])
def register():
    data = request.form
    accountlist = w3.eth.accounts.copy()
    account = random.choice(accountlist)
    accountlist.remove(account)
    with open(f"{data['username']}.txt", "w") as f:
        f.write(account)

    status = contract_interface.registerUser(
        data["username"],
        data["password"],
        data["firstname"],
        data["lastname"],
        account,
    )

    session["address"] = account
    session["username"] = data["username"]
    flash("Register successfully!")
    return redirect("/")


@app.route("/Login" ) 
def login():
    data = request.form
    username = data["username"]
    password = data["password"]
    info = contract_interface.get_user_info(username)[1]

    # Perform login authentication logic here
    if password == info:
        with open(f"{data['username']}.txt", "r") as f:
            session["address"] = f.read()

        session["username"] = username
        flash("Login successful!")
        return redirect("/vote")
    else:
        flash("Invalid username or password")
        return redirect("/login")


@app.route("/") 
def loginPage():
    return render_template("Login.html")


@app.route("/register_page")
def register_page():
    return render_template("register.html")


@app.route("/result")
def result():
    score = contract_interface.get_vote_counts_for_all_candidates()
    return render_template("result.html", score=score)


@app.route("/doingvote", methods=["POST"])
def doingvote():
    data = request.form
    contract_interface.vote_for_candidate(data["candidate_name"], session["address"])
    return redirect("/vote") 




if __name__ == "__main__":
    app.run("localhost", 5000)
