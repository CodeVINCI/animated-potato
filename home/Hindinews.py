import urllib
import json
import ssl
import bs4
from bs4 import BeautifulSoup
import re
import time
from home.models import Post
import requests
import tempfile
from django.core import files
from django.utils import timezone


#function for gaoconnection news scraping
def Scrape_gaoconnection_home():
    url = "https://www.gaonconnection.com/"
    context = ssl._create_unverified_context()
    response = requests.get(url, headers=headers,context=context)
    html_base=response.content
    soup_base=BeautifulSoup(html_base,"html.parser")
    soup_base=soup_base.find("div",{"class":"list-article"})
    newslinks=soup_base.findAll("article",{"class":"list-article"})
    articles=[]
    for link in newslinks:
        try:
            articleurl=url+str(link.a['href'])
            #print articleurl
            title=link.find("div",{"class":"list-article__content"}).find("a").find("h3").text
            #print title
            urlToimage=str(link.find("a").find("div",{"class":"list-article__image-container"}).find("figure").img["src"])
            #print urlToimage
            description = link.find("div",{"class":"list-article__content"}).find("a").find("p").text
            #print description
            author=link.find("div",{"class":"list-article__content"}).find("div",{"class":"list-article__byline"}).find("span").find("a").text
            #print author
            article={"author":author,"title":title,"description":description,"url":articleurl,"urlToImage":urlToimage,"publishedAt":None}
            articles.append(article)
        except:
            pass
    response={"source":"dainik-bhaskar","articles":articles}
    response=json.dumps(response)
    articlesave(response)

#function for dainikjagran news scraping
def Scrape_dainik_jagran():
    url= "http://www.jagran.com/top-news.html?src=eptn"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    context = ssl._create_unverified_context()
    response = requests.get(url, headers=headers,context=context)
    html_base=response.content
    soup_base=BeautifulSoup(html_base,"html.parser")
    soup_base=soup_base.find("ul",{"id":"grid"})
    newslinks=soup_base.findAll("li")
    articles=[]
    for link in newslinks:
        try:
            articleurl= "http://www.jagran.com"+link.find('a')['href']
            urlToImage= link.find('a').img['src']
            title= link.find('a')['title']
            title=" ".join(title.split())
            description=" "
            article={"author":"jagran.com","title":title,"description":description,"url":articleurl,"urlToImage":urlToImage,"publishedAt":None}
            articles.append(article)
        except:
            pass
    response={"source":"dainik-jagran","articles":articles}
    response=json.dumps(response)
    articlesave(response)


def articlesave(response):

    data=json.loads(response)
    source= data["source"].encode('utf-8')
    category="hindi"
    articles=data["articles"]
    for article in articles:
        storedarticles=Post.objects.filter(headline=article["title"].encode('utf-8'))
        if len(storedarticles)==0:
                articlesource=source
                if article["author"]==None:
                    author="Anonymous"
                else:
                    author=article["author"].encode('utf-8')
                headline=article["title"].encode('utf-8')
                story=article["description"].encode('utf-8')
                url=article["url"].encode('utf-8')
                if article["publishedAt"]==None:
                    date= str(timezone.now())
                    date=date[:10]
                else:
                    date= str(timezone.now())
                    date=date[:10]
                if not(article['urlToImage']==None):
                    image_url=article["urlToImage"].encode('utf-8')
                    a=Post(source=articlesource,author=author,headline=headline,story=story,link=image_url,date=date,pageurl=url,category=category)
                    a.save()
                    #request = requests.get(image_url, stream=True)
                    #time.sleep(2)
                    # Was the request OK?
                    #if request.status_code != requests.codes.ok:
                    # Nope, error handling, skip file etc etc etc
                    #    continue

                    # Get the filename from the url, used for saving later
                    #file_name = image_url.split('/')[-1]+".jpg"
                    #if len(file_name)>50:
                    #    file_name=file_name[:50]+".jpg"

                    # Create a temporary file
                    #lf = tempfile.NamedTemporaryFile()

                    # Read the streamed image in sections
                    #for block in request.iter_content(1024 * 8):

                        # If no more file then stop
                    #    if not block:
                    #        break

                        # Write image block to temporary file
                    #    lf.write(block)

                    # Create the model you want to save the image to
               

                    # Save the temporary image to the model#
                    # This saves the model so be sure that is it valid
                    #a.image.save(file_name, files.File(lf))




#function for amarujala news scraping
def Scrap_amarujala():
    url = "http://www.amarujala.com/search?search=top%20news"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    context = ssl._create_unverified_context()
    response = requests.get(url, headers=headers,context=context)
    html_base=response.content
    soup_base=BeautifulSoup(html_base,"html.parser")
    soup_base=soup_base.find("div",{"id":"allDiv"})
    newslinks=soup_base.findAll("div",{"class":"mostRdr"})
    articles=[]
    for link in newslinks:
        try:
            articleurl="http://www.amarujala.com"+str(link.find("section",{"class":"pd10"}).find('h3').a['href'])
            title=link.find("section",{"class":"pd10"}).find('h3').find('a').text
            urlToimage="http:"+str(link.find("section",{"class":"pd10"}).find("div",{"class":"imgDv"}).img['data-src'])
            description = link.find("section",{"class":"pd10"}).find("div",{"class":"desc"}).text
            articleurl=articleurl.strip()
            urlToImage=urlToimage.strip()
            title=title.strip()
            description=description.strip()
            article={"author":"amarujala.com","title":title,"description":description,"url":articleurl,"urlToImage":urlToImage,"publishedAt":None}
            articles.append(article)
        except:
            pass
    response={"source":"amarujala","articles":articles}
    response=json.dumps(response)
    articlesave(response)

def Scrape_hindustan():
    url = "http://www.livehindustan.com/national/news"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    context = ssl._create_unverified_context()
    response = requests.get(url, headers=headers, context = context)
    html_base=response.content
    soup_base=BeautifulSoup(html_base,"html.parser")
    soup_base=soup_base.find("ul",{"class":"right-top-news"})
    newslinks=soup_base.findAll("li")
    articles=[]
    for link in newslinks:
        try:
            maincol=link.find("div",{"class":"col-md-12"})
            articleurl= "http://www.livehindustan.com/"+str(maincol.find("div",{"class":"upper-first"}).find('a')['href'])
            urlToImage= maincol.find("div",{"class":"upper-first"}).find('a').img['src']
            title= maincol.find("div",{"class":"upper-first"}).find("h4",{"class":"hindustan-link"}).find('a').text
            description= maincol.find("div",{"class":"upper-first"}).find("div",{"class":"list-time-tags"}).find('p').text
            date= maincol.find("div",{"class":"upper-first"}).find("div",{"class":"list-time-tags"}).find('span').text
            articleurl=articleurl.strip()
            urlToImage=urlToImage.strip()
            title=title.strip()
            description=description.strip()
            date=date.strip()
            article={"author":"hindustan.com","title":title,"description":description,"url":articleurl,"urlToImage":urlToImage,"publishedAt":date}
            articles.append(article)
        except:
            pass
    response={"source":"livehindustan.com","articles":articles}
    response=json.dumps(response)
    articlesave(response)

