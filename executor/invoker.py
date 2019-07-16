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
import os
import sys
import subprocess
import ConfigParser
import xmltodict
import socket
import string
import traceback
import pprint
import time
from threading import Thread
from json import loads
from json import dumps
from StringIO import StringIO as _StringIO
from xml.etree.ElementTree import fromstring

'''
Import third party libs
'''
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.client import V1DeleteOptions
from kubernetes.client.models.v1_namespace_status import V1NamespaceStatus
from xmltodict import unparse
from xmljson import badgerfish as bf
from libvirt import libvirtError

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
from utils.libvirt_util import undefine_with_snapshot, destroy, undefine, create, setmem, setvcpus, is_vm_active, is_vm_exists, is_volume_exists, is_snapshot_exists
from utils import logger
from utils.uit_utils import is_block_dev_exists

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

cfg = "%s/default.cfg" % os.path.dirname(os.path.realpath(__file__))
config_raw = parser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
PLURAL_VM = config_raw.get('VirtualMachine', 'plural')
VERSION_VM = config_raw.get('VirtualMachine', 'version')
GROUP_VM = config_raw.get('VirtualMachine', 'group')
PLURAL_VMI = config_raw.get('VirtualMachineImage', 'plural')
VERSION_VMI = config_raw.get('VirtualMachineImage', 'version')
GROUP_VMI = config_raw.get('VirtualMachineImage', 'group')
PLURAL_VM_DISK = config_raw.get('VirtualMachineDisk', 'plural')
VERSION_VM_DISK = config_raw.get('VirtualMachineDisk', 'version')
GROUP_VM_DISK = config_raw.get('VirtualMachineDisk', 'group')
PLURAL_VM_SNAPSHOT = config_raw.get('VirtualMachineSnapshot', 'plural')
VERSION_VM_SNAPSHOT = config_raw.get('VirtualMachineSnapshot', 'version')
GROUP_VM_SNAPSHOT = config_raw.get('VirtualMachineSnapshot', 'group')
PLURAL_BLOCK_DEV_UIT = config_raw.get('VirtualMahcineBlockDevUit', 'plural')
VERSION_BLOCK_DEV_UIT = config_raw.get('VirtualMahcineBlockDevUit', 'version')
GROUP_BLOCK_DEV_UIT = config_raw.get('VirtualMahcineBlockDevUit', 'group')

LABEL = 'host=%s' % (socket.gethostname())

TIMEOUT = config_raw.get('WatcherTimeout', 'timeout')

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtctl.log')

'''
Handle support CMDs settings in default.cfg.
NOTE: if the key ends up with 'WithNameField' means that the CMD is using 'name' variable as index.
      The key ends up with 'WithDomainField' means that the CMD is using 'domain' variable as index.
      The key ends up with 'WithVolField' means that the CMD is using 'vol' variable as index.
'''
ALL_SUPPORT_CMDS = {}
ALL_SUPPORT_CMDS_WITH_NAME_FIELD = {}
ALL_SUPPORT_CMDS_WITH_DOMAIN_FIELD = {}
ALL_SUPPORT_CMDS_WITH_VOL_FIELD = {}
ALL_SUPPORT_CMDS_WITH_SNAPNAME_FIELD = {}

for k,v in config_raw._sections.items():
    if string.find(k, 'SupportCmds') != -1:
        ALL_SUPPORT_CMDS = dict(ALL_SUPPORT_CMDS, **v)
        if string.find(k, 'WithNameField') != -1:
            ALL_SUPPORT_CMDS_WITH_NAME_FIELD = dict(ALL_SUPPORT_CMDS_WITH_NAME_FIELD, **v)
        elif string.find(k, 'WithDomainField') != -1:
            ALL_SUPPORT_CMDS_WITH_DOMAIN_FIELD = dict(ALL_SUPPORT_CMDS_WITH_DOMAIN_FIELD, **v)
        elif string.find(k, 'WithVolField') != -1:
            ALL_SUPPORT_CMDS_WITH_VOL_FIELD = dict(ALL_SUPPORT_CMDS_WITH_VOL_FIELD, **v)
        elif string.find(k, 'WithSnapNameField') != -1:
            ALL_SUPPORT_CMDS_WITH_SNAPNAME_FIELD = dict(ALL_SUPPORT_CMDS_WITH_SNAPNAME_FIELD, **v)        

