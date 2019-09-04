'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
import copy

'''
Import python libs
'''
import ConfigParser
import time
import traceback
import os
import sys
import socket
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
from utils.libvirt_util import refresh_pool, get_volume_xml, get_snapshot_xml, is_vm_exists, get_xml, vm_state, _get_all_pool_path, get_all_vnc_info
from utils import logger
from utils.utils import runCmdRaiseException, CDaemon, addExceptionMessage, addPowerStatusMessage, updateDomainSnapshot, updateDomain, report_failure, get_hostname_in_lower_case
from utils.uit_utils import is_block_dev_exists, get_block_dev_json

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

cfg = "/etc/kubevmm/config"
if not os.path.exists(cfg):
    cfg = "/home/kubevmm/bin/config"
config_raw = parser()
config_raw.read(cfg)

VM_KIND = 'VirtualMachine'
VMI_KIND = 'VirtualMachineImage'
VMD_KIND = 'VirtualMachineDisk'
VMDI_KIND = 'VirtualMachineDiskImage'
VMSN_KIND = 'VirtualMachineSnapshot'
VMDEV_KIND = 'VirtualMahcineBlockDevUit'

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

PLURAL_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'plural')
VERSION_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'version')
GROUP_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'group')

VOL_DIRS = config_raw.items('DefaultVolumeDirs')
SYSTEM_VOL_DIRS = config_raw.items('DefaultStorageDir')
SNAP_DIRS = config_raw.items('DefaultSnapshotDir')
BLOCK_DEV_DIRS = config_raw.items('DefaultBlockDevDir')
LIBVIRT_XML_DIRS = config_raw.items('DefaultLibvirtXmlDir')
TEMPLATE_DIRS = config_raw.items('DefaultTemplateDir')
VMD_TEMPLATE_DIRS = config_raw.items('DefaultVirtualMachineDiskTemplateDir')

HOSTNAME = get_hostname_in_lower_case()

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

def createStructure(body, group, version, plural):
    retv = client.CustomObjectsApi().create_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, body=body)
    return retv

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
            spec.update(body)
    return jsondict

