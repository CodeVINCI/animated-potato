import celery
print (celery.__file__)
from celery.task.schedules import  crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from home.TheHindu import get_news
from home.unnewsstream import ScrapeUN
from home.fashion import Scrape_bussiness_of_fashion
from home.Hindinews import Scrape_hindustan,Scrap_amarujala,Scrap_dainik_bhaskar,Scrape_dainik_jagran
from account.models import Following,Compare
from home.models import Post
from datetime import datetime,timedelta
import os

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/90')),
    name= "scrape_Thehindu_task",
    ignore_results=True)
def scrape_Thehindu_task():
    URLs=["https://newsapi.org/v1/articles?source=business-insider&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=breitbart-news&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bloomberg&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bbc-sport&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=ars-technica&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=al-jazeera-english&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=abc-news-au&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-hindu&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90"]
    #Scrape_hindustan()
    logger.info("Scraped livehindustan.com")
    Scrap_amarujala()
    logger.info("Scraped amarujala.com")
    Scrape_dainik_jagran()
    logger.info("Scraped jagran.com")
    #Scrap_dainik_bhaskar()
    logger.info("Scraped bhaskar.com")


    #Scrape_bussiness_of_fashion()
    logger.info('Scraped Business of fashion')

    ScrapeUN()
    logger.info('Scraped United Nations News')

    for URL in URLs:
        get_news(URL)
        source=URL.strip()[32:].split('&')[0]
        logger.info("Scraped "+source)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name= "delete_Post",
    ignore_results=True)
def delete_Post():
    all_exclusions = []
    all_compares=Compare.objects.all()
    for co in all_compares:
        all_exclusions= all_exclusions+list(co.posts.all())
    all_followings= Following.objects.all()
    for following in all_followings:
        all_exclusions= all_exclusions+list(following.post.all())
    all_pks = []
    for exclusion in all_exclusions:
        all_pks.append(exclusion.pk)
    date_today = datetime.today()
    d = str(datetime.today()-timedelta(days=14))
    d = d[:10]
    all_deletes = Post.objects.exclude(pk__in = all_pks).exclude(date__range=[d,date_today])
    for post in all_deletes:
        url = post.image.url
        pa = os.getcwd()+'/website'+url
        os.remove(pa)
        post.delete()

