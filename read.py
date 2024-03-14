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
    picture_arr=PictueList()
    
    while(cursor < len(hex_no_space)):
        subclass_arr =[] # This array contains info about every chunk in picture
        length = int(hex_no_space[cursor:cursor+LENGTH_SIZE], 16)
        cursor+=LENGTH_SIZE
        subclass_arr.append(length)
        
        chunk_type_hex = hex_no_space[cursor:cursor+CHUNK_TYPE_SIZE]
        byte_string = bytes.fromhex(chunk_type_hex)  
        chunk_type = byte_string.decode("ASCII")  
        subclass_arr.append(chunk_type)
        cursor+=CHUNK_TYPE_SIZE
        if ((chunk_type == "IEND") and (hex_no_space[cursor:cursor+CRC_SIZE] == "AE426082")):
            print("Valid IEND appeared, EOF\n")
            subclass_arr.append(None)
            subclass_arr.append(None)
            picture_arr.append(subclass_arr)
            picture_arr._get_info_form_IHDR()
            picture_arr.print_IDHR_INFO()
            picture_arr.read_palette()
            print(picture_arr.palette)
            exit(0)
        
        elif (chunk_type == "IEND"):
            print("Invalid IEND appeared, file might be broken")
            exit(-1)

        content = hex_no_space[cursor:cursor+(length*2)] # Byte = 2x hex 
        content_with_spaces = add_spaces_to_hex(content)
        cursor+=length*2
        subclass_arr.append(content_with_spaces)

        crc = hex_no_space[cursor:cursor+CRC_SIZE]
        crc_with_spaces = add_spaces_to_hex(crc)
        cursor+=CRC_SIZE
        subclass_arr.append(crc_with_spaces)

        picture_arr.append(subclass_arr)

    