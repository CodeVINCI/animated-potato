import celery
print (celery.__file__)
from celery.task.schedules import  crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from home.TheHindu import get_news
from home.unnewsstream import ScrapeUN
from home.fashion import Scrape_bussiness_of_fashion
from home.Hindinews import Scrape_hindustan,Scrap_amarujala,Scrape_gaoconnection_home,Scrape_dainik_jagran

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name= "scrape_Thehindu_task",
    ignore_results=True)
def scrape_Thehindu_task():
    r = open("counter.txt",'r')
    earlier = int(r.read())
    r.close()

    if not(earlier==24):
        w = open('counter.txt','w')
        w.write(str(earlier+1))
        w.close()
    else:
        w = open('test.txt','w')
        w.write('0')
        w.close()

    URLs=["https://newsapi.org/v1/articles?source=business-insider&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=breitbart-news&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bloomberg&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bbc-sport&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=ars-technica&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=al-jazeera-english&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=abc-news-au&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-hindu&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90"]

    if earlier in [0,2,4,6,8,10,12,14,16,18,20,22]:
        #Scrap_amarujala()
        logger.info("Scraped amarujala.com")
        Scrape_hindustan()
        logger.info("Scraped livehindustan.com")

    if earlier in [1,3,5,7,9,11,13,15,17,19,21,23]:
        Scrape_dainik_jagran()
        logger.info("Scraped jagran.com")

    if earlier in [0,6,12,18]:
        Scrape_gaoconnection_home()
        logger.info("Scraped gaoconnection.com")

    if earlier in [0,8,16]:
        ScrapeUN()
        logger.info('Scraped United Nations News')
    if earlier not in [2,3]:
        for URL in URLs:
            get_news(URL)
            source=URL.strip()[32:].split('&')[0]
            logger.info("Scraped "+source)





