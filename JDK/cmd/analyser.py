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
    
    file = open("paramResults") 
    for line in file:
        if line.startswith('[vir') :
            subdict = {}
            dict[line[1:len(line)-2]] = subdict
        elif line.find('--') == -1:
            continue
        else:
            line=line.replace('[','')
            line=line.replace(']','')
            value=line.split()[0]
            if (line.find("<") != -1):
                subdict[value[2:]]='string'
            else:
                subdict[value[2:]]=True
            
    file.close()
    
    print(json.dumps(dict))
    
