import random
import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, UserInformation, Session

# Load trained model
model = load_model('chatbot_model.h5')

# Load tokenizer data and classes
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents from JSON file
intents = json.loads(open('intents1.json', encoding='utf-8').read())

# Function to clean up the input sentence
def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence, engine='newmm')
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word not in thai_stopwords()]
    return sentence_words

# Function to convert a sentence to a bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"found in bag: {w}")
    return(np.array(bag))

# Function to predict the class of a sentence
def predict_class(sentence):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # Sort by probability strength
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Function to get response based on intent
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "ขอโทษค่ะ ฉันไม่เข้าใจคำถามของคุณ"

# Function to register a new user
def register_user(email, password, nickname):
    # Check if the email is already used
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        return "อีเมลนี้ถูกใช้แล้วค่ะ กรุณาลองใหม่"

    # Add new user to the database
    new_user = User(email=email, password=password)
    session.add(new_user)
    session.commit()

    # Add user information
    user_info = UserInformation(nickname=nickname, user=new_user)
    session.add(user_info)
    session.commit()

    return "สมัครสมาชิกสำเร็จแล้วค่ะ!"

# Function to log in the user
def login_user(email, password):
    user = session.query(User).filter_by(email=email, password=password).first()
    if user:
        return user.info[0].nickname  # Return the user's nickname from the first UserInformation object
    return None


# Function to run the chatbot
def run_chatbot():
    print("Chatbot is running. Type 'exit' to quit.")
    logged_in = False
    nickname = ""

    while True:
        if not logged_in:
            message = input("You: ")
            if message.lower() == 'exit':
                break

            if "register" in message.lower():
                email = input("กรุณากรอกอีเมล: ")
                password = input("กรุณากรอกรหัสผ่าน: ")
                nickname = input("กรุณากรอกชื่อเล่น: ")
                response = register_user(email, password, nickname)
                print(f"Bot: {response}")

            elif "login" in message.lower():
                email = input("กรุณากรอกอีเมล: ")
                password = input("กรุณากรอกรหัสผ่าน: ")
                nickname = login_user(email, password)
                if nickname:
                    logged_in = True
                    print(f"Bot: เข้าสู่ระบบสำเร็จ สวัสดี {nickname}!")
                else:
                    print("Bot: อีเมลหรือรหัสผ่านไม่ถูกต้องค่ะ ลองใหม่อีกครั้ง")

        else:
            message = input(f"You ({nickname}): ")
            if message.lower() == 'exit':
                break
            ints = predict_class(message)
            res = get_response(ints, intents)
            print(f"Bot: {nickname} {res}")

if __name__ == '__main__':
    # Initialize the database session
    engine = create_engine('sqlite:///chatbot.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    run_chatbot()
