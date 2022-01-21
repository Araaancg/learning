from flask import Flask,g
import sqlite3

app = Flask(__name__)

DB = "./honey.db"

def con():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db


# @app.route("/honey/")





if __name__ == "__main__":
    app.run(debug=True)