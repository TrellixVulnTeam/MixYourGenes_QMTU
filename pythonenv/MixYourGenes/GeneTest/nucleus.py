
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from GeneTest.models import *
from django.urls import reverse
import datetime
from django.utils.timezone import utc
from django.views.generic.base import TemplateView
from random import randrange
import math
from django.contrib.auth.models import User
from scipy.special import comb
from matplotlib import pyplot as plt
from MixYourGenes.settings import MEDIA_DIR

#---------------------------METHODS--------------------------------

def gene_vector(request):
    u=user.objects.create(first_name=request.POST.get('u_first_name', False), last_name=request.POST.get('u_last_name', False), ID=request.POST.get('u_ID', False), e_mail=request.POST.get('u_e_mail', False), psw=request.POST.get('u_psw', False),sex=request.POST.get('u_sex', False),profile_picture=request.POST.get('u_profile_picture', False))
    for i in request.POST.keys():
        if i!='csrfmiddlewaretoken' and i.find('u_')==-1:
            h=have.objects.create(user_id=u, gene_name=gene.objects.get(name=request.POST.get(i, False)))
    return render(request,'index.html',{'user_data':u})




#-----------------------------TESTS---------------------------------
#import Bio.SeqIO


#for record in SeqIO.parse("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/sample/hg38.fa", "fasta"):
#    print(record.id)

global INHERITANCE
#INHERITANCE={"dominant":{2:(11/12),1:0.5,0:1},"intermedier":{2:,1.5:0,1:0,0.5:0,0:1},"kodominant":""}
INHERITANCE={"dominance":{2.0:["A.A;A.A","A.A;A.a","A.a;A.a"],1.0:["A.A;a.a","A.a;a.a;"],0.0:["a.a;a.a"]},
            "intermedier":{2.0:["A.A;A.A"],1.5:["A.A;A.a"],1.0:["A.a;A.a","A.A;a.a"],0.5:["A.a;a.a"],0.0:["a.a;a.a"]},
            "codominant":{2.0:["A.A;A.A","A.A;A.a","A.a;A.a"],1.0:["A.A;a.a","A.a;a.a;"],0.0:["a.a;a.a"],- 1.0:["B.B;b.b","B.b;b.b;"],- 2.0:["B.B;B.B","B.B;B.b","B.b;B.b"]},
            }

def deenterizator(string):
    string=list(string)
    string.pop()
    string="".join(string)
    return string

class Allele():
    def __init__(self,genotype,inheritance):
        self.max_likelihood=0
        self.min_likelihood=0
        self.is_new=False
        if inheritance=="dominance":
            self.DomRecombination(INHERITANCE[inheritance][genotype],'a')
        elif inheritance=="intermedier":
            self.IntRecombination(INHERITANCE[inheritance][genotype])
        elif inheritance=="codominant":
            if genotype<=0:
                self.DomRecombination(INHERITANCE[inheritance][genotype],'b')
            elif genotype>100:
                self.CoRecombination(genotype)
            elif genotype>=0:
                self.DomRecombination(INHERITANCE[inheritance][genotype],'a')

    def DomRecombination(self,allele_list,locus=None):
        DominantLikelihood=0
        RecessiveLikelihood=0
        cases=0
        for i in allele_list:
            a=i.split(';')
            b1=a[0].split('.')
            b2=a[1].split('.')
            for j in range(2):
                cases=cases+1
                if b1[j]>b2[j]:
                    RecessiveLikelihood=RecessiveLikelihood+1
                elif b1[j]==b2[j]:
                    if b1[j]==locus:
                        RecessiveLikelihood=RecessiveLikelihood+1
                    else:
                        DominantLikelihood=DominantLikelihood+1
                else:
                    DominantLikelihood=DominantLikelihood+1
        likelihoods=set([(DominantLikelihood/cases),(RecessiveLikelihood/cases)])
        self.max_likelihood=round(max(likelihoods),4)
        self.min_likelihood=round(min(likelihoods),4)

    def IntRecombination(self,allele_list):
        DominantLikelihood=0
        RecessiveLikelihood=0
        IntermedierLikelihood=0
        cases=0
        for i in allele_list:
            a=i.split(';')
            b1=a[0].split('.')
            b2=a[1].split('.')
            for j in range(2):
                cases=cases+1
                if b1[j]>b2[j]:
                    IntermedierLikelihood=IntermedierLikelihood+1
                elif b1[j]==b2[j]:
                    if b1[j]=="a":
                        RecessiveLikelihood=RecessiveLikelihood+1
                    else:
                        DominantLikelihood=DominantLikelihood+1
                else:
                    IntermedierLikelihood=IntermedierLikelihood+1
        likelihoods=set([(DominantLikelihood/cases),(RecessiveLikelihood/cases),(IntermedierLikelihood/cases)])
        self.max_likelihood=round(max(likelihoods),4)
        self.min_likelihood=round(min(likelihoods),4)
        if self.max_likelihood==IntermedierLikelihood or self.min_likelihood==IntermedierLikelihood:
            self.is_new=True

    def CoRecombination(self,genotype):
        CodominantLikelihood=0
        Dom1Likelihood=0
        Dom2Likelihood=0
        cases=0
        if genotype==999:
            CodominantLikelihood=(3/8)
            Dom1Likelihood=(1/8)
            Dom2Likelihood=0.5


        #elif genotype==999.5:
        #    pass
        elif genotype==1000:
            CodominantLikelihood=0
            Dom1Likelihood=0.5
            Dom2Likelihood=0.5
            self.is_new=True
        #elif genotype==1000.5:
        #    pass
        elif genotpye==1001:
            CodominantLikelihood=(3/8)
            Dom2Likelihood=(1/8)
            Dom1Likelihood=0.5
        elif genotype==2000:
            CodominantLikelihood=0.5
            Dom1Likelihood=0.25
            Dom2Likelihood=0.25
        likelihoods=set([Dom1Likelihood,Dom2Likelihood,CodominantLikelihood])
        self.max_likelihood=round(max(likelihoods),4)
        self.min_likelihood=round(min(likelihoods),4)
