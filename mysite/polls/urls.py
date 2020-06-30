from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns =[
    path('',views.main,name='main'),
    path('fileUp',views.fileUpPage,name='fileUpload'),
    path('pyang',views.pyang,name='pyang'),
    url(r'^upload/$', views.upload),
]