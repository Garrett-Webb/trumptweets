import pickle
import numpy as np
import pandas as pd
import re
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, GRU, Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Given a keyword return matching documents (tweets).
def subset_documents(documents, keyword):
    matches = []
    for document in documents.values():
        if 'key_phrases' in document:
            doc_keywords = [words for phrases in document['key_phrases'] for
                            words in phrases.split()]
            if keyword in doc_keywords:
                matches.append(document['text'])

    return matches

# More basic preprocessing for language model.
def clean(text):
    # lowercase text
    new_string = text.lower()
    new_string = re.sub(r"'s\b","",new_string)

    # remove punctuation
    new_string = re.sub("[^a-zA-Z]", " ", new_string)

    # remove short words
    long_words = []
    for word in new_string.split():
        if len(word) >= 3:
            long_words.append(word)
    return (" ".join(long_words)).strip()


def create_seq(text):
    # create a character mapping index
    chars = sorted(list(set(text)))
    mapping = dict((c, i) for i, c in enumerate(chars))

    length = 30
    sequences = list()
    for i in range(length, len(text)):
        # select sequence of tokens
        seq = text[i-length:i+1]
        # store
        sequences.append(seq)
    print('Total Sequences: %d' % len(sequences))
    return sequences


def encode_seq(seq):
    sequences = list()
    for line in seq:
        # integer encode line
        encoded_seq = [mapping[char] for char in line]
        # store
        sequences.append(encoded_seq)
    return sequences


# Load documents
with open('documents.pkl', 'rb') as f:
    documents = pickle.load(f)

keyword = 'immigration'
matches = subset_documents(documents, keyword)

text = " ".join(matches)
text = clean(text)

# create sequences
sequences = create_seq(text)

# encode the sequences
sequences = encode_seq(sequences)
