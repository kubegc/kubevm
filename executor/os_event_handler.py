'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

https://pypi.org/project/json2xml/
https://github.com/kubernetes/kubernetes/issues/51046
'''

'''
Import python libs
'''
import ConfigParser
import time
import traceback
import os
import sys
from json import loads
from json import dumps
from xml.etree.ElementTree import fromstring

'''
Import third party libs
'''
from watchdog.observers import Observer
from watchdog.events import *
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client import V1DeleteOptions
from xmljson import badgerfish as bf

'''
Import local libs
'''
from utils.libvirt_util import get_volume_xml, get_snapshot_xml
from utils import logger
from utils.utils import CDaemon, addExceptionMessage, addPowerStatusMessage
from utils.uit_utils import is_block_dev_exists, get_block_dev_json

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

cfg = "%s/default.cfg" % os.path.dirname(os.path.realpath(__file__))
config_raw = parser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
PLURAL_VM_DISK = config_raw.get('VirtualMachineDisk', 'plural')
VERSION_VM_DISK = config_raw.get('VirtualMachineDisk', 'version')
GROUP_VM_DISK = config_raw.get('VirtualMachineDisk', 'group')
PLURAL_VM_SNAPSHOT = config_raw.get('VirtualMachineSnapshot', 'plural')
VERSION_VM_SNAPSHOT = config_raw.get('VirtualMachineSnapshot', 'version')
GROUP_VM_SNAPSHOT = config_raw.get('VirtualMachineSnapshot', 'group')
PLURAL_BLOCK_DEV_UIT = config_raw.get('VirtualMahcineBlockDevUit', 'plural')
VERSION_BLOCK_DEV_UIT = config_raw.get('VirtualMahcineBlockDevUit', 'version')
GROUP_BLOCK_DEV_UIT = config_raw.get('VirtualMahcineBlockDevUit', 'group')

VOL_DIRS = config_raw.items('DefaultVolumeDirs')
SNAP_DIRS = config_raw.items('DefaultSnapshotDir')
BLOCK_DEV_DIRS = config_raw.items('DefaultBlockDevDir')

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=022, verbose=1):
        CDaemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name
 
    def run(self, output_fn, **kwargs):
        config.load_kube_config(config_file=TOKEN)
        try:
            main()
        except:
            traceback.print_exc()

def daemonize():
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print help_msg
        sys.exit(1)
    p_name = 'virtlet_os_event_handler'
    pid_fn = '/var/run/virtlet_os_event_handler_daemon.pid'
    log_fn = '/var/log/virtlet.log'
    err_fn = '/var/log/virtlet_error.log'
    cD1 = ClientDaemon(p_name, pid_fn, stderr=err_fn, verbose=1)
 
    if sys.argv[1] == 'start':
        cD1.start(log_fn)
    elif sys.argv[1] == 'stop':
        cD1.stop()
    elif sys.argv[1] == 'restart':
        cD1.restart(log_fn)
    elif sys.argv[1] == 'status':
        alive = cD1.is_running()
        if alive:
            print 'process [%s] is running ......' % cD1.get_pid()
        else:
            print 'daemon process [%s] stopped' %cD1.name
    else:
        print 'invalid argument!'
        print help_msg

def modifyStructure(name, body, group, version, plural):
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def deleteStructure(name, body, group, version, plural):
    retv = client.CustomObjectsApi().delete_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace(
                    'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')
                    
def updateJsonRemoveLifecycle(jsondict, body):
    if jsondict:
        spec = jsondict['spec']
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(loads(body))
    return jsondict

def myVmVolEventHandler(event, pool, name, group, version, plural):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                      version=version, 
                                                                      namespace='default', 
                                                                      plural=plural, 
                                                                      name=name)
    try:
    #     print(jsondict)
        if  event == "Delete":
            logger.debug('Callback volume deletion to virtlet')
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
        else:
            logger.debug('Callback volume changes to virtlet')
            vol_xml = get_volume_xml(pool, name)
            vol_json = toKubeJson(xmlToJson(vol_xml))
            vol_json = updateJsonRemoveLifecycle(jsondict, vol_json)
            body = addPowerStatusMessage(vol_json, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        report_failure(name, jsondict, 'VirtletError', str(info[1]))

class VmVolEventHandler(FileSystemEventHandler):
    def __init__(self, pool, target, group, version, plural):
        FileSystemEventHandler.__init__(self)
        self.pool = pool
        self.target = target
        self.group = group
        self.version = version
        self.plural = plural

    def on_moved(self, event):
        if event.is_directory:
            logger.debug("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
            _,vol = os.path.split(event.src_path)
            myVmVolEventHandler('Create', self.pool, vol, self.group, self.version, self.plural)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            _,vol = os.path.split(event.src_path)
            myVmVolEventHandler('Delete', self.pool, vol, self.group, self.version, self.plural)

    def on_modified(self, event):
        if event.is_directory:
            logger.debug("directory modified:{0}".format(event.src_path))
        else:
            logger.debug("file modified:{0}".format(event.src_path))
            
def myVmSnapshotEventHandler(event, vm, name, group, version, plural):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                      version=version, 
                                                                      namespace='default', 
                                                                      plural=plural, 
                                                                      name=name)
    try:
    #     print(jsondict)
        if  event == "Delete":
            logger.debug('Callback snapshot deletion to virtlet')
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
        else:
            logger.debug('Callback snapshot changes to virtlet')
            snap_xml = get_snapshot_xml(vm, name)
            snap_json = toKubeJson(xmlToJson(snap_xml))
            snap_json = updateJsonRemoveLifecycle(jsondict, snap_json)
            body = addPowerStatusMessage(snap_json, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        report_failure(name, jsondict, 'VirtletError', str(info[1]))

class VmSnapshotEventHandler(FileSystemEventHandler):
    def __init__(self, field, target, group, version, plural):
        FileSystemEventHandler.__init__(self)
        self.field = field
        self.target = target
        self.group = group
        self.version = version
        self.plural = plural

    def on_moved(self, event):
        if event.is_directory:
            logger.debug("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
            dirs,snap_file = os.path.split(event.src_path)
            _,vm = os.path.split(dirs)
            snap = os.path.splitext(os.path.splitext(snap_file)[0])[0]
            myVmSnapshotEventHandler('Create', vm, snap, self.group, self.version, self.plural)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            dirs,snap_file = os.path.split(event.src_path)
            _,vm = os.path.split(dirs)
            snap = os.path.splitext(os.path.splitext(snap_file)[0])[0]
            myVmSnapshotEventHandler('Delete', vm, snap, self.group, self.version, self.plural)

    def on_modified(self, event):
        if event.is_directory:
            logger.debug("directory modified:{0}".format(event.src_path))
        else:
            logger.debug("file modified:{0}".format(event.src_path))
            
def myVmBlockDevEventHandler(event, name, group, version, plural):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                      version=version, 
                                                                      namespace='default', 
                                                                      plural=plural, 
                                                                      name=name)
    try:
    #     print(jsondict)
        if  event == "Delete":
            logger.debug('Callback block dev deletion to virtlet')
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
        else:
            logger.debug('Callback block dev changes to virtlet')
            block_json = get_block_dev_json(name)
            block_json = updateJsonRemoveLifecycle(jsondict, block_json)
            body = addPowerStatusMessage(block_json, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        report_failure(name, jsondict, 'VirtletError', str(info[1]))

class VmBlockDevEventHandler(FileSystemEventHandler):
    def __init__(self, field, target, group, version, plural):
        FileSystemEventHandler.__init__(self)
        self.field = field
        self.target = target
        self.group = group
        self.version = version
        self.plural = plural

    def on_moved(self, event):
        if event.is_directory:
            logger.debug("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
            path,block = os.path.split(event.src_path)
            if is_block_dev_exists(event.src_path) and path != "/dev/mapper":
                myVmBlockDevEventHandler('Create', block, self.group, self.version, self.plural)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            _,block = os.path.split(event.src_path)
#             if is_block_dev_exists(event.src_path):
            myVmBlockDevEventHandler('Delete', block, self.group, self.version, self.plural)

    def on_modified(self, event):
        if event.is_directory:
#             logger.debug("directory modified:{0}".format(event.src_path))
            pass
        else:
#             logger.debug("file modified:{0}".format(event.src_path))
            pass
        
def report_failure(name, jsondict, error_reason, error_message, group, version, plural):
    try:
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
        body = addExceptionMessage(jsondict, error_reason, error_message)
        retv = client.CustomObjectsApi().replace_namespaced_custom_object(
            group=group, version=version, namespace='default', plural=plural, name=name, body=body)
        return retv
    except:
        logger.error('Oops! ', exc_info=1)
            
def main():
    observer = Observer()
    for ob in VOL_DIRS:
        if not os.path.exists(ob[1]):
            os.makedirs(ob[1])
        event_handler = VmVolEventHandler(ob[0], ob[1], GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
        observer.schedule(event_handler,ob[1],True)
    for ob in SNAP_DIRS:
        if not os.path.exists(ob[1]):
            os.makedirs(ob[1])
        event_handler = VmSnapshotEventHandler(ob[0], ob[1], GROUP_VM_SNAPSHOT, VERSION_VM_SNAPSHOT, PLURAL_VM_SNAPSHOT)
        observer.schedule(event_handler,ob[1],True)
    for ob in BLOCK_DEV_DIRS:
        if not os.path.exists(ob[1]):
            os.makedirs(ob[1])
        event_handler = VmBlockDevEventHandler(ob[0], ob[1], GROUP_BLOCK_DEV_UIT, VERSION_BLOCK_DEV_UIT, PLURAL_BLOCK_DEV_UIT)
        observer.schedule(event_handler,ob[1],True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()    

if __name__ == "__main__":
    daemonize()
