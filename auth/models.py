import json
from hashlib import sha256
from random import random

SECRET = b"navidad"

class User:
    def __init__(self,name,pwd):
        self.name = name
        e_pwd = sha256(pwd.encode()).hexdigest()
        self.pwd = e_pwd
    
    @property
    def user_dicc(self):
        return {
            "name":self.name,
            "pwd":self.pwd
        }

class Admin(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.is_admin = True


    def update_user(self, old_name, new_name, auth):
        users = auth.users
        for user in  users["data"]:
            if user["name"] == old_name:
                user["name"] = new_name
                break
        auth.write_data(users, auth.db)


class Auth:
    def __init__(self,db):
        self.db = db
    
    @property
    def users(self):
        with open(self.db, encoding="utf8") as file:
            return json.load(file)
        
    @property
    def cookies(self):
        with open("./cookies.json", encoding="utf8") as file:
            return json.load(file)
    
    def write_data(self, new_data, json_file):
        data = open(json_file, "w", encoding="utf8")
        json.dump(new_data, data, indent=4, ensure_ascii=False)
        data.close()

    def create_user(self, user):
        users = self.users
        users["data"].append(user)
        with open(self.db,encoding="utf8",mode="w") as file:
            json.dump(users, file, ensure_ascii=False,indent=4)
        
    def gen_token(self,user):
        token = sha256(user["name"].encode())
        token.update(SECRET)
        token.update(str(random()).encode())
        return token.hexdigest()
    
    def get_user(self,user_name):
        return next(filter(lambda user: user["name"] ==  user_name, self.users["data"]), False)

    def log_in(self,user):
        i, db_user = next(filter(lambda db_user: db_user[1]["name"] == user["name"], enumerate(self.users["data"])), (None, False))
        if db_user:
            if db_user["pwd"] == user["pwd"]:
                db_user["token"] = self.gen_token(db_user)
                users = self.users 
                users["data"][i] = db_user
                self.write_data(users,self.db)
                cookies = self.cookies
                cookies["token"] = {"name":user["name"], "token":db_user["token"]}
                self.write_data(cookies, "./cookies.json")
                return True
            else:
                return False
        else:
            return False
        
    def authentication(self, f): #outer
        def inner():
            user_name, user_token = self.cookies["token"].items()
            db_user = self.get_user(user_name)
            if db_user:
                if db_user["token"] == user_token:
                    return f()
                else:
                    return False
            else:
                return False
        return inner()
    
    def is_admin(self, f):
        def inner():
            user_name, _ = self.cookies["token"].values()
            db_user = self.get_user(user_name)
            if db_user["is_admin"]:
                return f()           
        return inner