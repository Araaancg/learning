from flask import Flask,request,g
from flask_cors import CORS
import sqlite3
app = Flask(__name__)

DB = "./deas.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

@app.route("/dea/api")
def api():
    cur = con().cursor()
    for field in cur.execute("PRAGMA table_info(users);"):
        print(field)
    return "api"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database',None)
    if db is not None:
        db.close()



if __name__ == "__main__":
    app.run(debug=True,port=3000)