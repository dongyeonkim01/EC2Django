from django.shortcuts import render
from django.http  import HttpResponse, Http404
import  time
import sys
sys.path.append('/home/ec2-user/django/EC2Django/mysite/polls')
import subprocess
import yangConverter
import YangRegex
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

    total_Yang = ''
    for file in file_list:
        kk = ''
        try:
            with open(file.replace(' ','') ,'r') as ff:
                kk += ff.readlines()
            total_Yang += kk
        except:
            pass
    with open('tmp.yang','w') as ft:
        ft.write(total_Yang)

    time.sleep(3)

    os.system('pyang -f jstree -o {}  {}'.format('/home/ec2-user/django/EC2Django/mysite/Files/result/out.html'
                                           , ' '.join(file_list)))

    A = YangRegex.regexClass('tmp.yang')
    dic = A.leaf_dicOut()
    B = yangConverter.Pharser('/home/ec2-user/django/EC2Django/mysite/Files/result/out.html')
    out = B.finalFile(dic)

    print(len(out),'tpye : ',type(out))
    with open('/home/ec2-user/django/EC2Django/mysite/Files/result/{}.html'.format('ttt1'), 'w') as fi:
        fi.write(out)
    print('-----------------------------')

    return render(request,"polls/uploadResult.html" ,{"data":file_list})

def convert(requset):
    file_list2 = subprocess.check_output(['find /home/ec2-user/django/EC2Django/mysite/Files/data -mindepth 1'], shell=True,
                                   encoding='utf-8').split('\n')
    os.system('rm /home/ec2-user/django/EC2Django/mysite/Files/result/out.html')
    os.system('rm /home/ec2-user/django/EC2Django/mysite/Files/tmp.yang')
    for i in file_list2:
        try:
            os.system('rm {}'.format(i.replace(' ','')))
        except:
            print('error file rm error')

    os.system('mv /home/ec2-user/django/EC2Django/mysite/Files/result/ttt1.html   /home/ec2-user/data')
    return  render(requset,'polls/convert.html')


def test(request):
    file_list = subprocess.check_output(['find /home/ec2-user/django/EC2Django/mysite/Files/data -mindepth 1'],
                                        shell=True, encoding='utf-8')
    file_list = file_list.split('\n')

    print(file_list)
    print('--------------------------------')
    total_Yang = ''
    # with open('/home/ec2-user/django/EC2Django/mysite/Files/data/ietf-hardware.yang' ,'r') as fa:
    #     data =fa.readlines()
    # print(data)
    print('--------------------------------------')
    for file in file_list:
        # print(file)
        try:
            with open(file.replace(' ',''), 'r') as ff:
                kk = ff.readlines()
            total_Yang += '\n'.join(kk)
        except:
            pass
            print('error')

    with open('tmp.yang', 'w') as ft:
        ft.write(total_Yang)

    A = YangRegex.regexClass('tmp.yang')
    dic = A.leaf_dicOut()
    B = yangConverter.Pharser('/home/ec2-user/django/EC2Django/mysite/Files/result/out.html')
    out = B.finalFile(dic)

    with open('{}.html'.format('ttest'), 'w') as fi:
        fi.write(out)

    return  HttpResponse("teststst")