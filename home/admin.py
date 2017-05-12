from django.contrib import admin
from .models import comment,Post

# Register your models here
class PostAdmin(admin.ModelAdmin):
    list_display = ('source','headline','date','likes','totalcomments')
    search_fields = ('source',)
    list_filter = ('date',)
    date_hierarchy = 'date'
    ordering = ('-date',)
admin.site.register(comment)
admin.site.register(Post,PostAdmin)
