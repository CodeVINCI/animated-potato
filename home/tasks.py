import celery
print (celery.__file__)
from celery.task.schedules import  crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from home.TheHindu import get_news

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name= "scrape_Thehindu_task",
    ignore_results=True)
def scrape_Thehindu_task():
    get_news()
    logger.info("Scraped The Hindu")
