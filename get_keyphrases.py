import os
import re
import csv
import math
import time
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import pickle
import random
from itertools import chain


filename = "trumptweets_unclean.csv"

def clean(filename):
    # read in file
    with open(filename, 'r') as f:
      reader = csv.reader(f)
      tweets = list(reader)

    # remove colname
    tweets.pop(0)

    counter = 0
    text = {}
    for data in tweets:
        if len(data) > 0:
            tweet = data[0]
        else:
            continue

        # don't include retweets
        if tweet[:2] == "RT":
            continue

        tweet = tweet.replace('"',"")
        tweet = tweet.replace('“',"")
        tweet = tweet.replace('”',"")

        # remove link
        tweet = re.sub(r'@\S+|https?://\S+', '', tweet, flags=re.MULTILINE)

        # remove hashtag
        tweet = re.sub(r'#([A-Za-z0-9_]+)', '', tweet, flags=re.MULTILINE)

        # remove mentions
        tweet = re.sub(r'@([A-Za-z0-9_]+)', '', tweet, flags=re.MULTILINE)

        obj = {'id': str(counter), 'language': 'en', 'text': tweet}
        text[str(counter)] = obj
        counter = counter + 1

    return text

# Authenticate text analytics and return client.
def authenticateClient():
    credentials = CognitiveServicesCredentials(config.subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=config.endpoint, credentials=credentials)
    return text_analytics_client

# Return key phrase responses for a text document.
def get_key_phrase_responses(documents):
    client = authenticateClient()
    chunk_size = 1000
    responses = []
    for i in range(math.ceil(len(documents) / chunk_size)):
        start = i * chunk_size
        end = chunk_size * (i + 1)
        if (i == math.ceil(len(documents) / chunk_size)):
            end = len(documents)

        response = client.key_phrases(documents =
            [x for x in documents.values()][start:end])
        responses.append(response.documents)
        time.sleep(65)

    responses = list(chain.from_iterable(responses))
    return responses

# Given API responses, add key phrases to document objects.
def add_key_phrases(documents, responses):
    if responses is None:
        with open('responses_unchained.pkl', 'rb') as f:
            responses = pickle.load(f)

    for response in responses:
        documents[response.id]['key_phrases'] = response.key_phrases

    return documents


documents = clean(filename)
# responses = get_key_phrase_responses(documents)
documents = add_key_phrases(documents, None)

# Save output
with open('documents.pkl', 'wb') as f:
    pickle.dump(documents, f)
