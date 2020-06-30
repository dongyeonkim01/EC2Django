import re
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
                    dic[k] = v
                    tt = ''

        # for kkk in dic.keys():
        #     print('key : ',kkk,' /// val::',dic[kkk])
        return dic


    def final_config(self,dic):
        html_text,out_html = '',''
        with open(self.data, 'r') as f1:
            text = f1.readlines()
        html_text = '\n'.join(text)
        patten = re.compile('\S+', re.M)
        for i in text:

            if '<em>' in i:
                lli = patten.findall(i)
                bool =False
                ins = 0
                for ind,val in enumerate(lli):
                    if val=='<em>':
                        ins = ind
                lli[ins] = '<em  onclick=" ' + " jq(' " + str(dic[lli[ins+1]]).replace("\n",'').replace('"','') + " ' )" + ' " >'
                i = ''.join(lli)
            out_html += i
        return out_html


    def test(self,dic):
        out_html = ''
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
                edit = ' '.join(lli[:ind2+1]) +' <em onclick="jq()">' +lli[-2]  +'</em></abbr>'
                i = edit
                text2 = ''
            out_html += i

        return out_html

if __name__ == "__main__":
    datass = ''
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
