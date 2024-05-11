import random
import math
import time

# A more robust prime-checking function
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def check_basic_prime(number):
    first_few_primes = []
    for i in range(3, 2**10, 2):
        if is_prime(i):
            first_few_primes.append(i)

    for prime in first_few_primes:
        if number % prime == 0:
            return False
        
    return True
    # for i in 

# Generate prime numbers with proper bit size
def generate_prime(bits):
    while True:
        random_number = random.randint(2**(bits-1), 2**bits - 1)
        if random_number % 2 ==0: # Number must be odd but it is bad idea to drop this random number
            random_number += 1 
        if (check_basic_prime(random_number)):
            # Perform Rabin Miller
            two_power = 2
            d = 0

            d = random_number - 1
            while (d % 2 == 0):
                d //= 2
            
            # Make it at least x times to be sure 
            is_prime_miller = True
            for i in range(20):
                if not miller_test(random_number, d):
                    is_prime_miller = False
                    break
            if is_prime_miller:
                return random_number


def miller_test(n, d):
    a = random.randint(2, n-2)
    x = pow(a, d, n)

    if x == 1 or x == n-1:
        return True
  
    while(d != n-1):
        x = (x*x) % n
        d*= 2
        if x == 1:
            return False
        
        if x == n-1:
            return True
        
    return False
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
        p = generate_prime(bits)

        q = generate_prime(bits)

        n = p * q
        phi = math.lcm(p - 1, q - 1)

    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    
    d = mod_inverse(e, phi)
    # print(f"P:  {p}\nq:     {q}\nn:     {n}\nphi:   {phi}\ne:   {e}\nd:     {d}")

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


def encrypt_chunk_cbc(chunk, iv, public_key):
    (e, n) = public_key
    arr = [pow(chunk[0] ^ iv, e, n)]
    for pixel in chunk[1:]:
        arr.append(pow(pixel ^ arr[-1], e, n))

    return arr


def decrypt_chunk_cbc(chunk, iv,private_key):
    (d, n) = private_key
    arr = [pow(chunk[0], d, n) ^iv]
    arr_2 = [pow(chunk[0], d, n) ^iv]
    for index, pixel in enumerate(chunk[1:]):
        arr.append(pow(pixel, d, n) ^ chunk[index])
        # arr[-1] = arr[-1] ^ chunk[index-1]
        arr_2.append(pow(pixel, d, n))

    return arr