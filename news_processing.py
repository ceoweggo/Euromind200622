import sys
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
from datetime import date, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import config
import datetime

sia = SentimentIntensityAnalyzer()
#nltk.download('vader_lexicon')
pd.set_option('display.max_colwidth', 1000)

# Get News sources
def GetSources(category = None):
    newsapi = NewsApiClient(api_key='2bb538255a2047efb9c9593b9f94d4ae')
    sources = newsapi.get_sources()
    if category is not None:
        rez = [source['id'] for source in sources['sources'] if source['category'] == category and source['language'] == 'en']
    else:
        rez = [source['id'] for source in sources['sources'] if source['language'] == 'en']
    return rez
print(GetSources('business'))

def GetArticlesSentiments(keyword, startd, sources_list = None, show_all_articles =  False):
    newsapi = NewsApiClient(api_key=config.API_KEY)
    if type(startd) == str:
        mydate = datetime.datetime.strptime(startd, '%Y-%m-%d')
    else:
        mydate = startd
    if sources_list:
        articles = newsapi.get_everything(q = keyword, from_param = mydate.isoformat(),
            to = (mydate + timedelta(days = 1)).isoformat(), language="en", 
            sources = ",".join(sources_list), sort_by="relevancy", page_size = 100)
    else:
        articles = newsapi.get_everything(q = keyword, from_param = mydate.isoformat(), 
        to = (mydate + timedelta(days=1)).isoformat(), 
        language="en", sort_by = "relevancy", page_size=100)
        #print(articles)
    
    article_content = ''
    seen = set()
    i = 0
    pos = list()
    neg = list()
    neu = list()
    compound = list() 
    content = list()
    for article in articles['articles']:
        if str(article['title']) in seen:
            continue
        else:
            seen.add(str(article['title']))
        article_content = str(article['title']) + '. ' + str(article['description'])
        # Get the sentiment score
        comp = sia.polarity_scores(article_content)['compound']
        positive = sia.polarity_scores(article_content)['pos']
        negative = sia.polarity_scores(article_content)['neg']
        neutral = sia.polarity_scores(article_content)['neu']
        compound.append(comp)
        pos.append(positive)
        neg.append(negative)
        neu.append(neutral)
        content.append(article_content)
    return pos,neu,neg,compound, content
    
sources = GetSources('business')
pos, neu, neg, compound, context = GetArticlesSentiments(keyword='stock', startd='2022-05-28', sources_list=sources, show_all_articles=True )

