from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

class Community(models.Model):
    community_picture = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=30, null=False, unique=True)
    is_adult = models.BooleanField(null=False)

    def __str__(self):
        return self.name

class UserInCommunity(models.Model):
    is_admin = models.BooleanField(null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' in ' + self.community.name

class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    attached_picture = models.CharField(max_length=255, null=True, blank=True)
    aura = models.IntegerField(null=False, default=0)
    is_adult = models.BooleanField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + ' tagged with ' + self.tag.name