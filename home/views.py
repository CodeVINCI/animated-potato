from django.shortcuts import render,redirect
from django.views.generic import TemplateView

from account.forms import SocratesSearchForm
from account.models import Userprofile
from home.models import Post,comment
from account.models import Following
from home.forms import comment_form
from home.scrapers.ScrapeUN import UN
from django.utils import timezone
from random import shuffle


# Home page view.
class home(TemplateView):
    template_name = "home/home.html"

    def get(self,request,filter):
        date_today= str(timezone.now())
        date_today=date_today[:10]
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        commentbox=comment_form()
        col1=[]
        col2=[]
        col3=[]
        all_posts=Post.objects.filter(date=date_today)
        j=0
        for i in xrange(0, len(all_posts), 3):
            col1.insert(j,all_posts[i])
            if (i+1)<len(all_posts):
                col2.insert(j,all_posts[i+1])
            if (i+2)<len(all_posts):
                col3.insert(j,all_posts[i+2])
            j=j+1
            if filter=='most_liked':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1].likes > col1[i].likes:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1].likes > col2[i].likes:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1].likes > col3[i].likes:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_disliked':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1].dislikes > col1[i].dislikes:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1].dislikes > col2[i].dislikes:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1].dislikes > col3[i].dislikes:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_suggested':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1].suggestions > col1[i].suggestions:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1].suggestions > col2[i].suggestions:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1].suggestions > col3[i].suggestions:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_commented':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1].totalcomments > col1[i].totalcomments:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1].totalcomments > col2[i].totalcomments:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1].totalcomments > col3[i].totalcomments:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]

        args={'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
        return render(request,self.template_name,args)

def homeSports(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    form=SocratesSearchForm()
    args={'user':request.user,'details':details,'pic':pic,'form':form}
    return render(request,'homeSports/home-sports.html',args)

def homeMarket(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    form=SocratesSearchForm()
    args={'user':request.user,'details':details,'pic':pic,'form':form}
    return render(request,'homeMarket/home-market.html',args)

class unitednations(TemplateView):
    template_name = 'unitednations/unitednations.html'

    def get(self,request):
        a=UN()
        News=a.news()
        image=News[0]
        Headline=News[1]
        Story=News[2]
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        args={'user':request.user,"image_url":image,"headline":Headline,"story":Story,'details':details,'pic':pic,'form':form}
        return render(request,self.template_name,args)

    def post(self,request):
        form=SocratesSearchForm(request.POST)
        if form.is_valid():
            socratessearch=form.save(commit=False)
            socratessearch.user=request.user
            socratessearch.save()
            return redirect('/account/searchsocrates')

