from flask import Flask,request,session,render_template,make_response,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from hashlib import sha256
# from auth import Auth
import secrets

app = Flask(__name__)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
db = SQLAlchemy(app)
app.secret_key = secrets.token_hex()

# SECRET = "4cfa98d37472801305b5d4a85bc98e6a9b4b0213de8762c35336a2b1a586c055"
# api_uri = "http://localhost:5000/api/users"
# auth = Auth(SECRET,request,api_uri,"http://localhost:5000/login", redirect_uri="http://localhost:5000/secret")

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    pwd = db.Column(db.String(20), nullable=False, unique=True)
    token = db.Column(db.String(50), nullable=True)
    grades = db.Column(db.String(200), nullable=True)

    def __rpr__(self):
        return f"ID: {self.id} NAME: {self.email}"


@app.route("/signup", methods=["GET","POST"])
def registration():
    if request.method == "GET":
        email = request.args.get("email")
        pwd = sha256(request.args.get("pwd").encode()).hexdigest()

        if email and pwd:
            id_u = str(uuid4())
            # id_u = "bfa0bcd5-cf6a-4ab3-9706-4f6629f2760e"
            print(id_u)
            token = secrets.token_hex(16)
            new_user = User(id=id_u, email=email, pwd=pwd, token=token)
            db.session.add(new_user)
            db.session.commit()
            # return {"success":True}
            return redirect(url_for("login"), code=307)
        else:
            return {"success":False}
    return "Sign up"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        email = request.args.get("email")
        pwd = request.args.get("pwd")
        print(pwd)
        user = User.query.filter_by(email=email).first()
        # print(user.pwd)
        print(sha256(pwd.encode()).hexdigest())
        if user.pwd == sha256(pwd.encode()).hexdigest():
            print(user.pwd)
            session["token"] = user.token
            session["id"] = user.id
            # return {"success":True}
            return redirect("http://localhost:5000/secret")
        return {"success":False,"msg":"Incorrect pwd"}
    return "login"

@app.route("/secret", methods=["GET"])
def secret_url():
    return "Secret"



# @app.route("/dea/api/token", methods=["PUT", "GET"])
# def token():
#     cur = con().cursor()
#     verb = request.method 
#     if verb == "PUT":
#         email = request.form.get("email")
#         pwd = request.form.get("pwd")
#         token = request.form.get("token")

#         user = next(cur.execute(f'''SELECT * FROM users WHERE email='{email}';'''), {})
#         if dict(user).get("pwd") == pwd:
#             cur.execute(f'''UPDATE users SET token='{token}' WHERE email='{email}';''')
#             con().commit()
#             return {"success": True, "id": user["id"], "token": token}
#         return {"success": False, "msg": "User not found!"}

#     elif verb == "GET":
#         cookie_id = request.args.get("id")
#         cookie_token = request.args.get("token")

#         # print(f"COOKIE_ID: {cookie_id}")
#         user = next(cur.execute(f'''SELECT * FROM users WHERE id='{cookie_id}';'''), {})
#         if dict(user).get("token") == cookie_token:
#             return {"success": True}

#     return {"success": False}
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


if __name__ == "__main__":
    app.run(debug=True)