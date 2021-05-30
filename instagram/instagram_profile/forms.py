from django import forms
from django.contrib.auth.models import User
from instagram_profile.models import Profile, Comment


class AddPostForm(forms.Form):
    text = forms.CharField(required=False)
    first_image = forms.ImageField()
    attachments = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}),required=False)


class UpdateProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UpdateProfileForm,self).__init__(*args,**kwargs)
        self.fields['bio'].required=False

    class Meta:
        model = Profile
        fields = ('image_pic','bio',)


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
