from random import random
from hashlib import sha256
import requests as req
from flask import redirect, make_response
from functools import wraps

class Auth:
    def __init__(self, secret, request, api_uri,login_uri ,**kwargs):
        self.secret = secret
        self.request = request
        self.api_uri = api_uri
        self.login_uri = login_uri
        self.kwargs = kwargs

    def gen_token(self):
        token = sha256()
        token.update(str(random()).encode())
        token.update(self.secret.encode())
        return token.hexdigest()

    def authenticate(self, f):
        @wraps(f)
        def i():
            res = f()
            email = self.request.form.get("email")
            pwd = self.request.form.get("pwd")
            print(email,pwd)
            if email and pwd:
                api_res = req.put(f"{self.api_uri}?email={email}&pwd={pwd}&token={self.gen_token()}").json()
                if api_res["success"]:
                    res.set_cookie("token", api_res["token"])
                    res.set_cookie("id", api_res["id"])
                    if self.kwargs.get("redirect_uri"):
                        res =  make_response(redirect(self.kwargs.get("redirect_uri")))
                        res.set_cookie("token", api_res["token"])
                        res.set_cookie("id", api_res["id"])
                        return res
            return res
        return i

    def authorize(self, f):
        @wraps(f)
        def i():
            cookie_id = self.request.cookies.get("id")
            cookie_token = self.request.cookies.get("token")
            if cookie_id and cookie_token:
                api_res = req.get(f"{self.api_uri}?token={cookie_token}&id={cookie_id}").json()
                if api_res["success"]:
                    return f()
 
            return redirect(self.login_uri)
        return i



'''from random import random
from hashlib import sha256
import requests as req

class Auth:
    def __init__(self,secret,request):
        self.secret = secret
        self.request = request
    
    def gen_token(self):
        token = sha256()
        token.update(str(random()).encode())
        token.update(self.secret.encode())
        return token.hexdigest()
    
    def token(self,f):
        def inner():
            for user in req.get("http://localhost:3000/dea/api").json()["users"]:
                if self.request.cookies.get("token") == user["token"]:
                    return f()
            return "Gotta login mate"
        return inner
    
    def update_token(self,con):
        cur = con().cursor()
        form = self.request.form
        print(form)
        query = f"UPDATE users SET token='{form['token']}' WHERE email='{form['email']}';"
        print(query)
        cur.execute(query)
        con().commit()
        return True
    
    def validate_pwd(self, pwd):
        res = req.get("http://localhost:3000/dea/api").json()["users"]
        for user in res:
            if user["pwd"] == pwd:
                return True
            return False'''