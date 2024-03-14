from hexFunctions import delete_spaces_from_hex, add_spaces_to_hex

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
    
    def read_palette(self):
        if self.color_type != 3:
            print("This picture doesn't contain color palette")
            return(-1)

        palette_index = 0
        for index, i in enumerate(self):
            if i[1] == "PLTE":
                palette_index = index

        palette_date = delete_spaces_from_hex(self[palette_index][2]) 
        self.palette = []
        for i in range(0, len(palette_date), 3):
            self.palette.append([int(palette_date[i], 16), 
                                 int(palette_date[i+1], 16), 
                                 int(palette_date[i+2], 16)])
    def generate_pixels(self):
        pixels = []
        IHDR_data = delete_spaces_from_hex(self[0][2])

        for index in range(0 ,len(IHDR_data), self.width):
            pixels.append(IHDR_data[index:index+self.width])

        print(index)
