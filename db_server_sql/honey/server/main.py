from flask import Flask,render_template
import requests as req

app = Flask(__name__)

@app.route("/honey")
def home():
    data = req.get("http://localhost:3000/api/collectors").json()["data"]
    return render_template("index.html", collectors=data)

@app.route("/honey/<table_name>")
def table(table_name):
    data = req.get(f"http://localhost:3000/honey/api/{table_name}").json()["data"]
    return render_template("index.html", info=data, name=table_name)

@app.route("/honey/new/<person>", methods=["GET","POST"])
def new(person):
    return render_template("new.html", url=f"http://localhost:3000/honey/api/{person}s", person=person)

@app.route("/honey/buy", methods=["GET","POST"])
def buy():
    collectors = req.get("http://localhost:3000/honey/api/collectors").json()["data"]
    name_collectors = [collector["name"] for collector in collectors]
    providers = req.get("http://localhost:3000/honey/api/providers").json()["data"]
    name_providers = [provider["name"] for provider in providers]
    return render_template("buy.html", collectors=name_collectors, providers=name_providers)

if __name__ == "__main__":
    app.run(debug=True)