from hashlib import sha256
import requests as req
from flask import redirect,request,url_for, session
from functools import wraps
import secrets

def authenticate(f):
        @wraps(f)
        def i():
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            
            if email and pwd:
                api_res = req.put("http://localhost:5000/api/token", data={"email":email,"pwd":sha256(pwd.encode()).hexdigest(),"token":secrets.token_hex(16)}).json()
                if api_res["success"]:
                    session["token"] = api_res["token"]
                    session["id"] = api_res["id"]
                    return redirect(url_for("home"))
            return f()
        return i
    
def authorize(f):
    @wraps(f)
    def i():
        cookie_id = session.get("id")
        cookie_token = session.get("token")
        if cookie_id and cookie_token:
            api_res = req.get(f"http://localhost:5000/api/token?token={cookie_token}&id={cookie_id}").json()
            if api_res["success"]:
                return f()
        return redirect(url_for("login"))
    return i
