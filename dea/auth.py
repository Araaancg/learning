from random import random
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
            return False