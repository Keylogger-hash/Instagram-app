from django.urls import path
from instagram_profile import views


urlpatterns = [
   path("",views.index,name="index"),
   path("profile/<int:pk>/",views.profile,name="profile"),
   path("post/<int:profile_id>/<int:post_id>/",views.post,name="post")
]
