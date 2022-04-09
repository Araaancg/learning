from flask import Flask,request,session,render_template,redirect, url_for
from uuid import uuid4
from hashlib import sha256
from models import db, User, Category, Pack, Card, mailbox
import secrets
import requests as req
import auth
import datetime as dt


app = Flask(__name__)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
app.secret_key = secrets.token_hex()
db.init_app(app)

@app.route("/test")
def test():
    return render_template("test.html", user_name=User.query.filter_by(id=session['id']).first().name)

################################### API #########################################

@app.route("/api/token", methods=["PUT", "GET"])
def token():
    if request.method == "PUT":
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        token = request.form.get("token")
        user = User.query.filter_by(email=email).first()
        if user:
            user.token = token
            db.session.commit()
            if user.pwd == pwd:
                return {"success": True, "id": user.id, "token": user.token}
            return {"success":False, "msg": "Incorrect password"}
        return {"success": False, "msg": "User not found"}

    elif request.method == "GET":
        cookie_id = request.args.get("id")
        cookie_token = request.args.get("token")
        user = User.query.filter_by(id=cookie_id).first()    

        if request.args.get("logout"):
            user.token = None
            db.session.commit()
            return {"success":True}

        if user.token == cookie_token:
            return {"success": True}
    return {"success": False}

@app.route("/api/categories", methods=["GET","POST"])
def category():
    if request.method == "POST":
        cat_id = uuid4().hex
        category = Category(id=cat_id,name=request.args.get("post"),id_user=request.args.get("id_user"),date=dt.date.today())
        db.session.add(category)
        db.session.commit()
        return {"id":cat_id,"name":request.args.get("post"),"id_user":category.id_user,"date":dt.date.isoformat(category.date)}

    if request.method == "GET":
        if request.args.get("get"):
            category = Category.query.filter_by(name=request.args.get("get")).first()
            if category:
                return {"id":category.id,"name":category.name,"id_user":category.id_user,"date":dt.date.isoformat(category.date)} 
            return None
        
        result = {"categories":[]}
        
        if request.args.get("id_user"):
            for cat in Category.query.filter_by(id_user=request.args.get("id_user")):
                category = {"id":cat.id,"name":cat.name,"id_user":cat.id_user,"date":dt.date.isoformat(cat.date)}
                result["categories"].append(category)
            return result

        for cat in Category.query.filter_by():
            category = {"id":cat.id,"name":cat.name,"date":dt.date.isoformat(cat.date)}
            result["categories"].append(category)
        return result

