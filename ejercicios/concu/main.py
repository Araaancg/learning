import time
import threading
import requests as req

# print("Empieza el programa")

# def get_data(data):
#     time.sleep(1)
#     print(f"Data downloaded from {data}")

# thread_1 = threading.Thread(target=get_data, args=["Num 1"])
# thread_2 = threading.Thread(target=get_data, args=["Num 2"])
# thread_3 = threading.Thread(target=get_data, args=["Num 3"])
# thread_4 = threading.Thread(target=get_data, args=["Num 4"])
# thread_1.start()
# thread_2.start()
# thread_3.start()
# thread_4.start()
# thread_1.join()
# thread_2.join()
# thread_3.join()
# thread_4.join()

# print("Termina el programa")

url = "https://restcountries.com/v3.1/all"

start = time.perf_counter() 

flag_urls = [country["flags"]["png"] for country in req.get(url).json()]

def get_flag(url):
    res = req.get(url).content
    with open(f"./flags/{url[-6:]}", "wb") as file:
        file.write(res)

for url in flag_urls:
    # get_flag(url)
    thread = threading.Thread(target=get_flag, args=[url])
    thread.start()

finish = time.perf_counter()

print(finish - start)
