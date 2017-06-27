from django.contrib import admin
from account.models import Userprofile,SocratesSearch,Following,newspaper,Notification,Compare

class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user','location')
    search_fields = ('location',)
admin.site.register(Userprofile)
admin.site.register(SocratesSearch)
admin.site.register(Following)
admin.site.register(newspaper)
admin.site.register(Notification)
admin.site.register(Compare)

