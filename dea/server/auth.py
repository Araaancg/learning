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
            
            if email and pwd:
                api_res = req.put(self.api_uri, data={"email":email,"pwd":pwd,"token":self.gen_token()}).json()
                print(api_res)
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

