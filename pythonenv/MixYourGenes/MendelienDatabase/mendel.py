from MendelienDatabase.models import MendelienGene

genes=MendelienGene.objects.all()
for i in genes:
    if i.phenotype=="":
        print(i.phenotype)
        i.delete()
