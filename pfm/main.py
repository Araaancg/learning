from flask import Flask,request,session,render_template,make_response,redirect, url_for
from uuid import uuid4
from hashlib import sha256
from models import db, User, Category, Pack, Card
import secrets
import requests as req
import auth


app = Flask(__name__)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
app.secret_key = secrets.token_hex()
db.init_app(app)

# 012cf1b5-629c-4fcc-80ce-5d7be629a772|test1|test1@email.com
# 600da809-44fa-4cb3-979b-4bfdaaaa7b3e|test2|test2@email.com

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

@app.route("/api/categories", methods=["GET","POST"])
def category():
    if request.method == "POST":
        cat_id = str(uuid4())
        category = Category(id=cat_id,name=request.args.get("post"))
        db.session.add(category)
        db.session.commit()
        return {"id":cat_id,"name":request.args.get("name")}

    if request.method == "GET":
        if request.args.get("get"):
            category = Category.query.filter_by(name=request.args.get("get")).first()
            return {"id":category.id,"name":category.name} 

        result = {"categories":[]}

        for cat in Category.query.filter_by():
            category = {"id":cat.id,"name":cat.name}
            result["categories"].append(category)
        return result

@app.route("/api/packages", methods=["GET","POST","DELETE","PUT"])
def package():
    result = {"packages":[]}
    form = dict(request.form)
    if request.method == "POST":
        #CATEGORIA
        category = req.get(f"http://localhost:5000/api/categories?get={form['category']}").json() #comprobamos si existe la categoria
        if not category: #si no existe la creamos
            category = req.post(f"http://localhost:5000/api/categories?post={form['category']}").json()
        #PAQUETE
        pack_id = uuid4().hex
        new_pack = Pack(id=pack_id,name=form["pack_name"],id_category=category["id"],id_user=form["id_user"])
        db.session.add(new_pack)
        #TARJETAS
        side_a = [v for k,v in form.items() if k.find("side") >= 0 and k.find("a") >= 0]
        side_b = [v for k,v in form.items() if k.find("side") >= 0 and k.find("b") >= 0]

        for element in zip(side_a,side_b):
            car_id = uuid4().hex
            new_card = Card(id=car_id,side_a=element[0],side_b=element[1],id_pack=new_pack.id)
            db.session.add(new_card)
        
        db.session.commit()
        return {"success":True}
    
    if request.method == "GET":
        #All the packages
        obj = Pack.query.all()
        
        if request.args.get("get"): #Just one
            obj = Pack.query.filter_by(id=request.args.get("get")).first()
            result["packages"] = {"id":obj.id,"name":obj.name,"category":{"id":obj.id_category},"id_user":obj.id_user}
            result["packages"]["category"]["name"] = Category.query.filter_by(id=obj.id_category).first().name
            result["packages"]["cards"] = [{"id":card.id,"side_a":card.side_a,"side_b":card.side_b} for card in obj.cards]
            return result

        elif request.args.get("filter_by"): # filtered by category or user, asign a new obj
            obj = Pack.query.filter_by(id_category=request.args.get('id')) if request.args.get('filter_by') == "category" else Pack.query.filter_by(id_user=request.args.get('id'))

        for pack in obj:
            package = {"id":pack.id,"name":pack.name,"category":{"id":pack.id_category},"id_user":pack.id_user}
            package["category"]["name"] = Category.query.filter_by(id=pack.id_category).first().name ##!!
            package["cards"] = [{"id":card.id,"side_a":card.side_a,"side_b":card.side_b} for card in pack.cards]
            result["packages"].append(package)
        return result
    
    if request.method == "DELETE":
        print("using delete")
        pack_to_delete = Pack.query.filter_by(id=request.form['id']).first()
        db.session.delete(pack_to_delete)
        db.session.commit()
        return {"success":True}
    
    if request.method == "PUT":
        if request.args.get("new_card"):
            print(form)
            pack_to_edit = Pack.query.filter_by(id=request.args.get("new_card")).first()
            side_a = [v for k,v in form.items() if k.find("side") >= 0 and k.find("a") >= 0]
            side_b = [v for k,v in form.items() if k.find("side") >= 0 and k.find("b") >= 0]
            for element in zip(side_a,side_b):
                card_id = uuid4().hex
                new_card = Card(id=card_id,side_a=element[0],side_b=element[1],id_pack=pack_to_edit.id)
                db.session.add(new_card)
            db.session.commit()
        return {"success":True}