def myVmVolEventHandler(event, pool, name, group, version, plural):
    #     print(jsondict)
    if event == "Delete":
        try:
            refresh_pool(pool)
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
#             vol_xml = get_volume_xml(pool, name)
#             vol_json = toKubeJson(xmlToJson(vol_xml))
            jsondict = updateJsonRemoveLifecycle(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM disk %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm disk %s, report to virtlet' % name)

            deleteStructure(name, V1DeleteOptions(), group, version, plural)
        except:
            logger.error('Oops! ', exc_info=1)
    elif event == "Create":
        try:
            logger.debug('Create vm disk %s, report to virtlet' % name)
            jsondict = {'spec': {'volume': {}, 'nodeName': HOSTNAME, 'status': {}}, 
                        'kind': VMD_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name}, 'apiVersion': '%s/%s' % (group, version)}
            vol_xml = get_volume_xml(pool, name)
            vol_json = toKubeJson(xmlToJson(vol_xml))
            jsondict = updateJsonRemoveLifecycle(jsondict, loads(vol_json))
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            try:
                createStructure(body, group, version, plural)
            except ApiException, e:
                if e.reason == 'Conflict':
                    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
                    jsondict = updateJsonRemoveLifecycle(jsondict, loads(vol_json))
                    body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                    modifyStructure(name, body, group, version, plural)
                else:
                    logger.error(e)
                    
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                               version=version, 
                                                                               namespace='default', 
                                                                               plural=plural, 
                                                                               name=name) 
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    else:
        refresh_pool(pool)
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
        try:
            pass
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

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
            try:
                myVmVolEventHandler('Create', self.pool, vol, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            _,vol = os.path.split(event.src_path)
            try:
                myVmVolEventHandler('Delete', self.pool, vol, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
            logger.debug("directory modified:{0}".format(event.src_path))
        else:
#            logger.debug("file modified:{0}".format(event.src_path))
            pass
            
def myVmSnapshotEventHandler(event, vm, name, group, version, plural):
    #     print(jsondict)
    if  event == "Delete":
        try:
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
#             snap_xml = get_snapshot_xml(vm, name)
#             snap_json = toKubeJson(xmlToJson(snap_xml))
#             snap_json = updateDomainSnapshot(loads(snap_json))
            jsondict = updateJsonRemoveLifecycle(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM snapshot %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm snapshot %s, report to virtlet' % name)
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
        except:
            logger.error('Oops! ', exc_info=1)
    elif event == "Create":
        try:
            logger.debug('Create vm snapshot %s, report to virtlet' % name)
            jsondict = {'spec': {'domainsnapshot': {}, 'nodeName': HOSTNAME, 'status': {}}, 
                        'kind': VMSN_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name}, 'apiVersion': '%s/%s' % (group, version)}
            snap_xml = get_snapshot_xml(vm, name)
            snap_json = toKubeJson(xmlToJson(snap_xml))
            snap_json = updateDomainSnapshot(loads(snap_json))
            jsondict = updateJsonRemoveLifecycle(jsondict, snap_json)
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            try:
                createStructure(body, group, version, plural)
            except ApiException, e:
                if e.reason == 'Conflict':
                    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
                    jsondict = updateJsonRemoveLifecycle(jsondict, snap_json)
                    body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                    modifyStructure(name, body, group, version, plural)
                else:
                    logger.error(e)
                    
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                               version=version, 
                                                                               namespace='default', 
                                                                               plural=plural, 
                                                                               name=name) 
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    else:
        try:
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

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
            try:
                myVmSnapshotEventHandler('Create', vm, snap, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            dirs,snap_file = os.path.split(event.src_path)
            _,vm = os.path.split(dirs)
            snap = os.path.splitext(os.path.splitext(snap_file)[0])[0]
            try:
                myVmSnapshotEventHandler('Delete', vm, snap, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
            logger.debug("directory modified:{0}".format(event.src_path))
        else:
            logger.debug("file modified:{0}".format(event.src_path))
            
def myVmBlockDevEventHandler(event, name, group, version, plural):
    #     print(jsondict)
    if  event == "Delete":
        try:
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
#             block_json = get_block_dev_json(name)
            jsondict = updateJsonRemoveLifecycle(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM block device %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm block %s, report to virtlet' % name)
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
        except:
            logger.error('Oops! ', exc_info=1)
    elif event == "Create":
        try:
            logger.debug('Create vm block %s, report to virtlet' % name)
            jsondict = {'spec': {'REPLACE': {}, 'nodeName': HOSTNAME, 'status': {}}, 
                        'kind': VMDEV_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name}, 'apiVersion': '%s/%s' % (group, version)}
            block_json = get_block_dev_json(name)
            jsondict = updateJsonRemoveLifecycle(jsondict, loads(block_json))
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            try:
                createStructure(body, group, version, plural)
            except ApiException, e:
                if e.reason == 'Conflict':
                    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)     
                    jsondict = updateJsonRemoveLifecycle(jsondict, loads(block_json))
                    body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')               
                    modifyStructure(name, body, group, version, plural)
                else:
                    logger.error(e)
                    
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                               version=version, 
                                                                               namespace='default', 
                                                                               plural=plural, 
                                                                               name=name) 
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    else:
        try:
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

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
                try:
                    myVmBlockDevEventHandler('Create', block, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            path, block = os.path.split(event.src_path)
#             if is_block_dev_exists(event.src_path):
            if path == '/dev/pts':
                logger.debug('Ignore devices %s' % event.src_path)
            else:
                try:
                    myVmBlockDevEventHandler('Delete', block, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
#             logger.debug("directory modified:{0}".format(event.src_path))
            pass
        else:
#             logger.debug("file modified:{0}".format(event.src_path))
            pass
        
def myVmLibvirtXmlEventHandler(event, name, xml_path, group, version, plural):
    #     print(jsondict)
    if  event == "Create":
        try:
            logger.debug('***Create VM %s from back-end, report to virtlet***' % name)
            jsondict = {'spec': {'domain': {}, 'nodeName': HOSTNAME, 'status': {}}, 
                        'kind': VM_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name}, 'apiVersion': '%s/%s' % (group, version)}
            vm_xml = get_xml(name)
            vm_power_state = vm_state(name).get(name)
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            jsondict = addPowerStatusMessage(jsondict, vm_power_state, 'The VM is %s' % vm_power_state)
            body = addNodeName(jsondict)
            try:
                createStructure(body, group, version, plural)
            except ApiException, e:
                if e.reason == 'Conflict':
                    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
                    vm_xml = get_xml(name)
                    vm_power_state = vm_state(name).get(name)
                    vm_json = toKubeJson(xmlToJson(vm_xml))
                    vm_json = updateDomain(loads(vm_json))
                    jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
                    jsondict = addPowerStatusMessage(jsondict, vm_power_state, 'The VM is %s' % vm_power_state)
                    body = addNodeName(jsondict)
                    modifyStructure(name, body, group, version, plural)  
                else:
                    logger.error(e)
                    
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                               version=version, 
                                                                               namespace='default', 
                                                                               plural=plural, 
                                                                               name=name) 
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1) 
    elif event == "Modify":
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
        try:
            logger.debug('***Modify VM %s from back-end, report to virtlet***' % name)
            vm_xml = get_xml(name)
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            body = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            modifyStructure(name, body, group, version, plural)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
    elif event == "Delete":
