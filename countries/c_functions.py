import requests as req
import json
import random

def menu():
    print("-"*30)
    print("LOS PAÍSES".center(30))
    print("1. Buscar información de un país")
    print("2. Descargar la bandera de un país")
    print("3. Jugar")
    print("Q. Terminar programa")
    print("-"*30)

def get_by_term(c, **kwargs):
    term = "name"
    if kwargs.get("continent"):
        term = "region"
    c_info = req.get(f"https://restcountries.com/v3.1/{term}/{c}").json()  
    try:
        country_info["status"]
        return None
    except:
        return c_info

def pretty_print(country_info):
    print(country_info[0]["name"]["common"].upper().center(30))
    print(f"       Capital: {country_info[0]['capital'][0]}")
    print(f"     Población: {country_info[0]['population']} habitantes")
    print(f"    Superficie: {country_info[0]['area']} km2")
    languages = list(country_info[0]['languages'].values())
    print(f"        Idioma: {languages}")
