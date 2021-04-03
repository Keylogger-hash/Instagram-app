from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from instagram_profile.models import Profile,Image,Post, Comment, Like,Room
from instagram_profile.serializers import ImageSerializer
from instagram_profile.forms import SignUpForm, LoginForm,AddPostForm,UpdateProfileForm

from django.db.models import Q
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
# from django.core import serializers
# from django.http import JsonResponse
from annoying.decorators import ajax_request
from rest_framework import generics

def index(request):
    if request.user.is_authenticated:
        return redirect("feed")
    else:
        return redirect("login")

@login_required
def update_profile(request,id):
    profile=get_object_or_404(Profile,pk=id)
    user = User.objects.get(pk=id)
    if request.method == 'GET':
        form = UpdateProfileForm(instance=profile)
        context = {"form":form,"profile":profile}
        return render(request,"profile/update_profile.html",context=context)
    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
        username = request.POST.get('username')
        if form.is_valid():
            form.save()
        if user.username!=username:
            user.username = username
            user.save()
        return redirect("profile",pk=id)

@login_required
def add_post(request):
    if request.method=='GET':
        form = AddPostForm()
        context={"form":form}
        return render(request,"post/add_post.html",context)
    elif request.method=='POST':
        user = request.user
        first_image = request.FILES.get('first_image')
        text = request.POST.get('text')
        post = Post(profile=user.profile,text=text,first_image=first_image)
        post.save()
        post = Post.objects.last()
        for im in request.FILES.getlist('attachments'):
            print(im)
            Image.objects.create(post_id=post.id,image_url=im)
        return redirect("post/1/1")


class ImageView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        profile_id = self.kwargs['profile_id']
        queryset = Image.objects.filter(post__id=post_id,post__profile__id=profile_id)
        return queryset



def post(request,profile_id,post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post__id=post_id,post__profile__id=profile_id)
    liked = False
    print(post_id)
    print(request.user)
    if Like.objects.filter(user=request.user.id,post__id=post_id).exists():
        liked=True
    print(liked)
    context={"post":post,"comments":comments,"is_liked":liked}
    return render(request,"post/post.html",context)


@login_required
@ajax_request
def add_comment(request):
    user = request.user
    image_pic = request.user.profile.image_pic.url
    username = request.user.username
    text = request.POST.get("comment_text")
    post_id = request.POST.get("post_id")

    try:
        comment = Comment(user=user,text=text,post_id=post_id)
        comment.save()
        commenter_info = {"comment_text":text,"username":username}
        result = 1
    except Exception as e:
        print(e)
        result = 0
    return {"commenter_info":commenter_info,"result":result,"post_id":post_id,"image_pic":image_pic}


def chat(request,label):
    room = Room.objects.get(label=label)
    message = reversed(room.messages.order_by('-date_send')[:50])
    context = {"room":room,"message":message}
    return render(request,"feed/chat.html",context=context)


@login_required
def new_chat(request):
    profiles =  request.user.profile.subscribers.all()
    context = {
    'profiles':profiles
    }
    return render(request,'feed/new_chat.html',context=context)


@login_required
def inbox(request):
    inbox = Room.objects.filter(Q(reciever=request.user)|Q(sender=request.user))
    context = {
    "inbox":inbox
    }
    return render(request,"feed/inbox.html",context=context)

@login_required
def chat_create(request,username):
    user_to_message = User.objects.get(username=username)
    room_label = request.user.username+'_'+user.username
    try:
        does_room_exist = Room.objects.get(label=label)
    except:
        room = Room(label,reciever=user_to_message,sender=request.user)
        room.save()
    return redirect('chat',label=room_label)

@login_required
@ajax_request
def subscribe(request):
    profile_id = request.POST.get('profile_id') # профиль человека на который подписываются (subscriber)
    user = request.user # человек который хочет подписаться или отписаться (follower)
    # что надо если:
    #     1. Если человек не подписан, то надо добавить подписчика к Тому профилю на который подписались, и подписку к человеку который подписался.
    #     2. Если человек подписан и хочет отписаться, то нужно соответственно удалить.
    # Как проверить кто подписан?
    subscriber = Profile.objects.get(id=profile_id)
    follower = Profile.objects.get(id=user.id)
    is_subscribed = True if request.user.profile in subscriber.subscribers.all() else False
    if is_subscribed==True:
        subscriber.subscribers.remove(follower)
        follower.followers.remove(subscriber)
        is_subscribed = False
    else:
        subscriber.subscribers.add(follower)
        follower.followers.add(subscriber)
        is_subscribed = True
    context = {
    "subscriber_count":subscriber.get_count_of_subscribers(),
    "is_subscribed":is_subscribed
    }
    return context


@login_required
@ajax_request
def add_like(request):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    user = request.user
    post_id = request.POST.get('post_id')
    is_liked = False
    if Like.objects.filter(post_id=post_id,user=user).exists():
        like = Like.objects.get(user=user,post_id=post_id)
        like.delete()
        is_liked = False
    else:
        like = Like(user=user,post_id=post_id)
        like.save()
        is_liked = True
    context = {
    'is_liked':is_liked,
    'total_likes':post.get_count_of_likes()
    }
    return context


def profile(request,pk):
    profile = Profile.objects.get(id=pk)
    post = Post.objects.filter(profile__id=pk)
    print(request.user.profile)
#    is_subscribed = False
    is_subscribed = True if request.user.profile in profile.subscribers.all() else False
    print(is_subscribed)
    print(profile)
    context = {"profile":profile,"post":post,"is_subscribed":is_subscribed}
    return render(request,"profile/profile.html",context=context)


def subscribers_list(request,username):
    profile = Profile.objects.get(user=User.objects.get(username=username))
    subscribers = profile.subscribers.all()
    context={"subscribers":subscribers}
    return render(request,"subscribers/subscribers_list.html",context=context)


def followers_list(request,username):
    profile = Profile.objects.get(user=User.objects.get(username=username))
    followers = profile.followers.all()
    context = {"followers":followers}
    return render(request,"followers/followers_list.html",context=context)


def profile_list(request):
    profile_to_list = Profile.objects.all()
    context = {"profile_to_list":profile_to_list}
    return render(request,"profile/profile_list.html",context=context)


def feed(request):
    profile = Profile.objects.get(user=request.user.id)
    subscribers = profile.followers.all()
    posts = Post.objects.filter(profile__in=subscribers).order_by("created_at")
    context = {"posts":posts}
    return render(request,"feed/feed.html",context=context)


def registerPage(request):
    #form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect("login")
    else:
        form = SignUpForm()
    context = {"form":form}
    return render(request,"authorization/register.html",context=context)


def loginPage(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("profile_list")
    else:
        form = LoginForm()
    context = {"form":form}
    return render(request,"authorization/login.html",context=context)
