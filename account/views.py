from django.shortcuts import render,redirect
from account.forms import UserProfile_form,Upload_form,SocratesSearchForm,SignUp_form,UserBasicEdit_form,Compare_form
from account.models import Userprofile,SocratesSearch,Following,newspaper,Notification,Compare
from home.models import Post,Likes,Dislikes
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from account.handle_upload import handle_uploaded_file
from home.forms import comment_form,compare_comment_form
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.friends_search import FriendSearch
from account.primary_search import NewsArticleSearch
from django.http import JsonResponse
import random
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import os
# view for login /account/login
def login(request):
    return redirect('/account/login')



# view for Signup /account/signup
class signup(TemplateView):

    template_name = 'signup/SignUp.html'

    def get(self, request):
        form = SignUp_form()
        return render(request, self.template_name,{'form':form})
    def post(self,request):
        form = SignUp_form(request.POST)
        print (form.is_valid())
        if form.is_valid():
            user=form.save(commit=False)
           # user.is_active=True
            user.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            auth_login(request, new_user)
            Userprofile.objects.create(user=user)
            Following.objects.create(current_user=user)
            paper1=newspaper.objects.get(name='unnewsstream.org')
            Following.Subscribenews(current_user=user,new_newspaper=paper1)
            return redirect('/account/Welcome-to-socrates')




#view for MyProfile /account/profile
class Profile(TemplateView):
    template_name = 'profile/profile.html'

    def get(self,request):
         date_today=datetime.today()
         time_stamp=date_today.strftime("%b %d,%Y")
         name=request.user

         all_notifications=Notification.objects.filter(user=request.user)
         new_notifications=all_notifications.filter(seen=0)
         ping= new_notifications.count()


         userprofile=Userprofile.objects.filter(user=name)
         followingobj=Following.objects.get(current_user=name)
         all=Following.objects.all()
         followers=0
         for person in all:
             if name in person.users.all():
                 followers=followers+1

         following=followingobj.users.all()
         subscription=followingobj.newspaper.all()
         firstpaper=followingobj.newspaper.all()[0]
         followingno= len(following)
         subscriptionno=len(subscription)
         details=userprofile[0]
         pic=details.image
         args={'all_notifications':all_notifications,'ping':ping,'user':request.user,'details':details,'pic':pic,'following':following,'subscription':subscription,'subscriptionno':subscriptionno,'followingno':followingno,"followerno":followers,"firstpaper":firstpaper,'date_today':time_stamp}
         return render(request,self.template_name,args)

    def post(self,request):
        form=SocratesSearchForm(request.POST)
        if form.is_valid():
            socratessearch=form.save(commit=False)
            socratessearch.user=request.user
            socratessearch.save()
            return redirect('/account/searchsocrates/'+str(request.POST['search']))


def myfollowers(request,user):
    userobj=User.objects.get(username=user)
    alluser=Following.objects.all()
    followers=[]
    profiles=[]
    for person in alluser:
        if userobj in person.users.all():
            followers.append(User.objects.get(username=person.current_user))
    for person in followers:
        profiles.append(Userprofile.objects.get(user=person))
    args={'followers':zip(followers,profiles)}
    return render(request,"followers/followers.html",args)

def imfollowing(request, user):
    followingobj=Following.objects.get(current_user__username=user)
    following=followingobj.users.all()
    profiles=[]
    for person in following:
        profiles.append(Userprofile.objects.get(user=person))
    list=zip(following,profiles)
    args={"following":list,"user":user}
    return render(request,'following/following.html',args)

def mysubscription(request,user):
    subscriptionsobj=Following.objects.get(current_user__username=user)
    subscriptions=subscriptionsobj.newspaper.all()
    subscribemore=newspaper.objects.exclude(id__in=subscriptions)
    args={"subscriptions":subscriptions,"subscribemore":subscribemore}
    return render(request,'following/subscribe.html',args)



