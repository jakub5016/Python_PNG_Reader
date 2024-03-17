import sys
from pictureList import PictueList
from hexFunctions import delete_spaces_from_hex, add_spaces_to_hex

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

    #### READ DATA
    with open(png_file_path, 'rb') as binary_file:
        binary_data = binary_file.read()

        hex_representation = ' '.join(f'{byte:02X}' for byte in binary_data)
        hex_no_space = delete_spaces_from_hex(hex_representation)

    #### CHECK IF PNG
    if(hex_no_space[0:len(PNG_SIGNATURE_NO_SPACE)] != PNG_SIGNATURE_NO_SPACE):
        print("Signeture check failed")
        raise(AttributeError)
    else:
       print("Signeture checked, file is an png")

    #### START CURSOR READING
    cursor = len(PNG_SIGNATURE_NO_SPACE)
    picture_arr=PictueList(hex_no_space=hex_no_space)
    picture_arr.mout()
    picture_arr.print_IDHR_INFO()
    picture_arr.print_chunk_types()
    picture_arr.delete_chunk("tRNS")
    print("=============AFTER CHUNK DELETE==================")
    picture_arr.print_chunk_types()
    file = open('new_file.png', "wb")
    file.write(bytes.fromhex(PNG_SIGNATURE_NO_SPACE))
    for i in picture_arr:

        file.write(i[0].to_bytes(4, "big"))
        file.write(bytes(i[1], "utf-8"))
        if (i[2] != None):
            file.write(bytes.fromhex(i[2]))
        if (i[3] != None):
            file.write(bytes.fromhex(i[3]))

        # Prompts to debug
        # 
        # print(i[0].to_bytes(4, "big").hex().upper()) 
        # print((bytes(i[1], "utf-8")).hex()) 
        # if (i[3] != None):
        #     print(bytes.fromhex((i[3])))
    file.close()

