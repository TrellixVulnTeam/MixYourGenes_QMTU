from django.conf.urls import url
from GeneTest import views

# SET THE NAMESPACE!
app_name = 'GeneTest'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^trait/$',views.TraitTest,name='trait_test'),
    url(r'^process/$',views.gene_registration,name="gene_registration"),
]
