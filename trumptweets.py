# -*- coding: utf-8 -*-

import sys
import csv
import os
import re
import tweepy
import model
import random
import time
import config


# Create API object
api = tweepy.API(config.auth)

#keyword = sys.argv[1]

list_of_good_ones = ['nancy', 'immigration', 'crazy', 'collusion', 'obama',
                     'china', 'fake', 'media', 'facts']

while True:
    keyword = random.choice(list_of_good_ones)
    print("Keyword: ")
    print(keyword)
    tweet = model.get_tweet(keyword)
    
    if len(tweet) > 280 or len(tweet.split()) < 8:
        print("\n\nEither too long or too short, sorry. Trying again.\n\n")
        continue
    tweet = model.treat_tweet(tweet)
    api.update_status(tweet)
    print("tweeting: ")
    print(tweet)
    time.sleep(7200)
