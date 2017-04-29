from django.shortcuts import render,redirect
from django.views.generic import TemplateView

from account.forms import SocratesSearchForm
from account.models import Userprofile
from home.models import Post
from home.scrapers.ScrapeUN import UN


# Create your views here.
class home(TemplateView):
    template_name = "home/home.html"

    def get(self,request):
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        posts=Post.objects.all()

        args={'user':request.user,'details':details,'pic':pic,'form':form,"posts":posts}
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

