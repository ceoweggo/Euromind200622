from gnews import GNews
import json, os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newspaper import Article
import pandas as pd

sia = SentimentIntensityAnalyzer()
#nltk.download('vader_lexicon')
pd.set_option('display.max_colwidth', 1000)


# Get News sources


def ScrapInfoFromPage(brand):
    files = os.listdir("news/")
    #print(files)
    articles = list()
    with open(f"news/{brand}.json", 'r', ) as file:
        data = json.load(file)
        for i in data:
            toi_article = Article(i['url'], language="en")
            if toi_article.is_valid_url:
                try:
                    toi_article.download()
                    toi_article.parse()
                    #print(toi_article.text)
                    articles.append(toi_article.text)
                except:
                    pass
    return articles

def GetArticlesSentiments(keyword, show_all_articles =  False):
    article_content = ''
    seen = set()
    i = 0
    pos = list()
    neg = list()
    neu = list()
    compound = list() 
    content = list()
    article = ScrapInfoFromPage(keyword)
    for article_content in article:
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

with open('quotes.json') as file:
    data = json.load(file)

    symbols_list = []
    for symbol_name in data:
        pos, neu, neg, compound, context = GetArticlesSentiments(keyword=symbol_name['symbol'],  show_all_articles=True )
        print(symbol_name['symbol'])
        print("pos")
        for p in pos:
            print(p)
        print("neg")
        for n in neg:
            print(n)