from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# GEtting news from Times of India

times_of_India_res = requests.get("https://timesofindia.indiatimes.com/briefs")
times_of_India_soup = BeautifulSoup(times_of_India_res.content, 'html5lib')

articles = times_of_India_soup.find_all('div', {"class":"brief_box"})

times_of_India=[]
for art in articles:
        try:
                article=dict()
                article['urlToImage']=art.a.div.img['onerror'].split("'")[1]
                article['url']='https://timesofindia.indiatimes.com'+art.a['href']
                article['title']=art.h2.text
                article['description']=art.p.text[:100]
                times_of_India.append(article)
        except:
                pass

  
newsapi_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=4dbc17e007ab436fb66416009dfb59a8"
  
# fetching data in json format 
open_bbc_page = requests.get(newsapi_url).json() 

articles = open_bbc_page["articles"]

newsapi=[]
for art in articles:
        article=dict()
        article['urlToImage']=art['urlToImage']
        article['url']=art['url']
        article['title']=art['title']
        article['description']=art['description']
        newsapi.append(article)

mn=min(len(times_of_India),len(newsapi))
times_of_India=times_of_India[:mn]
newsapi=newsapi[:mn]

def index(req):
    return render(req, 'news/index.html', {'toi_news':times_of_India, 'newsapi_news':newsapi})