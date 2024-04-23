import base64

import png
import os
from PIL import Image
from PIL import Image



class File:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'rb') as f:
            reader = png.Reader(file=f)
            self.width, self.height, self.pixels, self.metadata = reader.read_flat()
        self.key = os.urandom(10000)
        self.key = os.urandom(10000)
        self.ciphertext = None
        self.decrypted_pixels = None
        self.compress_pixels = None
        self.compress_pixels = None
    def ECB_encrypt(self):
        #print(self.pixels)
        block_size = len(self.key)
        num_blocks = len(self.pixels) // block_size
        if len(self.pixels) % block_size != 0:
            num_blocks += 1
        encrypted_blocks = []

        # Iterate over each block
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            block = self.pixels[block_start:block_end]

            # XOR the block with the key
            encrypted_block = []
            for b, k in zip(block, self.key):
                encrypted_block.append(b ^ k) # ^ Xor operation
            encrypted_blocks.append(encrypted_block)

        # Concatenate encrypted blocks
        #print(encrypted_blocks)
        self.ciphertext = ','.join([','.join(map(str, sublist)) for sublist in encrypted_blocks])
        self.ciphertext = self.ciphertext.split(",")
        self.ciphertext = list(map(int, self.ciphertext))
    def ECB_decrypt(self):
        block_size = len(self.key)
        num_blocks = len(self.ciphertext) // block_size
        decrypted_blocks = []

        # Iterate over each block
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            block = self.ciphertext[block_start:block_end]

            # XOR the block with the key
            decrypted_block = []
            for b, k in zip(block, self.key):
                decrypted_block.append(b ^ k)
            decrypted_blocks.append(decrypted_block)

        # Concatenate decrypted blocks
        decrypted_pixels = [item for sublist in decrypted_blocks for item in sublist]
        self.decrypted_pixels = decrypted_pixels
        #print(self.decrypted_pixels)

    def CBC_encrypt(self):
        block_size = len(self.key)
        num_blocks = len(self.pixels) // block_size
        if len(self.pixels) % block_size != 0:
            num_blocks += 1
        encrypted_blocks = []

        previous_block = self.key  # Initialize with IV

        # Iterate over each block
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            block = self.pixels[block_start:block_end]

            # XOR the block with the previous ciphertext block
            block_xor = [b1 ^ b2 for b1, b2 in zip(block, previous_block)]

            # Encrypt the XORed block using ECB mode
            encrypted_block = []
            for b, k in zip(block_xor, self.key):
                encrypted_block.append(b ^ k)
            encrypted_blocks.append(encrypted_block)

            # Update previous block for the next iteration
            previous_block = encrypted_block

        # Concatenate encrypted blocks
        self.ciphertext = ','.join([','.join(map(str, sublist)) for sublist in encrypted_blocks])
        self.ciphertext = self.ciphertext.split(",")
        self.ciphertext = list(map(int, self.ciphertext))

    def CBC_decrypt(self):
        block_size = len(self.key)
        num_blocks = len(self.ciphertext) // block_size
        decrypted_blocks = []

        previous_block = self.key  # Initialize with IV

        # Iterate over each block
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            block = self.ciphertext[block_start:block_end]

            # Decrypt the block using ECB mode
            decrypted_block = []
            for b, k in zip(block, self.key):
                decrypted_block.append(b ^ k)

            # XOR the decrypted block with the previous ciphertext block
            decrypted_block_xor = [b1 ^ b2 for b1, b2 in zip(decrypted_block, previous_block)]

            decrypted_blocks.append(decrypted_block_xor)

            # Update previous block for the next iteration
            previous_block = block

        # Concatenate decrypted blocks
        decrypted_pixels = [item for sublist in decrypted_blocks for item in sublist]
        self.decrypted_pixels = decrypted_pixels
    def CBC_encrypt(self):
        block_size = len(self.key)
        num_blocks = len(self.pixels) // block_size
        if len(self.pixels) % block_size != 0:
            num_blocks += 1
        encrypted_blocks = []

        previous_block = self.key  # Initialize with IV

        # Iterate over each block
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            block = self.pixels[block_start:block_end]

            # XOR the block with the previous ciphertext block
            block_xor = [b1 ^ b2 for b1, b2 in zip(block, previous_block)]

            # Encrypt the XORed block using ECB mode
            encrypted_block = []
            for b, k in zip(block_xor, self.key):
                encrypted_block.append(b ^ k)
            encrypted_blocks.append(encrypted_block)

            # Update previous block for the next iteration
            previous_block = encrypted_block

        # Concatenate encrypted blocks
        self.ciphertext = ','.join([','.join(map(str, sublist)) for sublist in encrypted_blocks])
        self.ciphertext = self.ciphertext.split(",")
        self.ciphertext = list(map(int, self.ciphertext))

    def CBC_decrypt(self):
        block_size = len(self.key)
        num_blocks = len(self.ciphertext) // block_size
        decrypted_blocks = []

        previous_block = self.key  # Initialize with IV

        # Iterate over each block
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = (i + 1) * block_size
            block = self.ciphertext[block_start:block_end]

            # Decrypt the block using ECB mode
            decrypted_block = []
            for b, k in zip(block, self.key):
                decrypted_block.append(b ^ k)

            # XOR the decrypted block with the previous ciphertext block
            decrypted_block_xor = [b1 ^ b2 for b1, b2 in zip(decrypted_block, previous_block)]

            decrypted_blocks.append(decrypted_block_xor)

            # Update previous block for the next iteration
            previous_block = block

        # Concatenate decrypted blocks
        decrypted_pixels = [item for sublist in decrypted_blocks for item in sublist]
        self.decrypted_pixels = decrypted_pixels
    def zapisz_zaszyfrowany_obraz(self):
        encrypted_image_path = 'zaszyfrowany_obraz.png'
        with open(encrypted_image_path, 'wb') as f:
            writer = png.Writer(width=self.width, height=self.height, **self.metadata)
            writer.write_array(f, self.ciphertext)
    def zapisz_zdeszyfrowany_obraz(self):
        decrypted_image_path = 'odszyfrowany_obraz.png'
        with open(decrypted_image_path, 'wb') as f:
            writer = png.Writer(width=self.width, height=self.height, **self.metadata)
            writer.write_array(f, self.decrypted_pixels)
    def compress(self,width,height,quality=85):
        with Image.open(self.filename) as img:
            # Resize the image
            img = img.resize((width, height), resample=Image.LANCZOS)
            # Compress the image
            img.save("compres.png", quality=quality, optimize=True)