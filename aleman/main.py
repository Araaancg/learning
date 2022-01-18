import json


def get_data(json_file):
    with open(json_file, encoding="utf8") as file:
        return json.load(file)

DB = get_data("./verbs.json")

def write_data(json_file,data):
    with open(json_file,"w") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)

def insert_verb(verb):
    dicc = {"infinitiv":verb}
    DB["verbs"].append(dicc)
    write_data("./verbs.json",DB)

# print(len(DB["verbs"])) #180

user = ""

#INSERTAR VERBOS
# while user.lower() != "q":
#     # print(DB)
#     user = input(": ")
#     if user.lower() != "q":
#         for verb in DB["verbs"]:
#             exist = True if user == verb["infinitiv"] else False
#             if exist:
#                 break
#         print(exist)
#         if exist:
#             pass
#         else:
#             insert_verb(user)

#INSERTAR DICC COMPLETO
# for verb in DB["verbs"][160:]:
#     verb["übersetzung"] =  None
#     verb["merkmals"] = None
#     verb["präsens"] = {
#         "ich":None,
#         "du":None,
#         "er,sie,es":None,
#         "wir":None,
#         "ihr":None,
#         "sie/Sie":None
#     }
#     verb["perfeckt"] = {
#         "konjugation":None,
#         "verb":None
#     }
#     verb["präteritum"] = None


#INSERTAR MAS INFO
for verb in DB["verbs"]:
    print(f"Deutsch: {verb['infinitiv']}")
    for k,v in verb.items():
        if k == "merkmals" and not verb["merkmals"]:
            v = input(f"{k}: ")
            if v:
                verb[k] = v    

    #     # if k == "präsens" or k == "perfekt":
    #     #     for k,v in verb[k].items():
    #     #         # print(f"Deutsch: {verb['infinitiv']}")
    #     if not v:
    #         v = input(f"{k}: ")
    #         if v:
    #             verb[k] = v

    write_data("./verbs.json",DB)
        

#CHANGE/ADD KEYS
# for verb in DB["verbs"][160:]:
#     verb["präteritum"] = verb.pop("präteritum")
#     # verb["präteritum"] = None

# write_data("./verbs.json",DB)

# print(DB["verbs"][0])