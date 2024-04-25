from ..src.cryptography.rsa import encrypt_chunk, decrypt_chunk, generate_keypair

def test_decrypt():
    str = "78 9C 0D C1 07 00 08 04 10 00 C0 47 A8 8C 48 64 2B 3B 33 09 65 6B 58 65 67"
    data_str = str.split()
    data = [int(x, 16) for x in data_str]


    public_key, private_key = generate_keypair(8)
    encrypted_chunk = encrypt_chunk(data, public_key)

    decrypted_chunk = decrypt_chunk(encrypted_chunk, private_key)

    assert decrypted_chunk == data
        
