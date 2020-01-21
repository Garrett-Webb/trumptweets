# trumptweets

[![What Would Trump Tweet?][image]][hyperlink]

  [hyperlink]: https://twitter.com/R3alFakeDonald
  [image]: https://imgur.com/uQ0W3Tt

## Disclaimer
This was made for CruzHacks 2020 by Garrett Webb and Chandni Nagda, please do
not steal our work, just ask us.

## Goal
Analyze Trump's nonsense using Microsoft Azure NLP and trigram language model.
Generate similar nonsense for a given topic.

## Usage

Install python3, nltk, tweepy, azure, and other general Python libraries

Simply make your own config.py file with API keys for twitter and Microsoft
Azure Text Analytics. Set the following for Microsoft Azure:
* `subscription_key`
* `endpoint`
* `filename`

Set the following for Twitter
* `auth = tweepy.OAuthHandler(...)`
* `auth.set_access_token(...)`

Then either run model.py with topic as the command line argument, or run
trumptweets.py and let it go (it will continuously tweet at the time interval
you set). Here is an example on the command line:

* `python3 model.py <keyword>`
will output a tweet to the console
* `python3 trumptweets.py`
will generate and output a tweet to the console as well as post it to twitter on the time interval you specify in the code.


Go to https://twitter.com/R3alFakeDonald (our twitter bot) or your make own
twitter developer account and bot to see your madness unfurl.
