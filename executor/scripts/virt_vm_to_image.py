'''
Import python libs
'''
import sys
import getopt
import os
import libvirt
import select
import errno
import time
import threading
import ConfigParser
import traceback
from json import loads
from json import dumps
from xml.etree.ElementTree import fromstring

'''
Import third party libs
'''
from kubernetes import client, config
from kubernetes.client.rest import ApiException 
from kubernetes.client import V1DeleteOptions
from xmljson import badgerfish as bf

import logging
import logging.handlers

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
from utils.libvirt_util import get_xml
from utils.utils import CDaemon
from utils import logger

class parser(ConfigParser.ConfigParser):  
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)
    def optionxform(self, optionstr):  
        return optionstr

LOG = '/var/log/virtctl.log'


def set_logger(header, fn):
    logger = logging.getLogger(header)

    handler1 = logging.StreamHandler()
    handler2 = logging.handlers.RotatingFileHandler(filename=fn, maxBytes=10000000, backupCount=10)

    logger.setLevel(logging.DEBUG)
    handler1.setLevel(logging.ERROR)
    handler2.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(name)s %(lineno)s %(levelname)s %(message)s")
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger

k8s_logger = set_logger(os.path.basename(__file__), LOG)
    
cfg = "%s/default.cfg" % os.path.dirname(os.path.realpath(__file__))
config_raw = parser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
PLURAL = config_raw.get('VirtualMachine', 'plural')
VERSION = config_raw.get('VirtualMachine', 'version')
GROUP = config_raw.get('VirtualMachine', 'group')

def modifyVM(name, body):
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=PLURAL, name=name, body=body)
    return retv

def deleteVM(name, body):
    k8s_logger.debug('deleteVMBackupdebug %s name')
    retv = client.CustomObjectsApi().delete_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=PLURAL, name=name, body=body)
    return retv

def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace(
                    'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')
                    
def updateXmlStructureInJson(jsondict, body):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['spec']
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(loads(body))
    return jsondict

def vmHandler(dom, operation):
    try:
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=GROUP, version=VERSION, namespace='default', plural=PLURAL, name=dom.name())
    #     print(jsondict)
        if operation == "Delete":
            logger.debug('Callback domain deletion to virtlet')
            deleteVM(dom.name(), V1DeleteOptions())
        else:
            logger.debug('Callback domain changes to virtlet')
            vm_xml = get_xml(dom.name())
            vm_json = toKubeJson(xmlToJson(vm_xml))
            body = updateXmlStructureInJson(jsondict, vm_json)
            modifyVM(dom.name(), body)
    except:
        logger.error('Oops! ', exc_info=1)