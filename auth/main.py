# AUTHENTIFICATION

import json
from models import User, Auth, Admin

db = "./users.json"
        
auth = Auth(db)
users_db = auth.users
user = ""


while user.lower() != "q":
    print("-"*30)
    print("AUTHENTIFICATION".center(30))
    print("1. Register")
    print("2. Log in")
    print("3. Edit user_name")
    print("Q. Quit")
    print("-"*30)
    user = input(": ")
    print("-"*30)

    if user == "1": # Create user
        name = input("Name: ")
        pwd = input("Password: ")
        user_object = User(name,pwd)
        auth.create_user(user_object.user_dicc)
        input(f"{'-'*30}\nPress enter to return to the main menu ")

    if user == "2": # Log in 
        name = input("Name: ")
        pwd = input("Password: ")
        print("-"*30)
        user_object = User(name,pwd)
        login = auth.log_in(user_object.user_dicc)
        if login:
            print("You've logged in succesfuly")
        else:
            print("Incorrect user_name or password")
        input(f"{'-'*30}\nPress enter to return to the main menu ")

    if user == "3": # Cambiar el nombre
        print("Hola")
        @auth.authentication
        @auth.is_admin   
        def update_user():
            for i, user in enumerate(auth.users["data"]):
                print(f"{i + 1}: {user['name']}")
            user = int(input(": ")) - 1
            new_name = input("Nuevo nombre: ")
            admin_instance = Admin("admin", "1234")
            print("Está seguro de que quiere realizar los cambios?")
            decision = input("(Y/N): ")
            if decision.lower() == "y":
                admin_instance.update_user(auth.users["data"][user]["name"], new_name, auth)
                print("Cambios realizados con éxito")
            else:
                print("No se han realizado los cambios")
        input(f"{'-'*30}\nPress enter to return to the main menu ")
