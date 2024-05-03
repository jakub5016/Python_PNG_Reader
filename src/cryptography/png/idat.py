from ..rsa import generate_keypair, encrypt_chunk, decrypt_chunk
from src.hex_functions import delete_spaces_from_hex, add_spaces_to_hex, refactor_32_bit
import zlib


def create_hex_chunk_from_int(int_chunk):
    hex_list = []  
    for num in int_chunk:
        hex_num = hex(num)[2:]
        width = (len(hex_num) + 3) // 4 * 4  # Calculate width to ensure full number output
        hex_list.append('{:0>{width}}'.format(hex_num, width=width))

    return ' '.join(hex_list)


def update_crc(hex_string, type=b"\x49\x44\x41\x54"):
    chunk_type = bytearray(type)
    hex_digits = hex_string.split()
    chunk_data = bytearray(int(d, 16) for d in hex_digits)
    chunk_type.extend(chunk_data)
    input_string = add_spaces_to_hex(hex(zlib.crc32(chunk_type))[2:].upper())

    elements = input_string.split()
    output_string = ""

    # Iterate through each element
    for element in elements:
        # Check if the element is a hexadecimal number
        if len(element) == 1:
            # If it's a single character, add a leading zero
            element = '0' + element

        # Add the modified element to the output string
        output_string += element + " "

    # Remove the trailing space
    output_string = output_string.strip()
    return output_string

def double_width_and_height(IHDR):
    width = delete_spaces_from_hex(IHDR[2])[0:8]
    height = delete_spaces_from_hex(IHDR[2])[8:16]

    width_dec = int(width.replace(' ', ''), 16)
    height_dec = int(height.replace(' ', ''), 16)

    new_width, new_height = width_dec*2, height_dec*2

    new_width_hex = '{:08X}'.format(new_width)
    new_height_hex = '{:08X}'.format(new_height)
    IHDR[2] = add_spaces_to_hex(new_width_hex + new_height_hex + delete_spaces_from_hex(IHDR[2])[16:])

    return IHDR

def divide_in_half_width_and_height(IHDR):
    width = delete_spaces_from_hex(IHDR[2])[0:8]
    height = delete_spaces_from_hex(IHDR[2])[8:16]

    width_dec = int(width.replace(' ', ''), 16)
    height_dec = int(height.replace(' ', ''), 16)

    new_width, new_height = int(width_dec/2), int(height_dec/2)

    new_width_hex = '{:08X}'.format(new_width)
    new_height_hex = '{:08X}'.format(new_height)

    IHDR[2] = add_spaces_to_hex(new_width_hex + new_height_hex + delete_spaces_from_hex(IHDR[2])[16:])

    return IHDR

def encrypt_idat(IDAT, IHDR):
    compressed_data_string = IDAT[2]

    # Convert the compressed data string to a bytes object
    compressed_data = bytes.fromhex(compressed_data_string.replace(" ", ""))

    # Decompress the compressed data using zlib
    decompressed_data = zlib.decompress(compressed_data)
    IDAT_decompressed = []
    for i in decompressed_data:
        IDAT_decompressed.append(hex(i)[2:])
        if len(hex(i)[2:]) == 1:
            IDAT_decompressed[-1] = "0" + IDAT_decompressed[-1]

    # Process data
    data = [""]
    number_of_zeros = 0
    for index, value in enumerate(IDAT_decompressed):
        if index % 265 == 0 and (index != 0):
            data[-1] = int(data[-1], 16)
            data.append(value)
        else:
            data[-1] += value
            
    while len(data[-1]) < 512:
        data[-1] += value
        number_of_zeros+=1
    
    data[-1] = int(data[-1], 16)

    # Create keys
    public_key, private_key = generate_keypair(2048)
    print("Generated key pair")
    # Encrypt data

    print(len(data))
    encrypted_chunk = encrypt_chunk(data, public_key)
    print(f"Data encrypted")

    to_flat =[]

    for i in encrypted_chunk:   
        to_flat.append(hex(i))
    
    to_flat_hex = ""
    for i in to_flat:
        while len(i) != 1026:
            i = i[:2] +"0"+ i[2:]      
        to_flat_hex += i[2:]


    to_flat_byte = bytes.fromhex(to_flat_hex)

    compressed_data = zlib.compress(to_flat_byte)

    encrypted_chunk = ""
    for i in compressed_data:
        if len(hex(i)[2:]) == 1:
            encrypted_chunk+= "0" + hex(i)[2:].upper()
        else:
            encrypted_chunk+= hex(i)[2:].upper()

    # Update IDAT
    IDAT[2] = encrypted_chunk

    IDAT[0] = int(len(IDAT[2])//2) 

    IDAT[2] = add_spaces_to_hex(IDAT[2])

    # Update CRC
    IDAT[3] = update_crc(IDAT[2])

    return IDAT, IHDR, public_key, private_key


def decrypt_idat(IDAT, IHDR, private_key):
    # Process data
    correct_str = ''
    space_ammout = 0
    for index, number in enumerate(IDAT[2]):
        if number == " ":
            space_ammout = (space_ammout +1)%2

            if space_ammout == 0:
                correct_str += number

        else:
            correct_str += number

    data_str = (correct_str.split())

    data = [int(x, 16) for x in data_str]

    # Calculate 
    decrypted_chunk = decrypt_chunk(data, private_key)
    hex_string = ' '.join(format(x, '02X') for x in decrypted_chunk)

    # Create hex to write to chunk 
    IDAT[2] = hex_string
    
    # Change length of chunk
    IDAT[0] = int(IDAT[0]/2) 
    
    # Update CRC
    print(IDAT[2])
    IDAT[3] = update_crc(IDAT[2])

    # Change width and height 
    IHDR = divide_in_half_width_and_height(IHDR)

    # Update CRC
    IHDR[3] = update_crc(IHDR[2], b'\x49\x48\x44\x52') 

    return IDAT, IHDR