from django.contrib import admin
from .models import Post, models, Tag, Comment
from django import forms

class PostAdminForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'post_added_date', 'tags_list']
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'user', 'tags', 'image')
        }),
        ('Additional Information', {
            'fields': ('post_added_date',),
            'classes': ('collapse',),
            'description': 'Additional information about the post.'
        })
    )
    readonly_fields = ('post_added_date',)
    form = PostAdminForm

    def tags_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

admin.site.register(Post, PostAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'content', 'comment_added_date']
    list_filter = ['post', 'user']
    search_fields = ['post__title', 'user__username']
    readonly_fields = ['comment_added_date']
    fieldsets = (
        (None, {
            'fields': ('post', 'user', 'content')
        }),
        ('Additional Information', {
            'fields': ('comment_added_date',),
            'classes': ('collapse',),
            'description': 'Additional information about the comment.'
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Comment, CommentAdmin)

