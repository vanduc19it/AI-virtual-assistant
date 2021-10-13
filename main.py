from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import playsound
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import json
import re
import ctypes
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
import random
import smtplib
import roman
from PIL import Image




numbers = {'hundred':100, 'thousand':1000, 'lakh':100000}
a = {'name':'your email'}
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def sendemail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('email id', 'password') 
    server.sendmail('email id', to, content)
    server.close()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        var.set("Good morning sir !") 
        window.update()
        speak("Chào buổi sáng bạn Đức. Chúc bạn một ngày tốt lành !")
    elif hour >= 12 and hour <= 18:
        var.set("Good afternoon sir !")
        window.update()
        speak("Chào buổi chiều bạn Đức. Bạn đã dự định gì cho chiều nay chưa !")
    else:
        var.set("Good night sir !")
        window.update()
        speak("Chào buổi tối bạn đức. Bạn đã ăn tối chưa nhỉ !")
    speak("Tôi là trợ lí ảo. Tôi có thể giúp gì cho bạn") 

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()
        print("Trợ lí ảo: Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        var.set("Recognizing...")
        window.update()
        print("Trợ lí ảo: Recognizing...")
        query = r.recognize_google(audio, language='vi-VN')
    except Exception as e:
        return "None"
    var1.set(query)
    window.update()
    return query

def play():
    btn2['state'] = 'disabled'
    btn0['state'] = 'disabled'
    btn1.configure(bg = 'orange')
    wishme()
    while True:
        btn1.configure(bg = 'orange')
        query = takeCommand().lower()
        if 'exit' in query:
            var.set("Bye sir")
            btn1.configure(bg = '#5C85FB')
            btn2['state'] = 'normal'
            btn0['state'] = 'normal'
            window.update()
            speak("Tạm biệt bạn. Hẹn gặp lại bạn sau !")
            break

        elif 'wikipedia' in query:
            if 'mở wikipedia' in query:
                webbrowser.open('wikipedia.com')
            else:
                try:
                    speak("searching wikipedia")
                    query = query.replace("according to wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia")
                    var.set(results)
                    window.update()
                    speak(results)
                except Exception as e:
                    var.set('Xin lỗi bạn, tôi không tìm thấy bất kì kết quả nào !')
                    window.update()
                    speak('Xin lỗi bạn, tôi không tìm thấy bất kì kết quả nào !')

        elif 'mở youtube' in query:
            var.set('Đang mở Youtube... !')
            window.update()
            speak('Chờ một chút, mình đang mở Youtube')
            webbrowser.open("youtube.com")

        elif 'open course error' in query:
            var.set('opening course era')
            window.update()
            speak('opening course era')
            webbrowser.open("coursera.com")

        elif 'mở google' in query:
            var.set('Đang mở Google... !')
            window.update()
            speak('Chờ một chút, mình đang mở google')
            webbrowser.open("google.com")

        elif 'chào bạn' in query:
            var.set('Chào bạn nha. Tôi có thể giúp gì cho bạn !')
            window.update()
            speak("Chào bạn nha. Tôi có thể giúp gì cho bạn !")
			
        elif 'mở stackoverflow' in query:
            var.set('Đang mở Stackoverflow... !')
            window.update()
            speak('Chờ một chút, mình đang mở stackoverflow cho bạn đây !')
            webbrowser.open('stackoverflow.com')

        elif ('nghe nhạc' in query) or ('change music' in query):
            var.set('Here are your favorites')
            window.update()
            speak('Here are your favorites')
            music_dir = 'D:\My Music\Favourites' # Enter the Path of Music Library
            songs = os.listdir(music_dir)
            n = random.randint(0,27)
            os.startfile(os.path.join(music_dir, songs[n]))

        elif 'giờ' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            var.set("Bây giờ là %s" % strtime)
            window.update()
            speak("Bây giờ là %s" %strtime)

        elif 'ngày' in query:
            strdate = datetime.datetime.today().strftime("%d %m %y")
            var.set("Hôm nay là ngày %s" %strdate)
            window.update()
            speak("Hôm nay là ngày %s" %strdate) 

        elif 'thank you' in query or 'cảm ơn' in query:
            var.set("Mình rất hân hạnh !!!")
            window.update()
            speak("Mình rất hân hạnh khi được phục vụ cho bạn. Có việc gì cứ nói mình giúp cho nhé !! ")

        elif 'can you do for me' in query:
            var.set('I can do multiple tasks for you sir. tell me whatever you want to perform sir')
            window.update()
            speak('I can do multiple tasks for you sir. tell me whatever you want to perform sir')

        elif 'tuổi' in query:
            var.set("Tôi năm nay hơn 70 tuổi rồi...")
            window.update()
            speak("Tôi năm nay hơn 70 tuổi rồi mà tôi chưa bao giờ thấy cái trường hợp nào như này cả !")

        elif 'open media player' in query:
            var.set("opening VLC media Player")
            window.update()
            speak("opening V L C media player")
            path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" 
            os.startfile(path)

        elif 'tên' in query:
            var.set("Tên của tôi là Jarvis thưa ngài")
            window.update()
            speak('Tên của tôi là Jarvis thưa ngài')

        elif 'tạo ra bạn' in query:
            var.set('Đó là bạn đức đẹp trai vip pro nha !')
            window.update()
            speak('Đó là bạn đức đẹp trai vip pro nha !')

        elif 'nói xin chào' in query:
            var.set('Xin chào tất cả mọi người. Mình tên là Jarvis')
            window.update()
            speak('Xin chào tất cả mọi người. Mình tên là Jarvis')

        elif 'open pycharm' in query:
            var.set("Openong Pycharm")
            window.update()
            speak("Opening Pycharm")
            path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2018.3.2\\bin\\pycharm64.exe" #Enter the correct Path according to your system
            os.startfile(path)

        elif 'mở chrome' in query:
            var.set("Đang mở Google Chrome...")
            window.update()
            speak("chờ một chút, mình đang mở Google Chrome")
            path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(path)

        elif 'email to me' in query:
            try:
                var.set("What should I say")
                window.update()
                speak('what should I say')
                content = takeCommand()
                to = a['name']
                sendemail(to, content)
                var.set('Email đã được gửi !')
                window.update()
                speak('Email đã được gửi !')

            except Exception as e:
                print(e)
                var.set("Xin lỗi bạn! Tôi không thể gửi email này !")
                window.update()
                speak('Xin lỗi bạn! Tôi không thể gửi email này')
		
        elif "mở python" in query:
            var.set("Opening Python Ide")
            window.update()
            speak('opening python Ide')
            os.startfile('C:\\Users\\mridu\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Python 3.7\\IDLE (Python 3.7 64-bit)') 

        elif 'open anaconda' in query:
            var.set('Opening Anaconda')
            window.update()
            speak('opening anaconda')
            os.startfile("C:\\Users\\mridu\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Anaconda3 (64-bit)\\Anaconda Navigator") 

        elif 'calculation' in query:
            sum = 0
            var.set('Yes Sir, please tell the numbers')
            window.update()
            speak('Yes Sir, please tell the numbers')
            while True:
                query = takeCommand()
                if 'answer' in query:
                    var.set('here is result'+str(sum))
                    window.update()
                    speak('here is result'+str(sum))
                    break
                elif query:
                    if query == 'x**':
                        digit = 30
                    elif query in numbers:
                        digit = numbers[query]
                    elif 'x' in query:
                        query = query.upper()
                        digit = roman.fromRoman(query)
                    elif query.isdigit():
                        digit = int(query)
                    else:
                        digit = 0
                    sum += digit
      
           

        elif 'chụp ảnh' in query:
            stream = cv2.VideoCapture(0)
            grabbed, frame = stream.read()
            if grabbed:
                cv2.imshow('pic', frame)
                cv2.imwrite('pic.jpg',frame)
            stream.release()

        elif 'quay video' in query:
            cap = cv2.VideoCapture(0)
            out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret:
                    
                    out.write(frame)

                    cv2.imshow('frame',frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
       
                

def update(ind):
    frame = frames[(ind)%100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)

label2 = Label(window, textvariable = var1, bg = '#FAB60C')
label2.config(font=("Courier", 20))
var1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable = var, bg = '#ADD8E6')
label1.config(font=("Courier", 20))
var.set('Welcome')
label1.pack()

frames = [PhotoImage(file='Assistant.gif',format = 'gif -index %i' %(i)) for i in range(100)]
window.title('JARVIS')

label = Label(window, width = 500, height = 500)
label.pack()
window.after(0, update, 0)

btn0 = Button(text = 'WISH ME',width = 20, command = wishme, bg = '#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text = 'PLAY',width = 20,command = play, bg = '#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text = 'EXIT',width = 20, command = window.destroy, bg = '#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()


window.mainloop()