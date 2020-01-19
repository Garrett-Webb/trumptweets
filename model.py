import pickle
import numpy as np
import re
import nltk
import random
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
import random
import sys

# TODO: clean key phrases (make all lowercase, ascii only)

# Given a keyword return matching documents (tweets).
def subset_documents(documents, keyword):
    if keyword == 'all':
        return [document['text'] for document in documents.values()]

    matches = []
    for document in documents.values():
        if 'key_phrases' in document:
            doc_keywords = [words for phrases in document['key_phrases'] for
                            words in phrases.split()]
            if keyword in doc_keywords:
                matches.append(document['text'])

    return matches


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)


def clean_nltk(text):
    # lowercase text
    new_string = text.lower()
    new_string = re.sub(r"'s\b","",new_string)
    new_string = re.sub("&amp;", "and", new_string)
    new_string = remove_non_ascii(new_string)

    return new_string

# Generate nltk corpus
def generate_corpus(text):
    text = " ".join(text)
    text = clean_nltk(text)
    text_file = open("corpus/tempout.txt", "w+")
    text_file.write(text)
    text_file.close()
    mycorpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader(
        r"corpus",
        r'(?!\.).*\.txt',
        cat_pattern=r'(neg|pos)/.*',
        encoding="ascii")

    return mycorpus


def train(mycorpus):
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

    return model


# Given two starting words return a sentence.
def generate_sentence(starting_words, model):
    if len(starting_words) < 2:
        print("ERROR: Less than 2 starting words")
        return

    sentence_finished = False
    while not sentence_finished:
      # select a random probability threshold
      r = random.random()
      accumulator = .0

      for word in model[tuple(starting_words[-2:])].keys():
          accumulator += model[tuple(starting_words[-2:])][word]
          # select words that are above the probability threshold
          if accumulator >= r:
              starting_words.append(word)
              break

      if starting_words[-2:] == [None, None]:
          sentence_finished = True

    return ' '.join([t for t in starting_words if t])


def generate_starting_words(documents):
    tweet = random.choice(documents)
    tweet = clean_nltk(tweet)
    words = tweet.split()[:2]
    return words


def main():
    keyword = sys.argv[1]
    # starting_words = [sys.argv[1], sys.argv[2]]
    # print(starting_words)

    with open('documents.pkl', 'rb') as f:
        documents = pickle.load(f)

    matches = subset_documents(documents, keyword)
    starting_words = generate_starting_words(matches)
    print(starting_words)

    mycorpus = generate_corpus(matches)
    numsents = len(mycorpus.sents('tempout.txt'))
    model = train(mycorpus)

    # starting_words = ["mexico", "is"]
    sentence = generate_sentence(starting_words, model)
    print(sentence)


if __name__ == "__main__":
    main()
