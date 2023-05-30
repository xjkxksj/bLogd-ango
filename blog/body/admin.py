
from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','post_added_date')
    list_filter = ("user",)
    search_fields = ['title', 'content']

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user','post_added_date')
    list_filter = ("user",)
    search_fields = ['post', 'content']

admin.site.register(Comment, CommentAdmin)