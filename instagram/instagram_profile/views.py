from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from instagram_profile.models import Profile,Image,Post, Comment, Like
from instagram_profile.forms import AddPostForm,UpdateProfileForm,UsernameForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
#for ajax,api
#HttpResponses,reverse
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
            post = Post(profile=profile,text=text,first_image=first_image)
            post.save()
            for im in attachments:
                Image.objects.create(post_id=post.id,image_url=im)
            return HttpResponseRedirect(reverse('instagram_profile:post',args=(profile.id,post.id)))





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


class ProfileView(View,LoginRequiredMixin):
    template_name = "instagram_profile/profile/profile.html"

    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(id=pk)
        follower = request.user.profile
        post = Post.objects.filter(profile__id=pk)
        is_subscribed = True if follower in profile.subscribers.all() else False
        context = {"profile":profile,"post":post,"is_subscribed":is_subscribed}
        return render(request,self.template_name,context=context)


class SubscribersView(View,LoginRequiredMixin):
    template_name = "instagram_profile/subscribers/subscribers_list.html"

    def get(self,request,username):
        profile = Profile.objects.get(user=User.objects.get(username=username))
        subscribers = profile.subscribers.all()
        context={"subscribers":subscribers}
        return render(request,self.template_name,context=context)


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
