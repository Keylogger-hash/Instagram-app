from django.contrib import admin
from instagram_profile.models import Profile,Image,Post,Comment,Like

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
