from .hexFunctions import delete_spaces_from_hex


class iTExItem:
    keyword = ""
    compression_flag = ""
    compression_method = ""
    language_tag =""
    translated_keywoard = ""
    text = ""

    def __str__(self) -> str:
        return(f"Keywoard = {self.keyword} "+
              f"\nCompression flag = {self.compression_flag}"+
              f"\nCompression method = {self.compression_method}" +
              f"\nLanguage tag = {self.language_tag}" +
              f"\nTranslated keywoard = {self.translated_keywoard}" +
              f"\nText = {self.text}\n")
KEYWORDS = ["Title", 
            "Author", 
            "Description", 
            "Copyright", 
            "Creation Time", 
            "Software", 
            "Disclaimer", 
            "Warning", 
            "Source", 
            "Comment"]

def get_text(picture_arr):
    key_value = []
    for index, item in enumerate(picture_arr):
        if item[1] == "iTXt":
            hex_values = delete_spaces_from_hex(picture_arr[index][2])
            result_string = ''.join([chr(int(hex_values[i:i+2], 16)) for i in range(0, len(hex_values), 2)])
            for key in KEYWORDS:
                if (result_string[0:len(key)] == key):
                    item = iTExItem()
                    item.keyword = key
                    if result_string[len(key)] != "\x00": break
                    
                    item.compression_flag = result_string[len(key)+1] 
                    item.compression_method = result_string[len(key)+2] 
                    
                    counter = 3
                    while(result_string[len(key)+counter]!="\00"):
                        item.language_tag += result_string[len(key)+counter]     
                        counter+=1                   
                    counter+=1
                    while(result_string[len(key)+counter]!="\00"):
                        item.translated_keywoard += result_string[len(key)+counter]     
                        counter+=1  
                    counter+=1
                    item.text = result_string[len(key)+counter:]
                    
                    key_value.append(item)
        
        result_string = ''


    for i in key_value:
        print(i)