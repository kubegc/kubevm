'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

Created on Apr 28, 2019

@author: wuheng@otcaix.iscas.ac.cn

https://github.com/guillon/xmlplain
https://github.com/martinblech/xmltodict

tools:
http://www.bejson.com/
http://tool.oschina.net/codeformat/xml/
'''

from xmlplain import obj_from_yaml
from xmlplain import obj_to_yaml
from xmltodict import parse
from xmltodict import unparse
from json import loads
from xmljson import badgerfish as bf
from json import dumps
from xml.etree.ElementTree import fromstring
import os
from textwrap import indent


INPUT    = "./"
OUTPUT   = "docs/"

def xmlToYaml(xmlstr):
    return obj_to_yaml(parse(xmlstr))

def yamlToXml(yamlstr):
    yaml = yamlstr.replace('_interface', 'interface').replace(
        '_', '@').replace('text', '#text').replace('\'', '"')
    return unparse(obj_from_yaml(yaml))

def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def jsontoXml(jsonstr):
    json = jsonstr.replace('_interface', 'interface').replace(
        '_', '@').replace('text', '#text').replace('\'', '"')
    return unparse(loads(json))

def readXml(name):
    xmlstr = ""
    file = open(INPUT + name)
    for line in file:
        xmlstr = xmlstr + line
    file.close()
    return xmlstr

def xmlStyle(INPUT):
    for name in os.listdir(INPUT):
        print("## " + name)
        print("\n```")
        print(readXml(name))
        print("```\n")
        
def yamlStyle(INPUT):
    for name in os.listdir(INPUT):
        print("## " + name.replace("xml", "yaml"))
        print("\n```")
        print(xmlToYaml(readXml(name)).decode().replace(
            '@', '_').replace('interface', '_interface').replace('#text', 'text').replace('nested-hv', "nested_hv").replace(
                    'transient', '_transient').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk'))
        print("```\n")
        
def jsonStyle(INPUT):
    for name in os.listdir(INPUT):
        print("## " + name.replace("xml", "json"))
        print("\n```")
        print(xmlToJson(readXml(name)).replace('@', '_').replace(
            'interface', '_interface').replace('$', 'text').replace('nested-hv', "nested_hv").replace(
                    'transient', '_transient').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk'))
        print("```\n")

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace('-','_')
#                     'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')
  
if __name__ == '__main__':
    json = xmlToJson(readXml("conf\domain.xml"))
    print (toKubeJson(json))