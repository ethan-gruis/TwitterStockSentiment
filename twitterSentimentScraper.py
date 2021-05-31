import pandas as pd
import re
import os
from sys import platform
from datetime import date, timedelta
import pysentiment2 as ps
from pandas._libs.tslibs.timestamps import Timestamp
import snscrape
import snscrape
import json
from bs4 import *
import requests

## EXAMPLE CODE: snscrape

# Using OS library to call CLI commands in Python
# tweet_count = 500
# os.system("snscrape --jsonl --max-results {} twitter-search '$GME'> user-tweets.json".format(tweet_count))

# mac:
#os.system("snscrape --jsonl twitter-search '$GME since:2021-03-01 until:2021-03-02'> tweets.json")

# windows:
# os.system("snscrape --jsonl --max-results 500 --since 2020-02-01 twitter-search \"$GME until:2021-02-02\" > text-query-tweets.json")


def pullStockTweets(stock, since = date.today() - timedelta(days = 8), until = date.today()):
    """Orchestrates the entirety of pulling together stock tweet sentiment & ticker values for the date range specified

    Args:
        stock: a string of a stock ticker (e.g. 'gme', 'aapl', etc.)
        since: the date the user would like to begin pulling tweets from, provided as a string (e.g. '2021-03-14')
               (default is 8 days before today's date if not specified)
        until: the date the user would like to end pulling tweet on, provided as a string (e.g. '2021-03-16')
               (default is today)

    Returns:
        DataFrame object with pivot table containing date range given, positive and negative sentiment, opening and closing stock values

    """
    stock = str(stock).upper()
    stock_tweet = "$" + str(stock)
    call = ""

    print('Pulling stock data for ticker: ' + stock_tweet)
    print('WARNING: this may take some time dependent on dates provided. Default: 1 week.')

    filename = 'data/' + str(stock) + str(since) + "-" + str(until) + ".json"
    if platform == "win32":
        call = "snscrape --jsonl twitter-search \"" + str(stock_tweet) + " since:" + str(since) + " until:" + str(until) + "\"> " + filename
        # do windows stuff
        os.system(call)
        win_path = os.getcwd() + '/' + filename
        data = pd.read_json(win_path, lines = True)
        print("Loaded stock tweet dataframe.")
    else:
        call = "snscrape --jsonl twitter-search '" + str(stock_tweet) + " since:" + str(since) + " until:" + str(until) + "'> " + filename
        os.system(call)
        unix_path = os.getcwd() + '/' + filename
        print(unix_path)
        data = pd.read_json(unix_path, lines = True)
        print("Loaded stock tweet dataframe")

    df_sent = getSentiment(data)
    df_pivot = makePivot(df_sent)
    df_pivot['ticker'] = stock_tweet
    stock_df= getStockTicker(stock)
    stock_merged = tickerSentMerge(df_pivot, stock_df)
    # if(stock_merged == 'ERROR: Majority Nulls in trading days, breaking function...'):
    #     print(stock_merged)
    #     return
    print('done!')
    # TODO: save stock_merged to csv and remove json
    csv_filename = filename[0:len(filename) - 5] + '.csv'
    stock_merged.to_csv(csv_filename, index = False)
    return(stock_merged)

def getSentiment(df, verbose = False):
    """Creates sentiment values from dataframe of scraped tweets and aggregates by date into a pivot table

    Args:
        df: a DataFrame object containing scraped tweets from snscrape

    Returns:
        df_pivot: a DataFrame object that is a pivot table of sentiment values by date

    """

    print('Fetching sentiment from stock tweets...')
    lm = ps.LM()
    df['Sent Tokenized'] = df.apply(lambda row: lm.tokenize(row['renderedContent']), axis = 1)
    df['Positive'] = df.apply(lambda row1: lm.get_score(row1['Sent Tokenized'])['Positive'], axis = 1)
    df['Negative'] = df.apply(lambda row2: lm.get_score(row2['Sent Tokenized'])['Negative'], axis = 1)
    return(df)

def makePivot(df):
    """Pivoting the sentiment tweet values to aggregate overall day value and unique dates

    Args:
        df: The data frame produced by the sentiment function of the twitter scrape


    Returns:
        The pivoted table including the Positive, Negative, and overall sentiment of tweets aggregated to a day.

    """

    print('Making pivot table of sentiment...')
    for i in range(0, len(df)):
        df.loc[i, 'strDate'] = str(df.loc[i, 'date'])[0:10]
    df_pivot = pd.pivot_table(df[['Positive', 'Negative', 'strDate']], index = 'strDate', aggfunc = 'sum')
    df_pivot['Overall'] = df_pivot['Positive'] - df_pivot['Negative']
    return(df_pivot)


