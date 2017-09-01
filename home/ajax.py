from account.models import Notification,Compare
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
