from django.shortcuts import render
from instagram.settings import EMAIL_HOST_USER
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from .forms import SignUpForm,LoginForm,PasswordSetForm
#models User,Profile
from django.contrib.auth.models import User
from instagram_profile.models import Profile
from django.contrib.auth import update_session_auth_hash
#sending,encode decode mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError
# Redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
#View layer
from django.views import View
#Token generator
from accounts.core.tokens import account_activation_token
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from accounts.tasks import send_email
class RegisterView(View):
    def get(self,request):
        form = SignUpForm()
        return render(request,"accounts/authorization/register.html",context={"form":form})

    def post(self,request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()

            subject = "Email complete from localhost"
            email_template_name = 'accounts/utils/registerActivate.html'
            to_email = form.cleaned_data["email"]
            c = {
            "email":to_email,
            "domain":"127.0.0.1:8000",
            "site_name":"test_instagram",
            "user":user,
            "user_id":urlsafe_base64_encode(force_bytes(user.pk)),
            "token":account_activation_token.make_token(user),
            "protocol":"http"
            }
            email_text = render_to_string(email_template_name,context=c)
            try:
                send_email.delay(subject,email_text,EMAIL_HOST_USER,to_email)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return render(request,"accounts/authorization/registerComplete.html")
        return render(request,"accounts/authorization/register.html",context={"form":form})

class ActivateLink(View):
    def get(self,request,user_id,token):
        try:
            user_id = force_text(urlsafe_base64_decode(user_id))
            user = User.objects.get(pk=user_id)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            user.is_active=True
            user.save()
            Profile.objects.create(user=user)
            login(request,user)

            return HttpResponseRedirect(reverse("accounts:password_setform"))
        else:

            return HttpResponse("Invalid activation link")


class PasswordSetView(View,LoginRequiredMixin):
    def get(self,request):
        form = PasswordSetForm(user=request.user)
        return render(request,"accounts/authorization/passwordSet.html",context={"form":form})
    def post(self,request):
        form = PasswordSetForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return HttpResponseRedirect(reverse("instagram_profile:index"))
        else:
            return render(request,"accounts/authorization/passwordSet.html",context={"form":form,"errors":form.errors})

class LoginView(View):
    template_name = "accounts/authorization/login.html"
    def get(self,request):
        form = LoginForm()
        return render(request,self.template_name,context={"form":form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse("instagram_profile:feed"))
            else:
                return HttpResponseRedirect(reverse("accounts:login"))

class LogoutView(View):
    template_name = ""
    def get(self,request):
        return render(request,"accounts/authorization/logout.html")

    def post(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))


class PasswordResetView(View):
    template_name = "accounts/authorization/passwordReset.html"

    def get(self,request):
        form = PasswordResetForm()
        return render(request,self.template_name,context={"form":form})

    def post(self,request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            subject = "Password reset from localhost"
            user_email = form.cleaned_data["email"]
            users = User.objects.filter(email=user_email)
            if users.exists():
                for user in users:
                    email_template_name = "accounts/utils/passwordResetEmail.txt"
                    c = {
                    "email":user_email,
                    "domain":"127.0.0.1:8000",
                    "site_name":"test_instagram",
                    "user":user,
                    "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                    "token":default_token_generator.make_token(user),
                    "protocol":"http"
                    }
                    email_text = render_to_string(email_template_name,context=c)
                    try:
                        send_email.delay(subject,email_text,EMAIL_HOST_USER,user_email)
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                return HttpResponseRedirect(reverse('accounts:password_reset_done'))
            else:
                return HttpResponseRedirect(reverse("accounts:password_reset"))


class PasswordResetDoneView(View):
    template_name = "accounts/authorization/passwordResetDone.html"
    def get(self,request):
        return render(request,self.template_name)


class PasswordChangeView(View):
    template_name = "accounts/authorization/passwordChange.html"
    def get(self,request):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        return render(request,self.template_name,context={"form":form})

    def post(self,request):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,request.user)
            return HttpResponseRedirect(reverse("instagram_profile:index"))
        else:
            return HttpResponseRedirect(reverse("accounts:password_change"))
