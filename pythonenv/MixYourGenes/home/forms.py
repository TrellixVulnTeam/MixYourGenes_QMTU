from django import forms
from django.contrib.auth.models import User
from home.models import UserProfileInfo
SEX=[(1,'Male'),(0,'Female')]
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password','first_name','last_name')


class UserProfileInfoForm(forms.ModelForm):
    sex=forms.ChoiceField(widget=forms.Select, choices=SEX)
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic','sex')
