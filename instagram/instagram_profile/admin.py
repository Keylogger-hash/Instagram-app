from django.contrib import admin
from instagram_profile.models import Profile,Image,Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
