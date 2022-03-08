from mimetypes import init
from xxlimited import new
from flask import Flask,request,session,render_template,redirect,url_for
from models import db, User, Question, Option, Test, Test_question
from uuid import uuid4
from hashlib import sha256
import secrets
import requests as req
import auth
import json
from random import shuffle
import datetime as dt

app = Flask(__name__)

DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
app.secret_key = secrets.token_hex()
db.init_app(app)

@app.route("/create")
def create_qs():
    def get_data():
        with open("pcep.json") as file:
            return json.load(file)
    qs = get_data()
    for block in list(qs.values())[1:]:
        for question in block:
            q_id = uuid4().hex
            for i, option in enumerate(question["options"]):
                o_id = uuid4().hex
                if i == question["answer"]:
                    a = o_id
                option = Option(id=o_id, o=option, question_id=q_id)
                db.session.add(option)
                
            question = Question(id=q_id, q=question["question"], a=a)
            db.session.add(question)
            # db.session.commit()
    return "create"

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

@app.route("/api/questions", methods=["GET","POST"])
def api_questions():
    result = {"data":[]}
    for question in Question.query.all():
        elem = {}
        elem["id"], elem["question"], elem["answer"] = question.id, question.q, question.a
        elem["options"] = []
        for option in question.options:
            op = {"id":option.id,"option":option.o}
            elem["options"].append(op)
        result["data"].append(elem)
    shuffle(result["data"])
    for o in result["data"]:
        shuffle(o["options"])
    
    # SAVING TEST
    id_new_test = uuid4().hex
    date_new_test = dt.datetime.isoformat(dt.datetime.today())
    new_test = Test(id=id_new_test,user_id=request.args.get("user"),date=date_new_test)
    print(new_test.date)
    db.session.add(new_test)
    for item in result["data"][:5]:
        new_test_question = Test_question(id=uuid4().hex,test_id=id_new_test,question_id=item['id'])
        db.session.add(new_test_question)
    db.session.commit()

    return {"data":result["data"][:5],"date":new_test.date}

@app.route("/api/grades",methods=["GET","POST"])
def api_grades():
    if request.method == "POST":
        user = User.query.filter_by(id=request.form['id_user']).first()
        if user.grades:
            existing_grades = user.grades
            user.grades = f"{existing_grades},{request.form['grade']}"
        else:
            user.grades= request.form['grade']
        db.session.commit()
    
    if request.args.get('user'):
        user = User.query.filter_by(id=request.args.get('user')).first()
        if user.grades:
            grades = [grade for grade in user.grades.split(",")]
            return {"grades":grades}
        return {"grades":None}
    return "working"

@app.route("/api/tests")
def api_tests():
    if request.args.get("user"):
        result = {"tests":[]}
        for test in Test.query.filter_by(user_id=request.args.get("user")):
            t = {"date":test.date,"grade":test.grade}
            result["tests"].append(t)
        return result
    
    if request.args.get("date"):
        test =  Test.query.filter_by(date=request.args.get("date")).first()
        t = {"date":test.date,"grade":test.grade,"test":[]}
        for question in Test_question.query.filter_by(test_id=test.id):
            quest = Question.query.filter_by(id=question.question_id).first()
            little = {
                "question_id":question.question_id,
                "question":quest.q,
                "options":[{"id":option.id,"option":option.o} for option in quest.options],
                "veredict":"incorrect",
                "user_choice":question.user_choice,
                "a":quest.a
            }
            if question.user_choice == quest.a:
                little["veredict"] = "correct"
            t["test"].append(little)
    


        return {"test":t}
        return {"success":True}



################# MAIN #################

@app.route("/signup", methods=["GET","POST"])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pwd = sha256(request.form.get("pwd").encode()).hexdigest()

        if email and pwd:
            id_u = str(uuid4())
            token = secrets.token_hex(16)
            new_user = User(id=id_u, email=email, pwd=pwd, token=token)
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

@app.route("/home", methods=["GET","POST"])
@auth.authorize
def home():
    if request.method == "POST":
        return req.get(f"http://localhost:5000/api/grades?user={session['id']}").json()
    return render_template("home.html")

@app.route("/test", methods=["GET", "POST"])
@auth.authorize
def test():
    if request.method == "POST":
        return req.get(f"http://localhost:5000/api/questions?user={session['id']}").json()
    
    if request.args.get("get_all"):
        return req.get(f"http://localhost:5000/api/tests?user={session['id']}").json()

    return render_template("index.html")

@app.route("/test/<date>")
def get_by_date(date):
    if request.args.get("get_test"):
        return req.get(f"http://localhost:5000/api/tests?date={date}").json()
    return render_template("one_test.html")

@app.route("/score", methods=["GET","POST"])
def score():
    score = 0
    n_questions = 0
    result = {"data":[]}
    if request.method == "POST":
        form = request.form
        for k,v in dict(form).items():
            score_result = {}
            if k != "date":
                id_q = v.split(",")[0]
                id_a = v.split(",")[1]

                score_result["question"] = id_q
                score_result["grade"] = "incorrect"

                question = Question.query.filter_by(id=id_q).first()

                if question.a == id_a:
                    score_result["grade"] = "correct"
                    score += 1
                n_questions += 1

                score_result["a"] = question.a
                result["data"].append(score_result)

            final_score = f"{score}/{n_questions}"
            result["final_score"] = final_score
            result["user_id"] = session['id']
            req.post("http://localhost:5000/api/grades", data={"id_user":session['id'],"grade":score})
        
        # UPDATE TEST WITH GRADE ADN USER_CHOICE
        print(result)
        print(request.form)
        print(request.form['date'])
        update_test = Test.query.filter_by(date=request.form['date']).first()
        update_test.grade = score

        for question in Test_question.query.filter_by(test_id=update_test.id):
            print(question.question_id)
            for k,v in dict(form).items():
                if k != "date":
                    if v.split(',')[0] == question.question_id:
                        question.user_choice = v.split(',')[1]
        db.session.commit()
    return result

if __name__ == "__main__":
    app.run(debug=True)
