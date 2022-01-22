import random
import json
import pickle
from nltk import metrics
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


import constants 
import handleFile
import addCommand





def trainbot():
    lemmatizer = WordNetLemmatizer()
    str_intents = handleFile.readFile(constants.URL_File +'intents.json')  
    intents = json.loads(str_intents) 
    dic_commands = addCommand.getCommandDic()
    for x in dic_commands:
        intents['intents'].append(
            {"tag": x,
            "patterns": [x],
            "responses": [x],
            "context_set": ""
        },)
  
    #print(intents)


    words = [] # các từ mình yêu cầu
    classes = [] # các nhãn tag 
    documents = [] # mảng các yêu cầu và nhãn 
    ignore_letters = ['?','!','.',',']

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern) # trả về mảng các từ và dấu câu ví dụ " xin chào . " trả về ["xin", "chao", "."]
            words.extend(word_list)  #thêm word_list vào words # thêm nhiều cái
            documents.append((word_list, intent['tag'])) # thêm một cái 
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    #print(documents)       
    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters] # xử tiền dữ liệu ví dụ đưa số nhiều về số ít, ..
    words = sorted(set(words)) # sắp xếp theo thứ tự tăng dần: số , chữ hoa , chữ thường
    classes = sorted(set(classes))
    pickle.dump(words, open( constants.URL_File +'words.pkl', 'wb'))  
    pickle.dump(classes, open( constants.URL_File +'classes.pkl', 'wb'))

    training = []
    output_empty = [0]*len(classes) # tạo mảng với độ rộng là số lượng các nhãn
    print(output_empty)
    for document in documents:
        bag = []
        word_patterns = document[0] # document[0] là các đầu vào yêu cầu người dùng, document[1] là các nhãn dãn
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)
            
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1 
        training.append([bag, output_row])
                
                
    random.shuffle(training) # xáo trộn mảng
    training = np.array(training) # tạo mảng

    train_x = list(training[:, 0])
    train_y = list(training[:, 1]) 

    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation = 'softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    model.save( constants.URL_File +'chatbotmodel.h5', hist)
    print("Done")

trainbot()
