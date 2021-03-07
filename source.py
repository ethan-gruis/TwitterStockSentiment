!python --version
# !pip install twitterscraper
# !pip install git+https://github.com/JustAnotherArchivist/snscrape.git

https://github.com/JustAnotherArchivist/snscrape/issues/81 

import twitterscraper
import pandas as pd
import re
import os


tweet_count = 500


# Using OS library to call CLI commands in Python
os.system("snscrape --jsonl --max-results {} twitter-search '$GME'> user-tweets.json".format(tweet_count))
# snscrape is some github package that helps you scrape twitter easily from cmd terminal

os.system("snscrape --jsonl twitter-search '$GME since:2021-03-01'> tweets.json")
# Reads the json generated from the CLI command above and creates a pandas dataframe

gme_tweets = pd.read_json('tweets.json', lines=True)
gme_tweets

def callStock(stockname):


https://github.com/JustAnotherArchivist/snscrape

# Creating finction to scrape stock ticker by name (done with snscrape)
# Formatting content to sentament able material
#Look into date range specification
#Look into plotting sentiments against stock reacton.
