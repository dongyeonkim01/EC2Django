from django.shortcuts import render
from django.http  import HttpResponse, Http404

import sys
import os
import subprocess


def main(request):
    return render(request,"polls/main.html")

def fileUpPage(request):
    return render(request,"polls/fileup.html")

def upload(request):
    for count,x in enumerate(request.FILES.getlist('files')):
        def process(f):
            with open('/home/ec2-user/django/EC2Django/mysite/Files/data/{}'.format(str(x)), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)
        # data = str(os.system("python test.py"))
        # data = "D:\pro\python\djan\django1\mysite\Files"
        print('-------------------------')
        lili = subprocess.check_output(['find /home/ec2-user/django/EC2Django/mysite/Files/data -mindepth 1'] ,shell=True ,encoding='utf-8')
        # print(os.system('ls'))
        print(type(lili))
        print('----------------------')


        # lili = os.listdir(data)
    return render(request,"polls/uploadResult.html" ,{"data":lili})