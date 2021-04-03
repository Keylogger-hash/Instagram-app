from django.urls import path
from instagram_profile import views


urlpatterns = [
   path("",views.index,name="index"),
   path("register/",views.registerPage,name="register"),
   path("login/",views.loginPage,name="login"),
   path("friends/",views.profile_list,name="profile_list"),
   path("feed/",views.feed,name="feed"),
   path("subscribe/",views.subscribe,name="subscribe"),
   path("inbox/",views.inbox,name="inbox"),
   path("chat/<str:label>/",views.chat,name="chat"),
   path("profile/<int:pk>/",views.profile,name="profile"),
   path("profile/update_profile/<int:id>/",views.update_profile,name="update_profile"),
   path("profile/subscribers/<str:username>/",views.subscribers_list,name="subscribers_list"),
   path("profile/followers/<str:username>/",views.followers_list,name="followers_list"),
   path("post/<int:profile_id>/<int:post_id>/",views.post,name="post"),
   path("post/add_post",views.add_post,name="add_post"),
   path("add_comment/",views.add_comment,name="comments"),
   path("add_like/",views.add_like,name="add_like"),
   path("api/image/<int:profile_id>/<int:post_id>/",views.ImageView.as_view(),name="image_view")
]
