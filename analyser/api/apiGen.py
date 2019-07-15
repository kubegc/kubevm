'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuheng@otcaix.iscas.ac.cn

def show():
    print("##")
    print("\nDesc:")
    print("\nURL:")
    print("\nParameters:")
    print("| cmd | optional | description|")
    print("| ----- | ------ | ------ |")
    print("\nExample:")
    print("```")
    print("```")
    print("\nYaml:")
    print("```")
    print("```")

'''

import configparser
from networkx.generators import line
from audioop import getsample
import json

########################################
##
##     My Parser
##
########################################

class parser(configparser.ConfigParser):  
    def __init__(self,defaults=None):  
        configparser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

commands_cfg = parser()
commands_cfg.read("default.cfg")

descs_cfg = parser()
descs_cfg.read("descriptions")

optional_cfg = parser()
optional_cfg.read("optional")

paramtype_cfg = parser()
paramtype_cfg.read("paramtype")

paramdesc_cfg = parser()
paramdesc_cfg.read("paramdesc")

############################################
##
##     Generator
##
##############################################

cmds = {}
for line in open("virsh"):
    strs = line.split("[")[0].split() 
    cmds[strs[0]] = strs[0]

def genOptional():
    for line in open("virsh"):
        strs = line.split("[")[0].split() 
        print ("[" + strs[0] + "]")   
        for i in range(1, len(strs)):
            print (strs[i][1: len(strs[i]) - 1] + "=" + strs[i]) 



def genParamDesc():
    for line in open("raw_params"):
        value = line.strip().rstrip("\n")
        if value in cmds.keys():
            print("["+value+"]")  
        elif value.startswith('--'):
            name = value.split()[0][2:]
            type = ''
            if value.find("<string>") != -1:
                type = 'String'
            elif value.find("<number>") != -1:
                type = 'Integer'
            else:
                type = 'Boolean'
            print(name + "=" + type)
            
def genParamType():
    for line in open("raw_params"):
        value = line.strip().rstrip("\n")
        if value in cmds.keys():
            print("["+value+"]")  
        elif value.startswith('--'):
            name = value.split()[0][2:]
            idx = value.find(">")
            if idx == -1:
                idx = len(name) + 2
            print(name + "=" + value[idx + 1:].strip())  

####################################################
##
##         Templates
##
######################################################

def createJSONTemplate(vname, params):
    data = {}
    data['apiVersion']='cloudplus.io/v1alpha3'
    data['kind']='VirtualMachine'
    meta = {}
    meta['name']='VM'
    data['metadata']=meta
    spec={}
    spec['image']='CentOS7.iso'
    lifc={}
    inst=InstJSON(params)
    lifc[vname]=inst
    spec['lifecycle']=lifc
    data['spec']=spec
    print(json.dumps(data, sort_keys=True, indent=4))
    
def updateJSONTemplate(vname, params):
    data = {}
    data['apiVersion']='cloudplus.io/v1alpha3'
    data['kind']='VirtualMachine'
    meta = {}
    meta['name']='VM'
    data['metadata']=meta
    spec={}
    dom = {}
    name = {}
    name["text"]="CentOS"
    dom['name']=name
    spec['domain']=dom
    spec['image']='CentOS7.iso'
    spec['nodeName']='node22'
    lifc={}
    inst=InstJSON(params)
    lifc[vname]=inst
    spec['lifecycle']=lifc
    data['spec']=spec
    print(json.dumps(data, sort_keys=True, indent=4))

def InstJSON(params):
    pair = {}
    for key in params.keys():
        if params.get(key) == 'String':
            pair[key]='String'
        elif params.get(key) == 'Integer':
            pair[key]=1
        elif params.get(key) == 'Boolean':
            pair[key]=True
    return pair 
        
    
def createSampleTemplate(vname, params):
    print("ExtendedKubernetesClient client =") 
    print("\tExtendedKubernetesClient.defaultConfig(\"config\");")
    print("VirtualMachineImpl vmi = client.virtualMachines();)")
    print("VirtualMachine vm = new VirtualMachine();")
    print("ObjectMeta metadata = new ObjectMeta();")
    print("metadata.setName(\"VM\");")
    print("vm.setMetadata(metadata );")
    print("VirtualMachineSpec spec = new VirtualMachineSpec();")
    print("Lifecycle lifecycle = new Lifecycle();")
    mname = vname[0:1].upper() + vname[1:]
    line = "%s %s = new %s();" %(mname, vname, mname)
    print(line)
    print("{")
    for fname in params.keys():
        fmname = fname[0:1].upper() + fname[1:]
        fvalue = ''
        if params.get(fname) == 'String':
            fvalue = '("string")'
        elif params.get(fname) == 'Integer':
            fvalue = '(1)'
        elif params.get(fname) == 'Boolean':
            fvalue = '(true)'  
        else:
            continue    
        fline = "\t%s.set%s%s;" %(vname, fmname, fvalue)
        print(fline)
    print("}")
    sline = "lifecycle.set%s(%s)" %(mname, vname)
    print(sline)
    print("spec.setLifecycle(lifecycle );")    
    print("vm.setSpec(spec );")
    print("vmi.create(vm );")
    
def updateSampleTemplate(vname, params):
    print("ExtendedKubernetesClient client =") 
    print("\tExtendedKubernetesClient.defaultConfig(\"config\");")
    print("VirtualMachineImpl vmi = client.virtualMachines();")
    print("VirtualMachine vm = vmi.withName(\"VM\").get();")
    print("VirtualMachineSpec spec = vm.getSpec();")
    print("Lifecycle lifecycle = new Lifecycle();")
    mname = vname[0:1].upper() + vname[1:]
    line = "%s %s = new %s();" %(mname, vname, mname)
    print(line)
    print("{")
    for fname in params.keys():
        fmname = fname[0:1].upper() + fname[1:]
        fvalue = ''
        if params.get(fname) == 'String':
            fvalue = '("string")'
        elif params.get(fname) == 'Integer':
            fvalue = '(1)'
        elif params.get(fname) == 'Boolean':
            fvalue = '(true)'  
        else:
            continue    
        fline = "\t%s.set%s%s;" %(vname, fmname, fvalue)
        print(fline)
    print("}")
    sline = "lifecycle.set%s(%s)" %(mname, vname)
    print(sline)
    print("spec.setLifecycle(lifecycle );")    
    print("vmi.update(vm );")


##################################################
##
##          Core
##
###################################################


def getDesc(cmd):
    print ("\n**Desc**:" + descs_cfg._sections['desc'].get(cmd))

def getParams(cmd):
    print("\n**Parameters**:\n")
    print("| name |  type  | optional | description|")
    print("| ----- | ------ | ------ | ------ |")
    pt = paramtype_cfg._sections[cmd]
    pd = paramdesc_cfg._sections[cmd]
    po = optional_cfg._sections[cmd]
    for name in pt.keys():
        value = '| '
        value = value + name + " | "
        value = value + pt.get(name) + " | "
        optional = 'Yes'
        if po.get(name) is None:
            optional = 'No'
        value = value + optional + " | "
        value = value + pd.get(name) + " | "
        print(value)
 
 
def getJSON(key, cmd):
    print("\n**JSON**:\n")
    print("```")
    if cmd == "virt-install":
        createJSONTemplate(key, paramtype_cfg._sections[cmd])
    else:
        updateJSONTemplate(key, paramtype_cfg._sections[cmd])
    print("```")
 
def getSamples(key, cmd):
    print("\n**Sample**:\n")
    print("```")
    if cmd == "virt-install":
        createSampleTemplate(key, paramtype_cfg._sections[cmd])
    else:
        updateSampleTemplate(key, paramtype_cfg._sections[cmd])
    print("```")
    
def getYaml(cmd):
    print("\n**JSON:**:")
    print("```")
    print("```")

########################################
##
##  Main
##
##########################################
    
if __name__ == '__main__':

    cmds = commands_cfg._sections['SupportCmds']   
    for key in cmds.keys():
        print("\n\n## API: " + key)
        cmd = cmds.get(key)
        strs = cmd.split( )
        cmd = ''
        if (len(strs) == 1):
            cmd = strs[0]
        else:
            cmd = strs[1]
        getDesc(cmd)
        getParams(cmd)
        getSamples(key, cmd)
        getJSON(key, cmd)

    pass