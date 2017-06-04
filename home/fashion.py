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


def Scrape_bussiness_of_fashion():
    url="https://www.businessoffashion.com/articles/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html_base=response.content
    soup_base=BeautifulSoup(html_base,"html.parser")
    soup_base=soup_base.find("div",{"class":"col-md-17"})
    soup_base=soup_base.find("div",{"class":"hidden-xs"})
    newslinks=soup_base.findAll("div",{"class":"panel-article"})
    articles=[]
    for link in newslinks:
        headline=link.find("h3",{"class":"h2"}).text
        headline=headline.strip()
        d=link.findAll("span")
        date=d[0].text
        date=date.strip()
        author=d[1].text
        author=author.strip()
        description=link.findAll("trust")[1]
        if len(description.text)>12:
            description=description.text.strip()
        else:
            description=" "
        articleurl="https://www.businessoffashion.com"+str(link.find("a",{"class":"hover-no-underline"})['href'])
        urlToImage=link.find("img")['src']
        urlToImage=urlToImage.split("?")[0]
        article={"author":author,"title":headline,"description":description,"url":articleurl,"urlToImage":urlToImage,"publishedAt":date}
        articles.append(article)

    response={"source":"www.businessoffashion.com","articles":articles}
    response=json.dumps(response)

    data=json.loads(response)
    source= data["source"].encode('utf-8')
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
                    a=Post(source=articlesource,author=author,headline=headline,story=story,link=image_url,date=date,pageurl=url)

                    # Save the temporary image to the model#
                    # This saves the model so be sure that is it valid
                    a.image.save(file_name, files.File(lf))

