from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username if self.user else 'No user'
    
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Image(models.Model):
    EXTENSION_SELECTION = [
        ("j", ".jpg"),
        ("je", ".jpeg"),
        ("p", ".png"),
        ("b", ".bmp"),
        ("g", ".gif"),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=EXTENSION_SELECTION)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    content = models.CharField(max_length=500)
    comment_added_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-comment_added_date']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Password(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    password = models.CharField(max_length=30)

class Post_Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
