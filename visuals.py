from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from twitterSentimentScraper import pullStockTweets, getSentiment
import pandas as pd
import datetime

# GET GME Tweets
# gme = pullStockTweets('gme', '2021-02-16', '2021-03-16')
# gme.to_csv('gme_month_sent.csv')

# GET AAPL Tweets
aapl = pullStockTweets('aapl')
aapl.head(9)
# aapl.to_csv('aapl_sent.csv', index = False)


gme_tweets = pd.read_json('../gme_2_16to3_16_tweets.json', lines = True)

sent_gme = getSentiment(gme_tweets, verbose = True)


pos_tweets = sent_gme.sort_values(by='Positive', ascending=False)
neg_tweets = sent_gme.sort_values(by='Negative', ascending=False)

pos_tweets.head(10).to_csv('./data/top5posGME.csv', index = False)
neg_tweets.head(10).to_csv('./data/top5negGME.csv', index = False)

gme = pd.read_csv('./data/gme_month_sent.csv')
gme['date'] = gme['strDate'].astype('datetime64[ns]')
gme['Daily Change'] = gme['adjusted_close'] - gme['open']


## RUN LINES 34-54 TOGETHER TO GET PLOT
# plot sentiment against the date over date range
####################              CODE BLOCK            ########################
sns.set_palette('Set1')
ax = sns.lineplot(
    data = gme,
    x = "date", y = 'Overall'
)

# format dates
ax.set_xlim(gme['date'].min(), gme['date'].max())
myFmt = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(myFmt)
for item in ax.get_xticklabels():
    item.set_rotation(45)

# theme & titles
sns.set_style('whitegrid')
sns.set_context("notebook", font_scale=1.10, rc={"lines.linewidth": 2.5})
ax.set_title("Overall Twitter Sentiment of GME Over Time")
ax.set_xlabel('Date')
ax.set_ylabel('Overall Twitter Sentiment')
plt.tight_layout() # the fact that this is necessary is trash, i hate matplotlib
plt.show()
################################################################################

fig = ax.get_figure()
fig.savefig('./images/sentimentOverTime.png', dpi = 400)


# plot daily sentiment vs change in ticker value

####################              CODE BLOCK            ########################
sns.set_palette('Set3')
ax = sns.lineplot(
    data = gme,
    x = "date", y = 'Daily Change',
    palette = 'Paired'
)
# format dates
ax.set_xlim(gme['date'].min(), gme['date'].max())
myFmt = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(myFmt)
for item in ax.get_xticklabels():
    item.set_rotation(45)

# theme & titles
sns.set_style('whitegrid')
sns.set_context("notebook", font_scale=1.10, rc={"lines.linewidth": 2.5})
ax.set_title("GME: Daily Change (Close - Open) Value")
# ax.set_xlabel('Date')
ax.set_ylabel('Daily Change')
plt.tight_layout()
plt.show()
################################################################################

fig = ax.get_figure()
fig.savefig('./images/dailyChange.png', dpi = 400)
