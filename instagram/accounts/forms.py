from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254,help_text='Enter a valid email for register')
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name')



class PasswordSetForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("Password1"),widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Password2"),widget=forms.PasswordInput)

    def __init__(self,user,*args,**kwargs):
        self.user = user
        super(PasswordSetForm,self).__init__(*args,**kwargs)

    def cleaned_password2(self):
        password1 = self.cleaned_data["new_password1"]
        password2 = self.cleaned_data["new_password2"]
        if password1 != password2:
            raise forms.ValidationError(
            self.error_messages["password_mismatch"],
            code="password_mismatch")
        return password2

    def save(self,commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
