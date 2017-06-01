from home.models import Post
from datetime import datetime, timedelta
import re

class NewsArticleSearch:
    def newsarticles(self,search_query):
        date_today=str(datetime.today())
        date_today=date_today[:10]
        d = str(datetime.today() - timedelta(days=7))
        d=d[:10]
        all_posts=Post.objects.filter(date__range=[d,date_today])
        ranked=[]
        terms=search_query.split(" ")
        for post in all_posts:
            rank=0
            for term in terms:
                pattern= str(term)
                matchobj=re.search(pattern,post.headline,re.IGNORECASE)
                if matchobj:
                    rank=rank+1
            if rank >0:
                ranked.append((post,rank))
        return ranked