@app.route("/api/packages", methods=["GET","POST","DELETE","PUT"])
def package():
    result = {"packages":[]}
    form = dict(request.form)
    if request.method == "POST":
        # COMPROBAMOS QUE EL FORMULARIO ESTÁ COMPLETO
        print(form)
        if not form.get('pack_name'):
            return {"success":False,"msg":"¡ponle un nombre al paquete!","lasting_input":"name"}
        if not form.get('category'):
            return {"success":False,"msg":"¡Añade una categoría al paquete!","lasting_input":"category"}
        #CATEGORIA
        category = req.get(f"http://localhost:5000/api/categories?get={form['category']}") #comprobamos si existe la categoria
        if not category:
            category = req.post(f"http://localhost:5000/api/categories?post={form['category']}&id_user={form['id_user']}")
        category = category.json()
        #PAQUETE
        pack_id = uuid4().hex
        status = form["status"] if form.get('status') != "null" else "private"
        print(status)
        new_pack = Pack(id=pack_id,name=form["pack_name"],id_cat=category["id"],id_user=form["id_user"],status=status,date=dt.date.today())

        #TARJETAS
        side_a = [v for k,v in form.items() if k.find("side") >= 0 and k.find("a") >= 0]
        side_b = [v for k,v in form.items() if k.find("side") >= 0 and k.find("b") >= 0]
        if len(side_a) != len(side_b):
            return {"success":False,"msg":"completa ambas caras de cada tarjeta","lasting_input":"card"}  # comprobamos que las tarjetas están completas
        

        for element in zip(side_a,side_b):
            car_id = uuid4().hex
            new_card = Card(id=car_id,side_a=element[0],side_b=element[1],date=dt.date.today(),id_user=form["id_user"])
            db.session.add(new_card)
            new_pack.cards.append(new_card)
            db.session.add(new_pack)
            db.session.commit()

        existing_cards = [v for k,v in form.items() if k.find("exist") >= 0]
        for item in existing_cards:
            existing_card = Card.query.filter_by(id=item).first()
            new_pack.cards.append(existing_card)
            db.session.add(new_pack)
            db.session.commit()

        db.session.commit()
        return {"success":True}
    
    if request.method == "GET":
        #All the packages
        obj = Pack.query.all()
        
        if request.args.get("get"): #Just one
            obj = Pack.query.filter_by(id=request.args.get("get")).first()
            result["packages"] = {"id":obj.id,"name":obj.name,"category":{"id":obj.id_cat,"name":obj.category.name},"id_user":obj.id_user}
            result["packages"]["cards"] = [{"id":card.id,"side_a":card.side_a,"side_b":card.side_b} for card in obj.cards]
            return result

        elif request.args.get("filter_by"): # filtered by category and/or user, asign a new obj
            if request.args.get("filter_by") == "user":
                obj = Pack.query.filter_by(id_user=request.args.get('id'))
            if request.args.get("filter_by") == "category":
                obj = Pack.query.filter_by(id_cat=request.args.get('id'))
            if request.args.get('filter_by') == 'cat_and_user':
                obj = Pack.query.filter_by(id_cat=request.args.get('cat')).filter_by(id_user=request.args.get('user'))
        
        for pack in obj:
            package = {"id":pack.id,"name":pack.name,"category":{"id":pack.id_cat},"id_user":pack.id_user}
            package["category"]["name"] = Category.query.filter_by(id=pack.id_cat).first().name ##!!
            package["cards"] = [{"id":card.id,"side_a":card.side_a,"side_b":card.side_b} for card in pack.cards]
            result["packages"].append(package)
        return result
    
    if request.method == "DELETE":
        pack_to_delete = Pack.query.filter_by(id=request.form['id']).first()
        db.session.delete(pack_to_delete)
        db.session.commit()
        return {"success":True}
    
    if request.method == "PUT":
        if request.args.get("new_card"):
            pack_to_edit = Pack.query.filter_by(id=request.args.get("new_card")).first()
            side_a = [v for k,v in form.items() if k.find("side") >= 0 and k.find("a") >= 0]
            side_b = [v for k,v in form.items() if k.find("side") >= 0 and k.find("b") >= 0]
            for element in zip(side_a,side_b):
                card_id = uuid4().hex
                new_card = Card(id=card_id,side_a=element[0],side_b=element[1],date=dt.date.today())
                db.session.add(new_card)
                pack_to_edit.cards.append(new_card)
            db.session.commit()
        
        if request.args.get('existing_cards'):
            pack_to_edit = Pack.query.filter_by(id=request.args.get('existing_cards')).first()
            existing_cards = [v for k,v in form.items() if k.find("exist") >= 0]
            for item in existing_cards:
                existing_card = Card.query.filter_by(id=item).first()
                pack_to_edit.cards.append(existing_card)
                db.session.add(pack_to_edit)
                db.session.commit()
        
        if request.args.get("delete_card"):
            pack = Pack.query.filter_by(id=request.args.get('id_pack')).first()
            card = Card.query.filter_by(id=form['id']).first()
            pack.cards.remove(card)
            db.session.commit()

        return {"success":True}

@app.route("/api/cards", methods=["GET","PUT","DELETE"])
def cards():
    form = dict(request.form)
    if request.method == "DELETE":
        card_to_delete = Card.query.filter_by(id=request.args.get('id')).first()
        db.session.delete(card_to_delete)
        db.session.commit()
        return {"success":True}

    if request.method == "PUT":
        if request.args.get("add_packs"):
            try:
                icard = Card.query.filter_by(id=request.args.get('edit_card')).first()
                for v in form.values():
                    ipack = Pack.query.filter_by(id=v).first()
                    ipack.cards.append(icard)
                    db.session.add(ipack)
                    db.session.commit()
                return {"success":True}
            except:
                return {"success":False}
        
        if request.args.get("delete_packs"):
            try:
                icard = Card.query.filter_by(id=request.args.get('edit_card')).first()
                for v in form.values():
                    ipack = Pack.query.filter_by(id=v).first()
                    ipack.cards.remove(icard)
                    db.session.add(ipack)
                    db.session.commit()
                return {"success":True}
            except:
                return {"success":False}

        card_to_edit = Card.query.filter_by(id=form['id']).first()
        card_to_edit.side_a = form['side_a'] if form['side_a'] else card_to_edit.side_a
        card_to_edit.side_b = form['side_b'] if form['side_b'] else card_to_edit.side_b
        db.session.commit()
        return {"success":True}

    result = {"cards":[]}
    # obj = Card.query.filter_by(id_user=request.args.get('id_user')) if request.args.get('id_user') else Card.query.all()

    obj = Card.query.all()
    if request.args.get('id_user'):
        obj = Card.query.filter_by(id_user=request.args.get('id_user'))
    if request.args.get('filter_by_pack'):
        obj = Pack.query.filter_by(id=request.args.get('filter_by_pack')).first().cards


    for card in obj:
        card_dic = {"id":card.id,"side_a":card.side_a,"side_b":card.side_b,"packages":[{
                "id":pack.id,
                "name":pack.name,
                "category":{"id":pack.category.id,"name":pack.category.name},
                "status":pack.status
            } for pack in card.packs]}
        result["cards"].append(card_dic)
    return result

