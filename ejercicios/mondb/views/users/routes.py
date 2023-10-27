from flask import Blueprint
from db import mongo

users = Blueprint("users", __name__)

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.String(32), primary_key=True)
#     email = db.Column(db.String(64), nullable=False)
#     pwd = db.Column(db.String(64), nullable=False)
#     token = db.Column(db.String(64), nullable=True)
#     grades = db.Column(db.String(100), nullable=True)

@users.route("/home")
def home():
    mongo.db.users.insert_one({
        "name":"Vito"
    })
    print(mongo.db.users.find())
    return "funciona"