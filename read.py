import sys

PNG_SIGNATURE= "89 50 4E 47 0D 0A 1A 0A"
PNG_SIGNATURE_NO_SPACE = "89504E470D0A1A0A"
LENGTH_SIZE = 4*2
CHUNK_TYPE_SIZE = 4*2
CRC_SIZE = LENGTH_SIZE
# Byte = 2x hex 

class PictueList(list):
    def print_chunk_types(self):    
        for i in self:
            print(i[1])

    def _get_info_form_IHDR(self):
        IHDR_data = delete_spaces_from_hex(self[0][2])
        self.width = int(IHDR_data[0:8], 16)
        self.height = int(IHDR_data[8:16], 16)
        self.bit_depth = int(IHDR_data[16:18], 16)
        self.color_type = int(IHDR_data[18:20], 16)
        self.compression_method = int(IHDR_data[20:22], 16)
        self.filter_method = int(IHDR_data[22:24], 16)
        self.interlace_method = int(IHDR_data[24:26], 16)

    def print_IDHR_INFO(self):
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")
        print(f"Bit Depth: {self.bit_depth}")
        print(f"Color Type: {self.color_type}")
        print(f"Compression Method: {self.compression_method}")
        print(f"Filter Method: {self.filter_method}")
        print(f"Interlace Method: {self.interlace_method}")


def add_spaces_to_hex(hex):
    hex_with_spaces =""
    for index, i in enumerate(hex): 
        if (index %2 == 0) and (index != 0):
            hex_with_spaces+= " "
        hex_with_spaces += i
    return hex_with_spaces

def delete_spaces_from_hex(hex):
    hex_no_space = ""
    for i in hex:
       if i != " ":
          hex_no_space += i
    return hex_no_space

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

    