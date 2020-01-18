import os
import re
import csv
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import pickle
import random

subscription_key = "fcbc20c49e2745e6985e31e46fc3b14d"
endpoint = "https://trumptweets-text-analytics.cognitiveservices.azure.com/"
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
        # text.append(obj)
        text[str(counter)] = obj
        counter = counter + 1

    return text

# Authenticate text analytics and return client.
def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client

# Return key phrases for a text document.
def key_phrases(documents):
    client = authenticateClient()

    # for document in documents.values():
        # print("Asking key-phrases on '{}' (id: {})".format(document['text'], document['id']))

    response = client.key_phrases(documents=[x for x in documents.values()][:100])

    responses = []
    for i in 1:ceil(len(documents) / 100):
        start = i * 100
        end = 100 * (i + 1)
        if (i == ceil(len(documents) / 100)):
            end = len(documents)

        response = client.key_phrases(documents=[x for x in documents.values()][start:end])
        responses.append(response)

    for response in response.documents:
        # print("Document Id: ", response.id)
        # print("\tKey Phrases:")
        documents[response.id]['key_phrases'] = response.key_phrases
        print(documents[response.id])
        # for phrase in response.key_phrases:
            # print("\t\t", phrase)

    return documents

# with open(filename, 'rb') as pickle_file:
#     documents = pickle.load(pickle_file)
#     documents = random.sample(documents.items(), k=10)
#     print(documents)
#     key_phrases(documents)

documents = clean(filename)
dict = key_phrases(documents)
# print(dict)
