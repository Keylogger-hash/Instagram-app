from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from instagram_profile.models import Profile, Comment

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)


class AddPostForm(forms.Form):
    text = forms.CharField()
    first_image = forms.ImageField()
    attachments = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}))

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image_pic','bio',)
