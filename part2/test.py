import png
import io
from cryptography.fernet import Fernet
import numpy as np

# Wczytaj obraz PNG
image_path = 'img.png'
with open(image_path, 'rb') as f:
    reader = png.Reader(file=f)
    width, height, pixels, metadata = reader.read_flat()

# Zaszyfruj tylko zawartość obrazu
key = Fernet.generate_key()
cipher = Fernet(key)
# Konwertuj dane na bytes przed szyfrowaniem
encrypted_pixels = cipher.encrypt(bytes(pixels))

# Zapisz zaszyfrowaną zawartość do nowego pliku PNG
encrypted_image_path = 'zaszyfrowany_obraz.png'
with open(encrypted_image_path, 'wb') as f:
    writer = png.Writer(width=width, height=height, **metadata)
    writer.write_array(f, encrypted_pixels)
