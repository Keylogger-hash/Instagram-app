from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    image_pic = models.ImageField(upload_to=settings.MEDIA_ROOT+"/photos/")
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["created_at"]

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return "Post id:"+str(self.id)+" "+str(self.user.username)


class Image(models.Model):
    image_url = models.ImageField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
