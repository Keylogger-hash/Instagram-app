from django.shortcuts import render
from instagram_profile.models import Profile,Image,Post


def index(request):
    context={}
    return render(request,"base.html",context=context)


def post(request,profile_id,post_id):
    image_to_post = Image.objects.filter(post__id=post_id,post__profile__id=profile_id)
    post = Post.objects.get(id=post_id)
    context={"image_to_post":image_to_post,"post":post}
    return render(request,"post/post.html",context)

def profile(request,pk):
    profile = Profile.objects.get(id=pk)
    context = {"profile":profile}
    return render(request,"profile/profile.html",context=context)
