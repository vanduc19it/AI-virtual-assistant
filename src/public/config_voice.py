from tkinter import StringVar
import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def hello(a , s = "oke bro"):
    print(a)
    print(s)

def get_voice(update_gui = hello):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Trợ lí ảo: Listening...")
        update_gui("Đang lắng nghe...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        update_gui("Đang xác nhận... ")
        print("Trợ lí ảo: Recognizing...")
        query = r.recognize_google(audio, language='vi-Vi')
    except Exception as e:
        update_gui("Không xác nhận được")
        query = ""
    return query


def get_ahhi(a = hello):
    print("check nào ban")
    a()
    print("ket thuc chekc")

# get_ahhi()
# speak("xin chào bạn nhé")
