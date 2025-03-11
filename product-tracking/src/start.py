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

from contract_interface import PKI_contract_interface
from contract_interface import Product_contract_interface

import json

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "secret_key"


@app.route("/")
@app.route("/landing")
def landing():
    return render_template("landing.html")


def get_information(username):
    attribute = PKI_contract_interface.decrypt_attribute(username)
    return attribute["message"]


@app.route("/my_profile", methods=["GET"])
def my_profile():
    attribute = get_information(session["username"])
    return render_template(
        "profile.html",
        name=attribute["name"],
        surname=attribute["surname"],
        number=attribute["number"],
        email=attribute["email"],
        address=attribute["address"],
        username=session["username"],
    )


@app.route("/profile", methods=["POST"])
def profile():
    data = request.form
    if "type" in data:
        if data["type"] == "Log in":
            username = data["username"]
            password = data["password"]
            login_status = PKI_contract_interface.credential_validation(
                username, password
            )

            if login_status["status_code"] < 0:
                flash("Username or Password is incorrect.")
                return render_template("landing.html")

            else:
                session["username"] = username
                return redirect("/product")

        elif data["type"] == "Sign up":
            username = data["username"]
            password = data["password"]
            attribute = data.to_dict()

            del attribute["type"]
            del attribute["username"]
            del attribute["password"]

            register_status = PKI_contract_interface.register(
                username, password, attribute
            )

            if register_status["status_code"] < 0:
                flash("Unable to register, username is duplicated.")
                return render_template("landing.html")

            else:
                flash("Register successfully")
                return redirect("/landing")

        elif data["type"] == "change_profile":
            username = session["username"]
            password = data["password"]
            login_status = PKI_contract_interface.credential_validation(
                username, password
            )

            if login_status["status_code"] < 0:
                flash("Username or Password is incorrect.")
                attribute = get_information(username)
                return render_template(
                    "profile.html",
                    name=attribute["name"],
                    surname=attribute["surname"],
                    number=attribute["number"],
                    email=attribute["email"],
                    address=attribute["address"],
                    username=username,
                )

            else:
                with open(f"{username}_local_storage/{username}_certificate.json") as f:
                    holder = f.read()

                holder = json.loads(holder)["serial_number"]
                attribute = data.to_dict()

                del attribute["type"]
                del attribute["password"]

                register_status = PKI_contract_interface.issue_attribute(
                    holder, attribute
                )

                attribute = get_information(username)
                return render_template(
                    "profile.html",
                    name=attribute["name"],
                    surname=attribute["surname"],
                    number=attribute["number"],
                    email=attribute["email"],
                    address=attribute["address"],
                    username=username,
                )
        else:
            abort(400, "Bad Request: Your request is illegal")
    else:
        abort(400, "Bad Request: Your request is illegal")


@app.route("/product")
def product():
    username = session["username"]
    my_product_list = []
    my_product = Product_contract_interface.get_my_product(username)
    for product_ID in my_product:
        my_product_list.append(
            [product_ID]
            + Product_contract_interface.get_last_product_record(product_ID)["message"]
        )

    return render_template("product.html", product_list=my_product_list)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/landing")


@app.route("/tracking", methods=["GET"])
def tracking():
    data = request.args
    product_id = data["product_id"]
    tracks = Product_contract_interface.get_product_track_table(product_id)["message"]
    return render_template("tracking.html", product_id=product_id, tracks=tracks)


@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.form
    username = session["username"]
    data = data.to_dict()
    data["manufacturer"] = username
    password = data["password"]
    verify_status = PKI_contract_interface.credential_validation(username, password)
    if verify_status["status_code"] < 0:
        flash("Username or Password is incorrect.")

    else:
        Product_contract_interface.add_new_product(
            data["product_name"],
            data["origin"],
            data["manufacturer"],
            data["detail"],
        )

    return redirect("/product")


@app.route("/send_product", methods=["POST"])
def send_product():
    data = request.form
    status = PKI_contract_interface.credential_validation(
        session["username"], data["password"]
    )
    if status["status_code"] < 0:
        flash("Username or Password is incorrect.")
    else:
        product_id = data["product_id"]
        new_owner = data["new_owner"]
        product_info = data["product_info"]
        recv_status = PKI_contract_interface.get_credential(new_owner)

        if recv_status["status_code"] < 0:
            flash("Cannot found matched receiver")

        elif session["username"] == new_owner:
            flash("The sender and reciever is the same!")

        else:
            Product_contract_interface.add_new_product_track(
                product_id, new_owner, product_info
            )

    return redirect("/product")


app.run("localhost", 5000)
