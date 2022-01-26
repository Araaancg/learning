from flask import Flask,render_template
import requests as req

app = Flask(__name__)

@app.route("/honey")
def home():
    data = req.get("http://localhost:3000/api/collectors").json()["data"]
    # print(data)
    return render_template("index.html", collectors=data)

@app.route("/honey/<table_name>")
def table(table_name):
    data = req.get(f"http://localhost:3000/honey/api/{table_name}").json()["data"]
    # print(data)
    return render_template("index.html", info=data, name=table_name)

@app.route("/honey/new_collector", methods=["GET","POST"])
def new():
    return render_template("new.html")

if __name__ == "__main__":
    app.run(debug=True)