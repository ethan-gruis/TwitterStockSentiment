# from twitterSentimentScraper import pullStockTweets, getSentiment, scrapeTopPerformers
from twitterSentObj import TwitterScraper, scrapeTopPerformers
import pandas as pd

df = scrapeTopPerformers()

df['Percent change'] = pd.to_numeric(df['Percent change'].str.slice(stop = -1))
df['Dollar change'] = pd.to_numeric(df['Dollar change'])
# TODO: date checks? check yesterday's top performers, two days ago, etc, look into file saving methods and match w/ date library

df.sort_values(by = ['Percent change'], ascending = False)
big_df = pd.DataFrame(columns = {'strDate', 'Negative', 'Positive', 'Overall', 'ticker', 'open', 'adjusted_close', 'dailyChange'})
for i in top10['ticker']:
    print(i)
    big_df.append(TwitterScraper(i).getPivot())



