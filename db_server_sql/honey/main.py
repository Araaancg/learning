from flask import Flask,g,request
import sqlite3
from funcs import *

app = Flask(__name__)

DB = "./honey.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

@app.route("/honey")
def home():
    return "Working on it, be patient :)"

@app.route("/honey/collectors", methods=["GET","POST"])
def collectors():
    if request.method == "GET":
        return get_all(con, "collectors")

    if request.method == "POST":
        create_id(con,"collectors")
        new_row = insert_new_row(con,request,"collectors")
        if new_row:
            return {"success":True}

@app.route("/honey/providers", methods=["GET","POST"])
def providers():
    if request.method == "GET":
        return get_all(con, "providers")
    
    if request.method == "POST":
        new_row = insert_new_row(con,request,"providers")
        if new_row:
            return {"success":True}

@app.route("/honey/purchases", methods=["GET"])
def pruchases():
    return get_all(con, "purchases")
    









if __name__ == "__main__":
    app.run(debug=True)