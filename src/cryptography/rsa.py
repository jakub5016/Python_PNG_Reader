import random
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
        num = random.randint(2**(bits-1), 2**bits - 1)
        if num % 2 == 0:  # Ensure the number is odd
            num += 1
        if is_prime(num):
            return num


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
    phi = 0
    while phi < 4:
        generate_time = time.time()
        p = generate_prime(bits)

        generate_time = time.time()
        q = generate_prime(bits)

        n = p * q
        phi = math.lcm(p - 1, q - 1)

    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    
    d = mod_inverse(e, phi)
    print(f"P:{p}, q:{q}, n:{n}, phi:{phi}, e:{e}, d:{d}")

    return ((e, n), (d, n))


# Encryption and decryption functions
def encrypt_chunk(chunk, public_key):
    (e, n) = public_key
    arr = []
    for pixel in chunk:
        arr.append(pow(pixel, e, n))
    return arr


def decrypt_chunk(chunk, private_key):
    (d, n) = private_key
    arr = []
    for pixel in chunk:
        arr.append(pow(pixel, d, n))
    return arr