import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import pickle

subscription_key = "fcbc20c49e2745e6985e31e46fc3b14d"
endpoint = "https://trumptweets-text-analytics.cognitiveservices.azure.com/"
filename = "clean.pkl"

# Authenticate text analytics and return client.
def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client

# Return key phrases for a text document.
def key_phrases(documents):
    client = authenticateClient()

    for document in documents:
        print(
            "Asking key-phrases on '{}' (id: {})".format(document['text'], document['id']))

    response = client.key_phrases(documents=documents)

    for document in response.documents:
        print("Document Id: ", document.id)
        print("\tKey Phrases:")
        for phrase in document.key_phrases:
            print("\t\t", phrase)

with open(filename, 'rb') as pickle_file:
    documents = pickle.load(pickle_file)
    # print(documents)
    key_phrases(documents[:10])
