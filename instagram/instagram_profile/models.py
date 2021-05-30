from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    followers = models.ManyToManyField('Profile',related_name='profile_followers',blank=True)
    subscribers = models.ManyToManyField('Profile',related_name='profile_subscribers',blank=True)
    image_pic = ProcessedImageField(upload_to="photos",default="default.jpg",format='JPEG',options={'quality':100},null=True,blank=True)
    bio = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["created_at"]

    def get_count_of_post(self):
        return self.post_set.count()

    def get_count_of_subscribers(self):
        return self.subscribers.count()

    def get_count_of_followers(self):
        return self.followers.count()

    def __str__(self):
        return self.user.username



class Post(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    text = models.CharField(max_length=200)
    first_image = ProcessedImageField(upload_to="first_image",format="JPEG",options={'quality':100},null=True,blank=True)

    def get_absolute_url(self):
        return reverse('post',args=[str(self.profile.id),str(self.id)])

    def get_count_of_likes(self):
        return self.like_set.count()

    def get_count_of_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return "Post id:"+str(self.id)+" "+str(self.profile.user.username)


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post","user")

    def __str__(self):
        return "Id: "+str(self.id) + " Username:"+self.user.username+" Post:"+str(self.post.id)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
            return "Id: "+str(self.id) + " Username:"+self.user.username+" Post:"+str(self.post.id)


class Image(models.Model):
    image_url = ProcessedImageField(upload_to="post",processors=[ResizeToFill(200,200)],format='JPEG',options={'quality':100},blank=True,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
