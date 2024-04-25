from ..src.picture_list import PictueList, delete_spaces_from_hex, add_spaces_to_hex
from ..src.open_image import open_image


def test_mout():
    png_file_path = "./test/green-leaf.png"
    [binary_file, hex_no_space] = open_image(png_file_path)
    picture_arr = PictueList(hex_no_space=hex_no_space)
    picture_arr.mout()
    picture_arr.get_chunk_index("")
    picture_arr.delete_chunk("")
    picture_arr.print_chunk_types()

    binary_file.close()
