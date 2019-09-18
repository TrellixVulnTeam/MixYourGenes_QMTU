from django.db import models

class MendelienGene(models.Model):
    ensemblID=models.CharField(max_length=300, primary_key=True, default="",blank=True)
    gene_name=models.CharField(max_length=300, default="",null=True, blank=True)
    sequence=models.TextField(max_length=2000000,default="",null=True,blank=True)
    type=models.CharField(max_length=300, default="",null=True,blank=True)
    phenotype=models.CharField(max_length=300, default="",null=True,blank=True)
    chromosome=models.CharField(max_length=30, default="",null=True,blank=True)
    GeneSymbol=models.CharField(max_length=30, default="",null=True,blank=True)
    reference=models.CharField(max_length=30, default="OMMIM")
    IsInheritanceKnown=models.BooleanField(default=True)
    def __str__(self):
        return self.ensemblID
