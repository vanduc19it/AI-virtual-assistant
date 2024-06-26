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


dic_commands = addCommand.getCommandDic()
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

URL_STOPWORDS_VI = "src/public/datas3_stopword_vi.txt"

def load_dataStopWord(txt_file):
    texts = []
    with open(txt_file, 'r', encoding='utf8') as fp:
        for line in fp.readlines():
            texts.append(line.strip())
    return texts

def func_stop_words(data2):
    stop_words = load_dataStopWord(URL_STOPWORDS_VI)

    word_tokens = nltk.word_tokenize(data2) 
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    
    filtered_sentence = [] 
    
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    
    return(filtered_sentence) 

def clean_up_sentence(sentence):
    sentence_words = func_stop_words(sentence)
    sentence_words = [lemartizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
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

def get_response(ints, intents_json):
    try:
        tag = ints[0]['intent']
        #print(tag)
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        return '00'
    except IndexError:
        return '00'

# print('Go! bot is running')

# while True:
#     message = input("")
#     ints = predict_class(message)
#     print(ints)
#     res = get_response(ints, intents)
#     print(res)

