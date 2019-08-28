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

@login_required
def index(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        user_traits=have.objects.filter(user_id=user)
        if len(user_traits)>0:
            results=tests.objects.filter(user_id1=user)
            results=results.union(tests.objects.filter(user_id2=user))
            print(results)
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
def TraitDeseaseTest(request,user1=None,user2=None):
    test_types={'Trait test':'trait','Desease test':'desease','Alltogether':'all'}
    if request.method=='POST':
        user1=User.objects.get(username=request.user.username)
        user1=UserProfileInfo.objects.get(user=user1)
        user2=User.objects.get(username=request.POST.get('User2',False))
        user2=UserProfileInfo.objects.get(user=user2)
        test_name=test_types[request.POST.get('test_type',False)]
        context=run(user1,user2,test_name)
        if user1.sex==user2.sex:
            return HttpResponse('Gays can\'t have children, sorry!')
        else:
            print(context)
            TEST={}
            TEST['test']=context['test']
            TEST['figure']=context['figure']
            TEST['result']=context['result']
            TEST['recombination']=recombination.objects.filter(test_id=context['test'])
            return render(request,'GeneTest/results.html',TEST)
    else:
        return HttpResponse('???')

@login_required
def SelfTest(request):
    if request.method=='POST':
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        mom=request.POST.get('mom')
        dad=request.POST.get('dad')
        user1=User.objects.get(username=mom)
        user1=UserProfileInfo.objects.get(user=user1)
        user2=User.objects.get(username=dad)
        user2=UserProfileInfo.objects.get(user=user2)
        test_name='trait'
        context=run(user1,user2,test_name)
        if user1.sex==user2.sex:
            return HttpResponse('Gays can\'t have children, sorry!')
        else:
            print(context)
            TEST={}
            TEST['test']=context['test']
            TEST['figure']=context['figure']
            TEST['result']=context['result']
            TEST['recombination']=recombination.objects.filter(test_id=context['test'])
            #t=tests.objects.get(test_id=TEST['test'].test_id)
            TEST['test'].accessor=user
            TEST['test'].save()
            return HttpResponseRedirect('/account/profile/')
    else:
        return HttpResponse('???')

@login_required
def result(request,test_id):
    if request.method=='GET':
        TEST={}
        TEST['test']=tests.objects.get(test_id=test_id)
        TEST['figure']=figure.objects.get(test_id=TEST['test'])
        TEST['result']=figure.objects.get(test_id=TEST['test'])
        TEST['recombination']=recombination.objects.filter(test_id=TEST['test'])
        print(TEST)
        return render(request,'GeneTest/results.html',TEST)
@login_required
def delete(request,test_id):
    if request.method=='GET':
        t=tests.objects.get(test_id=test_id)
        t.delete()
        return render(request,'account/index.html',{})
@login_required
def gene_registration(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        if request.method=='POST':
            for i in request.POST:
                if i!='csrfmiddlewaretoken':
                    h=have.objects.create(user_id=user, gene_name=gene.objects.get(NCIB_ID=request.POST.get(i)))
                    h.save()
            return render(request,'GeneTest/index.html',{})
@login_required
def DrawPedigree(request):
    user=User.objects.get(username=request.user.username)
    user=UserProfileInfo.objects.get(user=user)
    return render(request,'account/pedigree.html',{})
