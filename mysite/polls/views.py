from django.shortcuts import render
from django.http  import HttpResponse, Http404
import sys
sys.path.append('D:\pro\python\djan\EC2Django\mysite\polls')
import yangConverter
import YangRegex
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

        os.system('pyang -f jstree -o {}  {}'.format('/home/ec2-user/django/EC2Django/mysite/Files/result/out.html',
                                                     ' '.join(file_list)))


    return render(request,"polls/uploadResult.html" ,{"data":file_list})

def convert(requset):
    file_list2 = subprocess.check_output(['find /home/ec2-user/django/EC2Django/mysite/Files/data -mindepth 1'], shell=True,
                                   encoding='utf-8').split('\n')



    return  render(requset,'polls/convert.html')

def test(requset):
    # file_list2 = subprocess.check_output(['dir   D:\pro\python\djan\EC2Django\mysite\Files\data'],
    #                                      shell=True,encoding='utf-8')
    # file_list2 = subprocess.check_output(['dir '],
    #                                      shell=True, stderr=subprocess.STDOUT)

    A = YangRegex.regexClass('D:\pro\python\djan\EC2Django\mysite\Files\data2\\test.yang')
    dic = A.leaf_dicOut()
    B = yangConverter.Pharser('D:\pro\python\djan\EC2Django\mysite\Files\\result\out1.html')
    out = B.finalFile(dic)
    with open('test.html','w') as f3:
        f3.write(out)
    data = ' '
    return render(requset,'polls/test.html', {"data":out})