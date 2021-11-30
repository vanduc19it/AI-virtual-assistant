import tkinter as tk
from tkinter import messagebox


import addCommand
import addInforUser

def addPassword(entryPass):
    print("chức năng thêm pass  ")

def handleSaveUserName(rename):
    # username = entry_name.get()
    # if username == '':
    #     return messagebox.showerror( title="ERROR", message= 'please type your username!!')
    
    addInforUser.addUserName(rename)
    #current_username.set(rename)
    
    # return messagebox.showinfo(title="Success",message= 'save success')


def handleSavePass(passw):
    if passw == "":
        return messagebox.showerror( title="ERROR", message= 'please type your username!!')
    else: 
        addInforUser.addPass(passw)
    #current_username.set(rename)
    
    return messagebox.showinfo(title="Success",message= 'save success')

def createGuiSetting():
    root = tk.Tk()
    root.geometry("500x450")
    root.title("Setting ")

    frame_InputName = tk.Frame(root,pady=20)
    label_name = tk.Label(frame_InputName, text="Type your name:",font=("Courier", 10)) 
    label_name.grid(row=0,column=0)
    entry_name = tk.Entry(frame_InputName, width = 30 )
    entry_name.grid(row=0, column=1)

    btn_saveName = tk.Button(frame_InputName,text = 'save name', command=lambda:handleSaveUserName(entry_name.get()), font=("Courier", 10))
    btn_saveName.grid(column=2, row=0)
    frame_InputName.pack()

    frame_pass = tk.Frame(root, pady=10)
    lbl_pass =tk.Label(frame_pass, text="type your password", font=("Courier", 10))
    lbl_pass.grid(column=0, row=0)
    entry_pass = tk.Entry(frame_pass)
    entry_pass.grid(column=1, row=0)
    btn_save_pass = tk.Button(frame_pass, text="Save pass",command=lambda:handleSavePass(entry_pass.get()), font=("Courier", 10))
    btn_save_pass.grid(column=2, row=0)
    frame_pass.pack()

    
    btn_setting = tk.Button(text = 'add Command',width = 20, command = addCommand.createGui, bg = '#5C85FB', padx=10)
    btn_setting.config(font=("Courier", 12))
    btn_setting.pack()

    
    root.mainloop()


createGuiSetting()
