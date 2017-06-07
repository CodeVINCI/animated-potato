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

def Scrape_dainik_bhaskar():
    url= "http://www.jagran.com/"
    context = ssl._create_unverified_context()
    html_base=urllib.urlopen(url,context=context)
    soup_base=BeautifulSoup(html_base,"html.parser")
    newslinks=soup_base.findAll("ul",{"class":"tabbox"})
    articles=[]
    for link in newslinks:
         urlToImage=link.find("img")['src']
         urlToImage=urlToImage.split("?")[0]
         headline=link.find("span",{"class":"tabtext"}).text
         headline=headline.strip()
         url=link.find("li").find('a')['href']
         date=timezone.now()
         description=" "

         article={"author":"dainik-jagran","title":headline,"description":description,"url":url,"urlToImage":urlToImage,"publishedAt":date}
         articles.append(article)

    response={"source":"www.jagran.com","articles":articles}
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








