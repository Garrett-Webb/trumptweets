# -*- coding: utf-8 -*-

import sys
import csv
import os
import re
import tweepy
import model
import random
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler("HmdlcsDgiWlbYeJ4WNiAvdbts", "HPktksp3iGAo8IkTb3WANMNKguWudlz3csq9rNJyll6tiviDmY")
auth.set_access_token("1218718742978289665-14fuoeOIGwNRDWkl32438j67d5hJeU", "ChjeOUwo0vPXwA8Vxneb5fPfLvJ5xIfD2ioH54bm4lJrk")

# Create API object
api = tweepy.API(auth)

#keyword = sys.argv[1]

list_of_good_ones = ['nancy', 'immigration', 'crazy', 'collusion', 'obama', 'china', 'fake', 'media', 'facts']

while True:
    keyword = random.choice(list_of_good_ones)
    print("Keyword: ")
    print(keyword)
    tweet = model.get_tweet(keyword)
    print("tweeting: ")
    print(tweet)
    
    if len(tweet) > 280 or len(tweet.split()) < 6:
        print("\n\nEither too long or too short, sorry. Trying again.\n\n")
        continue
    model.treat_tweet(tweet)
    api.update_status(tweet)
    time.sleep(7200)