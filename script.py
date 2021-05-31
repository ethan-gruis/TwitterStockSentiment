# from twitterSentimentScraper import pullStockTweets, getSentiment, scrapeTopPerformers
from twitterSentObj import TwitterScraper, scrapeTopPerformers
import pandas as pd

df = scrapeTopPerformers()

top10 = df.head(10)



aapl = TwitterScraper('AAPL', '2021-05-12', '2021-05-13')

apple_pivot = aapl.getPivot()
apple_pivot
pullStockTweets('AAPL', '2021-05-16', '2021-05-17')

for i in top10['ticker']:
    big_df.append(pullStockTweets(i))


filename = "arg.json"
filename[0:len(filename) - 5]
