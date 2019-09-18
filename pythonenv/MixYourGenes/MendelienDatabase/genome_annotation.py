import requests, sys
#from MendelienDatabase import models
from pyensembl import EnsemblRelease
import pickle
def loader(name):
        f=''
        infile=open(f+name,'rb')
        return pickle.load(infile)
def saver(obj,name):
    outfile=open(name,'wb')
    pickle.dump(obj,outfile)
    outfile.close()
class MendelienGene():
    def __init__(self,ENSMBL=None,chromosome=None,phenotype1=None,phenotype2=None,name=None,comments=None,GeneSymbol=None,prefix=None,phenotype3=None):
        self.ENSMBL=ENSMBL
        self.chromosome=chromosome
        self.phenotype1=phenotype1
        self.phenotype2=phenotype2
        self.phenotype3=phenotype3
        self.name=name
        self.GeneSymbol=GeneSymbol
        self.comments=comments
        self.prefix=prefix
        self.alternative_name=None
        self.annotation_comment=None
        def __str__(self):
            return self.ENSML
def deenterizator(string):
     string=list(string)
     string.pop()
     string="".join(string)
     return string
def get_sequence(geneID):
    try:
        server = "http://rest.ensembl.org"
        ext = "/sequence/id/"+geneID+"?type=genomic"
        r =requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        return t.text
    except:
        return ""

mim2gene={}#0,1,4
with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/mim2gene.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split(';')
        if gene[4]!="":
            mim2gene[gene[0]]=gene[4]
AllGene=[]
mim2gene2={}
with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/genemap2.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split(';')
        if gene[5] in mim2gene.keys():
            mim2gene2[gene[5]]=MendelienGene(ENSMBL=mim2gene[gene[5]],chromosome=gene[0],phenotype1=gene[12],name=gene[7],comments=gene[11],GeneSymbol=gene[6])

with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/genemap.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split(';')
        if gene[6] in mim2gene2.keys():
            mim2gene2[gene[6]].phenotype2=gene[10]

with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/mimTitles.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split('__:__')
        if gene[1] in mim2gene2.keys():
            mim2gene2[gene[1]].alternative_name=gene[2]
            mim2gene2[gene[1]].prefix=gene[0]

def category(string):
    if string.find('(3)')>-1:
        return [string.replace(' (3)',''),'The molecular basis for the disorder is known; a mutation has been found in the gene.']
    elif string.find('(4)')>-1:
        return [string.replace(' (4)',''),'A contiguous gene deletion or duplication syndrome, multiple genes are deleted or duplicated causing the phenotype.']
    elif string.find('(1)')>-1:
        return [string.replace(' (1)',''),'The disorder is placed on the map based on its association with a gene, but the underlying defect is not known.']
    elif string.find('(2)')>-1:
        return [string.replace(' (2)',''),'The disorder has been placed on the map by linkage or other statistical method; no mutation has been found.']
    else:
        return [string,'NA']
with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/morbidmap.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split(';')
        g=category(gene[2])
        if g[0] in mim2gene2.keys():
            mim2gene2[g[0]].phenotype3=gene[0]
            #mim2gene2[g[0]].GeneSymbol=mim2gene[g[0]].GeneSymbol+";"+gene[1]
            mim2gene2[g[0]].annotation_comment=g[1]
#saver(mim2gene2,'backup')
#mim2gene2=genome_annotation.loader('backup')
print(len(mim2gene2.values()))
counter={}
#file=open("DataBase.txt",'w')
#file.write('EnsemblID;Name;Sequence;Comments;Phenotype;Chromosome;GeneSymbol;IsInheritanceKnown\n')
for i in mim2gene2.values():
    print(type(i))
    if i.ENSMBL is not None:
        EN=i.ENSMBL
    else:
        EN=""
    if i.name is not None:
        n=i.name
    else:
        n=""
    if i.comments is not None:
        com=i.comments
    else:
        com=""
    ph=""
    for pht in [i.phenotype1,i.phenotype2,i.phenotype3]:
        if pht!=None:
            ph=ph+pht
    if i.chromosome is not None:
        ch=i.chromosome
    else:
        ch=""
    if i.GeneSymbol is not None:
        gs=i.GeneSymbol
    else:
        gs=""

    if ph!="":
#        seq="NotRelevant"
        if ph.find("recessive")>-1 or ph.find("dominant")>-1:
#            file.write(EN+';'+n+';'+seq+';'+com+';'+ph+';'+ch+';'+gs+';True\n')
#        else:
#            file.write(EN+';'+n+';'+seq+';'+com+';'+ph+';'+ch+';'+gs+';False\n')
#file.close()
            if len(models.MendelienGene.objects.filter(ensemblID=EN))==0:
                counter[EN]=0
                m=models.MendelienGene.objects.create(ensemblID=EN,gene_name=n,sequence=seq,type=com,phenotype=ph,chromosome=ch,GeneSymbol=gs)
                m.save()
            else:
                counter[EN]=counter[EN]+1
                m=models.MendelienGene.objects.create(ensemblID=EN+"_"+str(counter[EN]),gene_name=n,sequence=seq,type=com,phenotype=ph,chromosome=ch,GeneSymbol=gs)
        else:
            if len(models.MendelienGene.objects.filter(ensemblID=EN))==0:
                counter[EN]=0
                m=models.MendelienGene.objects.create(ensemblID=EN,gene_name=n,sequence=seq,type=com,phenotype=ph,chromosome=ch,GeneSymbol=gs,IsInheritanceKnown=False)
                m.save()
            else:
                counter[EN]=counter[EN]+1
                m=models.MendelienGene.objects.create(ensemblID=EN+"_"+str(counter[EN]),gene_name=n,sequence=seq,type=com,phenotype=ph,chromosome=ch,GeneSymbol=gs,IsInheritanceKnown=False)
