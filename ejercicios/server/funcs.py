import json


def get_data():
    with open("bookshop.json", encoding="utf8") as file:
        return json.load(file)
    
DB = get_data()

def write_data(data):
    with open("bookshop.json", encoding="utf8", mode="w") as file:
        json.dump(data,file,ensure_ascii=False,indent=4)

def get_by_id(book_id):
    return next(filter(lambda book: book["id"] == book_id, DB["data"]), False)

def delete_by_id(book_id):
    book_to_delete = get_by_id(book_id)
    DB["data"].remove(book_to_delete)
    # print(DB)
    write_data(DB)
    return True

def update_book(book_id, request):
    book_to_update = get_by_id(book_id)
    if book_to_update:
        i = DB["data"].index(book_to_update)
        for k,v in request.form.items():
            if k in book_to_update.keys():
                if k == "stock":
                    book_to_update[k] = int(v)
                else:
                    book_to_update[k] = v
        DB["data"][i] = book_to_update
        write_data(DB)
        return True, book_to_update
    return False