def main():
    logger.debug("---------------------------------------------------------------------------------")
    logger.debug("------------------------Welcome to Virtctl Daemon.-------------------------------")
    logger.debug("------Copyright (2019, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn, wuheng@otcaix.iscas.ac.cn----------")
    logger.debug("---------------------------------------------------------------------------------")
    
    logger.debug("Loading configurations in 'default.cfg' ...")
    logger.debug("All support CMDs are:")
    logger.debug(ALL_SUPPORT_CMDS)
    try:
        thread_1 = Thread(target=vMWatcher)
        thread_1.daemon = True
        thread_1.name = 'vm_watcher'
        thread_1.start()
        thread_2 = Thread(target=vMDiskWatcher)
        thread_2.daemon = True
        thread_2.name = 'vm_disk_watcher'
        thread_2.start()
        thread_3 = Thread(target=vMImageWatcher)
        thread_3.daemon = True
        thread_3.name = 'vm_image_watcher'
        thread_3.start()
        thread_4 = Thread(target=vMSnapshotWatcher)
        thread_4.daemon = True
        thread_4.name = 'vm_snapshot_watcher'
        thread_4.start()
        thread_5 = Thread(target=vMBlockDevWatcher)
        thread_5.daemon = True
        thread_5.name = 'vm_block_dev_watcher'
        thread_5.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return
        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()
        thread_5.join()
    except:
        logger.error('Oops! ', exc_info=1)
        
def test():
    try:
        vMBlockDevWatcher()
    except:
        traceback.print_exc()
        logger.error('Oops! ', exc_info=1)
    
def vMWatcher():
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=GROUP_VM, version=VERSION_VM, plural=PLURAL_VM, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        try:
            jsondict = forceUsingMetadataName(metadata_name, jsondict)
    #             print(jsondict)
            if operation_type == 'ADDED':
                if _isInstallVMFromISO(jsondict):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd:
                        runCmd(cmd)
                    if is_vm_exists(metadata_name) and not is_vm_active(metadata_name):
                        create(metadata_name)
                elif _isInstallVMFromImage(jsondict):
                    (jsondict, new_vm_vcpus, new_vm_memory) = _preprocessInCreateVMFromImage(jsondict)
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
                    '''
                    Set new VM's CPU and Memory
                    '''
                    setvcpus(metadata_name, int(new_vm_vcpus), config=True)
                    setmem(metadata_name, int(new_vm_memory), config=True)
                    '''
                    Start VM
                    '''
                    create(metadata_name)
                else:
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd:     
                        runCmd(cmd)
            elif operation_type == 'MODIFIED':
                if is_vm_exists(metadata_name):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
            elif operation_type == 'DELETED':
                if is_vm_exists(metadata_name):
                    if is_vm_active(metadata_name):
                        destroy(metadata_name)
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
#                 if is_vm_exists(metadata_name):
#                     if is_vm_active(metadata_name):
#                         destroy(metadata_name)
#                     undefine_with_snapshot(metadata_name)
        except:
            logger.error('Oops! ', exc_info=1)
            report_failure(name, jsondict, GROUP_VM, VERSION_VM, PLURAL_VM)
        
                
def vMDiskWatcher():
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=GROUP_VM_DISK, version=VERSION_VM_DISK, plural=PLURAL_VM_DISK, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        try:
            pool_name = _get_field(jsondict, 'pool')
            jsondict = forceUsingMetadataName(metadata_name, jsondict)
            if operation_type == 'ADDED':
                cmd = unpackCmdFromJson(jsondict)
                if cmd:
                    runCmd(cmd)
            elif operation_type == 'MODIFIED':
                if is_volume_exists(metadata_name, pool_name):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
            elif operation_type == 'DELETED':
                if is_volume_exists(metadata_name, pool_name):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)   
        except:
            logger.error('Oops! ', exc_info=1)
            report_failure(name, jsondict, GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
                
                
def vMImageWatcher():
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=GROUP_VMI, version=VERSION_VMI, plural=PLURAL_VMI, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        try:
            jsondict = forceUsingMetadataName(metadata_name, jsondict)
            if operation_type == 'ADDED':
                cmd = unpackCmdFromJson(jsondict)
                if cmd:
                    runCmd(cmd)
            elif operation_type == 'MODIFIED':
                if is_vm_exists(metadata_name):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
            elif operation_type == 'DELETED':
                if is_vm_exists(metadata_name):
                    if is_vm_active(metadata_name):
                        destroy(metadata_name)
                    undefine(metadata_name)
        except:
            logger.error('Oops! ', exc_info=1)
            report_failure(name, jsondict, GROUP_VMI, VERSION_VMI, PLURAL_VMI)
        
def vMSnapshotWatcher():
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=GROUP_VM_SNAPSHOT, version=VERSION_VM_SNAPSHOT, plural=PLURAL_VM_SNAPSHOT, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        try:
            vm_name = _get_field(jsondict, 'domain')
            jsondict = forceUsingMetadataName(metadata_name, jsondict)
            if operation_type == 'ADDED':
                cmd = unpackCmdFromJson(jsondict)
                if cmd:
                    runCmd(cmd)
            elif operation_type == 'MODIFIED':
                if is_snapshot_exists(metadata_name, vm_name):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
            elif operation_type == 'DELETED':
                if is_snapshot_exists(metadata_name, vm_name):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)  
        except:
            logger.error('Oops! ', exc_info=1)
            report_failure(name, jsondict, GROUP_VM_SNAPSHOT, VERSION_VM_SNAPSHOT, PLURAL_VM_SNAPSHOT)

