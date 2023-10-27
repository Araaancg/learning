from flask import Flask, make_response, request, Response, redirect, render_template, session,g
import requests as req
from secrets import token_hex
from functools import wraps
import json
import sqlite3

app = Flask(__name__)
app.secret_key = token_hex()

DB = "./users.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

def get_all(con,table):
    result = {"users":[]}
    cur = con().cursor()
    query = f"SELECT * FROM {table};"
    fields = tuple(field[1] for field in cur.execute(f"PRAGMA table_info ({table});"))
    for element in cur.execute(query):
        result["users"].append(dict(zip(fields,element)))
    return json.dumps(result, sort_keys=False)

@app.route("/api/users", methods=["GET","POST"])
def all_users():
    return Response(get_all(con,"users"), content_type="application/json")


def authenticate(f):
        @wraps(f)
        def i():
            args_email = request.args["email"]
            args_pwd = request.args["pwd"]
            
            api_res = req.get("http://localhost:5000/api/users").json()
            
            for user in api_res:
                print(user)
                if user["email"] == args_email and user["pwd"] == args_pwd:
                    session["id"] = user["id"]
                    session["email"] = user["email"]
                    return True
            return False
        return i


@app.route("/login", methods=["GET","POST"])
@authenticate
def login():
    print(request.args)
    #localhost:5000/login?id=1t&email=test1@email.com
    # session["id"] = request.args["id"]
    # session["email"] = request.args["email"]
    print(session.values())
    return "login"

@app.route("/dea/secret")
def secret():
    print(request.cookies)
    return "secret"


if __name__ == "__main__":
    app.run(debug=True)