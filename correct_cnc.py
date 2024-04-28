import sys
import os
import struct
import binascii

CHUNK_START_OFFSET = 8
END_CHUNK = b'IEND'

class PNGChunk:
    def __init__(self, offset, length, chunk_type, data, crc):
        self.offset = offset
        self.length = length
        self.type = chunk_type
        self.data = data
        self.crc = crc

    def __str__(self):
        return f"{self.type.decode()}@{self.offset:x} - {self.crc:X} - Valid CRC? {self.is_crc_valid()}"

    def bytes(self):
        return self.type + self.data

    def is_crc_valid(self):
        return self.crc == self.calculate_crc()

    def calculate_crc(self):
        crc = binascii.crc32(self.bytes())
        return crc & 0xFFFFFFFF

    def crc_offset(self):
        return self.offset + 8 + self.length

def read_chunks(file_path):
    chunks = []

    with open(file_path, 'rb') as file:
        file.seek(CHUNK_START_OFFSET)
        while True:
            offset = file.tell()
            length_bytes = file.read(4)
            if not length_bytes:
                break

            length = struct.unpack('>I', length_bytes)[0]
            chunk_type = file.read(4)
            data = file.read(length)
            crc = struct.unpack('>I', file.read(4))[0]

            chunk = PNGChunk(offset, length, chunk_type, data, crc)
            chunks.append(chunk)

            if chunk.type == END_CHUNK:
                break

    return chunks

def fix_crc(file_path):
    chunks = read_chunks(file_path)

    with open(file_path, 'r+b') as file:
        for chunk in chunks:
            if not chunk.is_crc_valid():
                file.seek(chunk.crc_offset())
                correct_crc = chunk.calculate_crc()
                file.write(struct.pack('>I', correct_crc))
                print("Corrected CRC")


def main():
    if len(sys.argv) != 2:
        print("Usage: python fix_png_crc.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found")
        sys.exit(1)

    fix_crc(file_path)

if __name__ == "__main__":
    main()
