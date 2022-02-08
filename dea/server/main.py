from flask import Flask, make_response,request,redirect

app = Flask(__name__)

#4cfa98d37472801305b5d4a85bc98e6a9b4b0213de8762c35336a2b1a586c055


def token(f):
    def inner():
        print("It works")
        if request.cookies.get("token") == "1234":
            return f()
        return redirect ("http://google.com")
    return inner

@app.route("/login")
def log_in():
    res = make_response("Log in")
    res.set_cookie("token","1234")
    return res

@app.route("/secret")
@token
def secret():
    return "Secret"

if __name__ == "__main__":
    app.run(debug=True,port=5000)