def myarticles(request,user):
    subscriptionsobj=Following.objects.get(current_user__username=user)
    all_posts=subscriptionsobj.post.all()
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    commentbox=comment_form()
    all_notifications=Notification.objects.filter(user=request.user)
    new_notifications=all_notifications.filter(seen=0)
    ping= new_notifications.count()
    col1=[]
    col2=[]
    col3=[]
    liked_posts=[]
    disliked_posts=[]
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
    followingobj=Following.objects.get(current_user=name)
    firstpaper=followingobj.newspaper.all()[0]
    date_today=datetime.today()
    time_stamp=date_today.strftime("%b %d,%Y")
    args={'all_notifications':all_notifications,'ping':ping,'user':request.user,'details':details,'pic':pic,"col1":col1,"col2":col2,"col3":col3,"commentbox":commentbox,'firstpaper':firstpaper,'date_today':time_stamp}
    return render(request,'following/articles.html',args)


def viewprofile(request,pk):
    profile=Userprofile.objects.get(pk=pk)
    user=User.objects.get(username=profile.user)
    viewer=Userprofile.objects.get(user=request.user)
    viewerimg=viewer.image
    pic=profile.image
    followingobj=Following.objects.get(current_user__username=request.user)
    following=followingobj.users.all()
    if user in following:
        possibleaction="Unfollow"
    else:
        possibleaction="Follow"
    args={'viewer':request.user,'details':profile,'pic':pic,'user':user,'activeuserimage':viewerimg,"activeuser":viewer,"following":following,"possibleaction":possibleaction}
    return render(request,'viewprofile/viewprofile.html',args)

def viauserpk(request,pk):
    user=User.objects.get(pk=pk)
    profile=Userprofile.objects.get(user=user)
    viewerimg=Userprofile.objects.get(user=request.user)
    viewerimg=viewerimg.image
    pic=profile.image
    followingobj=Following.objects.get(current_user__username=request.user)
    following=followingobj.users.all()
    if user in following:
        possibleaction="Unfollow"
    else:
        possibleaction="Follow"
    args={'viewer':request.user,'details':profile,'pic':pic,'user':user,'activeuserimage':viewerimg,"following":following,"possibleaction":possibleaction}
    return render(request,'viewprofile/viewprofile.html',args)

