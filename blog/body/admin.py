from django.contrib import admin
from .models import Post, models
from django import forms

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'post_added_date']
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(attrs={'rows': 10, 'cols': 40})},
    }

admin.site.register(Post, PostAdmin)
