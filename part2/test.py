import FileClass

file = FileClass.File("img.png")
file.CBC_encrypt()
file.zapisz_zaszyfrowany_obraz()
file.CBC_decrypt()
file.zapisz_zdeszyfrowany_obraz()