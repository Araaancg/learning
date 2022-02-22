from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_URI = "test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_URI}"
db = SQLAlchemy(app)

class Owner(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"ID: {self.id} NAME: {self.name}"
    
@app.route("/create")
def create():
    id = request.args.get("id")
    name = request.args.get("name")
    if id and name:
        to_add = Owner(id=id,name=name)
        db.session.add(to_add)
        db.session.commit()
    return "Create"


if __name__ == "__main__":
    app.run(debug=True)