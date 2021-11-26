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
        country_to_search = cf.search_country(user)
        print("-"*30)
        if country_to_search:
            cf.pretty_print(country_to_search)
        else:
            print(f"El país {user.capitalize()} no existe en nuestra base de datos")
        print("-"*30)
        input("Presione enter para volver al menú principal ")

print("¡Hasta pronto!")
