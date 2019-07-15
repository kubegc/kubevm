'''

 Copyright (2019, ) Institute of Software
        Chinese Academy of Sciences
         Author: wuheng@otcaix.iscas.ac.cn
           Date: 2019-06-18

'''
import json

dict = {}
subdict = {}

if __name__ == '__main__':
    
    file = open("commands") 
    for line in file:
        if line.startswith('virsh'):
            subdict = {}
            dict[line.split()[1].replace('-','_')] = subdict
        elif line.startswith('error'):
            if (line.find("<") != -1):
                s = line.find("<")
                e = line.find(">")
                subdict[line[s+1:e]]='string'
            elif (line.find("--") != -1):
                s = line.find("--")
                e = line.find("option")
                subdict["__" + line[s+2:e-1]]='string'
            
    file.close()
    
    print(json.dumps(dict))
    
