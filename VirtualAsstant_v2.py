# Code for virtual assistant with GUI
import speech_recognition as sr
import pyttsx3
import time
import json
from time import ctime
import webbrowser
import playsound
import ctypes
import os
import re
import datetime
import random
import requests
import wikipedia
from time import strftime
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from gtts import gTTS
from tkinter import *
from PIL import ImageTk,Image
from youtube_search import YoutubeSearch


wikipedia.set_lang('vi')
path = ChromeDriverManager().install()
print('Say something...')
r = sr.Recognizer()
speaker = pyttsx3.init()

def record_audio(ask = False):
    #user voice record
    with sr.Microphone() as source:
        if ask:
            lee_voice(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language="vi-VN")
            print('Recognizer voice :'+ voice_data)
        except Exception:
            print('Oops something went Wrong')
            #lee_voice('Oops something went Wrong')
        return voice_data
    
def lee_voice(audio_string):
    #Play audio text to voice
    tts = gTTS(text=audio_string, lang='vi')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)
    
def get_text():
    for i in range(3):
        text = record_audio()
        if text:
            return text.lower()
        
        elif i < 2:
            lee_voice("Mình không nghe rõ. Bạn nói lại được không!")
            time.sleep(3)
    time.sleep(2)
    stop()
    return 0

def stop():
    lee_voice("Hẹn gặp lại bạn sau!")
    time.sleep(2)
    
