from django.urls import path
from instagram_profile import views
from instagram_profile.views import ProfileView


app_name="instagram_profile"
urlpatterns = [
   path("",views.index,name="index"),
   path("friends/",views.ProfileListView.as_view(),name="profile_list"),
   path("feed/",views.FeedView.as_view(),name="feed"),
   path("subscribe/",views.subscribe,name="subscribe"),
   path("profile/<int:pk>/",views.ProfileView.as_view(),name="profile"),
   path("profile/update_profile/<int:pk>/",views.UpdateProfileView.as_view(),name="update_profile"),
   path("profile/subscribers/<str:username>/",views.SubscribersView.as_view(),name="subscribers_list"),
   path("profile/followers/<str:username>/",views.FollowersView.as_view(),name="followers_list"),
   path("post/<int:profile_id>/<int:post_id>/",views.PostView.as_view(),name="post"),
   path("post/add_post",views.AddPostView.as_view(),name="add_post"),
   path("add_comment/",views.add_comment,name="comments"),
   path("add_like/",views.add_like,name="add_like"),
   path("api/image/<int:profile_id>/<int:post_id>/",views.ImageView.as_view(),name="image_view")
]
