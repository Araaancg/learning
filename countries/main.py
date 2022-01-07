import requests as req

'''
APP DE TERMINAL
características
- buscar un país y que te devuelva
    - capital
    - población
    - superficie
    - idioma
'''

import c_functions as cf


user = "0"

while user != "q".lower():
    cf.menu()
    user = input(": ")

    if user == "1":
        user = input("Introduzca el país: ").lower()
        country_to_search = cf.get_by_term(user)
        print("-"*30)
        if country_to_search:
            cf.pretty_print(country_to_search)
        else:
            print(f"El país {user.capitalize()} no existe en nuestra base de datos")
        print("-"*30)
        input("Presione enter para volver al menú principal ")

    if user == "2":
        user = input("Introduzca un país: ").lower()
        country_to_search = cf.get_by_term(user)
        if country_to_search:
            flag_url = country_to_search[0]["flags"]["svg"]
            print(flag_url)
            flag = req.get(flag_url).content
            with open(f"./img/{country_to_search[0]['name']['common'].lower()}.svg", mode="wb") as file:
                file.write(flag)
        else:
            print(f"El país {user.capitalize()} no existe en nuestra base de datos")
        print("-"*30)
        input("Presione enter para volver al menú principal ")

    if user == "3":
        pass 
        
print("¡Hasta pronto!")

