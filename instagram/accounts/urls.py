from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name="accounts"
urlpatterns = [
   path("register/",views.RegisterView.as_view(),name="register"),
   path("register/<str:user_id>/<str:token>/",views.ActivateLink.as_view(),name="register_done"),
   path("password_setform",views.PasswordSetView.as_view(),name="password_setform"),
   path("login/",views.LoginView.as_view(),name="login"),
   path("logout/",views.LogoutView.as_view(),name="logout"),
   path("password_reset/",views.PasswordResetView.as_view(),name="password_reset"),
   path("reset/<str:uidb64>/<str:token>/",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/authorization/passwordResetConfirm.html"),name="password_reset_confirm"),
   path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/authorization/passwordResetComplete.html"),name="password_reset_complete"),
   path("password_reset_done/",views.PasswordResetDoneView.as_view(),name="password_reset_done"),
   path("password_change/",views.PasswordChangeView.as_view(),name="password_change"),
]
