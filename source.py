# !python --version
# !pip install git+https://github.com/JustAnotherArchivist/snscrape.git
#!pip3 install --upgrade git+https://github.com/JustAnotherArchivist/snscrape@master

import pandas as pd
import re
import os
from sys import platform
from datetime import datetime



## EXAMPLE CODE

# Using OS library to call CLI commands in Python
# tweet_count = 500
# os.system("snscrape --jsonl --max-results {} twitter-search '$GME'> user-tweets.json".format(tweet_count))

# mac:
# os.system("snscrape --jsonl twitter-search '$GME since:2021-03-01 until:2021-03-02'> tweets.json")

# windows:
# os.system("snscrape --jsonl --max-results 500 --since 2020-02-01 twitter-search \"$GME until:2021-02-02\" > text-query-tweets.json")

def pullStockTweets(stock, since, until):
    stock = str(stock).upper()
    stock_tweet = "$" + str(stock)
    call = ""
    if platform == "win32":
        call = "snscrape --jsonl twitter-search \"" + str(stock_tweet) + " since:" + str(since) + " until:" + str(until) + "\"> function-tweets.json"
        # do windows stuff
        os.system(call)
        print("done")
    else:
        call = "snscrape --jsonl twitter-search '" + str(stock_tweet) + " since:" + str(since) + " until:" + str(until) + "'> function-tweets.json"
        os.system(call)
        print("done")
    return(pd.read_json('function-tweets.json', lines = True))
        # do unix stuff


gme = pullStockTweets("gMe", "2021-02-14", "2021-02-17")

# Creating finction to scrape stock ticker by name (done with snscrape)
# Function needs to include windows, linux,or OSX
# Formatting content to sentament able material
#Look into date range specification
#Look into plotting sentiments against stock reacton.
gme.head()

def StokTickerValue(stock):
    stock_link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(stock) + "&apikey=" + "R0GH7135BX9T3R6F" + "&datatype=csv&outputsize=full"
    stock_value = pd.read_csv(str(stock_link))
    return(stock_value)

GME = StokTickerValue("GME")

GME.head()

type(GME.timestamp)
datetime.strptime(GME.timestamp[1], '%Y-%m-%d')
GME.close[GME.timestamp == maybe]
maybe = pd.date_range(start="2019-09-09",end="2019-09-10")
print(maybe)
