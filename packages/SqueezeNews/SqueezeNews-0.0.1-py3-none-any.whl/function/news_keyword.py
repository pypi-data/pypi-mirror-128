import newspaper
from newspaper import Article
from newspaper.api import languages
import nltk
nltk.download('punkt')
from news_url_import import news_url_import

# 단어의 빈도수를 기반으로 10개의 키워드를 반환.

def get_keyword(url, language):
    article = Article(url, language = language)
    article.download()
    article.parse()
    article.nlp()

    keywords = article.keywords
    return keywords[:10]

# # test
# news_dict = news_url_import('강아지',10)
# news_url =news_dict[2]['url']
# mykeyword = get_keyword(news_url,'ko')
# print(mykeyword)