#             jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
#                                                                               version=version, 
#                                                                               namespace='default', 
#                                                                               plural=plural, 
#                                                                               name=name)
        logger.debug('***Delete VM %s , report to virtlet***' % name)
        try:
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
#             vm_xml = get_xml(name)
#             vm_json = toKubeJson(xmlToJson(vm_xml))
#             vm_json = updateDomain(loads(vm_json))
            body = updateDomainStructureAndDeleteLifecycleInJson(jsondict, {})
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
#                 vm_xml = get_xml(name)
#                 vm_json = toKubeJson(xmlToJson(vm_xml))
#                 vm_json = updateDomain(loads(vm_json))
#                 jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
#                 body = addExceptionMessage(jsondict, 'VirtletError', 'VM has been deleted in back-end.')
#                 modifyStructure(name, body, group, version, plural)   
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

class VmLibvirtXmlEventHandler(FileSystemEventHandler):
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
            _,name = os.path.split(event.dest_path)
            file_type = os.path.splitext(name)[1]
            vm = os.path.splitext(os.path.splitext(name)[0])[0]
            if file_type == '.xml' and is_vm_exists(vm):
                try:
                    myVmLibvirtXmlEventHandler('Create', vm, event.dest_path, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
#             _,name = os.path.split(event.src_path)
#             file_type = os.path.splitext(name)[1]
#             vm = os.path.splitext(os.path.splitext(name)[0])[0]
#             if file_type == '.xml' and is_vm_exists(vm):
#                 try:
#                     myVmLibvirtXmlEventHandler('Create', vm, event.src_path, self.group, self.version, self.plural)
#                 except ApiException:
#                     logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            _,name = os.path.split(event.src_path)
            file_type = os.path.splitext(name)[1]
            vm = os.path.splitext(os.path.splitext(name)[0])[0]
            if file_type == '.xml' and not is_vm_exists(vm):
                try:
                    myVmLibvirtXmlEventHandler('Delete', vm, event.src_path, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
#             logger.debug("directory modified:{0}".format(event.src_path))
            pass
        else:
            logger.debug("file modified:{0}".format(event.src_path))
            _,name = os.path.split(event.src_path)
            file_type = os.path.splitext(name)[1]
            vm = os.path.splitext(os.path.splitext(name)[0])[0]
            if file_type == '.xml' and is_vm_exists(vm):
                try:
                    myVmLibvirtXmlEventHandler('Modify', vm, event.src_path, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

def myVmdImageLibvirtXmlEventHandler(event, name, pool, xml_path, group, version, plural):
    #     print(jsondict)
    if event == "Create":
        try:
            '''
            Refresh pool manually
            '''
            refresh_pool(pool)
            logger.debug('Create vm disk image %s, report to virtlet' % name)
            jsondict = {'spec': {'volume': {}, 'nodeName': HOSTNAME, 'status': {}}, 
                        'kind': VMDI_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name}, 'apiVersion': '%s/%s' % (group, version)}
            vmd_xml = get_volume_xml(pool, name)
            vmd_json = toKubeJson(xmlToJson(vmd_xml))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, loads(vmd_json))
            jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            body = addNodeName(jsondict)
            try:
                createStructure(body, group, version, plural)
            except ApiException, e:
                if e.reason == 'Conflict':
                    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
                    jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, loads(vmd_json))
                    jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                    body = addNodeName(jsondict)
                    modifyStructure(name, body, group, version, plural)  
                else:
                    logger.error(e)
                    
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                               version=version, 
                                                                               namespace='default', 
                                                                               plural=plural, 
                                                                               name=name) 
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)         
    elif event == "Delete":
        try:
            '''
            Refresh pool manually
            '''
            refresh_pool(pool)
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
#             with open(xml_path, 'r') as fr:
#                 vm_xml = fr.read()
#             vmd_json = toKubeJson(xmlToJson(vm_xml))
#             vmd_json = updateDomain(loads(vmd_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM disk image %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm disk image %s, report to virtlet' % name)
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
#                 jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vmd_json)
#                 body = addExceptionMessage(jsondict, 'VirtletError', 'VM has been deleted in back-end.')
#                 modifyStructure(name, body, group, version, plural)   
        except:
            logger.error('Oops! ', exc_info=1)

