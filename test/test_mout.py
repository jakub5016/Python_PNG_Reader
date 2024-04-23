from ..src.pictureList import PictueList
from ..src.open_image import open_image


def test_mout():
    png_file_path = "./test/green-leaf.png"
    [binary_file, hex_no_space] = open_image(png_file_path)
    picture_arr = PictueList(hex_no_space=hex_no_space)
    picture_arr.mout()

    binary_file.close()
