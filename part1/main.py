import sys
import os

from src.show import show_image, show_menu
from src.pictureList import PictueList
from src.hexFunctions import delete_spaces_from_hex, add_spaces_to_hex
from src.open_image import open_image
from src.fourierTransform import fft_transform_show
from src.createColorPlot import create_color_plot

PNG_SIGNATURE= "89 50 4E 47 0D 0A 1A 0A"
PNG_SIGNATURE_NO_SPACE = "89504E470D0A1A0A"
LENGTH_SIZE = 4*2
CHUNK_TYPE_SIZE = 4*2
CRC_SIZE = LENGTH_SIZE
# Byte = 2x hex 

if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print("Too many or less arguments"+ len(sys.argv))
        raise(AttributeError)
   
    png_file_path = sys.argv[1]

    [binary_file, hex_no_space] = open_image(png_file_path)

    picture_arr=PictueList(hex_no_space=hex_no_space)
    picture_arr.mout()
    
    status = 1
    os.system("clear")
    os.system("echo \"Processing image: "+ sys.argv[1] + "\" | lolcat")

    show_menu()
    while status:
        status = int(input())
        os.system("clear")
        show_menu()
        if (status == 1): picture_arr.print_IDHR_INFO()
        if (status == 2): show_image(bytes_data=picture_arr.to_byte())
        if (status == 3): os.system("echo " + str(picture_arr.palette) + " | lolcat"); create_color_plot(picture_arr.palette); os.system("clear"); show_menu()
        if (status == 4): picture_arr.print_chunk_types()
        if (status == 5): 
            os.system("echo \"This picture contains this type of chunks: \"" + " | lolcat")
            picture_arr.print_chunk_types() 
            os.system("echo \"Witch chunk you want to delete?\"" + " | lolcat")
            chunk_name = input(); 
            delete_status = 1
            while delete_status:
                delete_status = picture_arr.delete_chunk(chunk_name)
                if delete_status == 0:
                    break
                chunk_name = input(); 
                try:
                    int(chunk_name)
                    if int(chunk_name) == 0:
                        break
                except:
                    pass

            os.system("clear")
            show_menu()
        if (status == 6): fft_transform_show(sys.argv[1])

    os.system("clear")