#        if self.max_likelihood==Dom2Likelihood or self.min_likelihood==Dom2Likelihood:
#            self.is_new=True

class Gene():
    def __init__(self,trait,name,inheritance,user,genotype):
        self.trait=trait
        self.name=name
        self.dominancy=genotype
        self.inheritance=inheritance
        self.user=user

    def max_recombination(self,other,ref):#according to the genotypes, it results the set of traits which have the highest likelihood to has been resulted
        if not ref:
            r=self.dominancy+other.dominancy
            cross_over=Allele(r,other.inheritance)
            if abs(self.dominancy)>abs(other.dominancy):
                if self.dominancy==1000:
                    if cross_over.is_new:
                        return Recombination_result(self.name,self.inheritance,1000,[],cross_over.max_likelihood)
                    else:
                        return Recombination_result(self.name,self.inheritance,1000,[self.user],cross_over.max_likelihood)
                else:
                    if cross_over.is_new:
                        return Recombination_result(self.name,self.inheritance,1,[],cross_over.max_likelihood)
                    else:
                        return Recombination_result(self.name,self.inheritance,1,[self.user],cross_over.max_likelihood)
            elif self.dominancy==other.dominancy:
                if cross_over.is_new:
                    return Recombination_result(self.name,self.inheritance,r/2,[],cross_over.max_likelihood)
                else:
                    return Recombination_result(self.name,self.inheritance,r/2,[self.user,other.user],cross_over.max_likelihood)
            else:
                if other.dominancy==1000:
                    if cross_over.is_new:
                        return Recombination_result(other.name,other.inheritance,1000,[],cross_over.max_likelihood)
                    else:
                        return Recombination_result(other.name,other.inheritance,1000,[other.user],cross_over.max_likelihood)
                else:
                    if cross_over.is_new:
                        return Recombination_result(other.name,other.inheritance,1,[],cross_over.max_likelihood)
                    else:
                        return Recombination_result(other.name,other.inheritance,1,[other.user],cross_over.max_likelihood)
        else:
            pass
    def min_recombination(self,other,ref):#according to the genotypes, it results the set of traits which have the lowest likelihood to has been resulted
        if not ref:
            r=self.dominancy+other.dominancy
            cross_over_s=Allele(r,self.inheritance)
            cross_over_o=Allele(r,other.inheritance)
            if self.dominancy>other.dominancy:
                if cross_over_s.is_new:
                    return Recombination_result(self.name,self.inheritance,1,[],cross_over_s.min_likelihood)
                else:
                    return Recombination_result(self.name,self.inheritance,1,[self.user],cross_over_s.min_likelihood)
            elif self.dominancy==other.dominancy:
                if cross_over_s.is_new:
                    return Recombination_result(self.name,self.inheritance,r/2,[],cross_over_s.min_likelihood)
                else:
                    return Recombination_result(self.name,self.inheritance,r/2,[self.user,other.user],cross_over_s.min_likelihood)
            else:
                if cross_over_o.is_new:
                    return Recombination_result(other.name,other.inheritance,1,[],cross_over_o.min_likelihood)
                else:
                    return Recombination_result(other.name,other.inheritance,1,[other.user],cross_over_o.min_likelihood)
        else:
            pass
