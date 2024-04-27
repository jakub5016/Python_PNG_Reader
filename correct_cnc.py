def make_crc_table():
    crc_table = [0] * 256
    for n in range(256):
        c = n
        for k in range(8):
            if c & 1:
                c = 0xedb88320 ^ (c >> 1)
            else:
                c = c >> 1
        crc_table[n] = c
    return crc_table

def update_crc(crc, buf, length, crc_table):
    c = crc
    for n in range(length):
        c = crc_table[(c ^ buf[n]) & 0xff] ^ (c >> 8)
    return c

def crc(buf, length):
    crc_table = make_crc_table()
    result = update_crc(0xffffffff, buf, length, crc_table) ^ 0xffffffff
    # Formatujemy wynik CRC jako szesnastkowy z dużymi literami, oddzielając każdy bajt spacją
    return ' '.join(f'{byte:02X}' for byte in result.to_bytes(4, byteorder='big'))
