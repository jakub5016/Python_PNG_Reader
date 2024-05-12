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
    print("Starting generating key.")
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    start_time = time.time()
    (e, n), (d, n), (p,q) = generate_keypair(4096, True)
    print(f"Generated in time: {time.time() - start_time}")
    data_to_pass = {"private_key": hex(e), 
                    "public_key": hex(d),
                    "n": hex(n),
                    "p": hex(p), 
                    "q": hex(q)}

    with open("key.json", "w") as file:
        json.dump(data_to_pass, file, indent=4)

