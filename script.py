# from twitterSentimentScraper import pullStockTweets, getSentiment, scrapeTopPerformers
from twitterSentObj import TwitterScraper, scrapeTopPerformers
import pandas as pd

df = scrapeTopPerformers()

top10 = df.head(10)
top10
big_df = pd.DataFrame(columns = {'strDate', 'Negative', 'Positive', 'Overall', 'ticker', 'open', 'adjusted_close', 'dailyChange'})
for i in top10['ticker']:
    print(i)
    big_df.append(TwitterScraper(i).getPivot())



