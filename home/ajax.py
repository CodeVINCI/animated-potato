from account.models import Notification,Compare
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
    Compare.objects.filter(pk=pk).update(published=1)
    return JsonResponse({'message':1})

def unpublishcompare(request,pk):
    Compare.objects.filter(pk=pk).update(published=0)
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
