from main import DB

def menu():
    print(f"{'-'*30}\nPRACTICAR VERBOS ALEMÁN")
    print("1. Consultar traducción (al-esp)")
    print("2. Traducir")
    print(f"Q. Quit\n{'-'*30}")

def search(request):
    try:
        return next(filter(lambda verb: verb["infinitiv"] == request, DB["verbs"]), False)
    except:
        return None


# print(search("sein"))

def pPrint(dicc):
    print(" ")
    print(f"{dicc['infinitiv']} - {dicc['übersetzung']}")
    # print("INFO".center(15))
    # print(f"Infinitiv: {dicc['infinitiv']}")
    # print(f"Übersetzung: {dicc['übersetzung']}")
