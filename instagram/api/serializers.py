from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from instagram_profile.models import Profile
from instagram_profile.models import Image,Post,Comment,Like
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SubscribeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text","user","post")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields=('user','post')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields=["image_url"]
        model = Image
