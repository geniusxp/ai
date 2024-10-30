import pandas as pd
import re, string
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from deep_translator import GoogleTranslator

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
    # text = re.sub('\s+', ' ', text)  
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

model: LogisticRegression = None
def get_model():
    if model is not None:
        return model
    
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

    return model

def predict_message(message: str):
    translated_message = GoogleTranslator(source='auto', target='en').translate(text=message)
    clean_message = lemmatizer(preprocess(translated_message))
    prediction = get_model().predict(vectorizer.transform([clean_message]))
    return prediction[0]
