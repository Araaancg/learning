from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    name = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    pwd = db.Column(db.String(20), nullable=False)
    token = db.Column(db.String(50), nullable=True)

    packs = db.relationship("Pack", backref=db.backref("users", lazy=True))
    categories = db.relationship("Category", backref=db.backref("categories", lazy=True))


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    id_user = db.Column(db.String(32), ForeignKey("users.id"))

    packs = db.relationship("Pack", backref=db.backref("categories", lazy=True))


class Pack(db.Model):
    __tablename__ = "packs"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    id_category = db.Column(db.String(12), ForeignKey("categories.id"))
    id_user = db.Column(db.String(32), ForeignKey("users.id"))
    status = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=True)

    cards = db.relationship("Card", backref=db.backref("packs", lazy=True))


class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    side_a = db.Column(db.Text, nullable=False)
    side_b = db.Column(db.Text, nullable=False)
    id_pack = db.Column(db.String(32), ForeignKey("packs.id"))

