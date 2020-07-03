import re
import json
class regexClass():

    def __init__(self,data):
        self.data = data

    def openFile(self):
        with open(self.data, 'r') as f:
            text = f.readlines()
            text = ''.join(text)
        return text


    def container_reg(self,text):
        patten      = re.compile('\S+', re.M)
        key,val     ='',''
        bools  ,st  = False,False
        counts      = 0
        tmp_kes     = ''

        for i in text.split('\n'):
            if 'container' in i:
                bools = True
            if bools:
                li = patten.findall(i)
                val = val + ' \n ' + i
                for inner in li:
                    if st:
                        if inner == '{':
                            counts +=1
                        elif inner == '}':
                            counts -=0
                        if counts ==0:
                            bools = False
                    else:
                        if inner =='{':
                            key = tmp_kes
                            counts +=1
                            st = True
                        elif inner =='}':
                            return False
                    tmp_kes = inner
        return key, val


    def leaf_reg(self,text):
        patten      = re.compile('\S+', re.M)
        key,val     = '',''
        bools  ,st  = False,False
        counts      = 0
        tmp_kes     = ''

        for i in text.split('\n'):
            if 'leaf' in i:
                bools = True
            if bools:
                li = patten.findall(i)
                val = val + ' \n ' + i
                for inner in li:
                    if st:
                        if inner == '{':
                            counts +=1
                        elif inner == '}':
                            counts -=0
                        if counts ==0:
                            bools = False
                    else:
                        if inner =='{':
                            key = tmp_kes
                            counts +=1
                            st = True
                        elif inner =='}':
                            return False
                    tmp_kes = inner
        return key, val

    def container_dicOut(self):
        dic = {}
        tt = ''
        cc = 0
        bb = False
        data = self.openFile()
        for i in data.split('\n'):
            if 'container' in i :
                bb = True

            if bb:
                tt = tt + '\n' + i
                if '{' in i:
                    cc += 1
                if '}' in i:
                    cc -= 1
                if cc ==0:
                    bb = False
                    k,v = self.container_reg(tt)
                    dic[k] = v
                    tt = ''

        for kkk in dic.keys():
            print('key : ',kkk,' /// val::',dic[kkk])
        return dic

    def leaf_dicOut(self):
        dic = {}
        tt = ''
        cc = 0
        bb = False
        data = self.openFile()
        for i in data.split('\n'):
            if 'leaf' in i :
                bb = True

            if bb:
                tt = tt + '\n' + i
                if '{' in i:
                    cc += 1
                if '}' in i:
                    cc -= 1
                if cc ==0:
                    bb = False
                    k,v = self.leaf_reg(tt)
                    k = k + '-1'
                    if k in dic.keys():
                        while True:
                            tmp = k.split('-')
                            tmp[-1] = str(int(tmp[-1]) + 1)
                            k = '-'.join(tmp)
                            if k not in dic.keys():
                                break

                        dic['-'.join(tmp)] = v
                    else:
                        dic[k] = v
                    tt = ''

        # for kkk in dic.keys():
        #     print('key : ',kkk,' /// val::',dic[kkk])
        return dic


    def final_config(self,dic):
        key_list = []
        out_html = ''
        json_data = json.dumps(dic)
        with open(self.data, 'r') as f1:
            html = f1.readlines()
        patten = re.compile('\S+', re.M)
        bool = False
        text2 = ''
        for i in html:
            if 'class="leaf"' in i or 'class="leaf-list' in i:
                bool = True
            if bool:
                text2 = text2 + ' ' + i

            if '</abbr>' in i and bool:
                text2 = text2.split('\n')[1:]
                text2 = '\n'.join(text2)
                bool = False
                lli = patten.findall(text2.replace('\n', ' '))
                ind2 = 0
                for ind, val in enumerate(lli):
                    if '">' in val:
                        ind2 = ind

                keys = lli[-2] + '-1'
                if keys in key_list:
                    while True:
                        tmp = keys.split('-')
                        tmp[-1] = str(int(tmp[-1]) + 1)
                        keys = '-'.join(tmp)
                        if keys not in key_list:
                            break
                    edit = ' '.join(
                        lli[:ind2 + 1]) + '<em id="' + keys + '"' + 'onclick="' + "jq('" + keys + "'" + ')">' + lli[
                               -2] + '</em></abbr>'
                    key_list.append(keys)
                else:
                    edit = ' '.join(
                        lli[:ind2 + 1]) + '<em id="' + keys + '"' + 'onclick="' + "jq('" + keys + "'" + ')">' + lli[
                               -2] + '</em></abbr>'
                    key_list.append(keys)
                i = edit
                text2 = ''

            if '<body' in i:
                i = i + ' \n <div class="div-right" style="width: 0%; float: right; "></div>' \
                        ' <div class="div-left" style="width: 100%; height:100%; float: left; overflow: scroll;">'

            if '</body>' in i:
                i = '''
                            </div>
                            </body>
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                            <script>
                                function jq(text){
                                    console.log(text);
                                  $(document).ready(function(){
                                        $('.div-right').css('width','35%');
                                        $('.div-left').css('width','65%');
                                        $('.div-right *').remove();
                                        $('.div-right').append('<div style="height:105px;"></div><div style="white-space: pre;">'+dicval[text]+'</div >');
                                  });
                                }
                            </script>    
                            <script>                    
                        ''' + 'var dicval = ' + json_data + '; </script>'
            out_html += i

        return out_html


    def test(self,dic):
        out_html = ''
        json_data = json.dumps(dic)
        with open(self.data,'r') as f1:
            html = f1.readlines()

        patten = re.compile('\S+' ,re.M)

        bool = False
        text2 = ''
        for i in html:
            if 'class="leaf"' in i or 'class="leaf-list' in i:
                bool = True
            if bool:
                text2 = text2+' ' +i

            if '</abbr>' in i and bool:
                text2 = text2.split('\n')[1:]
                text2 = '\n'.join(text2)
                bool = False

                lli = patten.findall(text2.replace('\n' ,' ') )
                ind2 = 0
                for ind,val in enumerate(lli):
                    if '">' in val:
                        ind2 = ind
                edit = ' '.join(lli[:ind2+1]) +'<em onclick="'+"jq('"+ lli[-2]+"'"+')">' +lli[-2]  +'</em></abbr>'
                i = edit
                text2 = ''

            if '<body' in i:
                i = i + ' \n <div class="div-right" style="width: 0%; float: right; "></div>' \
                        ' <div class="div-left" style="width: 100%; float: left; overflow: scroll;">'

            if '</body>' in i:
                i = '''
                    </div>
                    
                    </body>
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                    <script>
                        function jq(text){
                            console.log(text);
                          $(document).ready(function(){
                                $('.div-right').css('width','25%');
                                $('.div-left').css('width','75%');
                                $('.div-right *').remove();
                                $('.div-right').append('<div style="height:105px;"></div><div style="white-space: pre;">'+dicval[text]+'</div >');
                          });
                        }
                    </script>    
                    <script>                    
                ''' + 'var dicval = '+json_data + '; </script>'


            out_html += i

        return out_html

if __name__ == "__main__":
    datass = ''
    A = regexClass('D:\pro\python\djan\EC2Django\mysite\Files\data2\\test.yang')
    dic = A.leaf_dicOut()
    B = regexClass('D:\pro\python\djan\EC2Django\mysite\Files\\result\out1.html')
    out = B.test(dic)

    # with open('testx.html' , 'w') as f:
    #     f.write(out)


    # B = yangConverter.Pharser('D:\pro\python\djan\EC2Django\mysite\Files\\result\out1.html')


    # A = regexClass('test.yang')
    # tex = str(A.leaf_dicOut())
    # dic = A.leaf_dicOut()
    # # print(type(dic))
    # Test = regexClass('out.html')
    # # print(Test.test(dic))
    # tt = Test.test(dic)
    # with open('t1.html', 'w') as f1:
    #     f1.write(tt)


    # with open('test.txt','w') as f1:
    #     f1.write(tex)
