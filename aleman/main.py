'''
{
    "verbs":[
        {
            "infinitivo":"sein"
            "traducción":"ser o estar"
            "infinitiv":{
                "ich":"bin"
                "du":"bist"
                "er/sie/es":"ist"
                "wir":"sind"
                "ihr":"seid"
                "sie/Sie":"sind"
            }
            "perfekt":"ist gewesen"
            "präteritum":"waren"
        }
    ]
}
'''
import json
from socketserver import ThreadingUnixStreamServer

def get_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

DB = get_data("./verbs.json")

def insert_verb(verb):
    dicc = {"infinitive":verb}
    DB["verbs"].append(dicc)
    with open("./verbs.json", "w", encoding="utf8") as file:
        json.dump(DB,file,indent=4,ensure_ascii=False)


user = ""

while user.lower() != "q":
    # print(DB)
    user = input(": ")
    if user.lower() != "q":
        for verb in DB["verbs"]:
            exist = True if user == verb["infinitive"] else False
        if exist == False:
            insert_verb(user)
            print(True)
        else:
            print(False)
