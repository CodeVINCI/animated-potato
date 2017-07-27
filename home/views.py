from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from account.forms import SocratesSearchForm
from account.models import Userprofile,Notification,Following
from home.models import Post,comment,Likes,Dislikes
from account.models import Following,Compare
from home.forms import comment_form
from home.scrapers.ScrapeUN import UN
from django.utils import timezone
from random import shuffle
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.db.models import F
import json
from datetime import datetime, timedelta
import django.middleware.csrf

from django.shortcuts import get_object_or_404
# Home page view.
class home(TemplateView):
    template_name = "home/home.html"

    def get(self,request,filter):
        date_today=str(datetime.today())
        date_today=date_today[:10]
        d = str(datetime.today() - timedelta(days=4))
        d=d[:10]
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
        all_posts=Post.objects.filter(date__range=[d,date_today]).filter(category="general")
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
        col1=col1[:3]
        col2=col2[:3]
        col3=col3[:3]
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]
        compares=Compare.objects.filter(user=name)

        args={'compares':compares,'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
        return render(request,self.template_name,args)

def loadcontent(request,theme):
    date_today=str(datetime.today())
    date_today=date_today[:10]
    d = str(datetime.today() - timedelta(days=7))
    d=d[:10]

    ex=request.GET.get('posts','')
    ex=ex.strip()
    ex=ex.split(" ")
    print(theme)
    print(ex)
    if theme=="home":
        post=list(reversed(Post.objects.filter(category="general").exclude(pk__in=ex).order_by('date')))
    elif theme=="sports":
        post=list(reversed(Post.objects.filter(category="sports").exclude(pk__in=ex).order_by('date')))
    elif theme=="market":
        post=list(reversed(Post.objects.filter(category="business").exclude(pk__in=ex).order_by('date')))
    elif theme=="unitednations":
        post=list(reversed(Post.objects.filter(category="UN").exclude(pk__in=ex).order_by('date')))
    elif theme=="hindi":
        post=list(reversed(Post.objects.filter(category="hindi").exclude(pk__in=ex).order_by('date')))


    thumbnails=[]
    for i in range(6):
        whole=""
        a='<li><div class="thumbnail" id="'+str(post[i].pk)+'"><img src="'+str(post[i].image.url)+'" alt="..."><div class="caption"><p style="font-size:10px;">'+str((post[i].date).strftime("%b %d,%Y"))+'</p><h3 style="font-family:"Times New Roman", Times, serif;">'+(post[i].headline).encode("utf8")+'</h3><p style="font-size:10px;">'+(post[i].author).encode("utf8")+'</p><p style="font-size:20px;">'+(post[i].story).encode("utf8")+'</p><p style="font-size:10px;">'+(post[i].source).encode("utf8")+'</p><hr><div class="social_buttons" style="float:left;display:inline-block;width:-moz-calc(100% - 170px);width: -webkit-calc(100% -170px);width: calc(100% - 170px);"><button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;">'
        if len(Likes.objects.filter(post=post[i])) and request.user in Likes.objects.get(post=post[i]).users.all():
            b='<meta id="button_data" data-nextaction="social-unlike" data-pk="'+str(post[i].pk)+'"><span class="like"><i style="color:maroon;"class="glyphicon glyphicon-thumbs-up custom"></i></span>'
        else:
            b='<meta id="button_data" data-nextaction="social-like" data-pk="'+str(post[i].pk)+'"><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span>'

        c='<span class="count" >'+str(post[i].likes)+'</span></button>&nbsp;<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >'+str(post[i].dislikes)+'</span>'

        if len(Dislikes.objects.filter(post=post[i])) and request.user in Dislikes.objects.get(post=post[i]).users.all():
            d='<meta id="button_data" data-nextaction="social-undislike" data-pk="'+str(post[i].pk)+'"><span class="like"><i style="color:maroon;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button></div>'
        else:
            d='<meta id="button_data" data-nextaction="social-dislike" data-pk="'+str(post[i].pk)+'"><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button></div>'

        e='<p id="'+str(post[i].pk)+'"><a href="'+str(post[i].pageurl)+'" class="btn btn-primary" id="visitbutton" role="button" target="_blank">Visit Site</a> <a id="suggestbutton" class="btn btn-default" role="button">Suggest</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p><!-- Button trigger modal --><p><a data="#exampleModalLong'+str(post[i].pk)+'" class="popup" data-toggle="modal"><input id="post-comment" value="" required=True  placeholder="Write a comment..."/></a><a style="float:right;" href="http://www.facebook.com/sharer/sharer.php?u='+str(post[i].pageurl)+'&app_id=1885028298402855&image='+str(post[i].link)+'" target="_blank" class="fa fa-facebook"></a><button id="readlater" class="pin" style="border:none;background-color:transparent;margin-top:10px;float:right;"><span style="color:#0077b3;" class="glyphicon glyphicon-pushpin"></span></button><button id="addtocompare" class="pin" style="border:none;background-color:transparent;margin-top:10px;float:right;" data-toggle="modal" data-target="#myModal"><span class="glyphicon glyphicon-plus-sign"></span></button></p><!-- Modal --><div class="modal fade" id="exampleModalLong'+str(post[i].pk)+'" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><p style="font-size:10px;">'+str((post[i].created_on).strftime("%b %d,%Y"))+'</p><h3 style="font-family:"Times New Roman", Times, serif;">'+(post[i].headline).encode("utf8")+'</h3></div><div class="modal-body"><div class="conatiner"><img src="'+str(post[i].image.url)+'" alt="..." style="width:568px;height:400px;"><p style="font-size:10px;">'+(post[i].author).encode("utf8")+'</p><p style="font-size:20px;">'+(post[i].story).encode("utf8")+'</p><p style="font-size:10px;">'+(post[i].source).encode("utf8")+'</p><div class="media"><div class="media-left">'
        pic=Userprofile.objects.get(user=request.user).image
        csrf=django.middleware.csrf.get_token(request)

        f='<img src="'+str(pic.url)+'" alt="" style="width:40px;height:40px;border:1px solid #E6E6E6;border-radius:50%;"></a></div><div class="media-body"><h4 class="media-heading">'+str(request.user.first_name)+'&nbsp; '+str(request.user.last_name)+'&nbsp;</h4><form id="post-form"><input type="hidden" name="csrfmiddlewaretoken" value="'+str(csrf)+'" /><input id="post-comment" value="" required=True  placeholder="Write a comment..."/><meta id="comment_data" data-pk="'+str(post[i].pk)+'"><button type="button" id="comment_button" class="btn btn-default">Comment</button></form><ul id="talk" class="arguments">'

        h=""
        for comment in reversed(post[i].comments.all()):
            g='<li><span style="font-size:12px;"><b><a class="via_user" href="/account/viauserpk/'+str(comment.user.pk)+'">'+(comment.user.first_name).encode("utf8")+'&nbsp;'+(comment.user.last_name).encode("utf8")+'</a>&nbsp;&nbsp;</b><span style="font-size:10px;"><b>'+str(comment.created_on)+'</b></span></span><br><span style="font-size:12px;">'+(comment.text).encode("utf8")+'</span><br><div class="comment_action_line" style="height:10px;"><span style="font-size:10px;"><a class="comment_like" data-pk="'+str(comment.pk)+'" href="#" role="button">Like</a>&nbsp;&nbsp;&nbsp;<a class="comment_reply" data-pk="'+str(comment.pk)+'" href="#" role="button">Reply</a>&nbsp;&nbsp;&nbsp;'
            if comment.user.username==request.user.username:
                g=g+'<a class="comment_delete" data-pk="'+str(comment.pk)+'" href="#" role="button">Delete</a>'
            h=h+g
            replies='</span></div></li>'
            h=h+replies

        last='</ul><div class="modal-footer"><p id="'+str(post[i].pk)+'"><a href="'+str(post[i].pageurl)+'" class="btn btn-primary" id="visitbutton" role="button" target="_blank">Visit Site</a><a id="suggestbutton" class="btn btn-default" role="button">Suggest</a><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></p></div></div></div></div></div></div></div></div></div></div></li>'
        whole=a+b+c+d+e+f+h+last
        thumbnails.append(whole)


    response={'col1':thumbnails[0],'col2':thumbnails[1],'col3':thumbnails[2],'col4':thumbnails[3],'col5':thumbnails[4],'col6':thumbnails[5]}
    return JsonResponse(response)

class homeSports(TemplateView):
    template_name = "homeSports/home-sports.html"

    def get(self,request):
        filter="most_liked"
        date_today=str(datetime.today())
        date_today=date_today[:10]
        d = str(datetime.today() - timedelta(days=4))
        d=d[:10]
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
        all_posts=Post.objects.filter(date__range=[d,date_today]).filter(category="sports").order_by('date')
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
        col1=col1[:3]
        col2=col2[:3]
        col3=col3[:3]
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]
        compares=Compare.objects.filter(user=name)

        args={'compares':compares,'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
        return render(request,self.template_name,args)


class homeMarket(TemplateView):
    template_name = "homeMarket/home-market.html"

    def get(self,request):
        filter="most_liked"
        date_today=str(datetime.today())
        date_today=date_today[:10]
        d = str(datetime.today() - timedelta(days=4))
        d=d[:10]
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
        all_posts=Post.objects.filter(date__range=[d,date_today]).filter(category="business").order_by('?')
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
        col1=col1[:3]
        col2=col2[:3]
        col3=col3[:3]
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]
        compares=Compare.objects.filter(user=name)

        args={'compares':compares,'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
        return render(request,self.template_name,args)




class unitednations(TemplateView):
    template_name = 'unitednations/unitednations.html'

    def get(self,request,filter):
        date_today=str(datetime.today())
        date_today=date_today[:10]
        d = str(datetime.today() - timedelta(days=4))
        d=d[:10]
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
        all_posts=Post.objects.filter(source="unnewsstream.org").filter(date__range=[d,date_today])
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
        col1=col1[:3]
        col2=col2[:3]
        col3=col3[:3]
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]
        compares=Compare.objects.filter(user=name)

        args={'compares':compares,'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
        return render(request,self.template_name,args)



class hindi(TemplateView):
    template_name = "hindi/hindi.html"

    def get(self,request,filter):
        date_today=str(datetime.today())
        date_today=date_today[:10]
        d = str(datetime.today() - timedelta(days=4))
        d=d[:10]
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
        all_posts=Post.objects.filter(date__range=[d,date_today]).filter(category="hindi").order_by('date')
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
        col1=col1[:3]
        col2=col2[:3]
        col3=col3[:3]
        followingobj=Following.objects.get(current_user=name)
        firstpaper=followingobj.newspaper.all()[0]
        compares=Compare.objects.filter(user=name)

        args={'compares':compares,'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'filter':filter,'user':request.user,'details':details,'pic':pic,'form':form,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':date_today}
        return render(request,self.template_name,args)







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
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-unlike" data-pk='+str(pk)+'><span class="like"><i style="color:maroon;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">&nbsp;'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >&nbsp;'+str(postupdate.dislikes)+'&nbsp;</span><meta id="button_data" data-nextaction="social-dislike" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)

        elif action=='social-unlike':
            Post.objects.filter(pk=pk).update(likes = F('likes')-1)
            Likes.unlike(post,user)
            postupdate=Post.objects.get(pk=pk)
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-like" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">&nbsp;'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >&nbsp;'+str(postupdate.dislikes)+'&nbsp;</span><meta id="button_data" data-nextaction="social-dislike" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

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
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-like" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">&nbsp;'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >&nbsp;'+str(postupdate.dislikes)+'&nbsp;</span><meta id="button_data" data-nextaction="social-undislike" data-pk='+str(pk)+'><span class="like"><i style="color:maroon;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)

        elif action=='social-undislike':
            Post.objects.filter(pk=pk).update(dislikes = F('dislikes')-1)
            Dislikes.undislike(post,user)
            postupdate=Post.objects.get(pk=pk)
            args={"codeself":'<button id="like" class="social-like" style="border:none;background-color:transparent;margin-top:10px;"><meta id="button_data" data-nextaction="social-like" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-up custom"></i></span><span class="count">&nbsp;'+str(postupdate.likes)+'</span></button>&nbsp;'
                  +'<button id="dislike" class="social-dislike" style="border:none;background-color:transparent;"><span class="dislike" >&nbsp;'+str(postupdate.dislikes)+'&nbsp;</span><meta id="button_data" data-nextaction="social-dislike" data-pk='+str(pk)+'><span class="like"><i style="color:#7f8c8d;opacity:0.7;" class="glyphicon glyphicon-thumbs-down custom"></i></span></button>'}

            return JsonResponse(args)
#modified this view according to ajax and write a regex url for this if needed
def post_comment(request,pk):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        concerned_post=Post.objects.get(pk=pk)

        the_comment = comment(text=post_text, user=request.user,post=concerned_post)
        the_comment.save()
        concerned_post.comments.add(the_comment)
        Post.objects.filter(pk=pk).update(totalcomments = F('totalcomments')+1)
        a='<li><span style="font-size:12px;"><b><a class="via_user" href="/account/viewprofile/'+str(Userprofile.objects.get(user=request.user).pk)+'">'+str(request.user.first_name)+'&nbsp;'+str(request.user.last_name)+'&nbsp;&nbsp;</a></b><span style="font-size:10px;"><b>'+'just now'+'</b></span></span><br><span style="font-size:12px;">'+str(the_comment.text)+'</span><br><div class="comment_action_line" style="height:10px;"><span style="font-size:10px;"><a class="comment_like" data-pk="'+str(the_comment.pk)+'" href="#" role="button">Like</a>&nbsp;&nbsp;&nbsp;<a class="comment_reply" data-pk="'+str(the_comment.pk)+'" href="#" role="button">Reply</a>&nbsp;&nbsp;&nbsp;<a class="comment_delete" data-pk="'+str(the_comment.pk)+'" href="#" role="button">Delete</a></span></div></li>'
        args={'text':a}
        return JsonResponse(args)

def remove_comment(request,pk):
    if request.method=="GET":
        the_comment=comment.objects.get(pk=pk)
        the_comment.delete()
        return JsonResponse({'code':"deleted comment"})


def visits(request,pk):
    if request.method=='GET':
        Post.objects.filter(pk=pk).update(visits = F('visits')+1)
        return JsonResponse({'success':'success'})



def suggest(request,pk):
    if request.method=='GET':
        Post.objects.filter(pk=pk).update(suggestions=F('suggestions')+1)
        # make function to trigger a notification to all the followers username suggested post.headline post.source
        p=Post.objects.get(pk=pk)
        people=Following.objects.get(current_user=request.user)
        people=people.users.all()
        for person in people:
            message = str((request.user.username).encode('utf-8'))+': '+ str((request.user.first_name).encode('utf-8'))+' '+str((request.user.last_name).encode('utf-8'))+' suggested "'+str((p.headline).encode('utf-8'))+'"by "'+str((p.source).encode('utf-8'))+'".'
            url='account/suggested/'+str(pk)
            n= Notification(user=person,message=message,onclick_url=url)
            n.save()
        return JsonResponse({'message':'Article has been suggeted to your friends'})
