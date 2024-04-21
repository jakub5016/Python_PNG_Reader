import random
import png


# A more robust prime-checking function
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
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
    return t


# RSA keypair generation with larger bit size
def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))


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
    with open(filename, 'rb') as f:
        reader = png.Reader(file=f)
        width, height, pixels, metadata = reader.read_flat()
    return width, height, pixels, metadata


# Write PNG data
def write_png(filename, width, height, metadata, data):
    with open(filename, 'wb') as f:
        writer = png.Writer(width=width, height=height, **metadata)
        writer.write_array(f, data)


# Encrypting file with proper conversion
def encrypt_file(filename, public_key):
    width, height, pixels, metadata = read_png(filename)
    encrypted_pixels = [encrypt_chunk(p, public_key) % 256 for p in pixels]
    write_png("encrypted.png", width, height, metadata, encrypted_pixels)


# Decrypting file with correct conversion
def decrypt_file(filename, private_key):
    width, height, pixels, metadata = read_png(filename)
    decrypted_pixels = [decrypt_chunk(p, private_key) % 256 for p in pixels]
    write_png("decrypted.png", width, height, metadata, decrypted_pixels)


# Example usage with increased key size
if __name__ == '__main__':
    key_size = 1024  # This is a more reasonable key size for RSA

    # Generate key pair
    public_key, private_key = generate_keypair(key_size)

    # Encrypt the original PNG file
    original_file = "img.png"
    encrypt_file(original_file, public_key)

    # Decrypt the encrypted PNG file
    decrypt_file("encrypted.png", private_key)
