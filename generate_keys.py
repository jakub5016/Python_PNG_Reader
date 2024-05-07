from src.cryptography.rsa import generate_keypair
import json
import os
import time
from datetime import datetime

if __name__ == "__main__":
    number = 0
    start_time = 0 
    os.system("clear")
    now = datetime.now()
    print("Starting generating keys.")
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    while True:
        start_time = time.time()
        (e, n), (d, n)= generate_keypair(4096)
        print(f"Number of keys generated: {number}. Last generated in time: {time.time() - start_time}")
        with open("keys.txt", "+a") as file:
            file.write(f"e:{e}\nd:{d}\nn:{n}\n\n")

        file.close()

        number+=1