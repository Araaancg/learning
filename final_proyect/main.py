'''
Proyecto final: JUEGO PARA APRENDER ALEMÁN BÁSICO
En total habrá entre 4-6 niveles donde se aprenderá en cada uno un tipo de palabra diferente: sustantivo,
adjetivo, pronombre personal...
La batalla final será contra un mob pasivo (Duo) y consistirá en ordenar las palabras para formar una frase.
Si la frase está bien se le quitará vida al mob, sino en principio no pasa nada.

En principio las palabras aprendidas en los niveles previos a la batalla final se guardaran en un archivo y el usuario
las podrá consultar si quiere estudiar. En la batalla final se puede poner como ventaja consultar dicho archivo una sola vez
por si surjen dudas.

Habrá un objeto usuario desde el cual se podrá inciar sesión por dos razones:
- pueden jugar en el mismo ordenador mas de una persona, iniciando sesión en tu usuario
- cada usuario tendrá su propio progreso
- se podrán hacer batallas entres usuarios si se quiere
- no pierdes progreso ya que se te guarda en tu cuenta

'''

from funcs import *
import time


users_data = get_users()
user_names = [user["name"] for user in  users_data["users"]]
# print(user_names)

user = ""
separador = "-"*50

while user.lower() != "q":
    users_data = get_users()
    user_names = [user["name"] for user in  users_data["users"]]

    print(separador)
    main_menu()
    print(separador)
    user = input(": ")
    print(separador)
    
    if user == "1":
        name = input("Name: ")
        inexistent_user = False if name in user_names else True
        while inexistent_user:
            print("That user does not exist, please try again")
            name = input("Name: ")
            inexistent_user = False if name in user_names else True 
        pwd = input("Password: ")
        log_in = log_in(users_data,name,pwd)
        print(log_in)
        while log_in == False:
            print("Incorrect password, please try again")
            pwd = input("Password: ")
            log_in = log_in(users_data,name,pwd)
            print(log_in)
        print(f"Log in succesful, welcome {name}")
    
    if user == "2": # Resgistrarse
        name = input("Name: ")
        is_user_repeated = True if name in user_names else False
        # print(is_user_repeated)
        while is_user_repeated:
            print("\nThis user already exists, please try again")
            name = input("\nName: ")
            is_user_repeated = True if name in user_names else False
        
        pwd = input("Password: ")
        create_user(users_data,name,pwd) 
        print("\nCreating user...")
        time.sleep(1.5)
        print("User created")

        input(f"{separador}\nPress enter to return to the main menu ")

