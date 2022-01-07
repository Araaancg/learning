'''
funciones principales del juego que no tengan que ver con el usuario
'''
from hashlib import sha256
import json

def main_menu():
    print("JOLA".center(50))
    print("1. Sign in")
    print("2. Sign up / Register")
    print("Q. Quit game")

def get_users():
    with open("./users.json",encoding="utf8") as file:
        return json.load(file)

def create_user(data,name,pwd):
    pwd = sha256(pwd.encode())
    pwd = pwd.hexdigest()
    data["users"].append({"name":name,"pwd":pwd})
    with open("./users.json",encoding="utf8",mode="w") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)

def log_in(data,name,enter_pwd):
    enter_pwd = sha256(enter_pwd.encode())
    enter_pwd = enter_pwd.hexdigest()
    for user in data["users"]:
        if user["name"] == name:
            return True if user["pwd"] == enter_pwd else False
