from datetime import date, timedelta
import pandas as pd
import streamlit as st
import re
import os
from sys import platform
import snscrape
# !pipenv install twitter_scraper


def pullStockTweets(stock, since = date.today() - timedelta(days = 8), until = date.today()):
    call = ""
    st.write("WARNING: depending on the ticker and dates given, it may take some time to download tweets")
    st.write('Pulling stock info for ' + str(stock) + '...')
    # print("WARNING: depending on the ticker and dates given, it may take some time to download tweets")
    # print("Pulling stock info for " + str(stock) + "...")
    if platform == "win32":
        call = "snscrape --jsonl twitter-search \"" + str(stock) + " since:" + str(since) + " until:" + str(until) + "\"> function-tweets.json"
        # do windows stuff
        st.write(call)
        os.system(call)
        st.write("done")
    else:
        call = "snscrape --jsonl twitter-search \'" + str(stock) + " since:" + str(since) + " until:" + str(until) + "\'> function-tweets.json"
        st.write(call)
        os.system(call)
        st.write("done")
    return(pd.read_json('function-tweets.json', lines = True))

def main():
    st.title('hi.')
    #frame_queue = pullStockTweets()
    value = st.text_input("Some input")
    if value:
        value
        df = pullStockTweets(str(value))
        df

main()
os.system("snscrape --jsonl twitter-search '$GME since:2021-03-07 until:2021-03-15'> function-tweets.json")


# REORDER TO GET DATA FIRST THEN RUN STREAMLIT
