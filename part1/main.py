import sys
from src.pictureList import PictueList
from src.hexFunctions import delete_spaces_from_hex, add_spaces_to_hex
from src.open_image import open_image
import os
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

    while status:
        os.system("echo '\nChoose option you want to use" +
                  " \n 0 - exit " +
                  "\n 1 - print IHDR info" +
                  "\n 2 - show palette plot "+
                  "\n' | lolcat")
        status = int(input())
        print("\n")
        if (status == 1): picture_arr.print_IDHR_INFO()
        if (status == 2): os.system("echo " + str(picture_arr.palette) + " | lolcat"); create_color_plot(picture_arr.palette)

