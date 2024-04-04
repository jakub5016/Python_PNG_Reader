from src.hexFunctions import delete_spaces_from_hex

def print_chroma(picture_arr):
    val = delete_spaces_from_hex(picture_arr[picture_arr.get_chunk_index("cHRM")][2])
    white_point = [int(val[0:8],16)/100000, int(val[8:16],16)/100000]
    red = [int(val[16:24],16)/100000, int(val[24:32],16)/100000]
    green = [int(val[32:40],16)/100000, int(val[40:48],16)/100000]
    blue = [int(val[48:56],16)/100000, int(val[56:64],16)/100000]
    
    print("White point X,Y " + str(white_point))
    print("Red X,Y " + str(red))
    print("Green X,Y " + str(green))
    print("Blue X,Y " + str(blue))