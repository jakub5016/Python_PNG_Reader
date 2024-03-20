import os
import io

from PIL import Image

def show_image(bytes_data = None, file_name = None):
    if file_name != None:
        img = Image.open(file_name)
        
        # Display the image using PIL
        img.show()

    elif bytes_data !=None:
        image = Image.open(io.BytesIO(bytes_data))
        image.show()


def show_menu():
    os.system("echo '\nChoose option you want to use" +
                  " \n 0 - exit " +
                  "\n 1 - print IHDR info" +
                  "\n 2 - show img "+
                  "\n 3 - show palette plot "+
                  "\n 4 - show chunk types" +
                  "\n 5 - delete chunk" +
                  "\n 6 - show fourier transform" +
                  "\n' | lolcat")