'''

@author: yk
'''

from kubernetes import config, client
from json import loads
from utils import logger
import sys
import shutil
import os

# config.load_kube_config(config_file="/root/.kube/config")

GROUP= 'v1alpha3'
VERSION = 'cloudplus.io'
VM_PLURAL = 'virtualmachines'
VMI_PLURAL = 'virtualmachineimages'

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

def toImage(name):
    jsonString = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    jsonDict = loads(jsonString)
    jsonDict['Metadata']['Kind'] = 'VirtualMachineImage'
    client.CustomObjectsApi().create_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, body=jsonDict)
    client.CustomObjectsApi().delete_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    logger.debug('convert VM to Image successful.')
    
def toVM(name):
    jsonString = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, name=name)
    jsonDict = loads(jsonString)
    jsonDict['Metadata']['Kind'] = 'VirtualMachine'
    client.CustomObjectsApi().create_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, body=jsonDict)
    client.CustomObjectsApi().delete_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, name=name)
    logger.debug('convert Image to VM successful.')


def updateOS(name, source, target):
    jsonString = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    if source in jsonString:
        shutil.copyfile(target, source)
    

def cmd():
    help_msg = 'Usage: python %s <to-image|to-vm|update-os|--help>' % sys.argv[0]
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print (help_msg)
        sys.exit(1)
    
    if len(sys.argv)%2 != 0:
        print ("wrong parameter number")
        sys.exit(1) 
 
    params = {}
    for i in range (2, len(sys.argv)):
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