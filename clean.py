import csv
import re
import pickle

filename = "trumptweets_unclean.csv"
out = open("output.txt","w+")
# read in file
with open(filename, 'r') as f:
  reader = csv.reader(f)
  tweets = list(reader)

# remove colname
tweets.pop(0)

counter = 0
text = []
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
    text.append(obj)
    counter = counter + 1
    out.write(tweet)
    out.write("\n")
with open('clean.pkl', 'wb') as f:
    pickle.dump(tweets, f)
