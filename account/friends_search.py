from django.contrib.auth.models import User
from account.models import Userprofile
from django.db.models import Q

class FriendSearch:
    def get_list(self,firstname,lastname,name_user):

        if lastname!="":
            people=User.objects.filter(Q(first_name__icontains=firstname) | Q(last_name__icontains=lastname))
        else:
            people=User.objects.filter(Q(first_name__icontains=firstname) | Q(username__icontains=firstname) | Q(last_name__icontains=firstname))
        return people

    def get_pics(self,firstname,lastname,name_user):
        piclist=[]
        people_list=self.get_list(firstname,lastname,name_user)
        profile_list=Userprofile.objects.all()
        i=0
        for p in people_list:
            username=p.username
            for q in profile_list:
                if str(q.user) == str(username):
                    piclist.insert(i,q)
            i=i+1

        return piclist


