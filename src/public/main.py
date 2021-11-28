from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import playsound
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import requests
import os, sys
import json
import re
import time
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
from tkinter import messagebox
import threading


import constants 
import addCommand



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

current_username = StringVar()

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


def send_email(text):
    speak("Bạn gửi email cho ai vậy nhỉ ?")
    recipient = takeCommand()
    if "Đức" in recipient:
        speak("Nói cho tôi nội dung email bạn muốn gửi ! ... >")
        content = takeCommand()
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login("vanduc19it@gmail.com", "vanduc190401")
        mail.sendmail("vanduc19it@gmail.com",
                      "cvduc.19it1@vku.udn.vn", str(content).encode("utf-8"))
        mail.close()
        speak("Email của bạn đã được gửi. Bạn vui lòng kiểm tra lại giúp !  >")
    else:
        speak("Tôi không hiểu bạn muốn gửi email cho ai  ...")

def wishme():  
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        var.set("Good morning sir !") 
        window.update()
        speak("Chào buổi sáng bạn " + current_username.get() +". Chúc bạn một ngày tốt lành !")
    elif hour >= 12 and hour <= 18:
        var.set("Good afternoon sir !")
        window.update()
        speak("Chào buổi chiều bạn " + current_username.get() +". Bạn đã dự định gì cho chiều nay chưa !")
    else:
        var.set("Good night sir !")
        window.update()
        speak("Chào buổi tối bạn " + current_username.get() +". Bạn đã ăn tối chưa nhỉ !")
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

def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    # Đường dẫn trang web để lấy dữ liệu về thời tiết
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    # lưu tên thành phố vào biến city
    city = takeCommand()
    # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
    if not city:
        pass
    # api_key lấy trên open weather map
    api_key = "7fef1a10cde3184dbb68920a2b941d52"
    # tìm kiếm thông tin thời thời tiết của thành phố
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    # truy cập đường dẫn của dòng 188 lấy dữ liệu thời tiết
    response = requests.get(call_url)
    # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
    data = response.json()
    # kiểm tra nếu ko gặp lỗi 404 thì xem xét và lấy dữ liệu
    if data["cod"] != "404":
        # lấy value của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # 	lúc mặt trời mọc, mặt trời mọc
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        # lúc mặt trời lặn
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
        Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
        Nhiệt độ trung bình là {current_temperature} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        """
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        speak("Không tìm thấy địa chỉ của bạn")

def change_wallpaper():
    api_key = "j6ZG82EYXwnxVguvP5p6STmjO5ZzTXWOmzvHbwKU21g"
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
          api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']
    # Location where we download the image to.
    urllib2.urlretrieve(photo, r"C:\Users\acer\Desktop\DOANCS4\changeimage\image_change.png")
    image = os.path.join(r"C:\Users\acer\Desktop\DOANCS4\changeimage\image_change.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
    speak("Hình nền máy tính bạn đã được thay đổi. Bạn ra home xem có đẹp không nha ?")

def play_music(path):
    # path là tham số chứa đường dẫn thư mục chứa nhạc
    myPATH = path
    # lấy file nhạc ra
    ds = os.listdir(myPATH)
    # dùng for mở từng bài nhạc
    for i in ds:
        print("\nĐang phát bài :  " + i)
        os.system(myPATH + "\\" + i)
        print("\nĐã phát xong bài : \t\t" + i)


def play_youtube():
    speak("Nói nội dung bạn muốn tìm trên youtube")
    search = takeCommand()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak("Đây là thứ mà tôi tìm được bạn xem qua nhé")


def play_youtube_2():
    speak("Nói nội dung bạn muốn tìm trên youtube")
    search = takeCommand()
    while True:
        result = YoutubeSearch(search, max_results=10).to_dict()
        if result:
            break
    url = f"https://www.youtube.com" + result[0]['url_suffix']
    webbrowser.get().open(url)
    speak("Đây là thứ mà tôi tìm được bạn xem qua nhé")
    print(result)
    
def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Gửi email
    6. Dự báo thời tiết
    7. Mở video nhạc
    8. Thay đổi hình nền máy tính
    9. Đọc báo hôm nay
    10. Kể bạn biết về thế giới """)

def openWeb(nameWeb,url):
    var.set('Đang mở '+ nameWeb + '... !')
    window.update()
    speak('Chờ một chút, mình đang mở '+ nameWeb)
    webbrowser.open(url)

def openFile( path):
    var.set("Đang mở ")
    window.update()
    speak("chờ một chút, mình đang mở ")
    os.startfile(path)

def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        text = takeCommand()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(10)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            ans = takeCommand()
            if "có" not in ans:
                break    
            speak(content)
            time.sleep(10)

        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Mình không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")

