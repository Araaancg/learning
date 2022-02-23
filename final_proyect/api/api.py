from flask import Flask, g, Response
from flask_sqlalchemy import SQLAlchemy
# from funcs import *

app = Flask(__name__)

DB = "./vocab.db"

app = Flask(__name__)
DB_URI = "vocab.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
db = SQLAlchemy(app)

class Owner(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(60), nullable=False)


@app.route("/api/get_packs", methods=["GET"])
def get_packs():
    return "Working"




# return "Working on it"
# return Response(get_all(con,table), content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True, port=3000)

