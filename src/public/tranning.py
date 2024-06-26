import random
import json
import pickle
from nltk import metrics
import numpy as np
from underthesea import word_tokenize

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


import constants 
import handleFile
import addCommand



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

def trainbot():
    lemmatizer = WordNetLemmatizer()
    str_intents = handleFile.readFile(constants.URL_File +'intents.json')  
    intents = json.loads(str_intents) #đọc dữ liệu tròn file json

    dic_commands = addCommand.getCommandDic()
    for x in dic_commands:
        intents['intents'].append(
            {"tag": x,
            "patterns": [x],
            "responses": [x],
            "context_set": ""
        },)
  
    #print(intents)


    words = []
    classes = []
    documents = []
    ignore_letters = ['?','!','.',',']

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = func_stop_words(pattern)
            words.extend(word_list)
           
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
            
    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words)) 
    classes = sorted(set(classes))
    pickle.dump(words, open( constants.URL_File +'words.pkl', 'wb'))  
    pickle.dump(classes, open( constants.URL_File +'classes.pkl', 'wb'))

    training = []
    output_empty = [0]*len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)
            
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])
                
                
    random.shuffle(training)
    training = np.array(training)

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
