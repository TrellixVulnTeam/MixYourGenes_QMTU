from django.shortcuts import render
from GeneTest.nucleus import *
from GeneTest.models import *
from django.shortcuts import render
from home.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from home.models import UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def trait_test(request,user):
    genes=gene.objects.all()
    traits=[]
    for i in trait.objects.all():
        if i.type=="trait" and i.inheritance=="dominance":
            traits.append(i)
        context={'genes':genes,'traits':traits,'user_data':u}
    return render(request,'tests/trait.html',context)

def desease_test(request,u):
    genes=gene.objects.all()
    desease=[]
    for i in trait.objects.all():
        if i.type=="desease" and i.inheritance=="dominance":
            traits.append(i)
        context={'genes':genes,'desease':desease,'user_data':u}
    return render(request,'tests/desease.html',context)

@login_required
def index(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        user_traits=have.objects.filter(user_id=user)
        if len(user_traits)>0:
            results=tests.objects.filter(user1_id=user)
            results=results+tests.objects.filter(user2_id=user)
            #here's going to be some history, previous tests
            return render(request,'GeneTest/index.html',{'results':results})
        else:
            traits=trait.objects.all()
            genes={}
            for i in traits:
                genes[i]=gene.objects.filter(trait_name=i)
            print(genes)
            return render(request,'GeneTest/gene_registration.html',{'genes':genes})
@login_required
def TraitTest(request):
    return HttpResponse('hejhej')

@login_required
def gene_registration(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        if request.method=='POST':
            for i in request.POST:
                print(i)
            return render(request,'GeneTest/index.html',{})
