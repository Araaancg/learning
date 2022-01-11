from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>You are in the home page</h1>"

@app.route("/about")
def about():
    return "Your are on about's page"