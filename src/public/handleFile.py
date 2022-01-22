import io 
import json

def readFile(path):# đọc file 
    try:
        f_open = open(path, 'r', encoding='utf-8') # mở file và đọc 
        str = f_open.read()
        f_open.close
        return str # trả về chuỗi 
    except:
        print("err read file")
        return "error"
    

def wirteFile(path, content ): # ghi file  với path là đường dẫn và content là nội dung cần ghi ( file sẽ ghi đè lên nội dung cũ
    try:
        print(content)
        f_write = open(path, 'w+', encoding="utf8") 
        f_write.write(content)
        f_write.close
    except:
        print("err write file")
