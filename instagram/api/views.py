#models
from instagram_profile.models import Comment,Like,Profile,Post,Image
from django.contrib.auth.models import User
# APIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
#other things
from rest_framework.response import Response
from rest_framework import status
#serializers
from api.serializers import SubscribeSerializer
from api.serializers import ImageSerializer
from api.serializers import CommentSerializer
from api.serializers import LikeSerializer
# csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#get object
from django.shortcuts import get_object_or_404
#http object
from django.http import Http404
# Session authentication
from rest_framework.authentication import SessionAuthentication
# Create your views here.
class ImageView(ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        profile_id = self.kwargs['profile_id']
        queryset = Image.objects.filter(post__id=post_id,post__profile__id=profile_id)
        return queryset


class BaseLikeView(object):

    def _is_liked(self,post_id,user_id):
        is_liked=False
        if Like.objects.filter(post_id=post_id,user=user_id).exists():
            is_liked=True
        else:
            is_liked=False
        return is_liked

    def _get_total_likes(self,post_id):
        post = get_object_or_404(Post,id=post_id)
        return post.get_count_of_likes()

    def get_object(self,post_id,user_id):
        like = get_object_or_404(Like,post=post_id,user=user_id)
        return like


class CreateLikeView(APIView,BaseLikeView):

    def post(self,request):
        data = request.data.dict()
        data.pop("csrfmiddlewaretoken",None)
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            post = data["post"]
            user = data["user"]
            is_liked = self._is_liked(post,user)
            serializer.save()
            is_liked = True
            total_likes = self._get_total_likes(post)
            context = {
            'is_liked':is_liked,
            'total_likes':total_likes
            }
            return Response(context,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DeleteLikeView(APIView,BaseLikeView):
    permission_classes = ()
    authentication_classes = ()

    def delete(self,request,post_id,user_id,format=None):
        like = self.get_object(post_id,user_id)
        like.delete()
        is_liked = self._is_liked(post_id,user_id)
        total_likes = self._get_total_likes(post_id)
        context = context = {
        'is_liked':is_liked,
        'total_likes':total_likes
        }
        return Response(context,status=status.HTTP_201_CREATED)


class CreateCommentView(APIView):

    def get(self,request,format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)


    def post(self,request,format=None):
        data = request.data.dict()
        data.pop("csrfmiddlewaretoken",None)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            text = serializer.data["text"]
            post_id = serializer.data["post"]
            context = {"comment_text":text,
            "username":self.request.user.username,
            "post_id":post_id,
            "image_pic":self.request.user.profile.image_pic.url}
            return Response(context,
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BaseSubscribeView(object):

    def _get_subscriber(self,profile_id):
        subscriber = get_object_or_404(Profile,id=profile_id)
        return subscriber

    def _get_follower(self,user_id):
        follower = get_object_or_404(Profile,id=user_id)
        return follower


class CreateSubscribeView(APIView,BaseSubscribeView):

    def add_subscriber(self,subscriber,follower):
        subscriber.subscribers.add(follower)
        follower.followers.add(subscriber)

    def post(self,request):
        data = request.data.dict()
        data.pop("csrfmiddlewaretoken",None)
        serializer = SubscribeSerializer(data=data)
        if serializer.is_valid():
            profile_id = data["profile_id"]
            user_id = data["user_id"]
            subscriber = self._get_subscriber(profile_id)
            follower = self._get_follower(user_id)
            self.add_subscriber(subscriber,follower)
            subscribers_count = subscriber.get_count_of_subscribers()
            context = {
            "subscriber_count":subscriber.get_count_of_subscribers(),
            }
            return Response(context,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
           return None

        return (user, None)

class DeleteSubscribeView(APIView,BaseSubscribeView):

    authentication_classes = (UnsafeSessionAuthentication,)

    def remove_subscriber(self,subscriber,follower):
        subscriber.subscribers.remove(follower)
        follower.followers.remove(subscriber)

    def delete(self,request,profile_id,user_id):
        subscriber = self._get_subscriber(profile_id)
        follower = self._get_follower(user_id)
        self.remove_subscriber(subscriber,follower)
        subscribers_count = subscriber.get_count_of_subscribers()
        context = {
        "subscriber_count":subscriber.get_count_of_subscribers(),
        }
        return Response(context,status=status.HTTP_201_CREATED)
