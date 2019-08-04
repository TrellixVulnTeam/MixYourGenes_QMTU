from django.shortcuts import render
from GeneTest.nucleus import *
from django.shortcuts import render
from home.forms import UserForm,UserProfileInfoForm
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
    traits=[]
    for i in trait.objects.all():
        if i.type=="trait" and i.inheritance=="dominance":
            traits.append(i)
        context={'genes':genes,'traits':traits,'user_data':u}
    return render(request,'tests/desease.html',context)

@login_required
def index(request):
    return HttpResponse('hej')
@login_required
def TraitTest(request):
    return HttpResponse('hejhej')