class Figure():
    def __init__(self,user1=0,user2=0,common=0,new=0):

        self.user1_x=user1
        self.user2_x=user2
        self.common=+common
        self.new=new


class Recombination_result(Gene):
    def __init__(self,name, inheritance,genotype,anchestor,possibility):
        self.name=name
        self.inheritance=inheritance
        self.possibility=possibility
        self.anchestor=anchestor

class test():
    def __init__(self,test,iv1,iv2,ivr,parent1,parent2,id):#DON'T FORGET TO DECLARE ivr
        self.id=id
        self.inherit_vector1=iv1
        self.inherit_vector2=iv2
        self.reference_vector=ivr
        self.parent1=parent1
        self.parent2=parent2
        self.result=""
        self.new_chromosome={}
        self.possibility={'min':1,'max':1}
        self.new_DNA={'min':[],'max':[]}
        self_figure=Figure()
        if test=="trait":
            return self.trait_()
        elif test=="Desease":
            return self.desease()

    def trait_(self):
        ir1=set()
        ir2=set()
        irref=set()
        size=max([len(self.inherit_vector1),len(self.inherit_vector2),len(self.reference_vector)])
        for i in range(size):
            try:
                ir1.add(self.inherit_vector1[i].trait)
            except:
                pass
            try:
                ir2.add(self.inherit_vector2[i].trait)
            except:
                pass
            try:
                irref.add(self.reference_vector[i].trait)
            except:
                pass
        if len(irref)==0:
            genes=ir1.intersection(ir2)
        else:
            genes=ir1.intersection(ir2.intersection(irref))
        allele={'min':"",'max':""}
        for i in genes:
            allele['max']=self.get_gene(i,self.inherit_vector1).max_recombination(self.get_gene(i,self.inherit_vector2),self.get_gene(i,self.reference_vector))
            allele['min']=self.get_gene(i,self.inherit_vector1).min_recombination(self.get_gene(i,self.inherit_vector2),self.get_gene(i,self.reference_vector))
            self.possibility['min']=self.possibility['min']*allele['min'].possibility
            self.possibility['max']=self.possibility['max']*allele['max'].possibility
            print('allele\t',allele)
            self.new_DNA['min'].append(allele['min'])
            self.new_DNA['max'].append(allele['max'])
        self.new_chromosome['min']=[i for i in self.new_DNA['min']],self.possibility['min']
        self.new_chromosome['max']=[i for i in self.new_DNA['max']],self.possibility['max']
        self.which_user()
        self.BinomialDistribution(genes)

    def which_user(self):#according to the genotypes, it results the likelihood of which of the parents' trait is going to be passed to the successor
        new_chromosome=list(self.new_chromosome['max'][0])
        parents={self.parent1:0,self.parent2:0,'common':0,'new':0}
        up=(1/len(new_chromosome))
        for j in new_chromosome:
            print(j.name)
            if len(j.anchestor)==1:
                parents[j.anchestor[0]]=parents[j.anchestor[0]]+up
            elif len(j.anchestor)==2:
                parents['common']=parents['common']+up
            else:
                parents['new']=parents['new']+up
            self.figure=Figure(parents[self.parent2],parents[self.parent2],parents['common'],parents['new'])

    def get_gene(self,string,gene_vector):
        for i in gene_vector:
            if i.trait==string:
                return i
        return False

    def desease(self):
        pass

    def binomial(self,NumberOfGenes,AllGene,possibility):
        return comb(AllGene,NumberOfGenes)*(possibility**NumberOfGenes)*((1-possibility)**(AllGene-NumberOfGenes)),comb(AllGene,NumberOfGenes)
    def BinomialDistribution(self,gene_vector):
        PossibilityTrendLine=[]
        HistogramArray=[]
        DistributionDict={}
        carrier=0
        for i in gene_vector:
            if (self.get_gene(i,self.inherit_vector2).dominancy==0 and self.get_gene(i,self.inherit_vector1).dominancy==1) or (self.get_gene(i,self.inherit_vector2).dominancy==1 and self.get_gene(i,self.inherit_vector1).dominancy==0):
                carrier=carrier+1
        for j in range(0,carrier+1):
            PTL,HA=self.binomial(AllGene=carrier,NumberOfGenes=j,possibility=0.75)
            PossibilityTrendLine.append(PTL)
            for i in range(0,int(HA)):
                HistogramArray.append(j)


        #creating figure
        plt.figure(figsize=[10, 10])

        fig=plt.figure(figsize=[10,10])

        ax1 = fig.add_subplot(1,1,1)
        ax1.set_xlabel('Number of dominant genes')
        ax1.set_ylabel('Number of cases',)
        ax1.hist(HistogramArray, bins=7, color='blue')
        ax1.tick_params(axis='y')

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        ax2.set_ylabel('Possibility')  # we already handled the x-label with ax1
        ax2.plot([i for i in range(carrier+1)], PossibilityTrendLine, color="black")
        ax2.tick_params(axis='y')
        fig.tight_layout()
        fig.gca().set_position([0, 0, 1, 1])
        fig.savefig(str(MEDIA_DIR)+"/plots/"+str(self.id)+".svg")



