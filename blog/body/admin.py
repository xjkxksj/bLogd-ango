from django.contrib import admin
from .models import Post, models, Tag
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
