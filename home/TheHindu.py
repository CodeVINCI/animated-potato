import urllib
import json
from home.models import Post
import requests
import tempfile
import ssl
from django.core import files
from django.utils import timezone
import time



def get_news(URL):
    url=URL
    context = ssl._create_unverified_context()
    response=urllib.urlopen(url,context=context)
    data=json.loads(response.read())
    source= data["source"].encode('utf-8')
    if source in ['business-insider','bloomberg']:
        category="business"
    elif source in ["bbc-sport"]:
        category="sports"
    elif source in ["ars-technica"]:
        category="technology"
    else:
        category="general"

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
                if article["description"]:
                    story=article["description"].encode('utf-8')
                else:
                    story = ""
                url=article["url"].encode('utf-8')
                if article["publishedAt"]==None:
                    date= str(timezone.now())
                    date=date[:10]
                else:
                    date=article["publishedAt"].encode('utf-8')
                    date=date[:10]
                if not(article['urlToImage']==None):
                    image_url=article["urlToImage"].encode('utf-8')
                    #request = requests.get(image_url, stream=True)
                    #time.sleep(3)
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
                    a=Post(source=articlesource,author=author,headline=headline,story=story,link=image_url,date=date,pageurl=url,category=category)

                    # Save the temporary image to the model#
                    # This saves the model so be sure that is it valid
                    a.save()



