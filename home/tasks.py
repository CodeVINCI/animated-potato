import celery
print (celery.__file__)
from celery.task.schedules import  crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from home.TheHindu import get_news
from home.unnewsstream import ScrapeUN
from home.fashion import Scrape_bussiness_of_fashion

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name= "scrape_Thehindu_task",
    ignore_results=True)
def scrape_Thehindu_task():
    URLs=["https://newsapi.org/v1/articles?source=business-insider&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=breitbart-news&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bloomberg&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bild&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bbc-sport&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=ars-technica&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=al-jazeera-english&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=abc-news-au&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=the-hindu&sortBy=latest&apiKey=7b761e381bcc40ca88311d8ef360da90","https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=7b761e381bcc40ca88311d8ef360da90"]
    Scrape_bussiness_of_fashion()
    logger.info('Scraped Business of fashion')
    ScrapeUN()
    logger.info('Scraped United Nations News')
    for URL in URLs:
        get_news(URL)
        source=URL.strip()[32:].split('&')[0]
        logger.info("Scraped "+source)
