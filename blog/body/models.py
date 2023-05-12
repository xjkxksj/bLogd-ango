from django.db import models


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    date_of_registration = models.DateTimeField("Date of registration")
    nickname = models.CharField(max_length=30)


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_added_date = models.DateTimeField("Post added date")
    status = models.BooleanField()


class Image(models.Model):
    EXTENSION_SELECTION = [
        ("j", ".jpg"),
        ("je", ".jpeg"),
        ("p", ".png"),
        ("b", ".bmp"),
        ("g", ".gif"),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=EXTENSION_SELECTION)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    post_added_date = models.DateTimeField("Post added date")


class Password(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    password = models.CharField(max_length=30)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Post_Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)