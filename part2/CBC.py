from PIL import Image

import FileClass



file = FileClass.File("img.png")
file.CBC_encrypt()
file.zapisz_zaszyfrowany_obraz()
file.CBC_decrypt()
file.zapisz_zdeszyfrowany_obraz()
imZa = Image.open("zaszyfrowany_obraz.png")
imZa.show()
imZde = Image.open("zdeszyfrowany_obraz.png")
imZde.show()