def vMBlockDevWatcher():
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    logger.debug('UIT')
    logger.debug(GROUP_BLOCK_DEV_UIT, VERSION_BLOCK_DEV_UIT, PLURAL_BLOCK_DEV_UIT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=GROUP_BLOCK_DEV_UIT, version=VERSION_BLOCK_DEV_UIT, plural=PLURAL_BLOCK_DEV_UIT, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        try:
            jsondict = forceUsingMetadataName(metadata_name, jsondict)
            if operation_type == 'ADDED':
                cmd = unpackCmdFromJson(jsondict)
                if cmd:
                    runCmd(cmd)
            elif operation_type == 'MODIFIED':
                if is_block_dev_exists('/dev/%s/%s' % (metadata_name, metadata_name)):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)
            elif operation_type == 'DELETED':
                if is_block_dev_exists('/dev/%s/%s' % (metadata_name, metadata_name)):
                    cmd = unpackCmdFromJson(jsondict)
                    if cmd: 
                        runCmd(cmd)   
        except:
            logger.error('Oops! ', exc_info=1)
            report_failure(name, jsondict, GROUP_BLOCK_DEV_UIT, VERSION_BLOCK_DEV_UIT, PLURAL_BLOCK_DEV_UIT)

def report_failure(name, jsondict, group=None, version=None, plural=None):
    try:
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
        jsondict = deleteLifecycleInJson(jsondict)
        body = addExceptionMessage(jsondict)
        retv = client.CustomObjectsApi().replace_namespaced_custom_object(
            group=group, version=version, namespace='default', plural=plural, name=name, body=body)
        return retv
    except:
        logger.error('Oops! ', exc_info=1)

def deleteLifecycleInJson(jsondict):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['spec']
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
    return jsondict

def addExceptionMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'failed':{'message':message, 'reason':reason}}}}
        spec = jsondict['spec']
        if spec:
            spec['status'] = status
    return jsondict
         

def getMetadataName(jsondict):
    metadata = jsondict['raw_object']['metadata']
    metadata_name = metadata.get('name')
    if metadata_name:
        return metadata_name
    else:
        raise Exception('FATAL ERROR! No metadata name!') 

def forceUsingMetadataName(metadata_name,jsondict):
    spec = jsondict['raw_object']['spec']
    lifecycle = spec.get('lifecycle')
    if lifecycle:
        the_key = None
        keys = lifecycle.keys()
        for key in keys:
            if key in ALL_SUPPORT_CMDS.keys():
#                 cmd_head = ALL_SUPPORT_CMDS.get(key)
                the_key = key
                break;
#         print(cmd_head)
        if the_key in ALL_SUPPORT_CMDS_WITH_NAME_FIELD:
            lifecycle[the_key]['name'] = metadata_name    
        elif the_key in ALL_SUPPORT_CMDS_WITH_DOMAIN_FIELD:
            lifecycle[the_key]['domain'] = metadata_name
        elif the_key in ALL_SUPPORT_CMDS_WITH_VOL_FIELD:
            lifecycle[the_key]['vol'] = metadata_name
        elif the_key in ALL_SUPPORT_CMDS_WITH_SNAPNAME_FIELD:
            lifecycle[the_key]['snapshotname'] = metadata_name
    return jsondict


'''
Install VM from ISO.
'''
def _isInstallVMFromISO(jsondict):
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        cmd_head = ''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return False
        keys = lifecycle.keys()
        for key in keys:
            if key in ALL_SUPPORT_CMDS.keys():
                cmd_head = ALL_SUPPORT_CMDS.get(key)
                break;
        if cmd_head and cmd_head.startswith('virt-install'):
            return True
    return False

'''
Install VM from image.
'''
def _isInstallVMFromImage(jsondict):
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        cmd_head = ''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return False
        keys = lifecycle.keys()
        for key in keys:
            if key in ALL_SUPPORT_CMDS.keys():
                cmd_head = ALL_SUPPORT_CMDS.get(key)
                break;
        if cmd_head and cmd_head.startswith('virt-clone'):
            return True
    return False

