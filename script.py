from twitterSentimentScraper import pullStockTweets, getSentiment, scrapeTopPerformers
import pandas as pd

df = scrapeTopPerformers()
top10 = df.head(10)

top10
big_df = pd.DataFrame(columns = {'Positive', 'Negative', 'strDate'})
big_df

pullStockTweets('AAPL')

for i in top10['ticker']:
    big_df.append(pullStockTweets(i))


filename = "arg.json"
filename[0:len(filename) - 5]
