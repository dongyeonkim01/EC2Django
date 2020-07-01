from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns =[
    path('test',views.test,name='test'),

    path('',views.main,name='main'),
    path('fileUp',views.fileUpPage,name='fileUpload'),
    path('convert',views.convert,name='convert'),
    url(r'^upload/$', views.upload),
]