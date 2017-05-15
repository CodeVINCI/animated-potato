from django.shortcuts import render,redirect
from account.forms import UserProfile_form,Upload_form,SocratesSearchForm,SignUp_form,UserBasicEdit_form
from account.models import Userprofile,SocratesSearch,Following,newspaper
from home.models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from account.handle_upload import handle_uploaded_file

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.friends_search import FriendSearch
from django.http import JsonResponse
import random

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
            user.is_active=True
            user.save()
            Userprofile.objects.create(user=user)
            Following.objects.create(current_user=user)
            return redirect('/account/Welcome-to-socrates')




#view for MyProfile /account/profile
class Profile(TemplateView):
    template_name = 'profile/profile.html'

    def get(self,request):
         name=request.user
         userprofile=Userprofile.objects.filter(user=name)
         followingobj=Following.objects.get(current_user=name)
         all=Following.objects.all()
         followers=0
         for person in all:
             if name in person.users.all():
                 followers=followers+1

         following=followingobj.users.all()
         firstpaper=followingobj.newspaper.all()[0]
         followingno= len(following)
         details=userprofile[0]
         pic=details.image
         form=SocratesSearchForm()
         args={'user':request.user,'details':details,'pic':pic,'form':form,'following':following,'followingno':followingno,"followerno":followers,"firstpaper":firstpaper}
         return render(request,self.template_name,args)

    def post(self,request):
        form=SocratesSearchForm(request.POST)
        if form.is_valid():
            socratessearch=form.save(commit=False)
            socratessearch.user=request.user
            socratessearch.save()
            return redirect('/account/searchsocrates')


def myfollowers(request,user):
    all=Following.objects.all()
    followers=[]
    profiles=[]
    for person in all:
        if user in person.users.all():
            followers.append(person)
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


def viewprofile(request,pk):
    profile=Userprofile.objects.get(pk=pk)
    user=User.objects.get(username=profile.user)
    viewerimg=Userprofile.objects.get(user=request.user)
    viewerimg=viewerimg.image
    pic=profile.image
    form=SocratesSearchForm()
    followingobj=Following.objects.get(current_user__username=request.user)
    following=followingobj.users.all()
    if user in following:
        possibleaction="Unfollow"
    else:
        possibleaction="Follow"
    args={'viewer':request.user,'details':profile,'pic':pic,'form':form,'user':user,'activeuserimage':viewerimg,"following":following,"possibleaction":possibleaction}
    return render(request,'viewprofile/viewprofile.html',args)

# view for Account Settings /account/settings
@login_required
def settings(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    form=SocratesSearchForm()
    args={'user':request.user,'details':details,'pic':pic,'form':form}
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
    form=SocratesSearchForm()
    args={'user':request.user,'details':details,'pic':pic,'form':form}
    return render(request,'settings/psettings.html',args)

# view for email and notifications settings
@login_required
def ensettings(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    form=SocratesSearchForm()
    args={'user':request.user,'details':details,'pic':pic,'form':form}
    return render(request,'settings/ensettings.html',args)


@login_required
def blogs(request):
    return render(request,'blogs/blogs.html')


# view for personalised newspaper page /account/newspapers
class newspapers(TemplateView):
    template_name = 'newspapers/Newspapers.html'
    def get(self,request,sitename):
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        subscriptionsobj=Following.objects.get(current_user__username=request.user)
        subscriptions=subscriptionsobj.newspaper.all()
        col1=[]
        col2=[]
        all_posts=Post.objects.filter(source=sitename).order_by('date').reverse()
        j=0
        for i in xrange(0, len(all_posts), 2):
            col1.insert(j,all_posts[i])
            if (i+1)<len(all_posts):
                col2.insert(j,all_posts[i+1])
            j=j+1
        args={'user':request.user,'details':details,'pic':pic,'form':form,"subscriptions":subscriptions,'col1':col1,'col2':col2,'source':sitename}
        return render(request,'newspapers/Newspapers.html',args)


# /account/Welcome-to-socrates
@login_required
def Welcome(request):
    name=request.user
    userprofile=Userprofile.objects.filter(user=name)
    details=userprofile[0]
    pic=details.image
    form=SocratesSearchForm()
    args={'user':request.user,'details':details,'pic':pic,'form':form}
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
            pic=form.cleaned_data['image']
            return redirect('/account/profile')

        args={'user':request.user,'form':form,'pic':pic}
        return render(request,'profile/profile.html',args)

# view for Search result default takes to news article search
class Search_results(TemplateView):
    template_name = 'search/search_result_primary.html'

    def get(self,request):
        name=request.user
        search_query=SocratesSearch.objects.filter(user=name)
        search_query=search_query[0]
        form=SocratesSearchForm(initial={'search':search_query.search})
        #Call the search algorithm make it return all the arguments
        return render(request,self.template_name,{'form':form})

# view for Friends search
class People_search(TemplateView):
    template_name = 'search/search_people.html'

    def get(self,request):
        name=request.user
        search_query=SocratesSearch.objects.filter(user=name)
        search_query=search_query[0]
        form=SocratesSearchForm(initial={'search':search_query.search})
        a=FriendSearch()
        emptylastname=""
        name_split=search_query.search.split(" ")
        if len(name_split)>1:
            b=a.get_list(name_split[0],name_split[1],request.user)
            pic_list=a.get_pics(name_split[0],name_split[1],request.user)
            final=zip(pic_list,b)
        else:
            b=a.get_list(name_split[0],emptylastname,request.user)
            pic_list=a.get_pics(name_split[0],emptylastname,request.user)
            final=zip(pic_list,b)

        return render(request,self.template_name,{'form':form,'peoplelist':final})


# view for creating blog
class createblog(TemplateView):
    template_name = 'blog/createblog.html'

    def get(self,request):
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        args={'user':request.user,'details':details,'pic':pic,'form':form}
        return render(request,self.template_name,args)


class blog(TemplateView):
    template_name = 'blog/blog.html'

    def get(self,request):
        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        args={'user':request.user,'details':details,'pic':pic,'form':form}
        return render(request,self.template_name,args)


# view for My blogs
class Myblog(TemplateView):
    template_name = 'blog/Myblog.html'
    def get(self,request):

        name=request.user
        userprofile=Userprofile.objects.filter(user=name)
        details=userprofile[0]
        pic=details.image
        form=SocratesSearchForm()
        args={'user':request.user,'details':details,'pic':pic,'form':form}
        return render(request,self.template_name,args)

    def post(self,request):

        form=SocratesSearchForm(request.POST)
        if form.is_valid():
            socratessearch=form.save(commit=False)
            socratessearch.user=request.user
            socratessearch.save()
            return redirect('/account/searchsocrates')


def connections(request,action,pk):
    if request.method=='GET':
        person=User.objects.get(pk=pk)
        if action=='Follow':
            Following.followfriend(request.user, person)
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

