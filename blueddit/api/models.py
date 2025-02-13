from django.db import models

#TODO Check many to many

# Create your models here.
class User(models.Model):
    #TODO image routes
    #TODO test password field
    #TODO help_text if needed
    profile_picture = models.ImageField(upload_to='images/profile_pictures/', null=True, default='images/profile_pictures/default.jpg')
    name = models.CharField(max_length=30, null=False)
    nickname = models.CharField(max_length=20, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

class Community(models.Model):
    community_picture = models.ImageField(upload_to='images/community_pictures/', null=True, default='images/community_pictures/default.jpg')
    name = models.CharField(max_length=30, null=False, unique=True)
    is_adult = models.BooleanField(null=False)

    def __str__(self):
        return self.name

class UserInCommunity(models.Model):
    is_admin = models.BooleanField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.nickname + ' in ' + self.community.name

class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    attached_picture = models.ImageField(upload_to='images/post_picture/', null=True)
    aura = models.IntegerField(null=False, default=0)
    is_adult = models.BooleanField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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