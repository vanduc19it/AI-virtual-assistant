import random
import json
import pickle 
import numpy as np


import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

import constants 
import handleFile
import addCommand

lemartizer = WordNetLemmatizer()
str_intents = handleFile.readFile(constants.URL_File + 'intents.json')  
intents = json.loads(str_intents)


dic_commands = addCommand.getCommandDic() # trả về dạng json các câu lệnh mà người dùng tự thêm
for x in dic_commands:
    intents['intents'].append(
        {"tag": x,
            "patterns": [x],
            "responses": [x],
        "context_set": ""
    },)

words = pickle.load(open( constants.URL_File +'words.pkl', 'rb'))
classes = pickle.load(open( constants.URL_File +'classes.pkl', 'rb'))
model = load_model( constants.URL_File + 'chatbotmodel.h5')

# print(words)
# print(classes)
# print(intents)
# print(model)

def clean_up_sentence(sentence): # xử lý dữ liệu đầu vào 
    sentence_words = nltk.word_tokenize(sentence) # tách chuỗi thành các từ như "xin chào bạn ? " => ["xin", "chào", "bạn", "?"]
    sentence_words = [lemartizer.lemmatize(word) for word in sentence_words] # xử lý cơ bản đưa các từ về dạng số ít , hiện tại như played => play , better => good
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words): # enumerate là kiểu có trả về index (kiểu thứ tự trong mảng) và trong vòng for này thì i là thứ tự trong mảng 
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)   
    res = model.predict(np.array([bow]))[0] 
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(ints, intents_json): # return về kết quả với ints là mảng ( mảng có dạng {"intents": "nhãn", 'probability':"xác suất"} khi sử dụng machinelearning và intents_json là dữ liệu trong file intents.json
    try:
        tag = ints[0]['intent']
        #print(tag)
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag: # kiểm tra nhãn có = với nhãn khi machinelearning ko 
                return random.choice(i['responses']) # return một câu trả lời bất kỳ trong nhãn 
        return '00'
    except IndexError:
        return '00'

# print('Go! bot is running')

# while True:
#     message = input("")
#     ints = predict_class(message)
#     ##print(ints)
#     res = get_response(ints, intents)
#     print(res)

