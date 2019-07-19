'''
Copyright (2019, ) Institute of Software, Chinese Academy of 

@author: wuheng@otcaix.iscas.ac.cn
@author: wuyuewen@otcaix.iscas.ac.cn
'''

from kubernetes import config, client
from kubernetes.client import V1DeleteOptions
from json import loads
import sys
import shutil
import os
import json


import logging
import logging.handlers

def set_logger(header,fn):
    logger = logging.getLogger(header)

    handler1 = logging.StreamHandler()
    handler2 = logging.handlers.RotatingFileHandler(filename=fn, maxBytes=10000000, backupCount=10)

    logger.setLevel(logging.DEBUG)
    handler1.setLevel(logging.DEBUG)
    handler2.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(name)s %(lineno)s %(levelname)s %(message)s")
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger

config.load_kube_config(config_file="/root/.kube/config")

GROUP='v1alpha3'
VERSION='cloudplus.io'
VM_PLURAL='virtualmachines'
VMI_PLURAL='virtualmachineimages'

logger = set_logger(os.path.basename(__file__), '/var/log/virtctl.log')

def toImage(name):
    jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachines', name=name)
    jsonDict = jsonStr.copy()
    jsonDict['kind'] = 'VirtualMachineImage'
    jsonDict['metadata']['kind'] = 'VirtualMachineImage'
    del jsonDict['metadata']['resourceVersion']
    del jsonDict['spec']['lifecycle']
    client.CustomObjectsApi().create_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachineimages', body=jsonDict)
    client.CustomObjectsApi().delete_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachines', name=name, body=V1DeleteOptions())
    logger.debug('convert VM to Image successful.')
    
def toVM(name):
    jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachineimages', name=name)
    jsonDict = jsonStr.copy()
    jsonDict['kind'] = 'VirtualMachine'
    jsonDict['metadata']['kind'] = 'VirtualMachine'
    del jsonDict['spec']['lifecycle']
    del jsonDict['metadata']['resourceVersion']
    client.CustomObjectsApi().create_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachines', body=jsonDict)
    client.CustomObjectsApi().delete_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachineimages', name=name, body=V1DeleteOptions())
    logger.debug('convert Image to VM successful.')


def updateOS(name, source, target):
    jsonDict = client.CustomObjectsApi().get_namespaced_custom_object(
        group='cloudplus.io', version='v1alpha3', namespace='default', plural='virtualmachines', name=name)
    jsonString = json.dumps(jsonDict)
    if jsonString.find(source) >= 0 and os.path.exits(target):
        shutil.copyfile(target, source)
    else:
        raise Exception('Wrong source or target.')
    

def cmd():
    help_msg = 'Usage: python %s <to-image|to-vm|update-os|--help>' % sys.argv[0]
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print (help_msg)
        sys.exit(1)
    
    if len(sys.argv)%2 != 0:
        print ("wrong parameter number")
        sys.exit(1) 
 
    params = {}
    for i in range (2, len(sys.argv) - 1):
        params[sys.argv[i]] = sys.argv[i+1]
        i = i+2
    
    if sys.argv[1] == 'to-image':
        toImage(params['--name'])
    elif sys.argv[1] == 'to-vm':
        toVM(params['--name'])
    elif sys.argv[1] == 'update-os':
        updateOS(params['--name'], params['--source'], params['--target'])
    else:
        print ('invalid argument!')
        print (help_msg)    

if __name__ == '__main__':
    cmd()
    pass
