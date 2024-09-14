import pandas as pd
import re, string
import os
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from deep_translator import GoogleTranslator
import oracledb

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

wl = WordNetLemmatizer()
vectorizer = CountVectorizer(lowercase=True, 
                             stop_words=stopwords.words('english'),
                             max_features=1000)

def preprocess(text):
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
    text = text.lower() 
    text = text.strip()  
    text = re.compile('<.*?>').sub('', text) 
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)  
    text = re.sub('\s+', ' ', text)  
    text = re.sub(r'\[[0-9]*\]',' ',text) 
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    text = re.sub(r'\d',' ',text) 
    text = re.sub(r'\s+',' ',text) 
    return text

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatizer(string):
    word_pos_tags = nltk.pos_tag(word_tokenize(string))
    a=[wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for idx, tag in enumerate(word_pos_tags)]
    return " ".join(a)

df = None
if os.path.exists('./model/tweet_emotions_clean.csv'):
    print("Loading preprocessed data...")
    df = pd.read_csv('./model/tweet_emotions_clean.csv')
else:
    print('Preprocessing data...')
    df = pd.read_csv('./model/tweet_emotions.csv')
    
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset='content', inplace=True)

    df['clean_content'] = df['content'].apply(lambda x: lemmatizer(preprocess(x)))
    df.to_csv('./model/tweet_emotions_clean.csv', index=False)

X = vectorizer.fit_transform(df['clean_content'].values.astype('U'))

y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=42)

model = LogisticRegression(max_iter=1000, solver='sag')
model.fit(X_train, y_train)

def predict_message(message: str):
    translated_message = GoogleTranslator(source='auto', target='en').translate(text=message)
    clean_message = lemmatizer(preprocess(translated_message))
    prediction = model.predict(vectorizer.transform([clean_message]))
    return prediction[0]

connection = oracledb.connect(
    user="rm99565",
    password="140805",
    dsn="oracle.fiap.com.br/orcl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
async def app_status():
    return 'ok'

@app.post("/event/{event_id}/send-message")
async def send_message(message: str, event_id: int):
    emotion = predict_message(message)

    cursor = connection.cursor()
    cursor.callproc("INCREASE_EVENT_EMOTION", [event_id, emotion])
    connection.commit()
    return emotion

class EventDay(BaseModel):
    date: datetime
    empty: int
    sadness: int
    enthusiasm: int
    neutral: int
    worry: int
    surprise: int
    love: int
    fun: int
    hate: int
    happiness: int
    boredom: int
    relief: int
    anger: int

@app.get("/event/{event_id}")
async def get_event(event_id: int):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM TBL_EVENT_EMOTIONS WHERE EVENT_ID = :id", id=event_id)
    event_days = cursor.fetchall()

    event_day_list = [EventDay(
        date=row[2],
        empty=row[3],
        sadness=row[4],
        enthusiasm=row[5],
        neutral=row[6],
        worry=row[7],
        surprise=row[8],
        love=row[9],
        fun=row[10],
        hate=row[11],
        happiness=row[12],
        boredom=row[13],
        relief=row[14],
        anger=row[15]
    ) for row in event_days]

    return event_day_list
