from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username if self.user else 'No user'
    
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True)
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField()
    comment_added_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-comment_added_date']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
