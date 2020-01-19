import pickle
import numpy as np
import pandas as pd
import re
import nltk
from unidecode import unidecode
#from keras.utils import to_categorical
#from keras.preprocessing.sequence import pad_sequences
#from keras.models import Sequential
#from keras.layers import LSTM, Dense, GRU, Embedding
#from keras.callbacks import EarlyStopping, ModelCheckpoint

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

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def clean_nltk(text):
    # lowercase text
    new_string = text.lower()
    new_string = re.sub(r"'s\b","",new_string)
    
    new_string = remove_non_ascii(new_string)

    return new_string



# def create_seq(text):
#     # create a character mapping index
#     chars = sorted(list(set(text)))
#     mapping = dict((c, i) for i, c in enumerate(chars))

#     length = 30
#     sequences = list()
#     for i in range(length, len(text)):
#         # select sequence of tokens
#         seq = text[i-length:i+1]
#         # store
#         sequences.append(seq)
#     print('Total Sequences: %d' % len(sequences))
#     return sequences


# def encode_seq(seq):
#     sequences = list()
#     for line in seq:
#         # integer encode line
#         encoded_seq = [mapping[char] for char in line]
#         # store
#         sequences.append(encoded_seq)
#     return sequences


# Load documents
with open('documents.pkl', 'rb') as f:
    documents = pickle.load(f)

keyword = 'immigration'
matches = subset_documents(documents, keyword)

text = " ".join(matches)
text = clean_nltk(text)
text_file = open("corpus/tempout.txt", "w+")
text_file.write(text)
text_file.close()

mycorpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader(
    r"corpus",
    r'(?!\.).*\.txt', 
    cat_pattern=r'(neg|pos)/.*',
    encoding="ascii")

numsents = len(mycorpus.sents('tempout.txt'))
print(numsents)
#print(mycorpus.sents()[:208])

from nltk import bigrams, trigrams
from collections import Counter, defaultdict

# Create a placeholder for model
model = defaultdict(lambda: defaultdict(lambda: 0))

# Count frequency of co-occurance  
for sentence in mycorpus.sents():
    for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1
 
# Let's transform the counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count

#testing = dict(model["our", "immigration"])
#print(testing)

import random

# starting words
text = ["mexico", "must"]
sentence_finished = False
 
while not sentence_finished:
  # select a random probability threshold  
  r = random.random()
  accumulator = .0

  for word in model[tuple(text[-2:])].keys():
      accumulator += model[tuple(text[-2:])][word]
      # select words that are above the probability threshold
      if accumulator >= r:
          text.append(word)
          break

  if text[-2:] == [None, None]:
      sentence_finished = True
 
print (' '.join([t for t in text if t]))