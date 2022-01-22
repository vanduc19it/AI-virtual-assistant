import json
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


import handleFile

# content : {"abc":"aaaa"} json
def addData(content, url_file): # thêm dữ liệu
    try:
        str = handleFile.readFile(url_file)    # lấy dữ liệu ban đầu ra 
        contents = json.loads(str) # chuyển dữ liệu thành dạng json
        
        contents.update(content) # cập nhật lại dữ liệu
        content_data = json.dumps(contents,ensure_ascii=False) # chuyển dữ liệu về dạng String
        handleFile.wirteFile(url_file, content_data) # ghi file
        return "success"
    except:
        return "error"

def deleteData(item_delete, url_file):
    try:
        str = handleFile.readFile(url_file)    
        contents = json.loads(str)
        
        contents.pop(item_delete)# xóa dữ liệu giống với item_delete 
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
