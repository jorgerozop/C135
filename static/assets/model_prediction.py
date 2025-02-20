import pandas as pd 
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from datetime import datetime
#Hacer el diccionario del código y URL para las diferentes emociones
emo_code_url = {
    "empty": [0, "./static/assets/emoticons/Empty.png"],
    "sadness": [1, "./static/assets/emoticons/Sadness.png"],
    "enthusiasm": [2, "./static/assets/emoticons/Enthusiastic.png"],
    "neutral": [3, "./static/assets/emoticons/Neutral.png"],
    "worry": [4, "./static/assets/emoticons/Worry.png"],
    "surprise": [5, "./static/assets/emoticons/Surprise.png"],
    "love": [6, "./static/assets/emoticons/Love.png"],
    "fun": [7, "./static/assets/emoticons/Fun.png"],
    "hate": [8, "./static/assets/emoticons/Hate.png"],
    "happiness": [9, "./static/assets/emoticons/Happiness.png"],
    "boredom": [10, "./static/assets/emoticons/Boredom.png"],
    "relief": [11, "./static/assets/emoticons/Relief.png"],
    "anger": [12, "./static/assets/emoticons/Anger.png"],
}

train_data = pd.read_csv("./static/assets/data_files/tweet_emotions.csv")    
training_sentences = []

for i in range(len(train_data)):
    sentence = train_data.loc[i, "content"]
    training_sentences.append(sentence)

model = load_model("./static/assets/model_file/Tweets_Text_Emotion.h5")

vocab_size = 40000
max_length = 100
trunc_type = "post"
padding_type = "post"
oov_tok = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

def predict(text):
    predicted_emotion_img_url=""
    predicted_emotion=""

    if  text!="":
        sentence = []
        sentence.append(text)

        sequences = tokenizer.texts_to_sequences(sentence)

        padded = pad_sequences(
            sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
        )
        testing_padded = np.array(padded)

        predicted_class_label = np.argmax(model.predict(testing_padded), axis=-1)        
            
        for key, value in emo_code_url.items():
            if value[0]==predicted_class_label:
                predicted_emotion_img_url=value[1]
                predicted_emotion=key
        return predicted_emotion, predicted_emotion_img_url

#Mostrar entrada
#Valida todas las entradas tanto de textos como de imágenes
def show_entry():
    day_entry_list = pd.read_csv("./static/assets/data_files/data_entry.csv")
    #Crear un archivo csv con el nombre day_entry_list para guardar las entradas de texto
    day_entry_list = day_entry_list.iloc[::-1]
    #Leer las entradas de cada lista 
    date1 = (day_entry_list['date'].values[0])
    date2 =(day_entry_list['date'].values[1])
    date3 = (day_entry_list['date'].values[2])

    entry1 = day_entry_list['text'].values[0]
    entry2 = day_entry_list['text'].values[1]
    entry3 = day_entry_list['text'].values[2]

    emotion1 = day_entry_list["emotion"].values[0]
    emotion2 = day_entry_list["emotion"].values[1]
    emotion3 = day_entry_list["emotion"].values[2]

    emotion_url_1=""
    emotion_url_2=""
    emotion_url_3=""
#Estas entradas después de ser devueltas al html van a mostrar las emociones 
    for key, value in emo_code_url.items():
        if key==emotion1:
            emotion_url_1 = value[1]
        if key==emotion2:
            emotion_url_2 = value[1]
        if key==emotion3:
            emotion_url_3 = value[1]
#
    return [
        {
            "date": date1,
            "entry": entry1,
            "emotion": emotion1,
            "emotion_url": emotion_url_1
        },
        {
            "date": date2,
            "entry": entry2,
            "emotion": emotion2,
            "emotion_url": emotion_url_2
        },
        {
            "date": date3,
            "entry": entry3,
            "emotion": emotion3,
            "emotion_url": emotion_url_3
        }
    ]
