from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from api import views

app_name="api"

urlpatterns = [
  path("add_like/",views.CreateLikeView.as_view(),name="add_like"),
  path("image/<int:profile_id>/<int:post_id>/",views.ImageView.as_view(),name="image_view"),
  path("subscribe/",views.CreateSubscribeView.as_view(),name="add_subscriber"),
  path("comment/",views.CreateCommentView.as_view(),name="add_comment"),
  path("delete_subscribe/<profile_id>/<user_id>/",views.DeleteSubscribeView.as_view(),name="delete_subscriber"),
  path("delete_like/<post_id>/<user_id>/",csrf_exempt(views.DeleteLikeView.as_view()),name="delete_like")
]
