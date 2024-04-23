import FileClass

file = FileClass.File("compres.png")
file.compress(400, 300)
file.CBC_encrypt()
file.zapisz_zaszyfrowany_obraz()
file.CBC_decrypt()
file.zapisz_zdeszyfrowany_obraz()