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
        return render(request,'account/index.html')
    else:
        return render(request,'home/index.html')
@login_required
def profile(request):
    if request.user.is_authenticated:
        user=request.user.userprofileinfo
        genes=have.objects.filter(user_id=user)
        sibling1=Sibling.objects.filter(sibling1=user)
        sibling2=Sibling.objects.filter(sibling2=user)
        siblings=sibling1.union(sibling2)
        SelfTest=tests.objects.filter(accessor=user)
        if len(SelfTest)==0:
            SelfTest=False
        else:
            SelfTest=SelfTest[0]
        if user.sex:
            children=UserProfileInfo.objects.filter(dad=user)
        else:
            children=UserProfileInfo.objects.filter(mom=user)
        if user.mom.user.username=='BlankMom':
            user.mom=None
        if user.dad.user.username=="BlankDad":
            user.dad=None
        if len(siblings)==0 and len(children)==0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'test':SelfTest})
        elif len(siblings)>0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'siblings':siblings,'test':SelfTest})
        elif len(children)>0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'children':children,'test':SelfTest})
        elif len(children)>0 and len(siblings)>0:
            return render(request,'account/profile.html',{'profile':user,'genes':genes,'children':children, 'siblings':siblings,'test':SelfTest})


    else:
        return HttpResponseRedirect('/account/')

@login_required
def AddFamilyMember(request,member):
    user=request.user.userprofileinfo


    if member=='dad':
        dad=User.objects.get(username=request.POST.get('dad'))
        dad=UserProfileInfo.objects.get(user=dad)
        user.dad=dad
        user.save()
        return HttpResponseRedirect('/account/profile/')
    elif member=='mom':
        mom=User.objects.get(username=request.POST.get('mom'))
        mom=UserProfileInfo.objects.get(user=mom)
        user.mom=mom
        user.save()
        return HttpResponseRedirect('/account/profile/')
    elif member=='sibling':
        sibling=User.objects.get(username=request.POST.get('sibling'))
        sibling=UserProfileInfo.objects.get(user=sibling)
        s=Sibling.objects.create(sibling1=user,sibling2=sibling)
        s.save()
        return HttpResponseRedirect('/account/profile/')
    elif member=='child':
        child=User.objects.get(username=request.POST.get('child'))
        child=UserProfileInfo.objects.get(user=child)
        if user.sex:
            child.dad=user
            child.save()
        else:
            child.mom=user
            child.save()
        return HttpResponseRedirect('/account/profile/')