def ID_creator(test,user1,user2):
    return str(user1[:3])+test[:3]+user2[:3]+str(randrange(1000,9999))


def run(user1,user2,test_type):
    RESULT={'user1':None,'user2':None,'genes':[],'result':None,'figure':None}
    id=ID_creator(test_type,user1.user.username,user2.user.username)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    inherit_vector1,inherit_vector2=[],[]
    referece=[]
    #for i in request.POST.keys():
    #for i in request.keys():
    #    try:
    #        g=gene.objects.get(name=i)
    #        referece.append(Gene(g.name,trait.objects.get(name=g.trait_name.name).inheritance,user1.user.username,g.genotype))
    #    except:
    #        pass

    gene_vector=have.objects.filter(user_id=user1)
    for i in gene_vector:
        if i.user_id.user.username==user1.user.username:
            g=gene.objects.get(name=i.gene_name.name)
            inherit_vector1.append(Gene(g.trait_name.name,g.name,trait.objects.get(name=g.trait_name.name).inheritance,user1.user.username,g.genotype))
    gene_vector=have.objects.filter(user_id=user2)
    for i in gene_vector:
        if i.user_id.user.username==user2.user.username:
            g=gene.objects.get(name=i.gene_name.name)
            inherit_vector2.append(Gene(g.trait_name.name,g.name,trait.objects.get(name=g.trait_name.name).inheritance,user2.user.username,g.genotype))
    rc=tests.objects.create(user_id1=user1,user_id2=user2,date=now,test_type=test_type,test_id=id)
    r=test(test_type,inherit_vector1,inherit_vector2,referece,user1.user.username,user2.user.username,id)
    for i in ['min','max']:
        for j in r.new_chromosome[i][0]:
            if len(j.anchestor)==2:
                for k in j.anchestor:
                    if k==user1.user.username:
                        u=user1
                    else:
                        u=user2
                    rr=recombination.objects.create(test_id=rc,user_id=u,user_gene=gene.objects.get(name=j.name),possibility=j.possibility,type=i,label="common")
                    RESULT['genes'].append(rr)
            elif len(j.anchestor)==1:
                if j.anchestor[0]==user1.user.username:
                    u=user1
                else:
                    u=user2
                rr=recombination.objects.create(test_id=rc,user_id=u,user_gene=gene.objects.get(name=j.name),possibility=j.possibility,type=i, label="parent")
                RESULT['genes'].append(rr)
            elif len(j.anchestor)==0:
                rr=recombination.objects.create(test_id=rc,user_id=user1,user_gene=gene.objects.get(name=j.name),possibility=j.possibility,type=i, label="new")
                rr=recombination.objects.create(test_id=rc,user_id=user2,user_gene=gene.objects.get(name=j.name),possibility=j.possibility,type=i, label="new")
    rres=results.objects.create(test_id=rc,min_possibility=r.possibility['min'],max_possibility=r.possibility['max'])
    fig=figure.objects.create(test_id=rc,user1_x=r.figure.user1_x,user2_x=r.figure.user2_x,new=r.figure.new,common=r.figure.common)
    RESULT['result']=rres
    RESULT['user1']=user1
    RESULT['user2']=user2
    RESULT['figure']=fig
    RESULT['test']=rc
    return RESULT
