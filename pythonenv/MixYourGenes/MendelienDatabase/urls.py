from django.conf.urls import url
from MendelienDatabase import views

# SET THE NAMESPACE!
app_name = 'Mendel'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    #url(r'^register/$',views.register,name='register'),
    #url(r'^upload/$',views.user_login,name='user_login'),
]
