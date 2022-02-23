from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from hashlib import sha256
from auth import Auth

app = Flask(__name__)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
db = SQLAlchemy(app)

SECRET = "4cfa98d37472801305b5d4a85bc98e6a9b4b0213de8762c35336a2b1a586c055"
api_uri = "http://localhost:5000/api"
auth = Auth(SECRET,request,api_uri,"http://localhost:5000/login")

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    pwd = db.Column(db.String(20), nullable=False, unique=True)
    token = db.Column(db.String(50))
    grades = db.Column(db.String)

    def __rpr__(self):
        return f"ID: {self.id} NAME: {self.email}"


@app.route("/api/users", methods=["GET","PUT"])
def get_users():
    if request.method["PUT"]:
        email = request.args.get("email")
        pwd = request.args.get("pwd")
        token = request.args.get("token")
        user = User.query.filter_by(email=email)
        if user.pwd == pwd:
            user.token = token 
            session["token"] = token
    return "Working on it"

# @app.route("/create")
# def create():
#     id = uuid4().hex
#     email = "test1@email.com"
#     pwd = sha256(b"1234").hexdigest()
#     token = ""
#     grades = ""
#     to_add = User(id=id,email=email,pwd=pwd,token=token,grades=grades)
#     db.session.add(to_add)
#     db.session.commit()
#     return "Create"

@app.route("/login")
def login():
    return "Log in"

if __name__ == "__main__":
    app.run(debug=True)