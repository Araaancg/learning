from flask import Flask,g,request,Response,redirect
import sqlite3
from funcs import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


DB = "./honey.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

@app.route("/honey/api")
def home():
    return "Working on it, be patient :)"

@app.route("/honey/api/<table_name>", methods=["GET","POST"])
def get_tn(table_name):
    if request.method == "GET":
        return Response(get_all(con, table_name),content_type="application/json")

    if request.method == "POST":
        new_row = insert_new_row(con,request,table_name)
        if new_row:
            return redirect(f"http://localhost:5000/honey/{table_name}")
            return Response(get_all(con, table_name),content_type="application/json")

@app.route("/honey/api/<table_name>/<id>")
def get_id(table_name,id):
    requested_id = get_by_id(con,table_name,id)
    if requested_id:
        return Response(requested_id, content_type="application/json")
    return {"success":False}

@app.route("/honey/api/<table_name>/<id>/delete")
def delete_person(table_name,id):
    is_deleted = delete_id(con,table_name,id)
    if is_deleted:
        return redirect(f"http://localhost:5000/honey/{table_name}")
        return {"success":True}
    return {"success":False}

if __name__ == "__main__":
    app.run(debug=True,port=3000)