def read_news():
    speak("Bạn muốn đọc báo về gì")
    
    queue = takeCommand()
    params = {
        'apiKey': '8237fd81c2af4bb8b82986de19c66b47',
        "q": queue,
    }
    api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
    """)
        if number <= 3:
            webbrowser.open(result['url'])

def handleTask():
    while True:

        btn1.configure(bg = 'orange')
        query = takeCommand().lower()
        if 'tạm biệt' in query:
            var.set("Tạm biệt nhé !")
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
                    
        elif 'báo' in query or 'đọc báo' in query:
            read_news()
            
        elif 'định nghĩa' in query:
            tell_me_about()

        elif 'mở youtube' in query:
            openWeb('Youtube', "youtube.com")

        elif 'mở facebook' in query:
            openWeb('Facebook', "facebook.com")

        elif 'mở google' in query:
            openWeb('Google', "google.com")

        elif 'chào bạn' in query:
            var.set('Chào bạn nha. Tôi có thể giúp gì cho bạn !')
            window.update()
            speak("Chào bạn nha. Tôi có thể giúp gì cho bạn !")
			
        elif 'mở stackoverflow' in query:
            openWeb('Stackoverflow', "stackoverflow.com")

        elif "mở nhạc" in query or "nghe nhạc" in query:
            speak("Ok. Tôi bắt đầu mở nhạc đây")
            play_music(r"C:\Users\acer\Desktop\music")

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

        elif 'có thể làm gì' in query:
           help_me()

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
            path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2018.3.2\\bin\\pycharm64.exe" 
            os.startfile(path)

        elif 'mở chrome' in query or 'open chrome' in query:
            var.set("Đang mở Google Chrome...")
            window.update()
            speak("chờ một chút, mình đang mở Google Chrome")
            path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(path)
            
        elif 'mở word' in query or 'open word' in query or 'mở microsoft word' in query or 'open microsoft word' in query:
            var.set("Đang mở Microsoft Word...")
            window.update()
            speak("chờ một chút, mình đang mở Microsoft Word")
            path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(path)
            
        elif 'mở powerpoint' in query or 'open powerpoint' in query or 'mở microsoft powerpoint' in query or 'open microsoft powerpoint' in query:
            var.set("Đang mở Microsoft Powpoint...")
            window.update()
            speak("chờ một chút, mình đang mở Microsoft Powpoint")
            path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
            os.startfile(path)
        
        elif 'mở excel' in query or 'open excel' in query or 'mở microsoft excel' in query or 'open microsoft excel' in query:
            var.set("Đang mở Microsoft Excel...")
            window.update()
            speak("chờ một chút, mình đang mở Microsoft Excel")
            path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(path)
            
        elif 'mở notepad' in query or 'open notepad' in query:
            var.set("Đang mở Notepad...")
            window.update()
            speak("chờ một chút, mình đang mở Notepad")
            path = "C:\\WINDOWS\\System32\\notepad.exe"
            os.startfile(path)
            
        elif 'mở cmd' in query or 'open cmd' in query:
            var.set("Đang mở cmd...")
            window.update()
            speak("chờ một chút, mình đang mở cmd")
            path = "C:\\WINDOWS\\System32\\cmd.exe"
            os.startfile(path)
        
        elif "tìm kiếm" in query or 'search google' in query:
            var.set("Bạn muốn tìm kiếm gì ?")
            window.update()
            speak("Bạn muốn tìm kiếm gì ?")
            search= takeCommand().lower()
            url = f"https://google.com/search?q={search}"
            webbrowser.get().open(url)
            speak(f'OK. {search} trên google đây nhé ')

        elif 'youtube' in query:
                speak("Bạn muốn tìm kiếm đơn giản hay phức tạp")
                yeu_cau = takeCommand()
                if "đơn giản" in yeu_cau:
                    play_youtube()
                    if input():
                        pass
                elif "phức tạp" in yeu_cau:
                    play_youtube_2()
                    if input("Tiếp tục y/n: ") == "y":
                        pass
        
        elif "thời tiết" in query:
           current_weather()
        elif 'email' in query or 'mail' in query or 'gmail' in query:
            send_email(query)


        elif "hình nền" in query or "nền" in query or "background" in query:
            change_wallpaper()
		
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
                cv2.imshow( constants.URL_IMAGE + 'pic', frame)
                cv2.imwrite( constants.URL_IMAGE + 'pic.jpg',frame)
            stream.release()
            

        elif 'quay video' in query:
            cap = cv2.VideoCapture(0)
            out = cv2.VideoWriter( constants.URL_IMAGE +'output.mp4', -1, 20.0, (640,480))
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
        
        else :
            dic_commands = addCommand.getCommandDic()
            for x in dic_commands:
                if dic_commands[x]  in query:
                    print("mở filee")
                    openFile(x)
                    return 
        

def play():
    btn2['state'] = 'disabled'
    btn0['state'] = 'disabled'
    btn1.configure(bg = 'orange')

    t = threading.Thread(target=handleTask)
    t.start()


       

def handleSaveUserName():
    username = entry_name.get()
    if username == '':
        return messagebox.showerror( title="ERROR", message= 'please type your username!!')
    f = open('src/public/ahihi.txt', 'w+', encoding="utf8")
    f.write(username)
    current_username.set(username)
    f.close
    
    return messagebox.showinfo(title="Success",message= 'save success')


def getUserName():
    f = open('src/public/ahihi.txt', 'r', encoding='UTF-8')
    str = f.read()
    print(str)
    current_username.set(str)

    

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

frames = [PhotoImage(file= constants.URL_IMAGE + 'Assistant.gif',format = 'gif -index %i' %(i)) for i in range(100)]
window.title('JARVIS')

label = Label(window, width = 600, height = 500)
label.pack()
window.after(0, update, 0)


frame_InputName = Frame(window)

label_name = Label(frame_InputName, text="Type your name:",font=("Courier", 18),bg = '#ADD8E6') 
label_name.grid(row=0,column=0)
entry_name = Entry(frame_InputName, width = 30 )
entry_name.grid(row=0, column=1)
btn_saveName = Button(window,text = 'save name',width = 20, command = handleSaveUserName, bg = '#5C85FB')
btn_saveName.config(font=("Courier", 12))
frame_InputName.pack()
btn_saveName.pack()



btn_setting = Button(text = 'Setting',width = 20, command = addCommand.createGui, bg = '#5C85FB')
btn_setting.config(font=("Courier", 12))
btn_setting.pack()


btn0 = Button(text = 'WISH ME',width = 20, command = wishme, bg = '#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text = 'PLAY',width = 20,command = play, bg = '#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text = 'EXIT',width = 20, command = window.destroy, bg = '#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()

getUserName()

window.mainloop()

