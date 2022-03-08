from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    pwd = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(64), nullable=True)
    grades = db.Column(db.String(100), nullable=True)

class Test(db.Model):
    __tablename__ = "tests"
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), ForeignKey("users.id"))
    date = db.Column(db.String(32), nullable=False)
    grade = db.Column(db.Float, nullable=True)

    questions = db.relationship("Question", secondary='test_questions', backref=db.backref("test_questions", lazy=True))
    answers = db.relationship("Test_question", backref=db.backref("tests", lazy=True))

class Test_question(db.Model):
    __tablename__ = "test_questions"
    id = db.Column(db.String(32), primary_key=True)
    test_id = db.Column(db.String(32), ForeignKey("tests.id"))
    question_id = db.Column(db.String(32), ForeignKey("questions.id"))
    user_choice = db.Column(db.String(32), nullable=True)

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.String(32), primary_key=True)
    q = db.Column(db.Text, nullable=False, unique=True)
    a = db.Column(db.String(32), nullable=True)

    options = db.relationship("Option", backref=db.backref("questions", lazy=True))

class Option(db.Model):
    __tablename__ = "options"
    id = db.Column(db.String(32), primary_key=True)
    o = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.String(32), ForeignKey("questions.id"))