import pickle

# Given a keyword return matching documents (tweets)
def subset_documents(documents, keyword):
    matches = []
    for document in documents.values():
        if 'key_phrases' in document:
            doc_keywords = [words for phrases in document['key_phrases'] for
                            words in phrases.split()]
            if keyword in doc_keywords:
                matches.append(document['text'])

    return matches

# Load documents
with open('documents.pkl', 'rb') as f:
    documents = pickle.load(f)

keyword = 'immigration'
matches = subset_documents(documents, keyword)
# print(matches)
print(len(matches))
