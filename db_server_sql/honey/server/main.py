from flask import Flask,render_template
import requests as req

app = Flask(__name__)

@app.route("/")
def home():
    data = req.get("http://localhost:3000/api/collectors").json()
    print(data)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)