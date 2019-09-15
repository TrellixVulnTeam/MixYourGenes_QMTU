from django.contrib import admin
from MendelienDatabase import models
# Register your models here.
class MendelienGeneAdmin(admin.ModelAdmin):
    fields=["ensemblID","gene_name","phenotype","chromosome","GeneSymbol","reference"]
    search_fields=["ensemblID","gene_name","phenotype","chromosome","GeneSymbol","reference"]
    list_filter=["ensemblID","phenotype","chromosome","reference"]
    list_display=["ensemblID","gene_name","phenotype","chromosome","GeneSymbol","reference"]
    list_editable=["gene_name","phenotype","chromosome","GeneSymbol","reference"]
admin.site.register(models.MendelienGene)
