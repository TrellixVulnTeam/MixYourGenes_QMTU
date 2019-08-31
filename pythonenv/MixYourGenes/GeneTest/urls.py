from django.conf.urls import url
from GeneTest import views

# SET THE NAMESPACE!
app_name = 'GeneTest'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^result/$',views.TraitDeseaseTest,name='trait_desease_test'),
    url(r'^self_result/$',views.SelfTest,name='selftest'),
    url(r'^results/(?P<test_id>[\w-]+)/$',views.result,name='result'),
    url(r'^delete/(?P<test_id>[\w-]+)/$',views.delete,name='delete'),
    url(r'^process/$',views.gene_registration,name="gene_registration"),
    url(r'^family/$',views.DrawPedigree,name="pedigree"),
]
