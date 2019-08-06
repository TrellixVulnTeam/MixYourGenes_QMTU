from django.shortcuts import render
from home.forms import UserForm,UserProfileInfoForm
from home.models import UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        return render(request,'account/index.html',{'profile':user})
    else:
        return render(request,'account/index.html')