def _preprocessInCreateVMFromImage(jsondict):
    new_vm_memory = None
    new_vm_vcpus = None
    '''
    Get target VM name from Json.
    '''
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        the_cmd_key = None
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return
        keys = lifecycle.keys()
        for key in keys:
            if key in ALL_SUPPORT_CMDS.keys():
                the_cmd_key = key
                break;
        '''
        Get the CMD body from 'dict' structure.
        '''
        if the_cmd_key:
            contents = lifecycle.get(the_cmd_key)
            for k, v in contents.items():
                if k == "memory":
                    new_vm_memory = v
                    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k]
                elif k == 'vcpus':
                    new_vm_vcpus = v
                    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k]
                else:
                    continue
        print jsondict
        return (jsondict, new_vm_vcpus, new_vm_memory)
    
def _get_field(jsondict, field):
    pool_name = None
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        the_cmd_key = ''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return None
        keys = lifecycle.keys()
        for key in keys:
            if key in ALL_SUPPORT_CMDS.keys():
                the_cmd_key = key
                break;
        if the_cmd_key:
            contents = lifecycle.get(the_cmd_key)
            for k, v in contents.items():
                if k == field:
                    pool_name = v
    return pool_name    
        
def jsontoxml(jsonstr):
    json = jsonstr.replace('_interface', 'interface').replace('_transient', 'transient').replace(
        'suspend_to_mem', 'suspend-to-mem').replace('suspend_to_disk', 'suspend-to-disk').replace(
            'on_crash', 'on-crash').replace('on_poweroff', 'on-poweroff').replace('on_reboot', 'on-reboot').replace(
            'nested_hv', "nested-hv").replace('_', '@').replace('text', '#text').replace('\'', '"')
    return unparse(loads(json))

def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace(
                    'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')

def updateDomainStructureInJson(jsondict, body):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['raw_object']['spec']
        if spec:
            print spec.keys()
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(loads(body))
    return jsondict['raw_object']

def updateDomainStructureInJsonBackup(jsondict, body):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        vm_ = jsondict['items'][0].get('metadata').get('name')
        if not vm_:
            raise Exception('No target VM in Json')
        spec = jsondict['items'][0].get('spec')
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(loads(body))
    return jsondict['items'][0]

'''
Covert chars according to real CMD in back-end.
'''
def _convertCharsInJson(key, value):
#     if val[0:1] == '_':
#         val = '_' + val
    key, value = str(key), str(value)
    if value == 'True':
        value = ''
    return ('--%s' % key.replace('_', '-'), value)

'''
Unpack the CMD that will be executed in Json format.
'''
def unpackCmdFromJson(jsondict):
    cmd = None
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['raw_object'].get('spec')
        if spec:
            '''
            Iterate keys in 'spec' structure and map them to real CMDs in back-end.
            Note that only the first CMD will be executed.
            '''
            cmd_head = ''
            the_cmd_key = None
            lifecycle = spec.get('lifecycle')
            if not lifecycle:
                return
            keys = lifecycle.keys()
            for key in keys:
                if key in ALL_SUPPORT_CMDS.keys():
                    the_cmd_key = key
                    cmd_head = ALL_SUPPORT_CMDS.get(key)
                    break;
            '''
            Get the CMD body from 'dict' structure.
            '''
            if the_cmd_key:
                cmd_body = ''
                contents = lifecycle.get(the_cmd_key)
                for k, v in contents.items():
                    (k, v) = _convertCharsInJson(k, v)
#                     print k, v
                    cmd_body = '%s %s %s' % (cmd_body, k, v)
                cmd = '%s %s' % (cmd_head, cmd_body)
            logger.debug("The CMD is: %s" % cmd)
    return cmd

'''
Run back-end command in subprocess.
'''
def runCmd(cmd):
    std_err = None
    if not cmd:
#         logger.debug('No CMD to execute.')
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            logger.debug(str.strip(std_out[0]))
        if std_err:
            logger.error(str.strip(std_err[0]))
            raise Exception(str.strip(std_err[0]))
#         return (str.strip(std_out[0]) if std_out else '', str.strip(std_err[0]) if std_err else '')
        return
    finally:
        p.stdout.close()
        p.stderr.close()

# def randomUUID():
#     u = [random.randint(0, 255) for ignore in range(0, 16)]
#     u[6] = (u[6] & 0x0F) | (4 << 4)
#     u[8] = (u[8] & 0x3F) | (2 << 6)
#     return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2,
#                      "%02x" * 6]) % tuple(u)
#
# def randomMAC():
#     mac = [ 0x52, 0x54, 0x00,
#         random.randint(0x00, 0x7f),
#         random.randint(0x00, 0xff),
#         random.randint(0x00, 0xff) ]
#     return ':'.join(map(lambda x: "%02x" % x, mac))

if __name__ == '__main__':
    config.load_kube_config(config_file=TOKEN)
    main()
#     test()
