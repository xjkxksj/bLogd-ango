from django.contrib import admin
from .models import Post, Tag, Comment, models
from django import forms
from django.utils.html import format_html

class PostAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    privacy = forms.ChoiceField(choices=(('public', 'Public'), ('private', 'Private')))

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'post_added_date', 'tags_list', 'display_image', 'privacy']
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'user', 'tags', 'image')
        }),
        ('Additional Information', {
            'fields': ('post_added_date', 'privacy'),
            'classes': ('collapse',),
            'description': 'Additional information about the post.'
        })
    )
    readonly_fields = ('post_added_date',)
    form = PostAdminForm

    def tags_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return format_html('<img src="{}" width="50" height="50" />', '/static/noimage.jpg')

    display_image.short_description = 'Image'

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
