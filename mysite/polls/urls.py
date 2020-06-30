from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns =[
    path('',views.main,name='main'),
    path('fileUp',views.fileUpPage,name='fileUpload'),
    url(r'^upload/$', views.upload),
]