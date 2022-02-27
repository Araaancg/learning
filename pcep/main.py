from mimetypes import init
from flask import Flask,request,session,render_template
from models import db, User, Question, Option
from uuid import uuid4
from hashlib import sha256
import secrets
import requests as req
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
app.secret_key = secrets.token_hex()
db.init_app(app)

@app.route("/api/questions", methods=["GET"])
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
    return result


################# MAIN #################

@app.route("/test", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return req.get("http://localhost:5000/api/questions").json()
    return render_template("index.html")

@app.route("/score", methods=["GET","POST"])
def score():
    score = 0
    n_questions = 0
    result = {"data":[]}
    if request.method == "POST":
        form = request.form
        # print(dict(form))
        for k,v in dict(form).items():
            score_result = {}

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
        
    print(result)
    return result

if __name__ == "__main__":
    app.run(debug=True)








'''
count_q = 1
    count_o = 1
    while count_q <= 5:
        id_q = uuid4().hex
        question = Question(id=id_q, q=f"question_{count_q}")
        option_1 = Option(id=uuid4().hex, o=f"option_{count_o}", question_id=id_q)
        count_o += 1
        option_2 = Option(id=uuid4().hex, o=f"option_{count_o}", question_id=id_q)
        count_o += 1
        option_3 = Option(id=uuid4().hex, o=f"option_{count_o}", question_id=id_q)
        count_o += 1
        option_4 = Option(id=uuid4().hex, o=f"option_{count_o}", question_id=id_q)
        count_o += 1
        question.a = option_1.id
        db.session.add(question)
        db.session.add(option_1)
        db.session.add(option_2)
        db.session.add(option_3)
        db.session.add(option_4)
        count_q += 1
    db.session.commit()
'''