class VmdImageLibvirtXmlEventHandler(FileSystemEventHandler):
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
            vmdi = os.path.split(os.path.splitext(event.dest_path)[0])[1]
            try:
                myVmdImageLibvirtXmlEventHandler('Create', vmdi, self.pool, event.dest_path, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
            vmdi = os.path.split(os.path.splitext(event.src_path)[0])[1]
            try:
                myVmdImageLibvirtXmlEventHandler('Create', vmdi, self.pool, event.src_path, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            vmdi = os.path.split(os.path.splitext(event.src_path)[0])[1]
            try:
                myVmdImageLibvirtXmlEventHandler('Delete', vmdi, self.pool, event.src_path, self.group, self.version, self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
#             logger.debug("directory modified:{0}".format(event.src_path))
            pass
        else:
            logger.debug("file modified:{0}".format(event.src_path))
#             _,name = os.path.split(event.src_path)
#             file_type = os.path.splitext(name)[1]
#             vmi = os.path.splitext(os.path.splitext(name)[0])[0]
#             if file_type == '.xml':
#                 try:
#                     myVmdImageLibvirtXmlEventHandler('Modify', vmi, event.src_path, self.group, self.version, self.plural)
#                 except ApiException:
#                     logger.error('Oops! ', exc_info=1)
                    
def myImageLibvirtXmlEventHandler(event, name, xml_path, group, version, plural):
    #     print(jsondict)
    if event == "Create":
        try:
            logger.debug('Create vm image %s, report to virtlet' % name)
            jsondict = {'spec': {'domain': {}, 'nodeName': HOSTNAME, 'status': {}}, 
                        'kind': VMI_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name}, 'apiVersion': '%s/%s' % (group, version)}
            with open(xml_path, 'r') as fr:
                vm_xml = fr.read()
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            body = addNodeName(jsondict)
            try:
                createStructure(body, group, version, plural)
            except ApiException, e:
                if e.reason == 'Conflict':
                    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                              version=version, 
                                                                              namespace='default', 
                                                                              plural=plural, 
                                                                              name=name)
                    jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
                    jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                    body = addNodeName(jsondict)
                    modifyStructure(name, body, group, version, plural)  
                else:
                    logger.error(e)
                    
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                               version=version, 
                                                                               namespace='default', 
                                                                               plural=plural, 
                                                                               name=name) 
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)         
    elif event == "Modify":
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
        try:
            logger.debug('Modify vm image %s, report to virtlet' % name)
            with open(xml_path, 'r') as fr:
                vm_xml = fr.read()
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#             logger.debug(body)
            modifyStructure(name, body, group, version, plural)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
    elif event == "Delete":
#             jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
#                                                                               version=version, 
#                                                                               namespace='default', 
#                                                                               plural=plural, 
#                                                                               name=name)
        try:
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
#             with open(xml_path, 'r') as fr:
#                 vm_xml = fr.read()
#             vm_json = toKubeJson(xmlToJson(vm_xml))
#             vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**VM image %s already deleted, ignore this 404 error.' % name)
        except:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm image %s, report to virtlet' % name)
            deleteStructure(name, V1DeleteOptions(), group, version, plural)
#                 jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
#                 body = addExceptionMessage(jsondict, 'VirtletError', 'VM has been deleted in back-end.')
#                 modifyStructure(name, body, group, version, plural)   
        except:
            logger.error('Oops! ', exc_info=1)

