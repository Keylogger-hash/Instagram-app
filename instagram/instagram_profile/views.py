from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from instagram_profile.models import Profile,Image,Post, Comment, Like
from instagram_profile.forms import AddPostForm,UpdateProfileForm,UsernameForm
from instagram_profile.serializers import ImageSerializer

from django.db.models import Q

from django.contrib.auth.decorators import login_required

#for ajax
from annoying.decorators import ajax_request
from rest_framework import generics

from django.http import HttpResponse

from django.urls import reverse
from django.http import HttpResponseRedirect
#Views
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("instagram_profile:feed"))
    else:
        return HttpResponseRedirect(reverse("accounts:login"))
#

class UpdateProfileView(LoginRequiredMixin,UpdateView):
    model = Profile
    second_model = User
    form_class = UpdateProfileForm
    second_form_class = UsernameForm
    pk_url_kwarg = 'pk'
    template_name = "instagram_profile/profile/update_profile.html"

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return HttpResponseRedirect(reverse("instagram_profile:profile",args=(pk,)))

    def get_context_data(self,**kwargs):
        context = super(UpdateProfileView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        profile = get_object_or_404(self.model,id=int(pk))
        user = get_object_or_404(self.second_model,id=int(pk))
        context['profile_form'] = self.form_class(instance=profile)
        context['username_form'] = self.second_form_class(instance=user)
        return context

    def form_invalid(self,profile_form,username_form,*args,**kwargs):
        return self.render_to_response(self.get_context_data({'profile_form':profile_form,'username_form':username_form}))

    def post(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        profile = get_object_or_404(self.model,id=int(pk))
        user = get_object_or_404(self.second_model,id=int(pk))
        profile_form = self.form_class(instance=profile,data=request.POST,files=request.FILES)
        username_form = self.second_form_class(instance=user,data=request.POST)
        print(profile_form.is_valid())
        print(username_form.is_valid())
        if profile_form.is_valid() and username_form.is_valid():
            profile_form.save()
            username_form.save()
            return self.get_success_url()
        else:
            return self.form_invalid(profile_form,username_form)


class AddPostView(View,LoginRequiredMixin):
    template_name = "instagram_profile/post/add_post.html"
    form_class = AddPostForm

    def get(self,request,*args,**kwargs):
        form = self.form_class()
        context = {"form":form}
        return render(request,self.template_name,context=context)

    def post(self,request,*args,**kwargs):
        profile = self.request.user.profile
        form = self.form_class(data=request.POST,files=request.FILES)
        if form.is_valid():
            text = form.cleaned_data["text"]
            first_image = form.cleaned_data["first_image"]
            attachments = self.request.FILES.getlist("attachments")
            print(attachments)
            post = Post(profile=profile,text=text,first_image=first_image)
            post.save()
            for im in attachments:
                Image.objects.create(post_id=post.id,image_url=im)
            return HttpResponseRedirect(reverse('instagram_profile:post',args=(profile.id,post.id)))


class ImageView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        profile_id = self.kwargs['profile_id']
        queryset = Image.objects.filter(post__id=post_id,post__profile__id=profile_id)
        return queryset

class PostView(DetailView):
    model = Post
    template_name = "instagram_profile/post/post.html"
    context_object_name = "post"

    def get_object(self,**kwargs):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(id=post_id)

    def get_context_data(self,**kwargs):
        context = super(PostView,self).get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        profile_id = self.kwargs.get('profile_id')
        comments = Comment.objects.filter(post__id=post_id,post__profile__id=profile_id)
        liked = False
        if Like.objects.filter(user=self.request.user.id,post__id=post_id).exists():
            liked = True
        context["is_liked"] = liked
        context["comments"] = comments
        return context


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


class ProfileView(View,LoginRequiredMixin):
    template_name = "instagram_profile/profile/profile.html"

    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(id=pk)
        post = Post.objects.filter(profile__id=pk)
        is_subscribed = True if request.user.profile in profile.subscribers.all() else False
        context = {"profile":profile,"post":post,"is_subscribed":is_subscribed}
        return render(request,self.template_name,context=context)


class SubscribersView(View,LoginRequiredMixin):
    template_name = "instagram_profile/subscribers/subscribers_list.html"

    def get(self,request,username):
        profile = Profile.objects.get(user=User.objects.get(username=username))
        subscribers = profile.subscribers.all()
        context={"subscribers":subscribers}
        return render(request,self.template_naem,context=context)


class FollowersView(View,LoginRequiredMixin):
    template_name = "instagram_profile/followers/followers_list.html"
    def get(self,request,username):
        profile = Profile.objects.get(user=User.objects.get(username=username))
        followers = profile.followers.all()
        context = {"followers":followers}
        return render(request,self.template_name,context=context)


class ProfileListView(ListView,LoginRequiredMixin):
    model = Profile
    template_name = "instagram_profile/profile/profile_list.html"
    context_object_name = 'profile_to_list'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeedView(View,LoginRequiredMixin):
    template_name = "instagram_profile/feed/feed.html"

    def get(self,request):
        profile = Profile.objects.get(user=request.user.id)
        subscribers = profile.followers.all()
        posts = Post.objects.filter(profile__in=subscribers).order_by("created_at")
        context = {"posts":posts}
        return render(request,self.template_name,context=context)