def help_me():
    lee_voice("""Mình có thể giúp bạn thực hiện các câu lệnh sau đây:
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
    time.sleep(27)
    
def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        lee_voice("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        lee_voice("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
    else:
        lee_voice("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))
    time.sleep(5)


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        lee_voice('Bây giờ là %d giờ %d phút %d giây' % (now.hour, now.minute, now.second))
    elif "ngày" in text:
        lee_voice("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        lee_voice("Mình chưa hiểu ý của bạn. Bạn nói lại được không?")
    time.sleep(4)


def current_weather():
    lee_voice("Bạn muốn xem thời tiết ở đâu ạ.")
    time.sleep(3)
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        lee_voice(content)
        time.sleep(28)
    else:
        lee_voice("Không tìm thấy địa chỉ của bạn")
        time.sleep(2)
        
def tell_me_about():
    try:
        lee_voice("Bạn muốn nghe về gì ạ")
        time.sleep(2)
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        lee_voice(contents[0].split(".")[0])
        time.sleep(15)
        for content in contents[1:]:
            lee_voice("Bạn muốn nghe thêm không")
            time.sleep(2)
            ans = get_text()
            if "có" not in ans:
                break    
            lee_voice(content)
            time.sleep(15)

        lee_voice('Cảm ơn bạn đã lắng nghe!!!')
        time.sleep(3)
    except:
        lee_voice("Mình không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")
        time.sleep(5)

def change_wallpaper():
    api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
        api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']
    # Location where we download the image to.
    urllib2.urlretrieve(photo, "D:\\Download____CocCoc\\a.png")
    image=os.path.join("D:\\Download____CocCoc\\a.png")
    ctypes.windll.user32.SystemParametersInfoW(20,0,image,3)
    lee_voice('Hình nền máy tính vừa được thay đổi')
    time.sleep(3)

        
def send_email(text):
    lee_voice('Bạn gửi email cho ai nhỉ')
    time.sleep(2)
    recipient = get_text()
    if 'yến' in recipient:
        lee_voice('Nội dung bạn muốn gửi là gì')
        time.sleep(3)
        content = get_text()
        # mail = smtplib.SMTP('smtp.gmail.com', 587)
        # mail.ehlo()
        # mail.starttls()
        # mail.login('cvduc.19it1@vku.udn.vn', '11111111')
        # mail.sendmail('cvduc.19it1@vku.udn.vn',
        #               'pvphung.19it1@vku.udn.vn', content.encode('utf-8'))
        # mail.close()
        lee_voice('Email của bạn vùa được gửi. Bạn check lại email nhé hihi.')      
        time.sleep(4)  
    else:
        lee_voice('Mình không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?')
        time.sleep(5)
        
def play_song():
    lee_voice('Xin mời bạn chọn tên bài hát')
    time.sleep(2)
    mysong = get_text()
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    lee_voice("Bài hát bạn yêu cầu đã được mở.")
    time.sleep(3)

def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain + '.com'
        webbrowser.open(url)
        lee_voice("Trang web bạn yêu cầu đã được mở.")
        time.sleep(3)
        return True
    else:
        return False

def open_application(text):
    if "google" in text:
        lee_voice("Mở Google Chrome")
        time.sleep(2)
        os.startfile('Desktop\\Google Chrome')
    elif "word" in text:
        lee_voice("Mở Microsoft Word")
        time.sleep(2)
        os.startfile('Desktop\\Google Chrome')
    elif "excel" in text:
        lee_voice("Mở Microsoft Excel")
        time.sleep(2)
        os.startfile('Desktop\\Google Chrome')
    else:
        lee_voice("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")
        time.sleep(3)


def open_google_and_search(text):
    search_for = text.split("kiếm", 1)[1]
    lee_voice('Okay!')
    driver = webdriver.Chrome(path)
    driver.get("http://www.google.com")
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys(str(search_for))
    que.send_keys(Keys.RETURN)
    time.sleep(10)

def read_news():
    lee_voice("Chức năng còn đang xây dựng. Vui lòng chọn chức năng khác")
    time.sleep(5)

    
class Widget: 
    def __init__(self):
        root = Tk()
        root.title('VKU')
        root.geometry('470x295')

        img = ImageTk.PhotoImage(Image.open('b.jpg'))
        panel = Label(root, image=img)
        panel.pack(side='right', fill='both', expand='no')
        compText = StringVar()
        userText = StringVar()
        userText.set('My Virtual Assistant')
        userFrame = LabelFrame(root, text='VKU', font=('Railways', 24,
        'bold'))
        userFrame.pack(fill='both', expand='yes')
        top = Message(userFrame, textvariable=userText, bg='black',
        fg='white')
        top.config(font=("Century Gothic", 15, 'bold'))
        top.pack(side='top', fill='both', expand='yes')
      
        btn = Button(root, text='Speak', font=('railways', 10, 'bold'),
        bg='red', fg='white', command=self.clicked).pack(fill='x', expand='no')
        btn2 = Button(root, text='Close', font=('railways', 10,
        'bold'), bg='yellow', fg='black', command=root.destroy).pack(
        fill='x', expand='no')
        lee_voice('Chào bạn, bạn muốn tôi gọi bạn là gì nhỉ?')
        root.mainloop()
    
    def clicked(self):
        print("working...")
        voice_data = record_audio()
        voice_data = voice_data.lower()
        if 'chào' in voice_data:
            hello("Tôi cũng chào bạn nha")
        elif "có thể làm gì" in voice_data:
            help_me()
        elif 'search' in voice_data:
            search = record_audio('What do you want to search for ?')
            url = 'https://google.com/search?q=' + search
            webbrowser.get().open(url)
            lee_voice('Here is what i found' + search)
        elif 'địa điểm' in voice_data or 'google map' in voice_data:
            location = record_audio('Đâu là vị trí của bạn?')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            lee_voice('Đây là vị trí của bạn:' + location)
        elif 'what is the time' in voice_data:
            lee_voice("Sir the time is :" + ctime())
        elif "giờ" in voice_data or "ngày" in voice_data:
            get_time(voice_data)
        elif "thời tiết" in voice_data:
            current_weather()
        elif "đọc báo" in voice_data:
            read_news()
        elif "email" in voice_data or "mail" in voice_data or "gmail" in voice_data:
            send_email(voice_data)
        elif "hình nền" in voice_data:
            change_wallpaper()
        elif "mở " in voice_data:
            open_website(voice_data)
        elif "ứng dụng" in voice_data:
            lee_voice("Tên ứng dụng bạn muốn mở là ")
            time.sleep(3)
            text1 = get_text()
            open_application(text1)
        elif 'mở google và tìm kiếm' in voice_data:
            open_google_and_search(voice_data)
        elif "định nghĩa" in voice_data:
            tell_me_about()
        elif "open video" in voice_data:
            meme =r"C:\Users\acer\Videos\hahaa\hahaa.mp4"
            os.startfile(meme)
        elif "chơi nhạc" in voice_data:
            play_song()
        elif 'exit' in voice_data:
            lee_voice('Hẹn gặp lại bạn sau!!! ')
            exit()
        else:
            lee_voice("Bạn cần mình giúp gì ạ?")
            time.sleep(2)

if __name__== '__main__':
    widget = Widget()
time.sleep(1)
while 1:
    voice_data = record_audio()
    respond(voice_data)

speaker.runAndWait()


