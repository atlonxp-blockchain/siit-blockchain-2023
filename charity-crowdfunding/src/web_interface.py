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

import contract_interface as contract
import json
from datetime import datetime


app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "secret_key"

@app.route("/")
@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/login",methods=["POST"])
def login():
    data = request.form
    status = contract.credential_validation(data['username'],data['password'])
    if(status['status'] < 0):
        flash("Username or password is incorrect")
        return redirect("/landing")
    else:
        flash("Login successfully!")
        session['username'] = data['username']
        return redirect("/homepage")

@app.route("/register",methods=["POST"])
def register():
    data = request.form
    status = contract.register(data['username'],data['password'],data['firstname'],data['lastname'])
    
    if(status['status'] < 0):
        flash("Username is duplicated")
    else:
        session['username'] = data['username']
        flash("Register successfully!")

    return redirect("/landing")

@app.route("/add_project",methods=['POST'])
def add_project():
    data = request.form
    print(data)
    status = contract.credential_validation(session['username'],data['password'])
    if(status['status'] < 0):
        flash("Username or password is incorrect")
        
    else:
        datetime_obj = datetime.strptime(data['deadline'], "%Y-%m-%d")
        deadline = int(datetime_obj.timestamp())
        address = contract.get_user_info(session['username'])[0]
        contract.create_project(data['topic'],data['desc'],float(data['goal']),deadline,address)
        flash("Add project successfully!")

    return redirect("/homepage")

@app.route("/see_past")
def see_past():
    address,firstname,lastname = contract.get_user_info(session['username'])
    ethereum = contract.get_ETH(session['username'])
    project_list = []
    funder_list = []
    total_donate = 0
    total_fund = 0
    last_project_id = contract.get_last_project_ID()
    
    for project_id in range(1,last_project_id+1):

        if(not(contract.get_project(project_id)[-1] == 1 and contract.get_project(project_id)[6] > datetime.now().timestamp())):
            project_list.append(list(contract.get_project(project_id)))
            funder_list.append(list(contract.get_funder_list(project_id)))

    for project_id in range(len(project_list)):
            date_string = datetime.fromtimestamp(project_list[project_id][6]).strftime('%Y-%m-%d %H:%M:%S')
            project_list[project_id][6] = date_string

            date_string = datetime.fromtimestamp(project_list[project_id][5]).strftime('%Y-%m-%d %H:%M:%S')
            project_list[project_id][5] = date_string  

    for project_id in range(1,last_project_id+1):
        project = contract.get_project(project_id)
        total_donate+=(project[3]/1000000000000000000)
        total_fund+=(project[4]/1000000000000000000)

    project_id_index = [i for i in range(len(project_list))]


    return render_template("see_past.html",address=address,firstname=firstname,lastname=lastname,ETH=ethereum,project_list=project_list,funder_list=funder_list,total_donate=total_donate,total_fund=total_fund,project_id_index=project_id_index)


@app.route("/fund_project",methods=["POST"])

def fund_project():
    data = request.form
    print(data)
    status = contract.credential_validation(session['username'],data['password'])
    if(status['status'] < 0):
        flash("Username or password is incorrect")
        
    else:
        address = contract.get_user_info(session['username'])[0]
        status = contract.fund_project(int(data['id']),float(data['value']),address)
        if(status['status'] < 0):
            flash(f"Unable to fund: {status['output']}")
        else:
            flash("Fund successfully!")

    return redirect("/homepage") 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/landing")

@app.route("/homepage")
def homepage():
    address,firstname,lastname = contract.get_user_info(session['username'])
    ethereum = contract.get_ETH(session['username'])
    project_list = []
    funder_list = []
    total_donate = 0
    total_fund = 0
    last_project_id = contract.get_last_project_ID()
    
    for project_id in range(1,last_project_id+1):

        if(contract.get_project(project_id)[-1] == 1 and contract.get_project(project_id)[6] > datetime.now().timestamp()):
            project_list.append(list(contract.get_project(project_id)))
            funder_list.append(list(contract.get_funder_list(project_id)))

    for project_id in range(len(project_list)):
            date_string = datetime.fromtimestamp(project_list[project_id][6]).strftime('%Y-%m-%d %H:%M:%S')
            project_list[project_id][6] = date_string

            date_string = datetime.fromtimestamp(project_list[project_id][5]).strftime('%Y-%m-%d %H:%M:%S')
            project_list[project_id][5] = date_string  

    for project_id in range(1,last_project_id+1):
        project = contract.get_project(project_id)
        total_donate+=(project[3]/1000000000000000000)
        total_fund+=(project[4]/1000000000000000000)

    project_id_index = [i for i in range(len(project_list))]


    return render_template("homepage.html",address=address,firstname=firstname,lastname=lastname,ETH=ethereum,project_list=project_list,funder_list=funder_list,total_donate=total_donate,total_fund=total_fund,project_id_index=project_id_index)

app.run("localhost", 5000)
