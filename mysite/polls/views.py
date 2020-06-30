from django.shortcuts import render
from django.http  import HttpResponse, Http404

import subprocess
import os

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

        file_list = subprocess.check_output(['find /home/ec2-user/django/EC2Django/mysite/Files/data -mindepth 1'] ,shell=True ,encoding='utf-8')
        file_list = file_list.split('\n')
    return render(request,"polls/uploadResult.html" ,{"data":file_list})

def pyang(requset):
    file_list2 = subprocess.check_output(['find /home/ec2-user/django/EC2Django/mysite/Files/data -mindepth 1'], shell=True,
                                   encoding='utf-8').split('\n')


    os.system('pyang -f jstree -o {}  {}'.format('/home/ec2-user/django/EC2Django/mysite/Files/result/out.html', ' '.join(file_list2)))

    return  render(requset,'polls/convert.html')