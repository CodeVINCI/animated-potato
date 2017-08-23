from django.http import JsonResponse
from account.models import Compare
from home.models import Post

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

