from PIL import Image

import FileClass



file = FileClass.File("img.png")
file.ECB_encrypt()
file.zapisz_zaszyfrowany_obraz()
file.ECB_decrypt()
file.zapisz_zdeszyfrowany_obraz()
imZa = Image.open("zaszyfrowany_obraz.png")
imZa.show()
imZde = Image.open("odszyfrowany_obraz.png")
imZde.show()