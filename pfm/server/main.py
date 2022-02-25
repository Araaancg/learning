from flask import Flask,request,session,render_template,make_response,redirect, url_for
from uuid import uuid4
from hashlib import sha256
from models import db, User, Category, Pack, Card
import secrets
from functools import wraps
import requests as req


app = Flask(__name__)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
app.secret_key = secrets.token_hex()
db.init_app(app)

# 012cf1b5-629c-4fcc-80ce-5d7be629a772|test1|test1@email.com
# 600da809-44fa-4cb3-979b-4bfdaaaa7b3e|test2|test2@email.com


@app.route("/signup", methods=["GET","POST"])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pwd = sha256(request.form.get("pwd").encode()).hexdigest()

        if email and pwd:
            id_u = str(uuid4())
            print(id_u)
            token = secrets.token_hex(16)
            new_user = User(id=id_u,name=name, email=email, pwd=pwd, token=token)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"), code=307)
        else:
            return {"success":False}
    return render_template("signup.html")


@app.route("/api/token", methods=["PUT", "GET"])
def token():
    if request.method == "PUT":
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        token = request.form.get("token")
        user = User.query.filter_by(email=email).first()
        user.token = token
        db.session.commit()
        if user.pwd == pwd:
            return {"success": True, "id": user.id, "token": user.token}
        return {"success": False, "msg": "User not found!"}

    elif request.method == "GET":
        cookie_id = request.args.get("id")
        cookie_token = request.args.get("token")
        user = User.query.filter_by(id=cookie_id).first()    
        if user.token == cookie_token:
            return {"success": True}
    return {"success": False}

@app.route("/api/get_packs/<id_user>", methods=["GET"])
def api_packs(id_user):
    user_packs = User.query.filter_by(id=id_user)
    print(user_packs)
    if user_packs:
        return {"success":True}
    return {"success":False}
    return "working"

def authenticate(f):
        @wraps(f)
        def i():
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            
            if email and pwd:
                api_res = req.put("http://localhost:5000/api/token", data={"email":email,"pwd":sha256(pwd.encode()).hexdigest(),"token":secrets.token_hex(16)}).json()
                if api_res["success"]:
                    session["token"] = api_res["token"]
                    session["id"] = api_res["id"]
                    return redirect(url_for("home"))
            return f()
        return i

@app.route("/login", methods=["GET","POST"])
@authenticate
def login():
    return render_template("login.html")

def authorize(f):
    @wraps(f)
    def i():
        cookie_id = session.get("id")
        cookie_token = session.get("token")
        if cookie_id and cookie_token:
            api_res = req.get(f"http://localhost:5000/api/token?token={cookie_token}&id={cookie_id}").json()
            if api_res["success"]:
                return f()
        return redirect(url_for("login"))
    return i

@app.route("/home")
@authorize
def home():
    return render_template("home.html")

@app.route("/my_packages")
@authorize
def my_packages():
    return render_template("my_packs.html")

@app.route("/my_packages/create_new")
@authorize
def new_pack():
    return render_template("new_pack.html")

@app.route("/games")
@authorize
def games():
    return render_template("games.html")


if __name__ == "__main__":
    app.run(debug=True)