def getStockTicker(stock):
    """Api call to pull coresponding ticker values based on the twitter scrape

    Args:
        stock: a string of a stock ticker (e.g. 'gme', 'aapl', etc.) occuring from the original input


    Returns:
        DataFrame object with stock value related to previous stock call

    """
    print('Grabbing stock ticker info...')
    stock_link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + str(stock) + "&apikey=" + "R0GH7135BX9T3R6F" + "&datatype=csv&outputsize=full"
    stock_value = pd.read_csv(str(stock_link))
    return(stock_value)

def tickerSentMerge(df, stock_df):
    """Merges sentiment values with stock ticker values for given date range

    Args:
        df: DataFrame containing sentiment values (pivot table dataframe)
        stock_df: DataFrame containig stock ticker values

    Returns:
        DataFrame object with pivot table containing date range given, positive and negative sentiment, opening and closing stock values
        filling all NA values with previous trading day

    """
    print('Merging stock ticker info with sentiment pivot...')
    stock_df['strDate'] = stock_df['timestamp']
    merged_ticker = df.merge(stock_df[['strDate','open','adjusted_close']], how = 'left', on = 'strDate')
    merged_ticker['dailyChange'] = merged_ticker['open'] - merged_ticker['adjusted_close']

    merged_ticker = handleErrors(stock_df, merged_ticker)

    return(merged_ticker)

def handleErrors(stock_df, merged_ticker):
    """Checks if stock tickers are NaN's for a majority of trading days given, if so throws errors and ends function

    Args:
        stock_df: stock_df for the check on needed values when creating the method to fill NAs
        merged_ticker: DataFrame of merged sentiment and ticker values

    Returns:
        DataFrame object or error check of the function. Returns filled DataFrame and Error message if non-trading days selected.

    """
    if(sum(pd.isnull(stock_df['adjusted_close'])) >= len(merged_ticker) - 1):
        err = "ERROR: Majority Nulls in trading days, breaking function..."
        return err
    else:
         for i in range(1, len(merged_ticker)):
             if(pd.isnull(merged_ticker.loc[i, 'adjusted_close'])):
                 merged_ticker.loc[i, 'adjusted_close'] = merged_ticker.loc[i-1, 'adjusted_close']
    if(sum(pd.isnull(stock_df['open'])) >= len(merged_ticker) - 1):
         err = "ERROR: Majority Nulls in trading days, breaking function..."
         return err
    else:
         for i in range(1, len(merged_ticker)):
             if(pd.isnull(merged_ticker.loc[i, 'open'])):
                 merged_ticker.loc[i, 'open'] = merged_ticker.loc[i-1, 'open']
    return(merged_ticker)

def scrapeTopPerformers():
    print('Attempting to scrape trading view...')
    site = 'https://www.tradingview.com/markets/stocks-usa/market-movers-active/'
    request = requests.get(site).text
    print('Request successful. Scraping....')

    # get html parser
    soup = BeautifulSoup(request,'html.parser')
    table = soup.find('table') # grab table
    table_rows = table.find_all('tr') # grab table rows

    ind = [] # create empty list

    for tr in table_rows: # iterate through rows
        td = tr.find_all('td') # find each cell in each row
        row = [tr.text for tr in td] # create text for each cell
        ind.append(row) # append text
        #print(row)
        #ind.append(tr.text)
    print('Scrape Complete. Cleaning Data...')
    # make into dataframe
    df = pd.DataFrame(ind,columns=['ticker', 'last', 'Percent change', 'Dollar change', 'Rating', 'Volumne', 'Mkt Cap', 'P/E', 'EPS', 'Num Employees', 'Sector'])

    # get rid of newlines and tabs in ticker
    df['ticker'] = df['ticker'].str.replace('[\\t\\n\\r]', ' ', regex=True)

    # split on spaces created
    new = df['ticker'].str.split('         ', expand = True)

    # new ticker col
    df['ticker'] = new[0]
    # new company col
    df['company'] = new[1]

    # get rid of excess spaces in ticker
    df['ticker'] = df['ticker'].str.replace(' ', '')
    df = df.iloc[1: , :]
    today = date.today()
    filename = 'data/' + str(today) + '_top100volume.csv'
    df['date'] = today
    print('Cleaning complete. Saving file as ' + filename)
    df.to_csv(filename, index = False)
    return df
