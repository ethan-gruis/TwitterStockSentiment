# !python --version
# !pip install git+https://github.com/JustAnotherArchivist/snscrape.git
#!pip3 install --upgrade git+https://github.com/JustAnotherArchivist/snscrape@master

import pandas as pd
import re
import os
from sys import platform
from datetime import date, timedelta
import pysentiment2 as ps
from pandas._libs.tslibs.timestamps import Timestamp



## EXAMPLE CODE

# Using OS library to call CLI commands in Python
# tweet_count = 500
# os.system("snscrape --jsonl --max-results {} twitter-search '$GME'> user-tweets.json".format(tweet_count))

# mac:
# os.system("snscrape --jsonl twitter-search '$GME since:2021-03-01 until:2021-03-02'> tweets.json")

# windows:
# os.system("snscrape --jsonl --max-results 500 --since 2020-02-01 twitter-search \"$GME until:2021-02-02\" > text-query-tweets.json")


def pullStockTweets(stock, since = date.today() - timedelta(days = 8), until = date.today()):
    stock = str(stock).upper()
    stock_tweet = "$" + str(stock)
    print('Pulling stock data for ticker: ' + stock_tweet)
    print('WARNING: this make take some time dependent on dates provided. Default: 1 week.')
    call = ""

    if platform == "win32":
        call = "snscrape --jsonl twitter-search \"" + str(stock_tweet) + " since:" + str(since) + " until:" + str(until) + "\"> function-tweets.json"
        # do windows stuff
        os.system(call)
        print("Loaded stock tweet dataframe.")
    else:
        call = "snscrape --jsonl twitter-search '" + str(stock_tweet) + " since:" + str(since) + " until:" + str(until) + "'> function-tweets.json"
        os.system(call)
        print("Loaded stock tweet dataframe")
    data = pd.read_json('/Users/ethangruis/Documents/Unstructured/python/stocktwitterproj/function-tweets.json', lines = True)
    sentiment_pivot = getSentiment(data)
    sentiment_pivot['ticker'] = stock_tweet
    print('done!')
    return(sentiment_pivot)
        # do unix stuff

def getSentiment(df):
    print('Fetching sentiment from stock tweets...')
    lm = ps.LM()
    for i in range(0, len(df)):
        sentence_token = lm.tokenize(df['renderedContent'][i])
        score = lm.get_score(sentence_token)
        df.loc[i, 'Positive'] = score['Positive']
        df.loc[i, 'Negative'] = score['Negative']
    df_pivot = makePivot(df)
    return(df_pivot)

def makePivot(df):
    print('Making pivot table of sentiment...')
    for i in range(0, len(df)):
        df.loc[i, 'strDate'] = str(df.loc[i, 'date'])[0:10]
    df_pivot = pd.pivot_table(df[['Positive', 'Negative', 'strDate']], index = 'strDate', aggfunc = 'sum')
    df_pivot['overall'] = df_pivot['Positive'] - df_pivot['Negative']
    return(df_pivot)



aapl = pullStockTweets('aapl', '2021-03-08', '2021-03-10')
aapl

# data=pd.read_json('function-tweets.json', lines = True)

# put code here







gme.tail()

lm = ps.LM()
sentence_token = lm.tokenize(gme['renderedContent'][0])
sentence_token
for i in range(0, len(gme)):
    sentence_token = lm.tokenize(gme['renderedContent'][i])
    score = lm.get_score(sentence_token)
    gme.loc[i, 'Positive'] = (score['Positive'])
    gme.loc[i, 'Negative'] = (score['Negative'])


gme[['content', 'Positive','Negative']]

gme['Positive'].mean()

gme['Negative'].mean()

# Creating finction to scrape stock ticker by name (done with snscrape)
# Function needs to include windows, linux,or OSX
# Formatting content to sentament able material
#Look into date range specification
#Look into plotting sentiments against stock reacton.


def StockTickerValue(stock):
    stock_link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + str(stock) + "&apikey=" + "R0GH7135BX9T3R6F" + "&datatype=csv&outputsize=full"
    stock_value = pd.read_csv(str(stock_link))
    return(stock_value)

AAPL = StockTickerValue('AAPL')

type(AAPL['timestamp'][0])

ov_stock = sentiment_pivot.merge(stock_value[['strDate','open', 'adjusted_close']], how = 'left', on = 'strDate')

for i in range(1, len(ov_stock)):
    if((ov_stock.loc(i, 'adjusted_close').isnan()):
        ov_stock.loc(i, 'adjusted_close') = ov_stock.loc(i-1, 'adjusted_close')

GME = StokTickerValue("GME")

GME.head()


GME['date'] = pd.to_datetime(GME['timestamp'], format='%Y-%m-%d')

# for i in range(0, len(GME)):
#     GME.loc[i, 'date_actual'] = GME['date'][i].to_pydatetime()

type(GME['timestamp'][0])
print(GME['timestamp'][0])
print((str(gme['date'][5000]))[0:10])

if(GME['timestamp'][0] == str(gme['date'][5000])[0:10]):
    print('success')


gme['strDate'] = str(gme['date'])
gme['strDate'] = str(gme.loc[0, 'date'])[0:10]

for i in range(0, len(gme)):
    gme.loc[i, 'strDate'] = str(gme.loc[i, 'date'])[0:10]

gme_pivot = pd.pivot_table(gme[['Positive', 'Negative', 'strDate']], index = 'strDate', aggfunc = 'sum')

type(gme['Positive'][0])
gme_pivot['overall'] = gme_pivot['Positive'] - gme_pivot['Negative']
gme_pivot
