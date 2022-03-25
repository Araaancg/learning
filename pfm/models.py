from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id =  db.Column(db.String(32), primary_key=True, unique=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    pwd = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=True)

    categories = db.relationship("Category", backref="user", lazy=True)
    packs = db.relationship("Pack", backref="user", lazy=True)
    cards = db.relationship("Card", backref="user", lazy=True)

class Category(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=False)
    id_user = db.Column(db.String(32), db.ForeignKey("user.id"))

    packs = db.relationship("Pack", backref="category", lazy=True)

mailbox = db.Table('mailbox',
        db.Column('pack_id', db.String(32), db.ForeignKey('pack.id')),
        db.Column('card_id', db.String(32), db.ForeignKey('card.id'))
    )

class Pack(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=False)
    status = db.Column(db.String(255), nullable=False, unique=False)
    id_user = db.Column(db.String(32), db.ForeignKey("user.id"))
    id_cat = db.Column(db.String(32), db.ForeignKey("category.id"))

    cards = db.relationship("Card", secondary=mailbox, back_populates="packs")

class Card(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    date = db.Column(db.Date, nullable=False)
    side_a = db.Column(db.String(32), nullable=False, unique=False)
    side_b = db.Column(db.String(32), nullable=False, unique=False)
    id_user = db.Column(db.String(32), db.ForeignKey("user.id"))

    packs = db.relationship("Pack", secondary=mailbox, back_populates="cards")

    
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.String(32), primary_key=True, unique=True)
#     name = db.Column(db.String(12), unique=True, nullable=False)
#     email = db.Column(db.String(30), nullable=False, unique=True)
#     pwd = db.Column(db.String(20), nullable=False)
#     token = db.Column(db.String(50), nullable=True)

#     packs = db.relationship("Pack", backref=db.backref("users", lazy=True))
#     categories = db.relationship("Category", backref=db.backref("categories", lazy=True))


# class Category(db.Model):
#     __tablename__ = "categories"
#     id = db.Column(db.String(32), primary_key=True, unique=True)
#     name = db.Column(db.String(20), unique=True, nullable=False)
#     id_user = db.Column(db.String(32), ForeignKey("users.id"))

#     packs = db.relationship("Pack", backref=db.backref("categories", lazy=True))


# class Pack(db.Model):
#     __tablename__ = "packs"
#     id = db.Column(db.String(32), primary_key=True, unique=True)
#     name = db.Column(db.String(20), unique=True, nullable=False)
#     id_category = db.Column(db.String(12), ForeignKey("categories.id"))
#     id_user = db.Column(db.String(32), ForeignKey("users.id"))
#     status = db.Column(db.String(100), nullable=False)
#     color = db.Column(db.String(100), nullable=True)

#     cards = db.relationship("Card", backref=db.backref("packs", lazy=True))


# class Card(db.Model):
#     __tablename__ = "cards"
#     id = db.Column(db.String(32), primary_key=True, unique=True)
#     side_a = db.Column(db.Text, nullable=False)
#     side_b = db.Column(db.Text, nullable=False)
#     id_pack = db.Column(db.String(32), ForeignKey("packs.id"))







