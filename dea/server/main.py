from flask import Flask, make_response, request, Response, redirect, render_template
import requests as req
from auth import Auth


SECRET = "4cfa98d37472801305b5d4a85bc98e6a9b4b0213de8762c35336a2b1a586c055"
auth = Auth(SECRET, request,"http://localhost:3000/dea/api/token","http://localhost:5000/dea/login", redirect_uri="http://localhost:5000/dea/secret")
app = Flask(__name__)



@app.route("/dea/login", methods=["GET","POST"])
@auth.authenticate
def login():
    res = make_response(render_template("login.html"))
    return res

@app.route("/dea/signup", methods=["GET","POST"])
def sign_up():
    print(request.form)
    api_res = req.post("http://localhost:3000/dea/api/signup", data={"email":request.form.get("email"),"pwd":request.form.get("pwd")}).json()
    print(api_res)
    res = make_response(redirect("http://localhost:5000/dea/secret")) if  api_res["success"] else make_response(render_template("sign_up.html"))
    return res

@app.route("/dea/secret")
@auth.authorize
def secret():
    print(request.cookies)
    return "secret"

@app.route("/dea/finder", methods=["GET","POST"])
# @auth.authorize
def location():
    if request.method == "GET":
        # print(request.args)
        return render_template("position.html")
    if request.method == "POST":
        res = req.post(f"http://localhost:3000/dea/api/finder?lat={request.args['lat']}&lon={request.args['lon']}").json()
        return render_template("position.html")

if __name__ == "__main__":
    app.run(debug=True)



