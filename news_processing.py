import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
from datetime import date, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
from numpy import MAY_SHARE_BOUNDS
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
    date_sentiments = {}
    date_sentiments_list = []
    seen = set()
    for article in articles['articles']:
        if str(article['title']) in seen:
            continue
        else:
            seen.add(str(article['title']))
        article_content = str(article['title']) + '. ' + str(article['description'])
        # Get the sentiment score
        sentiment = sia.polarity_scores(article_content)['compound']
        
        date_sentiments.setdefault(mydate, []).append(sentiment)
        date_sentiments_list.append((sentiment, article['url'], article['title'], article['description']))
        date_sentiments_l = sorted(date_sentiments_list, key = lambda tup: tup[0],reverse=True)
        sent_list = list(date_sentiments.values())[0]
        # Return a dataframe with all sentiment scores and articles
    return pd.DataFrame(date_sentiments_list, columns=['Sentiment','URL', 'Title','Description'])
sources = GetSources('business')
return_articles = GetArticlesSentiments(keyword='stock', startd='2022-05-24', sources_list=sources, show_all_articles=True )
#print(type(return_articles))
return_articles.Sentiment.hist(bins=30,grid=False)
return_articles.sort_values(by='Sentiment', ascending=True)[['Sentiment','URL']].head(5)

print(return_articles.Sentiment.mean())
print(return_articles.Sentiment.count())
print(return_articles.Description)