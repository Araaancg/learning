import requests as req

url_base = "http://127.0.0.1:5000"



user = ""

while user.lower() != "q":
    print("1. Search book by id")
    # print("2. Update book")
    print("Q. Quit")

    user = input(": ")

    if user == "1":
        book_id = input("Enter id:")
        url_base += f"/book/{book_id}"
        book = req.get(url_base).json()
        print(book)
    
    if user == "2":
        book_id = input("Enter id: ")
        