@app.route("/api/user", methods=["GET", "PUT", "DELETE"])
def api_user():
    if request.method == "PUT":
        form = dict(request.form)
        change_email = True if form.get("email") else False
        print(change_email)
        user = User.query.filter_by(id=request.args.get("id_user")).first()
        if change_email: #se cambia el email
            if not User.query.filter_by(email=form.get('email')).first():
                user.email = form.get("email")
                db.session.add(user)
                db.session.commit()
                return {"success":True,"msg":"email cambiado"}
            return {"success":False,"msg":"este email ya está en uso"}
        
        #se cambia la contraseña
        if  sha256(form.get("current-pw").encode()).hexdigest() == user.pwd: #se comprueba que la currentpw es la misma
            if sha256(form.get("new-pw").encode()).hexdigest() == sha256(form.get("repeat-pw").encode()).hexdigest():
                user.pwd = sha256(form.get("new-pw").encode()).hexdigest()
                db.session.add(user)
                db.session.commit()
                return {"success":True, "msg":"contrseña cambiada"}
        return {"success":False,"msg":"vuelve a intentarlo"}
    
    if request.method == "DELETE":
        user = User.query.filter_by(id=request.args.get("id_user")).first()
        db.session.delete(user) # con el keyword cascade en las relationships se eliminará cualquier dato asociado (card,pack,category y registros de mailbox)
        db.session.commit()
        return {"success":True}

    if request.args.get("id_user"):
        user = User.query.filter_by(id=request.args.get("id_user")).first()
        return {"success":True,"id":user.id,"email":user.email,"name":user.name}

    return {"success":False}

##################################### MAIN #####################################

