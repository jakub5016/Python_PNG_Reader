# from ..src.pictureList import PictueList, delete_spaces_from_hex, add_spaces_to_hex


# PNG_SIGNATURE= "89 50 4E 47 0D 0A 1A 0A"
# PNG_SIGNATURE_NO_SPACE = "89504E470D0A1A0A"
# LENGTH_SIZE = 4*2
# CHUNK_TYPE_SIZE = 4*2
# CRC_SIZE = LENGTH_SIZE



# def test_delete_chunk():
#     png_file_path = "./test/green-leaf.png"
#     with open(png_file_path, 'rb') as binary_file:
#         binary_data = binary_file.read()

#         hex_representation = ' '.join(f'{byte:02X}' for byte in binary_data)
#         hex_no_space = delete_spaces_from_hex(hex_representation)

#     #### CHECK IF PNG
#     if(hex_no_space[0:len(PNG_SIGNATURE_NO_SPACE)] != PNG_SIGNATURE_NO_SPACE):
#         print("Signeture check failed")
#         raise(AttributeError)
#     else:
#        print("Signeture checked, file is an png")

#     #### START CURSOR READING
#     cursor = len(PNG_SIGNATURE_NO_SPACE)
#     picture_arr=PictueList(hex_no_space=hex_no_space)
#     picture_arr.mout()
    
#     picture_arr.print_IDHR_INFO()
#     picture_arr.print_chunk_types()
#     picture_arr.delete_chunk("tRNS")
#     print("=============AFTER CHUNK DELETE==================")
#     picture_arr.print_chunk_types()