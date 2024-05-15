from src.picture_list import PictueList
from src.open_image import open_image
from src.cryptography.png.idat import encrypt_idat, decrypt_idat, update_crc
from src.hex_functions import delete_spaces_from_hex, add_spaces_to_hex

import random
import json
import sys
import os
import rsa

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
            + "\n 3 - RSA encode using CBC"
            + "\n 4 - RSA decode using CBC"
            + "\n 5 - RSA encode using rsa python lib"
            + "\n 6 - RSA decode using rsa python lib"
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
            + "\n 3 - RSA encode using CBC"
            + "\n 4 - RSA decode using CBC"
            + "\n 5 - RSA encode using rsa python lib"
            + "\n 6 - RSA decode using rsa python lib"
            + "\n' | lolcat"
        )
        if status == 1:
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0

            if picture_arr.color_type == 6:
                new_IDAT, public_key, private_key, number_of_zeros, removed_hex = encrypt_idat(picture_arr[IDAT_index], picture_arr.width ,bit_depth=8)
            else:
                new_IDAT, public_key, private_key, number_of_zeros, removed_hex = encrypt_idat(picture_arr[IDAT_index], picture_arr.width)


            picture_arr[IDAT_index] = new_IDAT

            print(f"Your public and private keys are stored in JSON file named: {sys.argv[1][:-4]}_json_keys")

            file_to_write = open(sys.argv[1][:-4] + "_rsa_encoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

            data_to_pass = {"private_key": hex(private_key[0]), 
                            "public_key": hex(public_key[0]),
                            "n": hex(public_key[1]), 
                            "padding": number_of_zeros,
                            "removed_hex": removed_hex}

            with open(sys.argv[1][:-4] + "_rsa_encoded.json", "w") as file_for_keys:
                json.dump(data_to_pass, file_for_keys, indent=4)

            print("File succesfully encoded")


        if status == 2:
            with open(sys.argv[1][:-4] + ".json", "r") as read_keys:
                keys = json.load(read_keys)
            
            d = int(keys["private_key"], 16)
            n = int(keys["n"], 16)
            padding = keys["padding"]
            removed_hex = keys["removed_hex"]
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0
            
            new_IDAT = decrypt_idat(picture_arr[IDAT_index], picture_arr.width, private_key=(d,n), padding=padding, removed_hex=removed_hex)
            
            picture_arr[IDAT_index] = new_IDAT

            print("File decrypted and saved")

            file_to_write = open(sys.argv[1][:-16] + "_rsa_decoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

        if status ==3:
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0

            if picture_arr.color_type == 6:
                new_IDAT, public_key, private_key, number_of_zeros, removed_hex, iv = encrypt_idat(picture_arr[IDAT_index], picture_arr.width, bit_depth=8,type="CBC")
            else:
                new_IDAT, public_key, private_key, number_of_zeros, removed_hex, iv = encrypt_idat(picture_arr[IDAT_index], picture_arr.width, type="CBC")
            
            picture_arr[IDAT_index] = new_IDAT

            print(f"Your public and private keys are stored in JSON file named: {sys.argv[1][:-4]}_json_keys")

            file_to_write = open(sys.argv[1][:-4] + "_rsa_cbc_encoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

            data_to_pass = {"private_key": hex(private_key[0]), 
                            "public_key": hex(public_key[0]),
                            "n": hex(public_key[1]), 
                            "padding": number_of_zeros, 
                            "removed_hex": removed_hex , 
                            "iv":iv}

            with open(sys.argv[1][:-4] + "_rsa_cbc_encoded.json", "w") as file_for_keys:
                json.dump(data_to_pass, file_for_keys, indent=4)

            print("File succesfully encoded")

        if status == 4:
            with open(sys.argv[1][:-4] + ".json", "r") as read_keys:
                keys = json.load(read_keys)
            
            d = int(keys["private_key"], 16)
            n = int(keys["n"], 16)
            padding = keys["padding"]
            iv = int(keys["iv"])
            removed_hex = keys["removed_hex"]

            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0
            
            new_IDAT = decrypt_idat(picture_arr[IDAT_index], picture_arr.width, private_key=(d,n),removed_hex=removed_hex, padding=padding, iv=iv)
            

            picture_arr[IDAT_index] = new_IDAT

            print("File decrypted and saved")

            file_to_write = open(sys.argv[1][:-16] + "_decoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

        if status == 5:
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IDAT = picture_arr[IDAT_index]
            with  open("key.json", "r") as key_file:
                key_pair = json.load(key_file)
                d = int(key_pair["private_key"], 16)
                e = int(key_pair["public_key"], 16)
                n = int(key_pair["n"], 16)
                p = int(key_pair["p"], 16)
                q = int(key_pair["q"], 16)

            if picture_arr.color_type == 6:
                new_IDAT, public_key, private_key, number_of_zeros, removed_hex= encrypt_idat(picture_arr[IDAT_index], picture_arr.width, bit_depth=8 ,private_key=(d , n) ,public_key=(e , n), type="lib")
            else:
                new_IDAT, public_key, private_key, number_of_zeros, removed_hex= encrypt_idat(picture_arr[IDAT_index], picture_arr.width, private_key=(d , n) ,public_key=(e , n), type="lib")
            IDAT = new_IDAT
            IDAT[0] = int(len(IDAT[2])//2) 
            IDAT[3] = update_crc(IDAT[2])

            picture_arr[IDAT_index] = IDAT
            file_to_write = open(sys.argv[1][:-4] + "_rsa_lib_encoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

            data_to_pass = {"private_key": hex(private_key[0]), 
                            "public_key": hex(public_key[0]),
                            "n": hex(public_key[1]), 
                            "p": hex(p),
                            "q": hex(q),
                            "removed_hex": removed_hex,
                            "padding": number_of_zeros,
                            }

            with open(sys.argv[1][:-4] + "_rsa_lib_encoded.json", "w") as file_for_keys:
                json.dump(data_to_pass, file_for_keys, indent=4)

            print("File succesfully encoded")

        if status == 6:
            with open(sys.argv[1][:-4] + ".json", "r") as read_keys:
                keys = json.load(read_keys)
            
            d = int(keys["private_key"], 16)
            e = int(keys["public_key"], 16)
            n = int(keys["n"], 16)
            p = int(keys["p"], 16)
            q = int(keys["q"], 16)
            padding = keys["padding"]
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            IHDR_index = 0
            
            new_IDAT = decrypt_idat(picture_arr[IDAT_index], picture_arr.width, private_key=(d,n), padding=padding, e=e, p=p, q=q)
            
            picture_arr[IDAT_index] = new_IDAT

            print("File decrypted and saved")

            file_to_write = open(sys.argv[1][:-16] + "_rsa_decoded.png", "wb")
            picture_arr.write_to_file(file_to_write)

    os.system("clear")
