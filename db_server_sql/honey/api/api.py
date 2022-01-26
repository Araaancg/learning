from flask import Flask,g,request,Response
import sqlite3
from funcs import *

app = Flask(__name__)

DB = "./honey.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

@app.route("/api")
def home():
    return "Working on it, be patient :)"

@app.route("/honey/api/collectors", methods=["GET","POST"])
def collectors():
    if request.method == "GET":
        # return get_all(con, "collectors")
        return Response(get_all(con, "collectors"),content_type="application/json")

    if request.method == "POST":
        create_id(con,"collectors")
        new_row = insert_new_row(con,request,"collectors")
        if new_row:
            return {"success":True}

@app.route("/honey/api/providers", methods=["GET","POST"])
def providers():
    if request.method == "GET":
        # return get_all(con, "providers")
        return Response(get_all(con, "providers"),content_type="application/json")
    
    if request.method == "POST":
        new_row = insert_new_row(con,request,"providers")
        if new_row:
            return {"success":True}

@app.route("/honey/api/purchases", methods=["GET","POST"])
def pruchases():
    if request.method == "GET":
        # return get_all(con, "purchases")
        return Response(get_all(con, "purchases"),content_type="application/json")

    if request.method == "POST":
        print(request.form)
        # print(create_id(con,"purchases"))
        if purchase(con,request,"purchases"):
            return {"success":True}





if __name__ == "__main__":
    app.run(debug=True,port=3000)