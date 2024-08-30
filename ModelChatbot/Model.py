import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow import keras

nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents from JSON file
intents = json.loads(open('intents1.json', encoding='utf-8').read())

# Initialize lists
words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', ',']
ignoreWords = thai_stopwords()

# Preprocess data
for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = word_tokenize(pattern, engine='newmm')
        words.extend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and normalize words
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignoreLetters and word not in ignoreWords]
words = sorted(set(words))
classes = sorted(set(classes))

# Save words and classes to pickle files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Prepare training data
training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

# Shuffle and convert training data to numpy array
random.shuffle(training)
training = np.array(training)

# Split features and labels
trainX = training[:, :len(words)]
trainY = training[:, len(words):]

# Define the model
model = keras.Sequential([
    keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(len(trainY[0]), activation='softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)

# Save the model
model.save('chatbot_model.h5')
print('Done')
