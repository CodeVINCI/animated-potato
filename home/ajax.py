from account.models import Notification
from django.http import JsonResponse

def seennotification(request,pk):
    Notification.objects.filter(pk=pk).update(seen=1)
    return JsonResponse({"message":"message"})
