import sys
import os
import zlib
import struct

from src.hex_functions import delete_spaces_from_hex, add_spaces_to_hex
from src.show import show_image, show_menu
from src.picture_list import PictueList
from src.text import get_text
from src.open_image import open_image
from src.fourier_transform import fft_transform_show
from src.create_color_plot import create_color_plot
from src.histogram import histogram
from src.chroma import print_chroma
from src.cryptography.cbc import cbc_decrypt, cbc_encrypt
from src.cryptography.rsa import decrypt_chunk, encrypt_chunk, generate_keypair
# Byte = 2x hex

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
    show_menu()
    while status:
        status = int(input())
        os.system("clear")
        show_menu()
        if status == 1:
            picture_arr.print_IDHR_INFO()
        if status == 2:
            show_image(bytes_data=picture_arr.to_byte())
        if status == 3:
            if picture_arr.get_chunk_index("PLTE") != 0:
                os.system("echo " + str(picture_arr.palette) + " | lolcat")
                create_color_plot(picture_arr.palette)
                os.system("clear")
                show_menu()
            else:
                print(
                    f"This file doesn't contain palette color type is: {picture_arr.color_type}"
                )
        if status == 4:
            picture_arr.print_chunk_types()
        if status == 5:
            os.system(
                'echo "This picture contains this type of chunks: "' + " | lolcat"
            )
            picture_arr.print_chunk_types()
            os.system('echo "Witch chunk you want to delete?"' + " | lolcat")
            chunk_name = input()
            delete_status = 1
            while delete_status:
                delete_status = picture_arr.delete_chunk(chunk_name)
                if delete_status == 0:
                    break
                chunk_name = input()
                try:
                    int(chunk_name)
                    if int(chunk_name) == 0:
                        break
                except:
                    pass

            os.system("clear")
            show_menu()
        if status == 6:
            fft_transform_show(sys.argv[1])
        if status == 7:
            if (picture_arr.color_type == 3) and (
                picture_arr.get_chunk_index("hIST") != 0
            ):
                histogram(
                    picture_arr.palette,
                    picture_arr[picture_arr.get_chunk_index("hIST")],
                )
            else:
                print("This file doesn't contain histogram\n")
        if status == 8:
            get_text(picture_arr)
        if status == 9:
            picture_arr.anonymization()
        if status == 10:
            file_to_write = open(sys.argv[1][:-4] + "_copy.png", "wb")
            picture_arr.write_to_file(file_to_write)
        if status == 11:
            print_chroma(picture_arr)
        if status == 12:
            IDAT_index = picture_arr.get_chunk_index("IDAT")
            data_str = (picture_arr[IDAT_index][2].split())
            data = [int(x, 16) for x in data_str]

            chunk_type = b"\x49\x44\x41\x54"
            chunk_data = bytes.fromhex(picture_arr[IDAT_index][2])

            public_key, private_key = generate_keypair(8)
            encrypted_chunk = encrypt_chunk(data, public_key)
            print(f"Here is your public and public keys:\n   public key: {public_key}\n  private key: {private_key}\nKeep private key in secret in case of decrypting file!")

            hex_list = []
            for num in encrypted_chunk:
                hex_num = hex(num)[2:]
                width = (len(hex_num) + 3) // 4 * 4  # Calculate width to ensure full number output
                hex_list.append('{:0>{width}}'.format(hex_num, width=width))

            hex_string = ' '.join(hex_list)
            picture_arr[IDAT_index][2] = hex_string

            #Lenght of IDAT changed
            picture_arr[IDAT_index][0] = picture_arr[IDAT_index][0] * 2

            # You have to change widht and height
            IHDR_data = picture_arr[0][2]

            width_hex = delete_spaces_from_hex(IHDR_data)[0:8]
            height_hex = delete_spaces_from_hex(IHDR_data)[8:16]

            # Convert hexadecimal to decimal
            width_dec = int(width_hex.replace(' ', ''), 16)
            height_dec = int(height_hex.replace(' ', ''), 16)

            # Double the values
            new_width_dec = width_dec * 2
            new_height_dec = height_dec * 2

            # Convert decimal back to hexadecimal
            new_width_hex = '{:08X}'.format(new_width_dec)
            new_height_hex = '{:08X}'.format(new_height_dec)

            # Update picture_arr[0]
            picture_arr[0][2] = add_spaces_to_hex(new_width_hex + new_height_hex + delete_spaces_from_hex(IHDR_data)[16:])
            
            # Update CRC
            chunk_type = b"\x49\x44\x41\x54"
            chunk_data = bytes.fromhex(hex_string)
            picture_arr[IDAT_index][3] = hex(zlib.crc32(chunk_type + chunk_data))[2:].upper()
            print(hex(zlib.crc32(chunk_type + chunk_data)))

            # Write to file
            file_to_write = open(sys.argv[1][:-4] + "_rsa_encoded.png", "wb")
            picture_arr.write_to_file(file_to_write)


        if status == 13:
            d = ""
            while not d.isnumeric():
                print("Privide private key:\n d = ")
                d = input()
            d = int(d)

            n = ""
            while not n.isnumeric():
                print("Privide private key:\n n = ")
                n = input()
            n = int(n)

            IDAT_index = picture_arr.get_chunk_index("IDAT")
            data_str = picture_arr[IDAT_index][2]
            even = False
            modified_words = ""
            for i in data_str:
                if i != " ":
                    modified_words += i
                elif even == False:
                    even = True
                else:
                    even = False
                    modified_words += i

            data_str = modified_words.split()
            data = [int(x, 16) for x in data_str]
            decrypted_chunk = decrypt_chunk(data, (d, n))

            hex_string = ' '.join(format(x, '02X') for x in decrypted_chunk)
            picture_arr[IDAT_index][2] = hex_string
            picture_arr[IDAT_index][0] = picture_arr[IDAT_index][0]//2

            # You have to change widht and height
            IHDR_data = picture_arr[0][2]

            width_hex = delete_spaces_from_hex(IHDR_data)[0:8]
            height_hex = delete_spaces_from_hex(IHDR_data)[8:16]

            # Convert hexadecimal to decimal
            width_dec = int(width_hex.replace(' ', ''), 16)
            height_dec = int(height_hex.replace(' ', ''), 16)

            # Make val two times smaller
            new_width_dec = width_dec // 2
            new_height_dec = height_dec // 2

            # Convert decimal back to hexadecimal
            new_width_hex = '{:08X}'.format(int(new_width_dec))
            new_height_hex = '{:08X}'.format(int(new_height_dec))

            # Update picture_arr[0]
            picture_arr[0][2] = add_spaces_to_hex(new_width_hex + new_height_hex + delete_spaces_from_hex(IHDR_data)[16:])

            # Update CRC
            chunk_type = b"\x49\x44\x41\x54"
            chunk_data = bytes.fromhex(hex_string)
            picture_arr[IDAT_index][3] = hex(zlib.crc32(chunk_type + chunk_data))[2:].upper()
            # print(hex(zlib.crc32(chunk_type + chunk_data)))
            
            file_to_write = open(sys.argv[1][:-16] + "_rsa_decoded.png", "wb")
            picture_arr.write_to_file(file_to_write)


    os.system("clear")
