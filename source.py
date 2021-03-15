# !python --version
#!pip install git+https://github.com/JustAnotherArchivist/snscrape.git
#!pip3 install --upgrade git+https://github.com/JustAnotherArchivist/snscrape@master


import pandas as pd
import re
import os
from sys import platform
from datetime import date, timedelta
import pysentiment2 as ps


def pullStockTweets(stock, since = date.today() - timedelta(days = 8), until = date.today()):
    call = ""
    st.write("WARNING: depending on the ticker and dates given, it may take some time to download tweets")
    st.write('Pulling stock info for ' + str(user_input) + '...')
    # print("WARNING: depending on the ticker and dates given, it may take some time to download tweets")
    # print("Pulling stock info for " + str(stock) + "...")
    if platform == "win32":
        call = "snscrape --jsonl twitter-search \"" + str(stock) + " since:" + str(since) + " until:" + str(until) + "\"> function-tweets.json"
        # do windows stuff
        os.system(call)
        print("done")
    else:
        call = "snscrape --jsonl twitter-search '" + str(stock) + " since:" + str(since) + " until:" + str(until) + "'> function-tweets.json"
        os.system(call)
        print("done")
    return(pd.read_json('function-tweets.json', lines = True))
        # do unix stuff

st.title('Tweet Sentiment Analysis - Stock Tickers')

user_input = st.text_input("Input stock ticker here:", 'Please include a $, like $this')

if st.button('Say hello'):
    pullStockTweets(user_input)


## EXAMPLE CODE

# Using OS library to call CLI commands in Python
# tweet_count = 500
# os.system("snscrape --jsonl --max-results {} twitter-search '$GME'> user-tweets.json".format(tweet_count))

# mac:
# os.system("snscrape --jsonl twitter-search '$GME since:2021-03-01 until:2021-03-02'> tweets.json")

# windows:
# os.system("snscrape --jsonl --max-results 500 --since 2020-02-01 twitter-search \"$GME until:2021-02-02\" > text-query-tweets.json")



gme = pullStockTweets("$GME")

test1 = pullStockTweets("AAPL", "2021-03-10", "2021-03-11")

# Creating finction to scrape stock ticker by name (done with snscrape)
# Function needs to include windows, linux,or OSX
# Formatting content to sentament able material
#Look into date range specification
#Look into plotting sentiments against stock reacton.


# gme.head()
#
# lm = ps.LM()
# sentence_token = lm.tokenize(gme['renderedContent'][0])
# sentence_token
# for i in range(0, len(gme)):
#     sentence_token = lm.tokenize(gme['renderedContent'][i])
#     score = lm.get_score(sentence_token)
#     gme.loc[i, 'Positive'] = (score['Positive'])
#     gme.loc[i, 'Negative'] = (score['Negative'])
#
#
# gme[['content', 'Positive','Negative']]
#
# gme['Positive'].mean()
#
# gme['Negative'].mean()
