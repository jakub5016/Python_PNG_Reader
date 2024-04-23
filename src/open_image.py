from .picture_list import delete_spaces_from_hex, add_spaces_to_hex

PNG_SIGNATURE = "89 50 4E 47 0D 0A 1A 0A"
PNG_SIGNATURE_NO_SPACE = "89504E470D0A1A0A"
LENGTH_SIZE = 4 * 2
CHUNK_TYPE_SIZE = 4 * 2
CRC_SIZE = LENGTH_SIZE


def open_image(png_file_path):
    file = open(png_file_path, "rb")
    binary_data = file.read()

    hex_representation = " ".join(f"{byte:02X}" for byte in binary_data)
    hex_no_space = delete_spaces_from_hex(hex_representation)

    #### CHECK IF PNG
    if hex_no_space[0 : len(PNG_SIGNATURE_NO_SPACE)] != PNG_SIGNATURE_NO_SPACE:
        print("Signeture check failed")
        raise (AttributeError)
    else:
        print("Signeture checked, file is an png")

    return file, hex_no_space
