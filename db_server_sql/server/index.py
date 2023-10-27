import requests as req

def menu():
    print(separador)
    print("BOOKSHOP".center(30))
    print("1. Search book by id")
    print("2. Update book")
    print("3. Add new book")
    print("Q. Quit")
    print(separador)

# url_base = "http://localhost:5000"

separador = "-"*30

user = ""

while user.lower() != "q":
    menu()
    user = input(": ")
    print(separador)

    if user == "1":
        book_id = input("Enter id: ")
        url = "http://localhost:5000" + f"/book/{book_id}"
        print(url)
        book = req.get(url).json()
        print(f"\n{book}")

        input(f"{separador}\nPress enter to return to the main menu ")
    
    if user == "2":
        book_id = input("Enter id: ")
        print(separador)

        url = "http://localhost:5000" + f"/book/{book_id}"
        print(url)
        book = req.get(url).json()
        if book:
            print(f"\nLIBRO A MODIFICAR\n{book}")

            print("\nReescriba la información a su gusto\nPresione enter en lo que no quiera modificar\n")
            for k,v in list(book["book"].items()):
                if k == "id":
                    pass
                else:
                    user = input(f"{k.capitalize()}: ")
                    if user:    
                        book["book"][k] = user
            
            url = "http://localhost:5000" + f"/book/{book_id}"
            req.put(url, data={"title":book["book"]["title"],"author":book["book"]["author"], "genre":book["book"]["genre"], "stock":book["book"]["stock"]})

            print("success")
        else:
            print("action not succesful")

    if user == "3":
        # http://localhost:5000/create_book?title=jole&author=jole&genre=jole&stock=jole
        print("For creating a new book you have to introduce the following info")
        book_title = input("Title: ")
        book_author = input("Author: ")
        book_genre = input("Genre: ")
        book_stock = input("Stock: ")
        url = "http://localhost:5000/create_book"
        request = req.post(url, params={"title":book_title,"author":book_author,"genre":book_genre,"stock":book_stock})
        print(request)
        if request:
            print("success: True")
        else:
            print("success: False")