@app.route("/api/cards", methods=["GET","PUT","DELETE"])
def cards():
    form = request.form
    if request.method == "DELETE":
        card_to_delete = Card.query.filter_by(id=form['id']).first()
        db.session.delete(card_to_delete)
        db.session.commit()
        return {"success":True}

    if request.method == "PUT":
        card_to_edit = Card.query.filter_by(id=form['id']).first()
        card_to_edit.side_a = form['side_a'] if form['side_a'] else card_to_edit
        card_to_edit.side_b = form['side_b'] if form['side_b'] else card_to_edit
        db.session.commit()
        return {"success":True}

    result = {"cards":[]}
    obj = Card.query.all()
    for card in obj:
        card_dic = {"id":card.id,"side_a":card.side_a,"side_b":card.side_b,"id_pack":card.id_pack}
        result["cards"].append(card_dic)
    return result

##################################### MAIN #####################################

@app.route("/signup", methods=["GET","POST"])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pwd = sha256(request.form.get("pwd").encode()).hexdigest()

        if email and pwd:
            id_u = str(uuid4())
            # print(id_u)
            token = secrets.token_hex(16)
            new_user = User(id=id_u,name=name, email=email, pwd=pwd, token=token)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"), code=307)
        else:
            return {"success":False}
    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
@auth.authenticate
def login():
    return render_template("login.html")

@app.route("/home")
@auth.authorize
def home():
    return render_template("home.html")

@app.route("/my_packages", methods=["GET","POST"])
@auth.authorize
def my_packages():
    if request.method == "POST":
        return req.get(f"http://localhost:5000/api/packages?filter_by=user&id={session.get('id')}").json()
    return render_template("my_packs.html")

@app.route("/my_packages/<name>", methods=["GET","POST","PUT"])
@auth.authorize
def get_package(name):
    if request.method == "POST":
        id_pack = Pack.query.filter_by(name=name).first().id
        package = req.get(f"http://localhost:5000/api/packages?get={id_pack}").json()
        return {"data":package}

    if request.args.get("delete_card"):
        req.delete(f"http://localhost:5000/api/cards", data={"id":request.args.get("delete_card")})
        return {"succes":True}

    if request.args.get("edit_card"):
        print(request.form)
        req.put(f"http://localhost:5000/api/cards", data={"id":request.args.get("edit_card"),"side_a":request.form['side_a'],"side_b":request.form['side_b']})
        return {"succes":True}
    
    if request.args.get("delete_pack"):
        req.delete(f"http://localhost:5000/api/packages", data={"id":request.args.get("delete_pack")})
        return {"succes":True}  
    
    if request.args.get("new_card"):
        req.put(f"http://localhost:5000/api/packages?new_card={request.args.get('new_card')}", data=request.form)
        return {"success":True}

    return render_template("one_pack.html")

@app.route("/my_packages/create_new", methods=["GET","POST"])
@auth.authorize
def new_pack():
    if request.method == "POST":
        new_form = {k:v for k,v in request.form.items()}
        new_form["id_user"] = session.get("id")
        req.post("http://localhost:5000/api/packages", data=new_form)
    if request.args.get("get"):
        return req.get("http://localhost:5000/api/categories").json()
    return render_template("new_pack.html")

@app.route("/flash_cards")
@auth.authorize
def games():
    return render_template("flash_cards.html")

@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
