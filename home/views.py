from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from account.forms import SocratesSearchForm
from account.models import Userprofile,Notification,Following
from home.models import Post,comment,Likes,Dislikes
from account.models import Following
from home.forms import comment_form
from home.scrapers.ScrapeUN import UN
from django.utils import timezone
from random import shuffle
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.db.models import F
import json

from django.shortcuts import get_object_or_404
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
        all_notifications=Notification.objects.filter(user=request.user)
        new_notifications=all_notifications.filter(seen=0)
        ping= new_notifications.count()
        col1=[]
        col2=[]
        col3=[]
        liked_posts=[]
        disliked_posts=[]
        all_posts=Post.objects.filter(date=date_today).order_by('?')
        k=0
        for post in all_posts:
            p=Likes.objects.filter(post=post)
            if p.count()>0 and request.user in p[0].users.all():
                liked_posts.insert(k,1)
                k=k+1
            else:
                liked_posts.insert(k,0)
                k=k+1
        l=0
        for post in all_posts:
            p=Dislikes.objects.filter(post=post)
            if p.count()>0 and request.user in p[0].users.all():
                disliked_posts.insert(l,1)
                l=l+1
            else:
                disliked_posts.insert(l,0)
                l=l+1


        j=0
        for i in xrange(0, len(all_posts), 3):
            col1.insert(j,(all_posts[i],liked_posts[i],disliked_posts[i]))
            if (i+1)<len(all_posts):
                col2.insert(j,(all_posts[i+1],liked_posts[i+1],disliked_posts[i+1]))
            if (i+2)<len(all_posts):
                col3.insert(j,(all_posts[i+2],liked_posts[i+2],disliked_posts[i+2]))
            j=j+1
            if filter=='most_liked':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1][0].likes > col1[i][0].likes:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1][0].likes > col2[i][0].likes:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1][0].likes > col3[i][0].likes:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_disliked':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1][0].dislikes > col1[i][0].dislikes:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1][0].dislikes > col2[i][0].dislikes:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1][0].dislikes > col3[i][0].dislikes:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_suggested':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1][0].suggestions > col1[i][0].suggestions:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1][0].suggestions > col2[i][0].suggestions:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1][0].suggestions > col3[i][0].suggestions:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_commented':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1][0].totalcomments > col1[i][0].totalcomments:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1][0].totalcomments > col2[i][0].totalcomments:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1][0].totalcomments > col3[i][0].totalcomments:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])
            elif filter=='most_visited':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1][0].visits > col1[i][0].visits:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1][0].visits > col2[i][0].visits:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1][0].visits > col3[i][0].visits:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])

        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]

        args={'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
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


def sociallike(request,action,pk):
    if request.method=='GET':
        user=request.user
        post=Post.objects.get(pk=pk)
        if action=='social-like':
            Post.objects.filter(pk=pk).update(likes = F('likes')+1)
            Likes.like(post,user)
            dis=Dislikes.objects.filter(post=post)
            if dis.count()>0:
                if user in dis[0].users.all():
                    Post.objects.filter(pk=pk).update(dislikes = F('dislikes')-1)
                    Dislikes.undislike(post,user)
            postupdate=Post.objects.get(pk=pk)
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-unlike" data-pk='+str(pk)+'><span class="like"><i style="color:maroon;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >'+str(postupdate.dislikes)+'</span><meta id="button_data" data-nextaction="social-dislike" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)

        elif action=='social-unlike':
            Post.objects.filter(pk=pk).update(likes = F('likes')-1)
            Likes.unlike(post,user)
            postupdate=Post.objects.get(pk=pk)
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-like" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >'+str(postupdate.dislikes)+'</span><meta id="button_data" data-nextaction="social-dislike" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)

        elif action=='social-dislike':
            Post.objects.filter(pk=pk).update(dislikes = F('dislikes')+1)
            Dislikes.dislike(post,user)
            lik=Likes.objects.filter(post=post)
            if lik.count()>0:
                if user in lik[0].users.all():
                    Post.objects.filter(pk=pk).update(likes = F('likes')-1)
                    Likes.unlike(post,user)
            postupdate=Post.objects.get(pk=pk)
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-like" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >'+str(postupdate.dislikes)+'</span><meta id="button_data" data-nextaction="social-undislike" data-pk='+str(pk)+'><span class="like"><i style="color:maroon;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)

        elif action=='social-undislike':
            Post.objects.filter(pk=pk).update(dislikes = F('dislikes')-1)
            Dislikes.undislike(post,user)
            postupdate=Post.objects.get(pk=pk)
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-like" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >'+str(postupdate.dislikes)+'</span><meta id="button_data" data-nextaction="social-dislike" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)
#modified this view according to ajax and write a regex url for this if needed
def post_comment(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        the_comment = comment(text=post_text, user=request.user)
        the_comment.save()

        response_data['the_commentpk'] = the_comment.pk
        response_data['text'] = the_comment.text
        response_data['created_on'] = the_comment.created_on.strftime('%B %d, %Y %I:%M %p')
        response_data['user'] = the_comment.user.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def visits(request,pk):
    if request.method=='GET':
        Post.objects.filter(pk=pk).update(visits = F('visits')+1)
        return JsonResponse({'success':'success'})



def suggest(request,pk):
    if request.method=='GET':
        Post.objects.filter(pk=pk).update(suggestions=F('suggestions')+1)
        # make function to trigger a notification to all the followers username suggested post.headline post.source
        return JsonResponse({'message':'Article has been suggeted to your friends'})
