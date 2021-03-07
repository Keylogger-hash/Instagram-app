from django.shortcuts import render
from rest_framework import generics
from instagram_profile.serializers import ProfileListSerializer, ImageSerializer, PostSerializer
from instagram_profile.models import Profile, Image,Post
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class ListProfile(generics.ListCreateAPIView):
    serializer_class = ProfileListSerializer
    queryset = Profile.objects.all()



class DetailProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset=Profile.objects.all()
    serializer_class = ProfileListSerializer
    lookup_url_kwarg='id'


class PostDetail(generics.ListCreateAPIView):
    #queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Post.objects.filter(user__id=id)


class ImageDetail(generics.ListCreateAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Image.objects.filter(post__id=id)
