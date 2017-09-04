from account.models import Notification,Compare,Following
from .models import Post
from django.http import JsonResponse

def seennotification(request,pk):
    Notification.objects.filter(pk=pk).update(seen=1)
    return JsonResponse({"message":"message"})

def editcompare(request,pk):
    comp = Compare.objects.get(pk=pk)
    return JsonResponse({"title":comp.title,"description":comp.description})

def updatecompare(request,pk):
    title= request.GET.get('title',"")
    desc = request.GET.get('description',"")
    Compare.objects.filter(pk=pk).update(title=title,description=desc)
    return JsonResponse({"message":1})

def publishcompare(request,pk):
    c = Compare.objects.filter(pk=pk)
    c.update(published=1)
    c=c[0]
    people=Following.objects.get(current_user=request.user)
    people=people.users.all()
    for person in people:
        message = str((request.user.username).encode('utf-8'))+': '+ str((request.user.first_name).encode('utf-8'))+' '+str((request.user.last_name).encode('utf-8'))+' published "'+str((c.title).encode('utf-8'))+'".'
        url='/home/notification/compare/'+str(pk)
        n= Notification(user=person,message=message,onclick_url=url)
        n.save()
    return JsonResponse({'message':1})


def deletecompare(request,pk):
    Compare.objects.get(pk=pk).delete()
    return JsonResponse({'message':1})

def removefromcompare(request,pk):
    com=Compare.objects.get(pk=pk)
    p=request.GET.get('post','')
    post = Post.objects.get(pk=p)
    com.posts.remove(post)
    return JsonResponse({'message':1})
