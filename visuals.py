import seaborn as sns
from twitterSentimentScraper import pullStockTweets
import pandas as pd

gme = pullStockTweets('gme', '2021-02-16', '2021-03-16')

gme
gme.to_csv('gme_month_sent.csv')


aapl = pullStockTweets('aapl')
aapl

aapl.to_csv('aapl_sent.csv', index = False)

gme_tweets = pd.read_json('gme_2_16to3_16_tweets.json', lines = True)
