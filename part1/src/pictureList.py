from .hexFunctions import delete_spaces_from_hex, add_spaces_to_hex
import struct

PNG_SIGNATURE= "89 50 4E 47 0D 0A 1A 0A"
PNG_SIGNATURE_NO_SPACE = "89504E470D0A1A0A"
LENGTH_SIZE = 4*2
CHUNK_TYPE_SIZE = 4*2
CRC_SIZE = LENGTH_SIZE

class PictueList(list):
    def __init__(self, hex_no_space):
        cursor = len(PNG_SIGNATURE_NO_SPACE)
    
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
                self.append(subclass_arr)
                return(None)
            
            elif (chunk_type == "IEND"):
                print("Invalid IEND appeared, file might be broken")
                return(None)

            content = hex_no_space[cursor:cursor+(length*2)] # Byte = 2x hex 
            content_with_spaces = add_spaces_to_hex(content)
            cursor+=length*2
            subclass_arr.append(content_with_spaces)

            crc = hex_no_space[cursor:cursor+CRC_SIZE]
            crc_with_spaces = add_spaces_to_hex(crc)
            cursor+=CRC_SIZE
            subclass_arr.append(crc_with_spaces)

            self.append(subclass_arr)

    def mout(self):
        self._get_info_form_IHDR()
        self.read_palette()


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
    
    def get_chunk_index(self, chunk_name):
        chunk_index = 0
        for index, i in enumerate(self):
            if i[1] == chunk_name:
                chunk_index = index
        return chunk_index
    

    def read_palette(self):
        if self.color_type != 3:
            print("This picture doesn't contain color palette")
            return(-1)

        palette_index = self.get_chunk_index("PLTE")

        palette_data = delete_spaces_from_hex(self[palette_index][2]) 
        palette_data_bytes = bytes.fromhex(palette_data)

        self.palette = []
        for i in range(0, len(palette_data_bytes), 3):
            r = int(palette_data_bytes[i])
            g = int(palette_data_bytes[i+1])
            b = int(palette_data_bytes[i+2])

            color = [r, g, b]
            self.palette.append(color)

    def delete_chunk(self, chunk_name):
        if (chunk_name == "IDAT"or chunk_name == "IHDR" or chunk_name == "IEND"):
            print("You must not delete this chunk! Choose another or type 0")
            return 1

        for index, i in enumerate(self):
            if (i[1] == chunk_name):
                self.pop(index)
                return 0
            
        print("This chunk dosesn't exist")
        return 1
    

    def write_to_file(self, file):
        file.write(bytes.fromhex(PNG_SIGNATURE_NO_SPACE))
        for i in self:

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