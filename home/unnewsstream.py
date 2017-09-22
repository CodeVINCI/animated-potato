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


def ScrapeUN():
    url= "http://unnewsstream.org/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    context = ssl._create_unverified_context()
    response = requests.get(url, headers=headers,context=context)
    html_base=response.content
    soup_base=BeautifulSoup(html_base,"html.parser")
    newslinks=soup_base.findAll("div",{"class":"news"})
    articles=[]
    for link in newslinks:
        try:
            urlToImage=link.find("div",{"class":"media-box-image"})
            urlToImage=urlToImage.findAll('div')[0]['data-thumbnail']

            title=link.find("div",{"class":"media-box-title"}).text+"."
            title=" ".join(title.split())
            try:
                description=link.find("div",{"class":"media-box-text"}).text
                description=" ".join(description.split())
            except:
                description=" "

            url=link.find("div",{"class":"media-box-title"}).find('a')['href']

            date=link.find("div",{"class":"media-box-date"})
            date=date.text
            date=date.strip()

            article={"author":"un-news-stream","title":title,"description":description,"url":url,"urlToImage":urlToImage,"publishedAt":date}
            articles.append(article)
        except:
            pass
    response={"source":"unnewsstream.org","articles":articles}
    response=json.dumps(response)

    data=json.loads(response)
    source= data["source"].encode('utf-8')
    category="UN"
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
                    request = requests.get(image_url, stream=True)

                    # Was the request OK?
                    if request.status_code != requests.codes.ok:
                    # Nope, error handling, skip file etc etc etc
                        continue

                    # Get the filename from the url, used for saving later
                    file_name = image_url.split('/')[-1]+".jpg"
                    if len(file_name)>50:
                        file_name=file_name[:50]+".jpg"

                    # Create a temporary file
                    lf = tempfile.NamedTemporaryFile()

                    # Read the streamed image in sections
                    for block in request.iter_content(1024 * 8):

                        # If no more file then stop
                        if not block:
                            break

                        # Write image block to temporary file
                        lf.write(block)

                    # Create the model you want to save the image to
                    a=Post(source=articlesource,author=author,headline=headline,story=story,link=image_url,date=date,pageurl=url,category=category)

                    # Save the temporary image to the model#
                    # This saves the model so be sure that is it valid
                    a.image.save(file_name, files.File(lf))


