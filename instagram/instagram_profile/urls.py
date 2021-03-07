from django.urls import path
from instagram_profile import views


urlpatterns = [
   path("profile/",views.ListProfile.as_view(),name="list_profile"),
   path("profile/<int:id>/",views.DetailProfile.as_view(),name="detail_profile"),
   path("post_image/<int:id>/",views.ImageDetail.as_view(),name="detail_image"),
   path("profile/post/<int:id>/",views.PostDetail.as_view(),name="post_detail")
]
