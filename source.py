# !pip install git+https://github.com/JustAnotherArchivist/snscrape.git
import pandas as pd
import re
import os

tweet_count = 500

# Using OS library to call CLI commands in Python
os.system("snscrape --jsonl --max-results {} twitter-search '$GME'> user-tweets.json".format(tweet_count, username))
# snscrape is some github package that helps you scrape twitter easily from cmd terminal

# Reads the json generated from the CLI command above and creates a pandas dataframe
gme_tweets = pd.read_json('user-tweets.json', lines=True)
gme_tweets
