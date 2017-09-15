from django.http import JsonResponse
from account.models import Compare,Notification
from home.models import Post
import requests
import json

def newcompare(request):
    title= request.GET.get('title','')
    description=request.GET.get('description','')
    id= request.GET.get('post','')
    newcomp=Compare.objects.create(title=title,description=description,user=request.user)
    newcomp.posts.add(Post.objects.get(pk=id))
    return JsonResponse({'data':newcomp.pk})

def addposttocompare(request):
    compare_id= int(request.GET.get('compare',0))
    post_id=int(request.GET.get('post',0))
    comp=Compare.objects.get(pk=compare_id)
    comp.posts.add(Post.objects.get(pk=post_id))
    return JsonResponse({'count':comp.posts.count()})

def dictionary(request):
    if request.method=="GET":
        app_id = '9d07b61a'
        app_key = '6eaff0d616e455e40cbc291dcffed9be'
        language = 'en'
        word_id = request.GET.get('term',"")
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        print('executed')
        data = r.json()
        data=data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]
        return JsonResponse({'meaning':data['definitions'][0],'example':data['examples'][0]['text']})
