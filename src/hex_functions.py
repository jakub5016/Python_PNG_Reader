def add_spaces_to_hex(hex):
    hex_with_spaces = ""
    for index, i in enumerate(hex):
        if (index % 2 == 0) and (index != 0):
            hex_with_spaces += " "
        hex_with_spaces += i
    return hex_with_spaces


def delete_spaces_from_hex(hex):
    hex_no_space = ""
    for i in hex:
        if i != " ":
            hex_no_space += i
    return hex_no_space


def refactor_32_bit(hex):
    return(add_spaces_to_hex(delete_spaces_from_hex(hex)))