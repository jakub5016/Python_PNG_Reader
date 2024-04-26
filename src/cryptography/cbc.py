
import os


def cbc_encrypt(pixels):
    key =  os.urandom(10000)


    block_size = len(key)
    num_blocks = len(pixels) // block_size
    if len(pixels) % block_size != 0:
        num_blocks += 1
    encrypted_blocks = []

    previous_block = key  # Initialize with IV

    # Iterate over each block
    for i in range(num_blocks):
        block_start = i * block_size
        block_end = (i + 1) * block_size
        block = pixels[block_start:block_end]

        # XOR the block with the previous ciphertext block
        block_xor = [b1 ^ b2 for b1, b2 in zip(block, previous_block)]

        # Encrypt the XORed block using ECB mode
        encrypted_block = []
        for b, k in zip(block_xor, key):
            encrypted_block.append(b ^ k)
        encrypted_blocks.append(encrypted_block)

        # Update previous block for the next iteration
        previous_block = encrypted_block

    # Concatenate encrypted blocks
    ciphertext = ",".join(
        [",".join(map(str, sublist)) for sublist in encrypted_blocks]
    )
    ciphertext = ciphertext.split(",")
    ciphertext = list(map(int, ciphertext))

    return ciphertext, key



def cbc_decrypt(key, ciphertext):
    block_size = len(key)
    num_blocks = len(ciphertext) // block_size
    decrypted_blocks = []

    previous_block = key  # Initialize with IV

    # Iterate over each block
    for i in range(num_blocks):
        block_start = i * block_size
        block_end = (i + 1) * block_size
        block = ciphertext[block_start:block_end]

        # Decrypt the block using ECB mode
        decrypted_block = []
        for b, k in zip(block, key):
            decrypted_block.append(b ^ k)

        # XOR the decrypted block with the previous ciphertext block
        decrypted_block_xor = [
            b1 ^ b2 for b1, b2 in zip(decrypted_block, previous_block)
        ]

        decrypted_blocks.append(decrypted_block_xor)

        # Update previous block for the next iteration
        previous_block = block

    # Concatenate decrypted blocks
    decrypted_pixels = [item for sublist in decrypted_blocks for item in sublist]
    return decrypted_pixels