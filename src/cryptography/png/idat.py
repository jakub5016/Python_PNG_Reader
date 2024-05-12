from ..rsa import generate_keypair, encrypt_chunk, decrypt_chunk, encrypt_chunk_cbc, decrypt_chunk_cbc
from src.hex_functions import delete_spaces_from_hex, add_spaces_to_hex, refactor_32_bit
import zlib
import time
import random
KEY_LENGHT = 4096


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

def encrypt_idat(IDAT, width, private_key=None, public_key=None, type="ECB"):
    # Convert the compressed data string to a bytes object
    compressed_data = bytes.fromhex(IDAT[2].replace(" ", ""))

    # Decompress the compressed data using zlib
    decompressed_data = zlib.decompress(compressed_data) # Bytes
    IDAT_decompressed = [] # Hex val arr
    for i in decompressed_data:
        IDAT_decompressed.append(hex(i)[2:])
        if len(hex(i)[2:]) == 1:
            IDAT_decompressed[-1] = "0" + IDAT_decompressed[-1]

    # Process data
    # Int values from concentrated hex 
    # We want to create big hex to convert it to bit int
    data = [""] 
    number_of_zeros = 0
    for index, value in enumerate(IDAT_decompressed):
        if index % (KEY_LENGHT/8) == 0 and (index != 0):
            data[-1] = int(data[-1], 16)
            data.append(value)
        else:
            data[-1] += value
    
    while len(data[-1]) < (KEY_LENGHT/4):
        data[-1] += '0'
        number_of_zeros+=1
    
    data[-1] = int(data[-1], 16)

    # Create keys
    if (public_key == None) and (private_key == None):
        stat_time = time.time()
        public_key, private_key = generate_keypair(KEY_LENGHT)
        print(f"Generated key pair  in time {time.time() - stat_time} s")

    else:
        print("It seems you have pregenerated key values in keys.txt file.\nI've selected one")
    # Encrypt data
    print(f"Ammout of chunks to encrypt: {len(data)}")    
    if type == "ECB":
        stat_time = time.time()
        encrypted_chunk = encrypt_chunk(data, public_key)
    else:
        iv = random.randbytes(256)
        iv = int.from_bytes(iv, "big")
        stat_time = time.time()
        encrypted_chunk = encrypt_chunk_cbc(data, iv , public_key)
    
    print(f"Data encrypted in time: {time.time() - stat_time} s")

    # Preapare data to compression
    to_flat =[]
    for i in encrypted_chunk:   
        to_flat.append(hex(i))
    
    
    to_flat_hex = "" #<-
    for i in to_flat:
        while len(i) != (KEY_LENGHT/2) +2: # Fixed size of one batch to convert 
            i = i[:2] +"0"+ i[2:]      
        to_flat_hex += i[2:]

    # Apply filter to every row
    to_flat_hex_filter = "00"
    for i in range(0, len(to_flat_hex), width*2):
        to_flat_hex_filter += to_flat_hex[i:i+(width*2)] +"00"

    # Convert to bytes
    to_flat_byte = bytes.fromhex(to_flat_hex_filter)
    # Compress
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

    if type == "ECB":
        return IDAT, public_key, private_key, number_of_zeros
    else:
        return IDAT, public_key, private_key, number_of_zeros, iv

def decrypt_idat(IDAT, width, private_key, padding=0, iv=-1):
    # Process data
    compressed_data = bytes.fromhex(IDAT[2].replace(" ", ""))

    # Decompress the compressed data using zlib
    decompressed_data = zlib.decompress(compressed_data) # Bytes
    hex_val = hex_from_byte(decompressed_data)
    # Remove filters
    hex_val = hex_val[2:]
    hex_val_no_filter = ''
    for i in range(0, len(hex_val), (2*width) +2 ):
        hex_val_no_filter += hex_val[i:i+(2*width)]

    # We know that every batch have 1026 size (including "0x" so it will be 1024)
    batches =[""]
    for index, item in enumerate(hex_val_no_filter):
        if (index % (KEY_LENGHT/2) == 0) and (index !=0):
            batches.append(item)
        else:
            batches[-1] += item

    # Now we have to convert it to int to run decrypt script
    data =[]
    for batch in batches:
        data.append(int(batch, 16))

    # Decrypt data
    if iv != -1:
        decrypted_chunk = decrypt_chunk_cbc(data, iv, private_key)
    else:
        decrypted_chunk = decrypt_chunk(data, private_key)
    
    print("Succesfully decrypted")
    hex_string = ''
    for decrypded_int in decrypted_chunk:
        if len(hex(decrypded_int)[2:].upper()) < 1024:
            hex_string+= "0" * (1024 - len(hex(decrypded_int)[2:].upper()))

        hex_string += hex(decrypded_int)[2:].upper()

    # Convert to bytes and compress
    to_flat_byte = bytes.fromhex(hex_string[:len(hex_string) - padding])
    compressed_data = zlib.compress(to_flat_byte)
    decrypted_chunk = add_spaces_to_hex(hex_from_byte(compressed_data))

    # Create hex to write to chunk 
    IDAT[2] = decrypted_chunk
    
    # Change length of chunk
    IDAT[0] = int(IDAT[0]/2) 
    
    # Update CRC
    IDAT[3] = update_crc(IDAT[2])

    return IDAT


def hex_from_byte(bytes):
    arr= ""
    for val in bytes:
        if len(hex(val)[2:]) == 1:
            arr += ("0" + hex(val)[2:]).upper()
        else:
            arr += (hex(val)[2:]).upper()

    return arr