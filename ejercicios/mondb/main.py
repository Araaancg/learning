from flask import Flask
from views.users.routes import users
# from db import db
from db import mongo
import os

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Some secret key"
    app.config["DEBUG"] = True
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    mongo.init_app(app)
    app.register_blueprint(users)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()