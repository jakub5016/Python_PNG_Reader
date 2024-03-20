from .hexFunctions import delete_spaces_from_hex

def get_text(picture_arr):
    for index, item in enumerate(picture_arr):
        if item[1] == "iTXt":
            hex_values = delete_spaces_from_hex(picture_arr[index][2])
            result_string = ''.join([chr(int(hex_values[i:i+2], 16)) for i in range(0, len(hex_values), 2)])
            print(result_string)