from flask import Flask, g, Response
import sqlite3
from funcs import *

app = Flask(__name__)

DB = "./vocab.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

@app.route("/api/<table>")
def api(table):
    # return "Working on it"
    return Response(get_all(con,table), content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True, port=3000)

