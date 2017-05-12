from django.shortcuts import render,redirect
from django.views.generic import TemplateView

from account.forms import SocratesSearchForm
from account.models import Userprofile
from home.models import Post,comment
from home.forms import comment_form
from home.scrapers.ScrapeUN import UN
from django.utils import timezone


# Create your views here.
class home(TemplateView):
    template_name = "home/home.html"

    def get(self,request):
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        commentbox=comment_form()
        col1=[]
        col2=[]
        col3=[]
        all_posts=Post.objects.exclude().order_by('date').reverse()
        j=0
        for i in xrange(0, len(all_posts), 3):
            col1.insert(j,all_posts[i])
            if (i+1)<len(all_posts):
                col2.insert(j,all_posts[i+1])
            if (i+2)<len(all_posts):
                col3.insert(j,all_posts[i+2])
            j=j+1

        args={'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox}
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

