import sys
import os

from src.hex_functions import delete_spaces_from_hex
from src.show import show_image, show_menu
from src.picture_list import PictueList
from src.text import get_text
from src.open_image import open_image
from src.fourier_transform import fft_transform_show
from src.create_color_plot import create_color_plot
from src.histogram import histogram
from src.chroma import print_chroma

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

    os.system("clear")
