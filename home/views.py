from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import TemplateView

from account.forms import SocratesSearchForm
from account.models import Userprofile
from home.models import Post,comment
from account.models import Following
from home.forms import comment_form
from home.scrapers.ScrapeUN import UN
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import JsonResponse
from django.utils import timezone
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


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
        all_posts=Post.objects.exclude().order_by('date').reverse()[:30]
        j=0
        for i in xrange(0, len(all_posts), 3):
            col1.insert(j,all_posts[i])
            if (i+1)<len(all_posts):
                col2.insert(j,all_posts[i+1])
            if (i+2)<len(all_posts):
                col3.insert(j,all_posts[i+2])
            j=j+1
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]

        args={'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper}
        return render(request,self.template_name,args)

def create_comment(request):
    if request.method == 'POST':
        comment_text = comment.objects.create(text = request.POST['text'])
        return JsonResponse(model_to_dict(comment_text))


@login_required()
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            message = 'You disliked this'
        else:
            post.likes.add(user)
            message = 'You liked this'
    ctx = {'likes_count':post.total_likes,'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')




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

