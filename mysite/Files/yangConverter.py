import os
import sys
import YangRegex


class Pharser():
    def __init__(self,data):
        self.data = data

    def jstree(self):
        return os.system('pyang -f jstree -o {}.html {}'.format(str(self.data),self.data))

    def finalFile(self,dic):
        File2 = YangRegex.regexClass(self.data)
        outfile = File2.final_config(dic)
        with open('./result/files.html','w') as f2:
            f2.write(outfile)
        return outfile





if __name__ == "__main__":
    data = ''
    for i in range(len(sys.argv)-1):
        data = data + ' ' + sys.argv[i+1]

    one = YangRegex.regexClass('test.yang')
    dic1 = one.leaf_dicOut()


    outfin = Pharser("out.html")
    kk = outfin.finalFile(dic1)
    with open('ts.html','w') as f2:
        f2.write(kk)





    # out = Pharser(data)
    # out.jstree()

