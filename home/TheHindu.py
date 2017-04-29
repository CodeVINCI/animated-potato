import urllib
import json
from home.models import Post
import requests
import tempfile

from django.core import files







def get_news():
    url="https://newsapi.org/v1/articles?source=the-hindu&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90"
    response=urllib.urlopen(url)
    data=json.loads(response.read())
    source= data["source"].encode('utf-8')
    articles=data["articles"].encode('utf-8')
    for article in articles:
        storedarticles=Post.objects.filter(headline=article["title"])
        if len(storedarticles)==0:
                articlesource=source
                author=article["author"].encode('utf-8')
                headline=article["title"].encode('utf-8')
                story=article["description"].encode('utf-8')
                url=article["url"].encode('utf-8')
                date=article["publishedAt"].encode('utf-8')
                date=date[:10]
                image_url=article["urlToImage"].encode('utf-8')
                request = requests.get(image_url, stream=True)

                # Was the request OK?
                if request.status_code != requests.codes.ok:
                    # Nope, error handling, skip file etc etc etc
                    continue

                # Get the filename from the url, used for saving later
                file_name = image_url.split('/')[-1]

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


