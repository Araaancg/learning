from flask import Flask,request,g,Response
from flask_cors import CORS
import sqlite3
from funcs import *
import sys
sys.path.append("/home/arancha/progr_master/dea")
from auth import Auth

SECRET = "4cfa98d37472801305b5d4a85bc98e6a9b4b0213de8762c35336a2b1a586c055"

app = Flask(__name__)
auth = Auth(SECRET,request)

DB = "./deas.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

@app.route("/dea/api", methods=["GET","POST"])
def api():
    if request.method == "GET":
        return Response(get_all(con,"users"), content_type="application/json")
    
    elif request.method == "POST":
        if auth.update_token(con):
            return {"success":True}
        return {"success":True}

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database',None)
    if db is not None:
        db.close()



if __name__ == "__main__":
    app.run(debug=True,port=3000)