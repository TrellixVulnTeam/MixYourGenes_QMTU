import requests, sys
#from MendelienDatabase.models import MendelienGene
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
class MendelGene():
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
    server = "http://rest.ensembl.org"
    ext = "/sequence/id/"+geneID+"?type=genomic"
    r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
    if not r.ok:
        r.raise_for_status()
        sys.exit()
        print(r.text)
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
            mim2gene2[gene[5]]=MendelGene(ENSMBL=mim2gene[gene[5]],chromosome=gene[0],phenotype1=gene[12],name=gene[7],comments=gene[11],GeneSymbol=gene[6])
print(mim2gene2)
print('2')
with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/genemap.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split(';')
        if gene[6] in mim2gene2.keys():
            mim2gene2[gene[6]].phenotype2=gene[10]
print(mim2gene2)
print('3')
with open("/Users/Kovszasz/Documents/Munka/Projektek/MixYourGenes/pythonenv/MixYourGenes/static/additional/mimTitles.txt") as mimgene:
    for gene in mimgene:
        gene=deenterizator(gene).split('__:__')
        if gene[1] in mim2gene2.keys():
            mim2gene2[gene[1]].alternative_name=gene[2]
            mim2gene2[gene[1]].prefix=gene[0]
print(mim2gene2)
print('4')
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
print(mim2gene2)
print('5')
#saver(mim2gene2,'backup')
#mim2gene2=genome_annotation.loader('backup')
for i in mim2gene2.values():
    m=MendelienGene.objects.create(ensemblID=i.ENSMBL,gene_name=i.name,sequence=get_sequence(i.ENSMBL),type=i.comments,phenotype=i.phenotype3,chromosome=i.chromosome,GeneSymbol=i.GeneSymbol)
    m.save()
