import json
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


import handleFile

# content : {"abc":"aaaa"} json
def addData(content, url_file):
    try:
        str = handleFile.readFile(url_file)    
        contents = json.loads(str)
        
        contents.update(content)
        content_data = json.dumps(contents,ensure_ascii=False)
        handleFile.wirteFile(url_file, content_data)
        return "success"
    except:
        return "error"

def deleteData(item_delete, url_file):
    try:
        str = handleFile.readFile(url_file)    
        contents = json.loads(str)
        
        contents.pop(item_delete)
        content_data = json.dumps(contents,ensure_ascii=False)
        handleFile.wirteFile(url_file, content_data)
        return "success"
    except:
        return "error"

def getData(url_file):
    str = handleFile.readFile(url_file)
    datas = json.loads(str)
    #print(datas)
    return datas
