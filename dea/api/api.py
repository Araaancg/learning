from flask import Flask, request, g, make_response,Response
from flask_cors import CORS
import sqlite3
from funcs import get_all

app = Flask(__name__)
CORS(app)

DB = "./deas.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db


@app.route("/dea/api")
def api():
    # cur = con().cursor()
    # for field in cur.execute("SELECT * FROM users;"):
    #     print(field)
    # return "api"
    return Response(get_all(con,"users"), content_type="application/json")

@app.route("/dea/api/token", methods=["PUT", "GET"])
def token():
    cur = con().cursor()
    verb = request.method 
    if verb == "PUT":
        email= request.form.get("email")
        pwd= request.form.get("pwd")
        email = "a@test.com"
        pwd = "1234"
        token= request.args.get("token")

        user = next(cur.execute(f'''SELECT * FROM users WHERE email='{email}';'''), {})
        print(user)
        if dict(user).get("pwd") == pwd:
            cur.execute(f'''UPDATE users SET token='{token}' WHERE email='{email}';''')
            con().commit()
            return {"success": True, "id": user["id"], "token": token}
        return {"success": False, "msg": "User not found!"}

    elif verb == "GET":
        cookie_id = request.args.get("id")
        cookie_token = request.args.get("token")

        print(f"COOKIE_ID: {cookie_id}")
        user = next(cur.execute(f'''SELECT * FROM users WHERE id='{cookie_id}';'''), {})
        print(user)
        print(dict(user).get("token"))
        if dict(user).get("token") == cookie_token:
            print("TOKEN COORERECTORS")
            return {"success": True}

    return {"success": False}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=3000)




'''from flask import Flask,request,g,Response
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
    app.run(debug=True,port=3000)'''