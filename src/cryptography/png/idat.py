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


def update_crc_idat(hex_string):
    chunk_type = bytearray(b"\x49\x44\x41\x54")
    hex_digits = add_spaces_to_hex(delete_spaces_from_hex(hex_string)).split()
    chunk_data = bytearray(int(d, 16) for d in hex_digits)
    chunk_type.extend(chunk_data)
    input_string = add_spaces_to_hex(hex(zlib.crc32(chunk_type))[2:].upper())
    elements = input_string.split()
    output_string = ""

    elements = input_string.split()

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
    # Process data
    data_str = (IDAT[2].split())
    data = [int(x, 16) for x in data_str]

    print(f"CRC calculated {update_crc_idat(IDAT[2])}")

    # Create keys
    public_key, private_key = generate_keypair(8)

    # Calculate 
    encrypted_chunk = encrypt_chunk(data, public_key)
    
    # Create hex to write to chunk 
    IDAT[2] = refactor_32_bit(create_hex_chunk_from_int(encrypted_chunk))
    
    # Change length of chunk
    IDAT[0] = IDAT[0]*2 
    
    # Change width and height 
    IHDR = double_width_and_height(IHDR)

    # Update CRC
    IDAT[3] = update_crc_idat(IDAT[2])

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

    print(correct_str)
    data_str = (correct_str.split())

    data = [int(x, 16) for x in data_str]

    # Calculate 
    decrypted_chunk = decrypt_chunk(data, private_key)
    hex_string = ' '.join(format(x, '02X') for x in decrypted_chunk)

    # Create hex to write to chunk 
    IDAT[2] = hex_string
    
    # Change length of chunk
    IDAT[0] = int(IDAT[0]/2) 
    
    # Change width and height 
    IHDR = divide_in_half_width_and_height(IHDR)

    # Update CRC
    IDAT[3] = update_crc_idat(IDAT[2])

    return IDAT, IHDR