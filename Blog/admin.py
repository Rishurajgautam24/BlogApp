from django.contrib import admin
from .models import *
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'upload_to')
    list_filter = ('user', 'created_at', 'upload_to')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    save_on_top = True
    list_per_page = 10

    



admin.site.register(Blog, BlogAdmin)   

 


