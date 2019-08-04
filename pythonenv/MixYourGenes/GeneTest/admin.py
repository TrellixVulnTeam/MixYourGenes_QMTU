from django.contrib import admin
from GeneTest import models
# register your models here.
admin.site.register(models.gene)
admin.site.register(models.trait)
admin.site.register(models.have)
admin.site.register(models.tests)
admin.site.register(models.figure)
admin.site.register(models.results)
admin.site.register(models.recombination)