class ImageLibvirtXmlEventHandler(FileSystemEventHandler):
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
            _,name = os.path.split(event.dest_path)
            file_type = os.path.splitext(name)[1]
            vmi = os.path.splitext(os.path.splitext(name)[0])[0]
            if file_type == '.xml':
                try:
                    myImageLibvirtXmlEventHandler('Create', vmi, event.dest_path, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
#             _,name = os.path.split(event.src_path)
#             file_type = os.path.splitext(name)[1]
#             vmi = os.path.splitext(os.path.splitext(name)[0])[0]
#             if file_type == '.xml':
#                 try:
#                     myImageLibvirtXmlEventHandler('Create', vmi, event.src_path, self.group, self.version, self.plural)
#                 except ApiException:
#                     logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            _,name = os.path.split(event.src_path)
            file_type = os.path.splitext(name)[1]
            vmi = os.path.splitext(os.path.splitext(name)[0])[0]
            if file_type == '.xml':
                try:
                    myImageLibvirtXmlEventHandler('Delete', vmi, event.src_path, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
#             logger.debug("directory modified:{0}".format(event.src_path))
            pass
        else:
#             logger.debug("file modified:{0}".format(event.src_path))
            _,name = os.path.split(event.src_path)
            file_type = os.path.splitext(name)[1]
            vmi = os.path.splitext(os.path.splitext(name)[0])[0]
            if file_type == '.xml':
                try:
                    myImageLibvirtXmlEventHandler('Modify', vmi, event.src_path, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

def updateDomainStructureAndDeleteLifecycleInJson(jsondict, body):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['spec']
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(body)
    return jsondict

def addNodeName(jsondict):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['spec']
        if spec:
            jsondict['spec']['nodeName'] = HOSTNAME
    return jsondict

            
def main():
    observer = Observer()
    try:
        # for ob in VOL_DIRS:
        #     if not os.path.exists(ob[1]):
        #         os.makedirs(ob[1], 0711)
        #         try:
        #             runCmdRaiseException('virsh pool-create-as --name %s --type dir --target %s' % (ob[0], ob[1]))
        #         except:
        #             os.removedirs(ob[1])
        #             logger.error('Oops! ', exc_info=1)
        #     event_handler = VmVolEventHandler(ob[0], ob[1], GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
        #     observer.schedule(event_handler,ob[1],True)
        # for ob in SYSTEM_VOL_DIRS:
        #     if not os.path.exists(ob[1]):
        #         os.makedirs(ob[1], 0711)
        #     event_handler = VmVolEventHandler(ob[0], ob[1], GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
        #     observer.schedule(event_handler,ob[1],True)
        for ob in SNAP_DIRS:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0711)
            event_handler = VmSnapshotEventHandler(ob[0], ob[1], GROUP_VM_SNAPSHOT, VERSION_VM_SNAPSHOT, PLURAL_VM_SNAPSHOT)
            observer.schedule(event_handler,ob[1],True)
        for ob in BLOCK_DEV_DIRS:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0711)
            event_handler = VmBlockDevEventHandler(ob[0], ob[1], GROUP_BLOCK_DEV_UIT, VERSION_BLOCK_DEV_UIT, PLURAL_BLOCK_DEV_UIT)
            observer.schedule(event_handler,ob[1],True)
        for ob in LIBVIRT_XML_DIRS:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0711)
            event_handler = VmLibvirtXmlEventHandler(ob[0], ob[1], GROUP_VM, VERSION_VM, PLURAL_VM)
            observer.schedule(event_handler,ob[1],True)
        for ob in TEMPLATE_DIRS:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0711)
            event_handler = ImageLibvirtXmlEventHandler(ob[0], ob[1], GROUP_VMI, VERSION_VMI, PLURAL_VMI)
            observer.schedule(event_handler,ob[1],True)
        for ob in VMD_TEMPLATE_DIRS:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0711)
                try:
                    runCmdRaiseException('virsh pool-create-as --name %s --type dir --target %s' % (ob[0], ob[1]))
                except:
                    os.removedirs(ob[1])
                    logger.error('Oops! ', exc_info=1)
            event_handler = VmdImageLibvirtXmlEventHandler(ob[0], ob[1], GROUP_VM_DISK_IMAGE, VERSION_VM_DISK_IMAGE, PLURAL_VM_DISK_IMAGE)
            observer.schedule(event_handler,ob[1],True)
        observer.start()

        OLD_PATH_WATCHERS = {}
        while True:
            try:
                paths = _get_all_pool_path()
                if paths.has_key('vmdi'):
                    del paths['vmdi']
                # unschedule not exist pool path
                watchers = {}
                for path in OLD_PATH_WATCHERS.keys():
                    if path not in paths.values():
                        observer.unschedule(OLD_PATH_WATCHERS[path])
                    else:
                        watchers[path] = OLD_PATH_WATCHERS[path]
                OLD_PATH_WATCHERS = watchers


                for pool in paths.keys():
                    # schedule new pool path
                    if paths[pool] not in OLD_PATH_WATCHERS.keys() and os.path.isdir(paths[pool]):
                        logger.debug(paths[pool])
                        event_handler = VmVolEventHandler(pool, paths[pool], GROUP_VM_DISK, VERSION_VM_DISK,
                                                          PLURAL_VM_DISK)
                        watcher = observer.schedule(event_handler, paths[pool], True)
                        OLD_PATH_WATCHERS[paths[pool]] = watcher

            except Exception, e:
                logger.debug(traceback.print_exc())
                logger.debug("error occur when watch all storage pool")

            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except:
        logger.warning('Oops! ', exc_info=1)
    observer.join()    

if __name__ == "__main__":
    config.load_kube_config(config_file=TOKEN)
    main()
