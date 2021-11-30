import io 
import json

def readFile(path):
    try:
        f_open = open(path, 'r', encoding='utf-8')
        str = f_open.read()
        f_open.close
        return str
    except:
        print("err read file")
        return "error"
    

def wirteFile(path, content ):
    try:
        print(content)
        f_write = open(path, 'w+', encoding="utf8")
        f_write.write(content)
        f_write.close
    except:
        print("err write file")
