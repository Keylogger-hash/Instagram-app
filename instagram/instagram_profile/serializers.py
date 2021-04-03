from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from instagram_profile.models import Profile
from instagram_profile.models import Image,Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username","first_name","last_name")

class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields="__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields=["image_url"]
        model = Image







# class PostListSerializer(serializers.ModelSerializer):
#     class Meta:
#         models = Post
#         fields = "__all__"
#
# class ImageListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = "__all__"
