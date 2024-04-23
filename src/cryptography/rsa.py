import random
import png
import math
import time


ENCRYPTED_PIXELS = []


# A more robust prime-checking function
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# Generate prime numbers with proper bit size
def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        if is_prime(n):
            return n


# Function to calculate gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# Function to generate the modular inverse
def mod_inverse(e, phi):
    # Using Extended Euclidean Algorithm
    t, newt = 0, 1
    r, newr = phi, e
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise Exception("e is not invertible")
    if t < 0:
        t += phi

    print((e * t) % phi)  # Check if mod_inverse works

    return t


# RSA keypair generation with larger bit size
def generate_keypair(bits):
    phi = 0
    while phi < 4:
        generate_time = time.time()
        p = generate_prime(bits // 2)
        print(f"Got P value = {p} in {time.time()-generate_time} s")

        generate_time = time.time()
        q = generate_prime(bits // 2)
        print(f"Got Q value = {q} in {time.time()-generate_time} s")

        n = p * q
        phi = math.lcm(p - 1, q - 1)

    print(f"Got phi value = {phi}")

    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break

    print(f"Got e = {e}")
    d = mod_inverse(e, phi)

    print(f"Got d = {d}")
    return ((e, n), (d, n))

    # return ((17, 3233), (413, 3233)) #Fixed values for debug


# Encryption and decryption functions
def encrypt_chunk(chunk, public_key):
    (e, n) = public_key
    c = pow(chunk, e, n)
    return c


def decrypt_chunk(chunk, private_key):
    (d, n) = private_key
    m = pow(chunk, d, n)
    return m


# Read PNG data
def read_png(filename):
    with open(filename, "rb") as f:
        reader = png.Reader(file=f)
        width, height, pixels, metadata = reader.read_flat()
    return width, height, pixels, metadata


# Write PNG data
def write_png(filename, width, height, metadata, data):
    with open(filename, "wb") as f:
        writer = png.Writer(width=width, height=height, **metadata)
        writer.write_array(f, data)


# Encrypting file with proper conversion
def encrypt_file(filename, public_key):
    width, height, pixels, metadata = read_png(filename)
    global ENCRYPTED_PIXELS
    ENCRYPTED_PIXELS = [encrypt_chunk(p, public_key) for p in pixels]


# Decrypting file with correct conversion
def decrypt_file(filename, private_key):
    width, height, pixels, metadata = read_png(filename)
    decrypted_pixels = []
    for p in ENCRYPTED_PIXELS:
        decrypted = decrypt_chunk(p, private_key)
        # if not (0 <= decrypted <= 255):
        #     print(decrypted)
        decrypted_pixels.append(decrypted)

    write_png("decrypted.png", width, height, metadata, decrypted_pixels)


# Example usage with increased key size
if __name__ == "__main__":
    key_size = 12  # This is a more reasonable key size for RSA

    # Generate key pair
    print("Getting key")
    public_key, private_key = generate_keypair(key_size)

    # x = encrypt_chunk(65,public_key)
    # print(f"Encrypted 65 got decrypted: {decrypt_chunk(x, private_key)}")
    generate_time = time.time()
    # Encrypt the original PNG file
    original_file = "img.png"
    encrypt_file(original_file, public_key)
    print(f"Encrypted in in {time.time()-generate_time} s")

    generate_time = time.time()
    # Decrypt the encrypted PNG file
    decrypt_file("encrypted.png", private_key)
    print(f"Decrypted in in {time.time()-generate_time} s")
