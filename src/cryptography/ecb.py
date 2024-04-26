import os

def ecb_encrypt(pixels):
    key =  os.urandom(10000)

    block_size = len(key)
    num_blocks = len(pixels) // block_size
    if len(pixels) % block_size != 0:
        num_blocks += 1
    encrypted_blocks = []

    # Iterate over each block
    for i in range(num_blocks):
        block_start = i * block_size
        block_end = (i + 1) * block_size
        block = pixels[block_start:block_end]

        # XOR the block with the key
        encrypted_block = []
        for b, k in zip(block, key):
            encrypted_block.append(b ^ k)  # ^ Xor operation
        encrypted_blocks.append(encrypted_block)

    # Concatenate encrypted blocks
    # print(encrypted_blocks)
    ciphertext = ",".join(
        [",".join(map(str, sublist)) for sublist in encrypted_blocks]
    )
    ciphertext = ciphertext.split(",")
    ciphertext = list(map(int, ciphertext))

    return ciphertext, key

def ecb_decrypt(key, ciphertext):
    block_size = len(key)
    num_blocks = len(ciphertext) // block_size
    decrypted_blocks = []

    # Iterate over each block
    for i in range(num_blocks):
        block_start = i * block_size
        block_end = (i + 1) * block_size
        block = ciphertext[block_start:block_end]

        # XOR the block with the key
        decrypted_block = []
        for b, k in zip(block, key):
            decrypted_block.append(b ^ k)
        decrypted_blocks.append(decrypted_block)

    # Concatenate decrypted blocks
    decrypted_pixels = [item for sublist in decrypted_blocks for item in sublist]
    return decrypted_pixels