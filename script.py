# from twitterSentimentScraper import pullStockTweets, getSentiment, scrapeTopPerformers
from twitterSentObj import TwitterScraper, scrapeTopPerformers
import pandas as pd


df = scrapeTopPerformers()

top10 = df.head(100)

top10

aapl = TwitterScraper('NVDA', '2021-06-03', '2021-06-04')



apple_pivot = aapl.getPivot()
apple_pivot

amc_pivot = TwitterScraper('AMC', '2021-05-01', '2021-06-01')

big_df = pd.DataFrame(columns = {'strDate', 'Negative', 'Positive', 'Overall', 'ticker', 'open', 'adjusted_close', 'dailyChange'})
for i in top10['ticker']:
    big_df.append(TwitterScraper(i).getPivot())


filename = "arg.json"
filename[0:len(filename) - 5]
