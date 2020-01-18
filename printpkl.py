import pickle
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from itertools import chain

with open('responses.pkl', 'rb') as f:
    responses = pickle.load(f)
responses = list(chain.from_iterable(responses))
#print(responses[:10])
print([response.key_phrases for response in responses])