@app.route("/signup", methods=["GET","POST"])
def registration():
    msg = {"msg": None, "error": None}
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pwd = sha256(request.form.get("pwd").encode()).hexdigest()
        pwd2 = sha256(request.form.get("pwd2").encode()).hexdigest()

        print(dict(request.form))

        name_not_exist = False if User.query.filter_by(name=name).first() else True
        email_not_exist = False if User.query.filter_by(email=email).first() else True
        same_pwd = True if pwd == pwd2 else False

        print(name_not_exist,email_not_exist,same_pwd)

        if name_not_exist and email_not_exist and same_pwd:
            id_u = str(uuid4())
            token = secrets.token_hex(16)
            new_user = User(id=id_u,name=name, email=email, pwd=pwd, token=token, date=dt.datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"), code=307)
        else:
            msg = {"msg":f"el usuario '{name}' ya existe","error":1} if not name_not_exist else {"msg":f"el email '{email}' ya está en uso","error":2}
            if not same_pwd:
                msg = {"msg":"las contraseñas tienen que ser iguales","error":3}
            pass
    return render_template("signup.html", msg=msg)


@app.route("/login", methods=["GET","POST"])
@auth.authenticate
def login(msg):
    return render_template("login.html", msg=msg)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/home")
@auth.authorize
def home():
    if request.args.get("logout"):
        res = req.get(f"http://localhost:5000/api/token?logout=true&token={session.get('token')}&id={session.get('id')}").json()
        if res["success"]:
            return redirect(url_for("welcome"))
    return render_template("home.html", user_name=User.query.filter_by(id=session['id']).first().name)

@app.route("/my_packages", methods=["GET","POST"])
@auth.authorize
def my_packages():
    if request.method == "POST":
        return req.get(f"http://localhost:5000/api/packages?filter_by=user&id={session.get('id')}").json()

    if request.args.get('filter'):
        if request.args.get('filter') == "null":
            return req.get(f"http://localhost:5000/api/packages?filter_by=user&id={session.get('id')}").json()
        return req.get(f"http://localhost:5000/api/packages?filter_by=cat_and_user&user={session.get('id')}&cat={request.args.get('filter')}").json()


    return render_template("my_packs.html", user_name=User.query.filter_by(id=session['id']).first().name)

@app.route("/my_packages/<id>", methods=["GET","POST","PUT"])
@auth.authorize
def get_package(id):
    if request.method == "POST":
        print(id)
        id_pack = Pack.query.filter_by(id=id).first().id
        package = req.get(f"http://localhost:5000/api/packages?get={id_pack}").json()
        return {"data":package}

    if request.args.get("delete_card"):
        #solo se quita la relación entre le paquete y la tarjeta, la tarjeta en sí no se elimina
        req.put(f"http://localhost:5000/api/packages?delete_card=true&id_pack={id}", data={"id":request.args.get("delete_card")}) 
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

    if request.args.get("existing_cards"):
        print(request.form)
        return req.put(f"http://localhost:5000/api/packages?existing_cards={request.args.get('existing_cards')}", data=request.form).json()

    return render_template("one_pack.html", user_name=User.query.filter_by(id=session['id']).first().name)

@app.route("/my_packages/create_new", methods=["GET","POST"])
@auth.authorize
def new_pack():
    if request.method == "POST":
        new_form = {k:v for k,v in request.form.items()}
        new_form["id_user"] = session.get("id")
        print(new_form)
        return req.post("http://localhost:5000/api/packages", data=new_form).json()

    if request.args.get("get"):
        result = {"categories":[
            {"public":[]},
            {"private":[]}
        ]}
        public = req.get("http://localhost:5000/api/categories?id_user=public").json()
        private = req.get(f"http://localhost:5000/api/categories?id_user={session['id']}").json()
        result["categories"][0]["public"] = [{k:v for k,v in dicc.items()} for dicc in public["categories"]]
        result["categories"][1]["private"] = [{k:v for k,v in dicc.items()} for dicc in private["categories"]]
        return result
    return render_template("new_pack.html", user_name=User.query.filter_by(id=session['id']).first().name)

@app.route("/flash_cards", methods=["GET","POST"])
@auth.authorize
def choose_pack():
    if request.method == "POST":
        return req.get(f"http://localhost:5000/api/packages?filter_by=user&id={session.get('id')}").json()
    return render_template("fc_choose_pack.html", user_name=User.query.filter_by(id=session['id']).first().name)

@app.route("/flash_cards/<id>")
@auth.authorize
def flash_cards(id):
    return render_template("flash_cards.html", user_name=User.query.filter_by(id=session['id']).first().name)

@app.route("/profile", methods=["GET","POST","PUT"])
@auth.authorize
def profile():
    if request.method == "POST":
        print(request.form)
        return req.put(f"http://localhost:5000/api/user?id_user={session.get('id')}", data=request.form).json()

    if request.args.get("get") == "user":
        return req.get(f"http://localhost:5000/api/user?id_user={session.get('id')}").json()
    
    if request.args.get("get") == "mycards":
        return req.get(f"http://localhost:5000/api/cards?id_user={session.get('id')}").json()
    
    if request.args.get("delete_user"):
        return req.delete(f"http://localhost:5000/api/user?id_user={session.get('id')}").json()

    if request.args.get("delete_card"):
        return req.delete(f"http://localhost:5000/api/cards?id={request.args.get('delete_card')}").json()

    if request.args.get("get_pack_names"):
        return req.get(f"http://localhost:5000/api/packages?filter_by=user&id={session.get('id')}").json()
    
    if request.args.get("filter_by_pack"):
        return req.get(f"http://localhost:5000/api/cards?filter_by_pack={request.args.get('filter_by_pack')}").json()
    
    if request.method == "PUT":
        if request.args.get("edit_card"):
            form = dict(request.form)
            for k,v in form.items():
                if k.find("add") >= 0:
                    return req.put(f"http://localhost:5000/api/cards?edit_card={request.args.get('edit_card')}&add_packs=true", data={k:v for k,v in form.items() if k.find("add") >= 0}).json()
                if k.find("delete") >= 0:
                    return req.put(f"http://localhost:5000/api/cards?edit_card={request.args.get('edit_card')}&delete_packs=true", data={k:v for k,v in form.items() if k.find("delete") >= 0}).json()
            return req.put(f"http://localhost:5000/api/cards", data={"id":request.args.get("edit_card"),"side_a":request.form['side_a'],"side_b":request.form['side_b'],"new_pack":request.form['side_a']}).json()

    return render_template("profile.html", user_name=User.query.filter_by(id=session['id']).first().name)



if __name__ == "__main__":
    app.run(debug=True)
