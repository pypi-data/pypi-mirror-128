import newspaper
from newspaper import Article

# url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'

def text_extraction(url):
    article = Article(url)
    
    article.download()
    article.parse()
    
    text = article.text
    text = text.replace("\n\n"," ") # '\n' -> ''
    
    return text
