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
import config

class TwitterScraper():
    """An object that scrapes tweets, currently stock tickers, based on a given string and date range.

    Scrapes twitter using snscrape backend, combined with alphavantage API for up to date stock info, this is a valuable
    tool for stock analysis and aggregating social media stock sentiment over time.
    """

    def __init__(self, stock, startDate = date.today() - timedelta(days = 8), endDate = date.today()):
        """Initializes all facets of the object:

        df: raw twitter data pulled in from twitter.json file
        pivot:     (pandas DataFrame) pivot table of day by day stock data
        stockData: (pandas DataFrame) full stock data for date range from alphaVantage
        stock:     (string) stock name
        startDate: (string) starting date in YYYY/MM/DD format ex: '2021-02-16'
        endDate:   (string) ending date in YYYY/MM/DD format
        fileName:  (string) name of the output json file, predetermined based on stock name
        csv:       (string) name of output csv file, predetermined based on stock name
        platform:  (sys) determines whether to build OS call in unix based or windows based CMD
        """

        self.df = pd.DataFrame()
        self.pivot = pd.DataFrame()
        self.stockData = pd.DataFrame()
        self.stock = str(stock).upper()
        self.startDate = str(startDate)
        self.endDate = str(endDate)
        self.fileName = 'data/json/' + self.stock + self.startDate + "-" + self.endDate + ".json"
        self.csv = 'data/csv/sent/' + self.stock + '-' + self.startDate + "-" + self.endDate + '.csv'
        self.platform = platform
        self.__getStockTicker__()
        self.__fetch__()


    def __fetch__(self):
        print('Formulating call..')
        if(self.platform == 'win32'):
            call = "snscrape --jsonl twitter-search \"" + '$' + self.stock + " since:" + self.startDate + " until:" + self.endDate + "\"> " + self.fileName
        else:
            call = "snscrape --jsonl twitter-search '" + '$' + self.stock + " since:" + self.startDate + " until:" + self.endDate + "'> " + self.fileName
        print('Fetching call... this make take some time')
        os.system(call)
        path = os.getcwd() + '/' + self.fileName
        print(path)
        self.df = pd.read_json(path, lines = True)
        print('fetched data')
        self.__getSentiment__()
        self.cleanUp()

    def __getSentiment__(self):
        print('Fetching sentiment from stock tweets...')
        lm = ps.LM()
        print('Tokenizing...')
        self.df['Sent Tokenized'] = self.df.apply(lambda row: lm.tokenize(row['renderedContent']), axis = 1)
        print('Getting positive sentiment')
        self.df['Positive'] = self.df.apply(lambda row1: lm.get_score(row1['Sent Tokenized'])['Positive'], axis = 1)
        print('Getting negative sentiment')
        self.df['Negative'] = self.df.apply(lambda row2: lm.get_score(row2['Sent Tokenized'])['Negative'], axis = 1)
        print('Successly processed sentiment')
        print()
        self.__makePivot__()

    def __makePivot__(self):
        print('Making pivot table of sentiment...')
        for i in range(0, len(self.df)):
            self.df.loc[i, 'strDate'] = str(self.df.loc[i, 'date'])[0:10]
        self.pivot = pd.pivot_table(self.df[['Positive', 'Negative', 'strDate']], index = 'strDate', aggfunc = 'sum')
        self.pivot['Overall'] = self.pivot['Positive'] - self.pivot['Negative']
        self.pivot['ticker'] = self.stock
        print('Successfully created pivot table.')
        self.__tickerSentMerge__()

    def __getStockTicker__(self):
        print('Grabbing stock ticker info...')
        stock_link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + self.stock + "&apikey=" + config.api_key + "&datatype=csv&outputsize=full"
        self.stockData = pd.read_csv(str(stock_link))
        print('Fetched stock ticker data.')
        print()

    def __tickerSentMerge__(self):
        print('Merging stock ticker info with sentiment pivot...')
        self.stockData['strDate'] = self.stockData['timestamp']
        self.pivot = self.pivot.merge(self.stockData[['strDate','open','high', 'low', 'close']], how = 'left', on = 'strDate')
        self.pivot['dailyChange'] = self.pivot['close'] - self.pivot['open']
        print("Done")
        # merged_ticker = handleErrors(stock_df, merged_ticker)

    def getPivot(self):
        self.pivot.to_csv(self.csv)
        return(self.pivot)

    def cleanUp(self):
        os.remove(self.fileName)

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
        # print(row)
        # ind.append(tr.text)
    print('Scrape Complete. Cleaning Data...')
    # make into dataframe
    df = pd.DataFrame(ind,columns=['ticker', 'last', 'Percent change', 'Dollar change', 'Rating', 'Volumne', 'Ignore', 'Mkt Cap', 'P/E', 'EPS', 'Num Employees', 'Sector'])

    # # get rid of newlines and tabs in ticker
    df['ticker'] = df['ticker'].str.replace('[\\t\\n\\r]', ' ', regex=True)
    df['ticker'] = df['ticker'].str.findall(r'(\w+)')
    for i in range(0,len(df.index)):
        if(len(str(df['ticker'].str[0][i])) == 1):
            df.iloc[i]['ticker'] = df['ticker'].str[1][i]
        else:
            df.iloc[i]['ticker'] = df['ticker'].str[0][i]
    
    # get rid of excess spaces in ticker
    df['ticker'] = df['ticker'].str.replace(' ', '')
    df = df.iloc[1: , :]
    today = date.today()
    filename = 'data/csv/topPerformers/' + str(today) + '_top100volume.csv'
    df['date'] = today
    print('Cleaning complete. Saving file as ' + filename)
    df.to_csv(filename, index = False)
    return df
