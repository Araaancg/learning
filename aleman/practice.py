from main import *
from random import shuffle
from funcs import *

user = ""

# print(len(DB["verbs"]))

while user.lower() != "q":
    menu()

    user = input(": ")
    print("-"*30)

    if user == "1":
        while user != "q":
            user = input("Verbo: ")
            verb = search(user)
            if verb: 
                pPrint(verb)
            elif user != "q":
                print("Verbo no encontrado")
            print("-"*30)
        # user = ""

        # input("\nPress enter to return to the main menu ")


    if user == "2":
        verbs_al = [{"infinitiv":verb["infinitiv"],"übersetzung":verb["übersetzung"]} for verb in DB["verbs"]]
        shuffle(verbs_al)
        for verb in verbs_al:
            user = input(f"\nDeutsch: {verb['infinitiv']} ")
            if user.lower() == "q":
                user = ""
                break
            print(f"Spanisch: {verb['übersetzung']}")