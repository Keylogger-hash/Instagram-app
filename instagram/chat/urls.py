from django.urls import path
from chat import views

app_name="chat"
urlpatterns = [
    path("inbox/",views.inbox,name="inbox"),
    path("chat/<str:label>/",views.chat,name="chat"),
    path("chat_create/<str:username>/",views.chat_create,name="chat_create")
]
