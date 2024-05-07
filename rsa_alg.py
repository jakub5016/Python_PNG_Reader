from src.picture_list import PictueList
from src.open_image import open_image
from src.cryptography.png.idat import encrypt_idat, decrypt_idat

import random
import json
import sys
import os
if __name__ == "__main__":

    if len(sys.argv) != 2:
            print("Too many or less arguments" + len(sys.argv))
            raise (AttributeError)

    png_file_path = sys.argv[1]

    [binary_file, hex_no_space] = open_image(png_file_path)

    picture_arr = PictueList(hex_no_space=hex_no_space)
    picture_arr.mout()

    status = 1
    os.system("clear")
    os.system('echo "Processing image: ' + sys.argv[1] + '" | lolcat')

    os.system(
        "echo '\nChoose option you want to use"
        + " \n 0 - exit "
        + "\n 1 - RSA encode using EBC"
        + "\n 2 - RSA decode using EBC"
        + "\n' | lolcat"
    )

    while status:
        status = int(input())
        os.system("clear")
        os.system(
            "echo '\nChoose option you want to use"
            + " \n 0 - exit "
            + "\n 1 - RSA encode using EBC"
            + "\n 2 - RSA decode using EBC"
            + "\n' | lolcat"
        )
        if status == 1:
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0

            try:
                keys_file = open("keys.txt", "r")
                lines = keys_file.readlines()
                selected_line = random.randint(0, len(lines)-1)
                while selected_line % 4 != 0:
                    selected_line = random.randint(0, len(lines)-1)
                
                e = int(lines[selected_line][2:])
                d = int(lines[selected_line+1][2:])
                n = int(lines[selected_line+2][2:])

                new_IDAT, public_key, private_key, number_of_zeros = encrypt_idat(picture_arr[IDAT_index], picture_arr.width, private_key=(d , n) ,public_key=(e , n))

            except FileNotFoundError:
                new_IDAT, public_key, private_key, number_of_zeros = encrypt_idat(picture_arr[IDAT_index], picture_arr.width)

            picture_arr[IDAT_index] = new_IDAT

            print(f"Your public and private keys are stored in JSON file named: {sys.argv[1][:-4]}_json_keys")

            file_to_write = open(sys.argv[1][:-4] + "_rsa_encoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

            data_to_pass = {"private_key": hex(private_key[0]), "public_key": hex(public_key[0]),"n": hex(public_key[1]), "padding": number_of_zeros}

            with open(sys.argv[1][:-4] + "_rsa_encoded.json", "w") as file_for_keys:
                json.dump(data_to_pass, file_for_keys, indent=4)

            print("File succesfully encoded")
        if status == 2:
            with open(sys.argv[1][:-4] + ".json", "r") as read_keys:
                keys = json.load(read_keys)
            
            d = int(keys["private_key"], 16)
            n = int(keys["n"], 16)
            padding = keys["padding"]

            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0
            
            new_IDAT = decrypt_idat(picture_arr[IDAT_index], picture_arr.width, (d,n), padding)
            

            picture_arr[IDAT_index] = new_IDAT

            print("File decrypted and saved")

            file_to_write = open(sys.argv[1][:-16] + "_rsa_decoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

    os.system("clear")