# view for Account Settings /account/settings
@login_required
def settings(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    all_notifications=Notification.objects.filter(user=request.user)
    new_notifications=all_notifications.filter(seen=0)
    ping= new_notifications.count()
    args={'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'user':request.user,'details':details,'pic':pic}
    return render(request,'settings/settings.html',args)



# view for change Password from inside the settings
@login_required
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/settings')
        else:
            return redirect('/account/changepassword')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'edit/changepassword.html',args)



# view for personal settings
@login_required
def psettings(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    all_notifications=Notification.objects.filter(user=request.user)
    new_notifications=all_notifications.filter(seen=0)
    ping= new_notifications.count()
    args={'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'user':request.user,'details':details,'pic':pic}
    return render(request,'settings/psettings.html',args)

# view for email and notifications settings
@login_required
def ensettings(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    all_notifications=Notification.objects.filter(user=request.user)
    new_notifications=all_notifications.filter(seen=0)
    ping= new_notifications.count()
    args={'all_notifications':all_notifications,'new_notifications':new_notifications,'ping':ping,'user':request.user,'details':details,'pic':pic}
    return render(request,'settings/ensettings.html',args)


@login_required
def blogs(request):
    return render(request,'blogs/blogs.html')


# view for personalised newspaper page /account/newspapers
class newspapers(TemplateView):
    template_name = 'newspapers/Newspapers.html'
    def get(self,request,sitename):
        #dates
        date_today=datetime.today()
        time_stamp=date_today.strftime("%b %d,%Y")
        date_today=str(date_today)[:10]
        d = str(datetime.today() - timedelta(days=3))
        d=d[:10]
        # today and a day before

        #navbar content
        all_notifications=Notification.objects.filter(user=request.user)
        new_notifications=all_notifications.filter(seen=0)
        ping= new_notifications.count()

        commentbox=comment_form()
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image

        subscriptionsobj=Following.objects.get(current_user__username=request.user)
        subscriptions=subscriptionsobj.newspaper.all()
        col1=[]
        col2=[]
        liked_posts=[]
        disliked_posts=[]
        all_posts=Post.objects.filter(source=sitename).filter(date__range=[d,date_today])[0:6]
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
        for i in xrange(0, len(all_posts), 2):
            col1.insert(j,(all_posts[i],liked_posts[i],disliked_posts[i]))
            if (i+1)<len(all_posts):
                col2.insert(j,(all_posts[i+1],liked_posts[i+1],disliked_posts[i+1]))
            j=j+1

        for j in range(len(col1)-1):
            for i in range(len(col1)-1):
                if col1[i+1][0].likes > col1[i][0].likes:
                    (col1[i],col1[i+1])=(col1[i+1],col1[i])

        for j in range(len(col2)-1):
            for i in range(len(col2)-1):
                if col2[i+1][0].likes > col2[i][0].likes:
                    (col2[i],col2[i+1])=(col2[i+1],col2[i])
        compares=Compare.objects.filter(user=name)
        args={'compareform':Compare_form(),'compares':compares,'all_notifications':all_notifications,'ping':ping,'commentbox':commentbox,'user':request.user,'details':details,'pic':pic,"subscriptions":subscriptions,'col1':col1,'col2':col2,'source':sitename,'date_today':time_stamp}
        return render(request,'newspapers/Newspapers.html',args)




# /account/Welcome-to-socrates
@login_required
def Welcome(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    args={'user':request.user,'details':details,'pic':pic}
    return render(request,'welcome/Welcome.html',args)


# view for Users name and last name edit form
@login_required
def UserBasicEdit(request):
    if request.method=='POST':
        form = UserBasicEdit_form(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:
        form= UserBasicEdit_form(instance=request.user)
        args={'form':form}
    return render(request,'edit/UserBasicEdit.html',args)



# view for User profile information edit
class UserProfileEdit(TemplateView):
    template_name = 'edit/UserProfile.html'

    def get(self,request):
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image


        profiles=Userprofile.objects.get(user=request.user)
        form=UserProfile_form(initial={'workAndemployment':profiles.workAndemployment,'location':profiles.location,'website':profiles.website,'description':profiles.description})
        args={'form':form,'profiles':profiles,'user':request.user,'details':details,'pic':pic,}
        return render(request,self.template_name,args)

    def post(self,request):
        name=request.user
        details=Userprofile.objects.get(user=name)
        pic=details.image
        primarykey=details.pk

        form=UserProfile_form(request.POST)
        if form.is_valid():
            Userprofile.objects.filter(user=name).delete()
            userprofile=form.save(commit=False)
            userprofile.user=request.user
            userprofile.image= pic
            userprofile.pk=primarykey
            userprofile.save()
            text1 = form.cleaned_data['workAndemployment']
            text2 = form.cleaned_data['location']
            text3 = form.cleaned_data['website']
            text4 = form.cleaned_data['description']
            return redirect('/account/profile')

        args={'user':request.user,'form':form,'workAndemployment':text1,'location':text2,'website':text3,'description':text4}
        return render(request,'profile/profile.html',args)


# view for Userprofile picture upload
class Profileupload(TemplateView):
    template_name= 'edit/upload.html'

    def get(self,request):
        name=request.user
        profile=Userprofile.objects.get(user=name)
        form = Upload_form(initial={'image':profile.image})
        return render(request,self.template_name,{'form':form,'pic':profile.image})
    def post(self,request):
        name=request.user
        picture=Userprofile.objects.get(user=name).image
        form=Upload_form(request.POST,request.FILES)
        if form.is_valid():
            profile=Userprofile.objects.get(user=name)
            Userprofile.objects.filter(user=name).delete()
            userprofile=form.save(commit=False)
            userprofile.user=name
            userprofile.workAndemployment= profile.workAndemployment
            userprofile.location=profile.location
            userprofile.website=profile.website
            userprofile.description=profile.description
            userprofile.pk=profile.pk
            userprofile.image= request.FILES['image']
            userprofile.save()
            pa = os.getcwd()+"/website"+picture.url
            os.remove(pa)
            return redirect('/account/profile')

        args={'user':request.user,'form':form,'pic':picture}
        return render(request,'profile/profile.html',args)

# view for Search result default takes to news article search
class Search_results(TemplateView):
    template_name = 'search/search_result_primary.html'

    def get(self,request,search_terms):
        name=request.user
        form=SocratesSearchForm(initial={'search':search_terms})
        date_today=datetime.today()
        time_stamp=date_today.strftime("%b %d,%Y")
        date_today=str(date_today)[:10]
        d = str(datetime.today() - timedelta(days=1))
        d=d[:10]

        commentbox=comment_form()
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image

        all_notifications=Notification.objects.filter(user=request.user)
        new_notifications=all_notifications.filter(seen=0)
        ping= new_notifications.count()

        compares= Compare.objects.filter(user=name)
        #Call the search algorithm make it return all the arguments
        a=NewsArticleSearch()
        col1=[]
        col2=[]
        col3=[]
        liked_posts=[]
        disliked_posts=[]
        all_posts=[]
        ranks=[]
        posts=a.newsarticles(search_terms)
        for post in posts:
            all_posts.append(post[0])
        for rank in posts:
            ranks.append(rank[1])
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
            col1.insert(j,(all_posts[i],liked_posts[i],disliked_posts[i],ranks[i]))
            if (i+1)<len(all_posts):
                col2.insert(j,(all_posts[i+1],liked_posts[i+1],disliked_posts[i+1],ranks[i+1]))
            if (i+2)<len(all_posts):
                col3.insert(j,(all_posts[i+2],liked_posts[i+2],disliked_posts[i+2],ranks[i+2]))
            j=j+1
            filter='most_ranked'
            if filter=='most_ranked':
                for j in range(len(col1)-1):
                    for i in range(len(col1)-1):
                        if col1[i+1][3] > col1[i][3]:
                            (col1[i],col1[i+1])=(col1[i+1],col1[i])
                for j in range(len(col2)-1):
                    for i in range(len(col2)-1):
                        if col2[i+1][3] > col2[i][3]:
                            (col2[i],col2[i+1])=(col2[i+1],col2[i])
                for j in range(len(col3)-1):
                    for i in range(len(col3)-1):
                        if col3[i+1][3] > col3[i][3]:
                            (col3[i],col3[i+1])=(col3[i+1],col3[i])

        return render(request,self.template_name,{'compareform':Compare_form(),'compares':compares,'all_notifications':all_notifications,'ping':ping,'form':form,'col1':col1,'col2':col2,'col3':col3,'date_today':time_stamp,'commentbox':commentbox,'user':request.user,'details':details,'pic':pic,'search_terms':search_terms})

# view for Friends search
class People_search(TemplateView):
    template_name = 'search/search_people.html'

    def get(self,request,search_terms):

        all_notifications=Notification.objects.filter(user=request.user)
        new_notifications=all_notifications.filter(seen=0)
        ping= new_notifications.count()

        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image

        search_query=search_terms
        form=SocratesSearchForm(initial={'search':search_query})
        a=FriendSearch()
        emptylastname=""
        name_split=search_query.split(" ")
        if len(name_split)>1:
            b=a.get_list(name_split[0],name_split[1],request.user)
            pic_list=a.get_pics(name_split[0],name_split[1],request.user)
            final=zip(pic_list,b)
        else:
            b=a.get_list(name_split[0],emptylastname,request.user)
            pic_list=a.get_pics(name_split[0],emptylastname,request.user)
            final=zip(pic_list,b)

        return render(request,self.template_name,{'form':form,'peoplelist':final,'search_terms':search_terms,'all_notifications':all_notifications,'ping':ping,'user':request.user,'details':details,'pic':pic})



class ComparePublish(TemplateView):
    template_name = 'compare/compare.html'
    def get(self,request):

        date_today=str(timezone.now())
        date_today=date_today[:10]
        name=request.user

        commentbox=compare_comment_form()
        userprofile=Userprofile.objects.filter(user=name)
        followingobj=Following.objects.get(current_user=name)
        compareobj = Compare.objects.filter(user=name)

        all_notifications=Notification.objects.filter(user=request.user)
        new_notifications=all_notifications.filter(seen=0)
        ping= new_notifications.count()
        firstpaper=followingobj.newspaper.all()[0]
        details=userprofile[0]
        pic=details.image
        compareform=Compare_form()
        args={"compareform":compareform,'commentbox':commentbox,'comp':compareobj,'all_notifications':all_notifications[:10],'ping':ping,'user':request.user,'details':details,'pic':pic,"subscriptions":subscriptions,'date_today':date_today,'firstpaper':firstpaper}
        return render(request,self.template_name,args)


def connections(request,action,pk):
    if request.method=='GET':
        person=User.objects.get(pk=pk)
        if action=='Follow':
            Following.followfriend(request.user, person)
            msg= str(request.user.username)+": "+str(request.user.first_name)+" "+(request.user.last_name) +" started following you, click here to view profile."
            id=Userprofile.objects.get(user=request.user).pk
            url="/account/viewprofile/"+str(id)
            notification=Notification(user=person, message=msg, onclick_url=url, seen=0, created_on=timezone.now() )
            notification.save()
            #args={'button':'<button type="button" class="btn btn-secondary" style="background-color:maroon;color:white;">Unfollow</button>',
             #     'meta':'<meta id="my-data" data-possibleaction="Unfollow" data-pk="'+str(pk)+'">'}
            args={"code":'<button type="button" class="btn btn-secondary" style="background-color:maroon;color:white;">Unfollow</button>'+'<meta id="my-data" data-possibleaction="Unfollow" data-pk="'+str(pk)+'">'}
            return JsonResponse(args)
        elif action=='Unfollow':
            Following.unfollowfriend(request.user, person)
            #args={'button':'<button type="button" class="btn btn-secondary" style="background-color:maroon;color:white;">Follow</button>',
             #     'meta':'<meta id="my-data" data-possibleaction="Follow" data-pk="'+str(pk)+'">'}
            args={"code":'<button type="button" class="btn btn-secondary" style="background-color:maroon;color:white;">Follow</button>'+'<meta id="my-data" data-possibleaction="Follow" data-pk="'+str(pk)+'">'}
            return JsonResponse(args)

def subscriptions(request,newssite,action):
    print("reached")
    if request.method=='GET':
        if action=='Subscribe':
            key=newspaper.objects.get(name=newssite)
            Following.Subscribenews(request.user,key)
            args={"code":'<li>'+str(newssite)+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button type="button" class="btn btn-secondary" style="float:right;width:100px;height:25px;padding:2px;background-color:maroon;color:white;">Unsubscribe</button></li><hr>'}
            return JsonResponse(args)
        elif action=='Unsubscribe':
            key=newspaper.objects.get(name=newssite)
            Following.Unsubscribenews(request.user,key)
            args={"code":'<li>'+str(newssite)+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button type="button" class="btn btn-secondary" style="float:right;width:100px;height:25px;padding:2px;background-color:maroon;color:white;">Subscribe</button></li><hr>'}
            return JsonResponse(args)

def savepost(request,pk):
    Following.addpost(request.user,Post.objects.get(pk=pk))
    return JsonResponse({'g':'h'})

def removepost(request,pk):
    Following.removepost(request.user,Post.objects.get(pk=pk))
    return JsonResponse({'g':'h'})
