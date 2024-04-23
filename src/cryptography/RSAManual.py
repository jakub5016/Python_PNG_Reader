import png
from cryptography.hazmat.primitives.asymmetric import rsa
import rsa
from PIL import Image

# Generowanie kluczy RSA
(public_key, private_key) = rsa.newkeys(2048)


def RSA_encryption(txt):
    result = []
    for n in range(0, len(txt), 245):
        part = txt[n : n + 245]
        result.append(rsa.encrypt(part, public_key))
    return b"".join(result)


def RSA_decryption(RSA_content):
    result = []
    for n in range(0, len(RSA_content), 256):
        part = RSA_content[n : n + 256]
        result.append(rsa.decrypt(part, private_key))
    return b"".join(result)


image_path = "img.png"
with open(image_path, "rb") as f:
    reader = png.Reader(file=f)
    width, height, pixels, metadata = reader.read_flat()
crypted_data = RSA_encryption(pixels)
# Zapisz zaszyfrowaną zawartość do nowego pliku PNG
encrypted_image_path = "zaszyfrowany_obraz.png"
with open(encrypted_image_path, "wb") as f:
    writer = png.Writer(width=width, height=height, **metadata)
    writer.write_array(f, crypted_data)

decrypted_data = RSA_decryption(crypted_data)
decrypted_image_path = "odszyfrowany_obraz.png"
with open(decrypted_image_path, "wb") as f:
    writer = png.Writer(width=width, height=height, **metadata)
    writer.write_array(f, decrypted_data)
imZa = Image.open("zaszyfrowany_obraz.png")
imZa.show()
imZde = Image.open("odszyfrowany_obraz.png")
imZde.show()
