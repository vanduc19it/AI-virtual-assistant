
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import Frame, Label, StringVar, messagebox

import constants
import handleData
import config_voice

url_command  = constants.URL_File + "command.json"

row_current = 1

global var_label_voice 
global frame
global frame_display

def updateUi( s = "hhi"):
 
    var_label_voice.set(s)
    frame.update()


def speak(audio):
    try:
        config_voice.speak(audio)
    except:
        pass

def tackcommand(entry_command):
    s  =  config_voice.get_voice(updateUi)

    len_entry = len(entry_command.get())
    entry_command.delete(0, len_entry)
    entry_command.insert(0,s)
    updateUi("hello")



def addCommand(path , command, frame):
    if path == "" or command == "":
        return messagebox.showerror( title="ERROR", message= 'type enough infor ,please !!')

    handleData.addData({''+command: path }, url_command)
    # str = handleFile.readFile(url_command)    
    # content = json.loads(str)
    
    # content.update({''+path: command})
    # content_cmd = json.dumps(content,ensure_ascii=False)
    # handleFile.wirteFile(url_command, content_cmd)
    addRowInTable(path, command, frame)


def getCommandDic():
    return handleData.getData(url_command)

def selectFile(entryfile):

    filename = askopenfilename() # open dialog to select file
    
    len_entry = len(entryfile.get())
    entryfile.delete(0, len_entry)
    entryfile.insert(0,filename)
    #entryfile.set(filename+ "")
    
def handle_btnAddCommand(entry_file, entry_command, frame):
    str_file = entry_file.get()
    str_cmd = entry_command.get()
    print(str_cmd)
    print(str_file)
    if str_cmd == "" or str_file == "":
        return messagebox.showerror( title="ERROR", message= 'Bạn cần nhập đầy đủ thông tin ,please !!')

    addCommand(str_file, str_cmd,frame)


def delete_command(item):
    def wrapper(item_delete=item):
        handleData.deleteData(item_delete, url_command)
        #return format(x)+format(y)
        global frame_display
        frame_display.update()
        return messagebox.showerror( title="Warrning", message= 'Bạn cần khởi động lại chương trình đề hoàn thành tác vụ !!')
    return wrapper


def createGui():
   
    root = tk.Tk()
    global var_label_voice  
    var_label_voice = StringVar()
    root.geometry("500x450")
    root.title("Add Command")
        
    label1 = tk.Label(root, text="Setting command")
    global frame
    frame = tk.Frame(root)

    entry_File = tk.Entry(frame)
    entry_File.grid(row=0, column=0)
    btn_file = tk.Button(frame, text="select File", command=lambda:selectFile(entry_File))
    btn_file.grid(row=0, column=1)

    #global var_label_voice 
    #var_label_voice = StringVar()

    entry_command = tk.Entry(frame)
    entry_command.grid(row=1, column=0)
    btn_command = tk.Button(frame, text="voice", command=lambda:tackcommand(entry_command))
    btn_command.grid(row=1, column=1)
    label_voice = Label(frame, textvariable = var_label_voice)
    var_label_voice.set("haha")
    label_voice.grid(row=1, column=2)
    
    btn_addCommand = tk.Button(root, text="add", command=lambda:handle_btnAddCommand( entry_File,entry_command, frame_display))


    label1.pack()
    frame.pack()
    btn_addCommand.pack()
    
    global frame_display
    frame_display = Frame(root)

    
    commands = getCommandDic()

    for column in range(3):
        text_heading = ""
        if column  == 0:
            text_heading = "command"
        elif column == 1:
            text_heading = "path"
        
        label = tk.Label(frame_display, text=text_heading, bg="white", fg="black", padx=3, pady=3)
        label.config(font=('Arial', 14))
        label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
        frame_display.grid_columnconfigure(column, weight=1)

    global row_current
    for row in commands:
       
        for column in range(3):
            if column == 0:
                label=tk.Label(frame_display,text=row,bg="black",fg="white",padx=3,pady=3)
                label.grid(row=row_current,column=column,sticky="nsew",padx=1,pady=1)
                frame_display.grid_columnconfigure(column,weight=1)
            elif column == 1:
                label=tk.Label(frame_display,text=commands[row],bg="black",fg="white",padx=3,pady=3)
                label.grid(row=row_current,column=column,sticky="nsew",padx=1,pady=1)
                frame_display.grid_columnconfigure(column,weight=1)
            elif column == 2:
                button=tk.Button(frame_display,text="Delete",bg="blue",fg="white",padx=3,pady=3, command=delete_command(row))
                button.grid(row=row_current,column=column,sticky="nsew",padx=1,pady=1)
                #button['command']=lambda btn=button:showData(btn)
                frame_display.grid_columnconfigure(column,weight=1)
        row_current = row_current + 1
        #print(row_current)

  
    frame_display.pack()

    root.mainloop()




def addRowInTable(path, command,frame_display) :
    global row_current
    for column in range(3):
        if column == 0:
            label=tk.Label(frame_display,text=command,bg="black",fg="white",padx=3,pady=3)
            label.grid(row=row_current,column=column,sticky="nsew",padx=1,pady=1)
            frame_display.grid_columnconfigure(column,weight=1)
        elif column == 1:
            label=tk.Label(frame_display,text=path,bg="black",fg="white",padx=3,pady=3)
            label.grid(row=row_current,column=column,sticky="nsew",padx=1,pady=1)
            frame_display.grid_columnconfigure(column,weight=1)
        elif column == 2:
            button=tk.Button(frame_display,text="Delete",bg="blue",fg="white",padx=3,pady=3)
            button.grid(row=row_current,column=column,sticky="nsew",padx=1,pady=1)
            #button['command']=lambda btn=button:showData(btn)
            frame_display.grid_columnconfigure(column,weight=1)
    row_current = row_current + 1
    frame_display.update()

#createGui()

#getCommandDic()
# addCommand("ahi3i", "ahaha2")
#updateUi("helo")
