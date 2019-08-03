from django.conf.urls import url
from account import views

# SET THE NAMESPACE!
app_name = 'account'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^$',views.index,name='index'),
]
