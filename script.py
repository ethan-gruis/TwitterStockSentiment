# from twitterSentimentScraper import pullStockTweets, getSentiment, scrapeTopPerformers
from twitterSentObj import TwitterScraper, scrapeTopPerformers
import pandas as pd


def main():

    df = scrapeTopPerformers()

    top10 = df.head(10)
    top10
    twitter = TwitterScraper('TWTR', '2022-03-01', '2022-04-08')

    twitter_pivot = twitter.getPivot()

    twitter_pivot
    twitter_pivot['Perc Change'] = ((twitter_pivot['close'] - twitter_pivot['open']) / twitter_pivot['open']) * 100
    twitter_pivot


    apple_pivot
    pullStockTweets('AAPL', '2021-05-16', '2021-05-17')

    for i in top10['ticker']:
        big_df.append(pullStockTweets(i))


    filename = "arg.json"
    filename[0:len(filename) - 5]
