from django.shortcuts import render
from home.forms import UserForm,UserProfileInfoForm
from home.models import *
from GeneTest.models import *
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
@login_required
def profile(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        genes=have.objects.filter(user_id=user)
        parents=Parent.objects.filter(user=user)
        siblings=Sibling.objects.filter(user=user)
        if len(parents)==0 and len(siblings)==0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes})
        elif len(parents)>0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'parents':parents[0]})
        elif len(siblings)>0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'siblings':siblings})
        elif len(siblings)>0 and len(parents)>0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'siblings':siblings, 'parents':parents[0]})
    else:
        return HttpResponseRedirect('/account/')

@login_required
def AddFamilyMember(request,member):
    user=User.objects.get(username=request.user.username)
    user=UserProfileInfo.objects.get(user=user)
    if member=='dad':
        dad=User.objects.get(username=request.POST.get('dad'))
        dad=UserProfileInfo.objects.get(user=dad)
        parents=Parent.objects.filter(user=user)
        if len(parents)>0:
            parents[0].dad=dad
            parents[0].save()
        else:
            parents=Parent.create(user=user,dad=dad)
    elif member=='mom':
        mom=User.objects.get(username=request.POST.get('dad'))
        mom=UserProfileInfo.objects.get(user=mom)
        parents=Parent.objects.filter(user=user)
        if len(parents)>0:
            parents[0].mom=mom
            parents[0].save()
        else:
            parents=Parent.create(user=user,mom=mom)
    elif member=='sibling':
        sibling=User.objects.get(username=request.POST.get('sibling'))
        sibling=UserProfileInfo.objects.get(user=user)
        s=Sibling.create(user=user,sibling=sibling)
        s.save()

        return HttpResponseRedirect('/account/profile/')
