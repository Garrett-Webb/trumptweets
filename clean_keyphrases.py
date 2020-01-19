from model import clean_nltk
import pickle

with open('documents.pkl', 'rb') as f:
    documents = pickle.load(f)

for document in documents.values():
    key_phrases_clean = []
    if 'key_phrases' in document:
        for key_phrases in document['key_phrases']:
            key_phrases_clean.append(clean_nltk(key_phrases))
        documents[document['id']]['key_phrases'] = key_phrases_clean

with open('documents.pkl', 'wb') as f:
    pickle.dump(documents, f)
