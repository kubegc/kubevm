'''
Copyright (2021, ) Institute of Software, Chinese Academy of 

@author: wuheng@otcaix.iscas.ac.cn
@author: wuyuewen@otcaix.iscas.ac.cn
'''
import json
from json import loads, load, dumps, dump
import re
import fcntl
import shlex
import errno
from functools import wraps
import os, sys, time, signal, atexit, subprocess
import threading
import random
import socket
import datetime
import traceback
import operator
from dateutil.tz import gettz
from pprint import pformat
from six import iteritems
from xml.etree import ElementTree
from collections import namedtuple
import subprocess
import collections
from pprint import pprint
from xml.dom import minidom
from io import StringIO as _StringIO
import logging
import logging.handlers

'''
Import third party libs
'''
try:
    import libvirt
    HAS_LIBVIRT = True
except ImportError:
    HAS_LIBVIRT = False
import yaml

'''
Import third party libs
'''
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from kubernetes import config, client
from kubernetes.client import V1DeleteOptions
sys.path.append('..')
sys.path.append('/home/kubevmm/core/')
sys.path.append('./core/')
from xml.dom.minidom import Document
from xml.etree.ElementTree import fromstring

from xmljson import badgerfish as bf

from kubernetes.client.rest import ApiException

from utils import constants
from utils.exception import InternalServerError, NotFound, Forbidden, BadRequest
from utils.libvirt_util import create, destroy, check_pool_content_type, refresh_pool, get_vol_info_by_qemu, get_volume_xml, get_pool_path, is_volume_in_use, is_volume_exists, get_volume_current_path, vm_state, is_vm_exists, is_vm_active, get_boot_disk_path, get_xml, undefine_with_snapshot, undefine, define_xml_str
from utils.misc import get_l2_network_info, get_address_set_info, get_l3_network_info, updateDomain, randomMAC, runCmd, get_rebase_backing_file_cmds, add_spec_in_volume, get_hostname_in_lower_case, DiskImageHelper, updateDescription, get_volume_snapshots, updateJsonRemoveLifecycle, addSnapshots, report_failure, addPowerStatusMessage, RotatingOperation, string_switch, deleteLifecycleInJson, get_field_in_kubernetes_by_index, write_config
from utils import logger
from utils.k8s import K8sHelper

VM_PLURAL = constants.KUBERNETES_PLURAL_VM
VMP_PLURAL = constants.KUBERNETES_PLURAL_VMP
VMD_PLURAL = constants.KUBERNETES_PLURAL_VMD
VMDI_PLURAL = constants.KUBERNETES_PLURAL_VMDI
VMDSN_PLURAL = constants.KUBERNETES_PLURAL_VMDSN
VM_KIND = constants.KUBERNETES_KIND_VM
VMP_KIND = constants.KUBERNETES_KIND_VMP
VMD_KIND = constants.KUBERNETES_KIND_VMD
VMDI_KIND = constants.KUBERNETES_KIND_VMDI
VMDSN_KIND = constants.KUBERNETES_KIND_VMDSN
VERSION = constants.KUBERNETES_API_VERSION
GROUP = constants.KUBERNETES_GROUP
DEFAULT_DEVICE_DIR = constants.KUBEVMM_VM_DEVICES_DIR

HOSTNAME = get_hostname_in_lower_case()

LOG = constants.KUBEVMM_VIRTCTL_LOG
logger = logger.set_logger(os.path.basename(__file__), LOG)


def create_vmdi_from_disk(params):
    name, sourceVolume, sourcePool, targetPool = _get_param('--name',params), _get_param('--sourceVolume', params)
    _get_param('--sourcePool',params), _get_param('--targetPool', params)
    # cmd = os.path.split(os.path.realpath(__file__))[0] +'/scripts/convert-vm-to-image.sh ' + name
    
    '''
    A list to record what we already done.
    '''
    done_operations = []
    doing = ''
    
#     class step_1_dumpxml_to_path(RotatingOperation):
#         
#         def __init__(self, vmd, sourcePool, tag):
#             self.tag = tag
#             self.vmd = vmd
#             self.sourcePool = sourcePool
#             self.temp_path = '%s/%s.xml.new' % (DEFAULT_VMD_TEMPLATE_DIR, vmd)
#             self.path = '%s/%s.xml' % (DEFAULT_VMD_TEMPLATE_DIR, vmd)
#     
#         def option(self):
#             vmd_xml = get_volume_xml(self.sourcePool, self.vmd)
#             with open(self.temp_path, 'w') as fw:
#                 fw.write(vmd_xml)
#             shutil.move(self.temp_path, self.path)
#             done_operations.append(self.tag)
#             return 
#     
#         def rotating_option(self):
#             if self.tag in done_operations:
#                 if os.path.exists(self.path):
#                     os.remove(self.path)
#             return 
    
    class step_1_copy_template_to_path(RotatingOperation):
        
        def __init__(self, name, vmd, sourcePool, targetPool, tag, full_copy=True):
            self.tag = tag
            self.name = name
            self.vmd = vmd
            self.pool = sourcePool
            self.full_copy = full_copy
            self.source_dir = '%s/%s' % (get_pool_path(sourcePool), vmd)
            self.dest_dir = '%s/%s' % (get_pool_path(targetPool), name)
            self.dest = '%s/%s' % (self.dest_dir, name)
            self.source_config_file = '%s/config.json' % (self.source_dir)
            self.target_config_file = '%s/config.json' % (self.dest_dir)
#             self.store_source_path = '%s/%s.path' % (DEFAULT_VMD_TEMPLATE_DIR, vmd)
#             self.xml_path = '%s/%s.xml' % (DEFAULT_VMD_TEMPLATE_DIR, vmd)
    
        def option(self):
            '''
            Copy template's boot disk to destination dir.
            '''
            if os.path.exists(self.target_config_file):
                raise Exception('409, Conflict. Resource %s already exists, aborting copy.' % self.target_config_file)
#             set_backing_file_cmd = get_rebase_backing_file_cmds(self.source_dir, self.dest_dir)
            source_current = _get_current(self.source_config_file)
            
            if self.full_copy:
                copy_template_cmd = 'cp -f %s %s' % (source_current, self.dest)
            runCmd(copy_template_cmd)
            
            cmd1 = 'qemu-img rebase -f qcow2 %s -b "" -u' % (self.dest)
            runCmd(cmd1)
            
#             for cmd in set_backing_file_cmd:
#                 runCmd(cmd)
            
            config = {}
            config['name'] = self.name
            config['dir'] = self.dest_dir
            config['current'] = self.dest

            with open(self.target_config_file, "w") as f:
                dump(config, f)
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                for path in [self.dest_dir]:
#                 for path in [self.dest_path, self.store_source_path, self.xml_path]:
                    if os.path.exists(path):
                        runCmd('rm -rf %s' %(path))
            return 

    class step_2_delete_source_file(RotatingOperation):
        
        def __init__(self, vmd, sourcePool, tag):
            self.tag = tag
            self.vmd = vmd
            self.source_dir = '%s/%s' % (get_pool_path(sourcePool), vmd)
    
        def option(self):
            '''
            Remove source path of template's boot disk
            '''
            if os.path.exists(self.source_dir):
                runCmd('rm -rf %s' %(self.source_dir))
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                logger.debug('In final step, rotating noting.')
            return 
        
#     jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    '''
    #Preparations
    '''
    doing = 'Preparations'
    if not sourcePool:
        raise Exception('404, Not Found. Source pool not found.')
    if not is_volume_exists(sourceVolume, sourcePool):
        raise Exception('VM disk %s not exists!' % name)
#     if is_volume_in_use(vol=name, pool=sourcePool):
#         raise Exception('Cannot covert vmd in use to image.')
    if not check_pool_content_type(targetPool, 'vmdi'):
        raise Exception('Target pool\'s content type is not vmdi.')
    dest_dir = '%s/%s' % (get_pool_path(targetPool), name)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, 0o711)
#     step1 = step_1_dumpxml_to_path(name, sourcePool, 'step1')
    step1 = step_1_copy_template_to_path(name, sourceVolume, sourcePool, targetPool, 'step1')
    try:
        #cmd = 'bash %s/scripts/convert-vm-to-image.sh %s' %(PATH, name)
        '''
        #Step 1
        '''
        doing = step1.tag
        step1.option()
#         '''
#         #Step 4: synchronize information to Kubernetes
#         '''   
#         doing = 'Synchronize to Kubernetes'       
#         jsonDict = jsonStr.copy()
#         jsonDict['kind'] = 'VirtualMachineImage'
#         jsonDict['metadata']['kind'] = 'VirtualMachineImage'
#         del jsonDict['metadata']['resourceVersion']
#         del jsonDict['spec']['lifecycle']
#         try:
#             client.CustomObjectsApi().create_namespaced_custom_object(
#                 group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, body=jsonDict)
#             client.CustomObjectsApi().delete_namespaced_custom_object(
#                 group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name, body=V1DeleteOptions())
#         except ApiException:
#             logger.warning('Oops! ', exc_info=1)
#         '''
#         #Check sychronization in Virtlet.
#           timeout = 3s
#         '''
#         i = 0
#         success = False
#         while(i < 3):
#             try: 
#                 client.CustomObjectsApi().get_namespaced_custom_object(group=VMDI_GROUP, version=VMDI_VERSION, namespace='default', plural=VMDI_PLURAL, name=name)
#             except:
#                 time.sleep(1)
#                 success = False
#                 continue
#             finally:
#                 i += 1
#             success = True
#             break;
#         if not success:
#             raise Exception('Synchronize information in Virtlet failed!')
        config_file = '%s/config.json' % (dest_dir)
        current = _get_current(config_file)
        write_result_to_server(name, 'create', VMDI_KIND, VMDI_PLURAL, {'current': current, 'pool': targetPool})
#         '''
#         #Step 2
#         '''
#         doing = step2.tag
#         step2.option()
#         write_result_to_server(name, 'delete', VMD_KIND, VMD_PLURAL, {'pool': sourcePool})
    except:
        logger.debug(done_operations)
        error_reason = 'VmmError'
        error_message = '%s failed!' % doing
        logger.error(error_reason + ' ' + error_message)
        logger.error('Oops! ', exc_info=1)
#         report_failure(name, jsonStr, error_reason, error_message, GROUP, VERSION, VM_PLURAL)
        step1.rotating_option()

'''
A atomic operation: Convert image to vm.
'''
def convert_vmdi_to_vmd(params):
    '''
    A list to record what we already done.
    '''
    name, sourcePool, targetPool = _get_param('--name', params), 
    _get_param('--sourcePool', params), _get_param('--targetPool', params)
    done_operations = []
    doing = ''
    
    class step_1_copy_template_to_path(RotatingOperation):
        
        def __init__(self, vmdi, sourcePool, targetPool, tag, full_copy=True):
            self.tag = tag
            self.vmdi = vmdi
            self.pool = targetPool
            self.full_copy = full_copy
            self.source_dir = '%s/%s' % (get_pool_path(sourcePool), vmdi)
            self.dest_dir = '%s/%s' % (get_pool_path(targetPool), vmdi)
            self.config_file = '%s/config.json' % (self.dest_dir)
#             self.store_target_path = '%s/%s.path' % (DEFAULT_VMD_TEMPLATE_DIR, vmdi)
#             self.xml_path = '%s/%s.xml' % (DEFAULT_VMD_TEMPLATE_DIR, vmdi)
    
        def option(self):
            if not os.path.exists(self.dest_dir):
                os.makedirs(self.dest_dir, 0o711)
            if os.path.exists(self.config_file):
                raise Exception('409, Conflict. Resource %s already exists, aborting copy.' % self.config_file)
            
            set_backing_file_cmd = get_rebase_backing_file_cmds(self.source_dir, self.dest_dir)
            
            if self.full_copy:
                copy_template_cmd = 'cp -rf %s/* %s' % (self.source_dir, self.dest_dir)
            runCmd(copy_template_cmd)
            
            for cmd in set_backing_file_cmd:
                runCmd(cmd)
                
            current = _get_current(self.config_file).replace(self.source_dir, self.dest_dir)
            config = {}
            config['name'] = self.vmdi
            config['dir'] = self.dest_dir
            config['current'] = current
            with open(self.config_file, "w") as f:
                dump(config, f)
    
        def rotating_option(self):
            if self.tag in done_operations:
                if os.path.exists(self.dest_dir):
                    runCmd('rm -rf %s' %(self.dest_dir))
            return 
        
    class step_2_delete_source_file(RotatingOperation):
        
        def __init__(self, vmdi, sourcePool, tag):
            self.tag = tag
            self.vmdi = vmdi
            self.source_dir = '%s/%s' % (get_pool_path(sourcePool), vmdi)
#             self.store_target_path = '%s/%s.path' % (DEFAULT_VMD_TEMPLATE_DIR, vmdi)
#             self.xml_path = '%s/%s.xml' % (DEFAULT_VMD_TEMPLATE_DIR, vmdi)
    
        def option(self):
            '''
            Remove source path of template's boot disk
            '''
            for path in [self.source_dir]:
                if os.path.exists(path):
                    runCmd('rm -rf %s' %(path))
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                logger.debug('In final step, rotating noting.')
            return 
        
#     jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, name=name)
    if not sourcePool:
        raise Exception('404, Not Found. Source pool not found.')
    dest_dir = '%s/%s' % (get_pool_path(targetPool), name)
    step1 = step_1_copy_template_to_path(name, sourcePool, targetPool, 'step1')
    step2 = step_2_delete_source_file(name, sourcePool, 'step2')
    try:
        '''
        #Step 1: copy template to original path
        '''
        doing = step1.tag
        step1.option()
#         '''
#         #Step 3: synchronize information to Kubernetes
#         '''  
#         jsonDict = jsonStr.copy()
#         jsonDict['kind'] = 'VirtualMachine'
#         jsonDict['metadata']['kind'] = 'VirtualMachine'
#         del jsonDict['metadata']['resourceVersion']
#         del jsonDict['spec']['lifecycle']
#         try:
#             client.CustomObjectsApi().create_namespaced_custom_object(
#                 group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, body=jsonDict)
#             client.CustomObjectsApi().delete_namespaced_custom_object(
#                 group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, name=name, body=V1DeleteOptions())
#         except ApiException:
#             logger.warning('Oops! ', exc_info=1)
        config_file = '%s/config.json' % (dest_dir)
        current = _get_current(config_file)
        write_result_to_server(name, 'create', VMD_KIND, VMD_PLURAL, {'current': current, 'pool': targetPool})
        
        '''
        #Check sychronization in Virtlet.
          timeout = 3s
        '''
        i = 0
        success = False
        while(i < 3):
            try:
                client.CustomObjectsApi().get_namespaced_custom_object(group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=name)
            except:
                time.sleep(1)
                success = False
                continue
            finally:
                i += 1
            success = True
            break;
        if not success:
            raise Exception('Synchronize information in Virtlet failed!')
        '''
        #Step 2: define VM
        '''       
        doing = step2.tag
        step2.option()
        
        write_result_to_server(name, 'delete', VMDI_KIND, VMDI_PLURAL, {'pool': sourcePool})
    except:
        logger.debug(done_operations)
        error_reason = 'VmmError'
        error_message = '%s failed!' % doing
        logger.error(error_reason + ' ' + error_message)
        logger.error('Oops! ', exc_info=1)
#         report_failure(name, jsonStr, error_reason, error_message, GROUP, VERSION, VM_PLURAL)
        step2.rotating_option()
        step1.rotating_option()
        
def create_vmdi(params):
    name, source, target = _get_param('--name', params), _get_param('--source', params),
    _get_param('--targetPool', params)
    dest_dir = '%s/%s' % (get_pool_path(target), name)
    dest = '%s/%s' % (dest_dir, name)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, 0o711)
    if os.path.exists(dest):
        raise Exception('409, Conflict. File %s already exists, aborting copy.' % dest)
    if not check_pool_content_type(target, 'vmdi'):
        raise Exception('Target pool\'s content type is not vmdi.')
    cmd = 'cp -f %s %s' % (source, dest)
    try:
        runCmd(cmd)
    except:
        if os.path.exists(dest_dir):
            runCmd('rm -rf %s' % dest_dir)
        raise Exception('400, Bad Reqeust. Copy %s to %s failed!' % (source, dest))
    cmd1 = 'qemu-img rebase -f qcow2 %s -b ""' % (dest)
    try:
        runCmd(cmd1)
    except:
        if os.path.exists(dest_dir):
            runCmd('rm -rf %s' % dest_dir)
        raise Exception('400, Bad Reqeust. Execute "qemu-img rebase -f qcow2 %s" failed!' % (dest))
    
    config = {}
    config['name'] = name
    config['dir'] = dest_dir
    config['current'] = dest

    with open(dest_dir + '/config.json', "w") as f:
        dump(config, f)
    
    write_result_to_server(name, 'create', VMDI_KIND, VMDI_PLURAL, {'current': dest, 'pool': target})
    
def create_disk_from_vmdi(params):
    name, targetPool, source = _get_param('--name', params), _get_param('--targetPool', params), 
    _get_param('--source', params)
    dest_dir = '%s/%s' % (get_pool_path(targetPool), name)
    dest = '%s/%s' % (dest_dir, name)
    dest_config_file = '%s/config.json' % (dest_dir)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, 0o711)    
    if os.path.exists(dest_config_file):
        raise Exception('409, Conflict. Path %s already in use, aborting copy.' % dest_dir)
    cmd = 'cp -f %s %s' % (source, dest)
    try:
        runCmd(cmd)
    except:
        if os.path.exists(dest_dir):
            runCmd('rm -rf %s' % dest_dir)
        raise Exception('400, Bad Reqeust. Copy %s to %s failed!' % (source, dest))
    
    cmd1 = 'qemu-img rebase -f qcow2 %s -b "" -u' % (dest)
    try:
        runCmd(cmd1)
    except:
        if os.path.exists(dest_dir):
            runCmd('rm -rf %s' % dest_dir)
        raise Exception('400, Bad Reqeust. Execute "qemu-img rebase -f qcow2 %s" failed!' % (dest))
    
    config = {}
    config['name'] = name
    config['dir'] = dest_dir
    config['current'] = dest

    with open(dest_dir + '/config.json', "w") as f:
        dump(config, f)
    
    time.sleep(1)
    
    write_result_to_server(name, 'create', VMD_KIND, VMD_PLURAL,  {'current': dest, 'pool': targetPool})

# def toImage(name):
#     jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachines', name=name)
#     jsonDict = jsonStr.copy()
#     jsonDict['kind'] = 'VirtualMachineImage'
#     jsonDict['metadata']['kind'] = 'VirtualMachineImage'
#     del jsonDict['metadata']['resourceVersion']
#     del jsonDict['spec']['lifecycle']
#     client.CustomObjectsApi().create_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachineimages', body=jsonDict)
#     client.CustomObjectsApi().delete_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachines', name=name, body=V1DeleteOptions())
#     logger.debug('convert VM to Image successful.')
#     
# def toVM(name):
#     jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachineimages', name=name)
#     jsonDict = jsonStr.copy()
#     jsonDict['kind'] = 'VirtualMachine'
#     jsonDict['metadata']['kind'] = 'VirtualMachine'
#     del jsonDict['spec']['lifecycle']
#     del jsonDict['metadata']['resourceVersion']
#     client.CustomObjectsApi().create_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachines', body=jsonDict)
#     client.CustomObjectsApi().delete_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachineimages', name=name, body=V1DeleteOptions())
#     logger.debug('convert Image to VM successful.')

# def delete_image(name):
#     file1 = '%s/%s.xml' % (DEFAULT_TEMPLATE_DIR, name)
#     file2 = '%s/%s' % (DEFAULT_TEMPLATE_DIR, name)
#     file3 = '%s/%s.path' % (DEFAULT_TEMPLATE_DIR, name)
#     file4 = '%s/%s-nic-*' % (DEFAULT_TEMPLATE_DIR, name)
#     file5 = '%s/%s-disk-*' % (DEFAULT_TEMPLATE_DIR, name)
#     cmd = 'rm -rf %s %s %s %s %s' % (file1, file2, file3, file4, file5)
#     try:
#         runCmd(cmd)
#     except:
#         logger.error('Oops! ', exc_info=1)

def delete_vmdi(params):
    name, sourcePool= _get_param('--name', params), _get_param('--sourcePool', params)
    pool_path = get_pool_path(sourcePool)
    if not pool_path:
        logger.debug('Cannot get pool path for %s' % sourcePool)
        raise BadRequest('Cannot get pool path for %s' % sourcePool)
    targetDir = '%s/%s' % (pool_path, name)
    cmd = 'rm -rf %s' % (targetDir)
    runCmd(cmd)
    
    write_result_to_server(name, 'delete', VMDI_KIND, VMDI_PLURAL, {'pool': sourcePool})

def updateOS(params):
    name, source, target = _get_param('--domain', params), _get_param('--source', params), 
    _get_param('--target', params)
    jsonDict = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    jsonString = json.dumps(jsonDict)
    if jsonString.find(source) >= 0 and os.path.exists(target):
        runCmd('cp %s %s' %(target, source))
    else:
        raise Exception('Wrong source or target.')
    jsonDict = deleteLifecycleInJson(jsonDict)
    vm_power_state = vm_state(name).get(name)
    body = addPowerStatusMessage(jsonDict, vm_power_state, 'The VM is %s' % vm_power_state)
    body = updateDescription(body)
    try:
        client.CustomObjectsApi().replace_namespaced_custom_object(
            group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name, body=body)
    except ApiException as e:
        if e.reason == 'Conflict':
            logger.debug('**Other process updated %s, ignore this 409 error.' % name) 
        else:
            logger.error(e)
            raise e   

def delete_disk(params):
    params_dict = _get_params(params)
    vol, pool, type = params_dict.get('vol'), params_dict.get('pool'), params_dict.get('type')
    pool_path = get_field_in_kubernetes_by_index(pool, GROUP, VERSION, VMP_PLURAL, ['spec','pool','url'])
    if not os.path.isdir(pool_path):
        raise BadRequest('can not get pool path: %s.' % pool_path)
    disk_dir = "%s/%s" % (pool_path, vol)
    cmd1 = 'rm -rf %s' % disk_dir
    operation_queue = [cmd1]
    _runOperationQueue(operation_queue)
    helper = K8sHelper(VMD_KIND)
    helper.delete(vol)
    return

def delete_pool(params):
    params_dict = _get_params(params)
    pool = params_dict.get('pool')
    cmd1 = 'virsh pool-destroy %s' % pool
    cmd2 = 'virsh pool-undefine %s' % pool
    operation_queue = [cmd1, cmd2]
    try:
        _runOperationQueue(operation_queue)
    except Exception as e:
        logger.error('Oops! ', exc_info=1)
        reverse1 = 'virsh pool-start --pool %s' % (pool)
        operation_queue1 = [reverse1]
        _runOperationQueue(operation_queue1, False)
        raise e
    helper = K8sHelper(VMP_KIND)
    helper.delete(pool)
    return
        
def create_disk(params):
    params_dict = _get_params(params)
    vol, pool, capacity, format, type = params_dict.get('vol'), params_dict.get('pool'), params_dict.get('capacity'), \
                    params_dict.get('format'), params_dict.get('type')
    pool_path = get_field_in_kubernetes_by_index(pool, GROUP, VERSION, VMP_PLURAL, ['spec','pool','url'])
    if not os.path.isdir(pool_path):
        raise BadRequest('can not get pool path: %s.' % pool_path)
    # create disk dir and create disk in dir.
    disk_dir = "%s/%s" % (pool_path, vol)
    if os.path.isdir(disk_dir):
        raise BadRequest('error: disk path %s already exists.' % disk_dir)
    cmd1 = 'mkdir -p %s' % disk_dir
    vol_name_with_format = '%s.%s' % (vol, format)
    disk_path = os.path.join(disk_dir, vol_name_with_format)
    cmd2 = 'qemu-img create -f %s %s %s' % (format, disk_path, capacity)
    operation_queue = [cmd1, cmd2]
    try:
        _runOperationQueue(operation_queue)
    except Exception as e:
        logger.error('Oops! ', exc_info=1)
        reverse1 = 'rm -rf %s' % (disk_path)
        operation_queue1 = [reverse1]
        _runOperationQueue(operation_queue1, False)
        raise e
    write_config(vol, disk_dir, disk_path, pool)
    helper = K8sHelper(VMD_KIND)
    data = params_dict
    data['current'] = disk_path
    helper.update(vol,'volume',data)
    return

def create_pool(params):
    params_dict = _get_params(params)
    pool, pool_type, pool_content, auto_start, pool_url, pool_uuid = params_dict.get('pool'), params_dict.get('type'), \
                  params_dict.get('content'), params_dict.get('auto-start'), params_dict.get('url'), params_dict.get('uuid')
    cmd1 = 'mkdir -p %s' % pool_url
    cmd2 = 'virsh pool-define-as --name %s --type %s --target %s' % (pool, pool_type, pool_url)
    if auto_start:
        cmd3 = 'virsh pool-autostart --pool %s' % (pool)
    else:
        cmd3 = None
    cmd4 = 'virsh pool-start --pool %s' % (pool)
    operation_queue = [cmd1, cmd2, cmd3, cmd4]
    try:
        _runOperationQueue(operation_queue)
    except Exception as e:
        logger.error('Oops! ', exc_info=1)
        reverse1 = 'virsh pool-destroy --pool %s' % (pool)
        reverse2 = 'virsh pool-undefine --pool %s' % (pool)
        operation_queue1 = [reverse1, reverse2]
        _runOperationQueue(operation_queue1, False)
        raise e
    with open('%s/content' % pool_url, 'w') as f:
        f.write(pool_content)
    helper = K8sHelper(VMP_KIND)
    data = params_dict
    data['state'] = 'active'
    data['autostart'] = auto_start
    del data['auto-start']
    helper.update(pool,'pool',data)
    return
    
def create_disk_snapshot(params):
    vol, pool, snapshot = _get_param('--name', params), _get_param('--pool', params),
    _get_param('--snapshotname', params)
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=vol)
    vol_path = get_volume_current_path(pool, vol)
    snapshots = get_volume_snapshots(vol_path)['snapshot']
    name_conflict = False
    for sn in snapshots:
        if sn.get('name') == snapshot:
            name_conflict = True
            break;
        else:
            continue
    if name_conflict:
        raise Exception('409, Conflict. Snapshot name %s already in use.' % snapshot)
    cmd = 'qemu-img snapshot -c %s %s' % (snapshot, vol_path)
    try:
        runCmd(cmd)
        vol_xml = get_volume_xml(pool, vol)
        vol_path = get_volume_current_path(pool, vol)
        vol_json = toKubeJson(xmlToJson(vol_xml))
        vol_json = addSnapshots(vol_path, loads(vol_json))
        jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
        body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
        body = updateDescription(body)
        try:
            client.CustomObjectsApi().replace_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=vol, body=body)
        except ApiException as e:
            if e.reason == 'Conflict':
                logger.debug('**Other process updated %s, ignore this 409 error.' % vol) 
            else:
                logger.error(e)
                raise e   
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        report_failure(vol, jsondict, 'VirtletError', str(info[1]), GROUP, VERSION, VMD_PLURAL)

def delete_disk_snapshot(params):
    vol, pool, snapshot = _get_param('--name', params), _get_param('--pool', params),
    _get_param('--snapshotname', params)
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=vol)
    vol_path = get_volume_current_path(pool, vol)
    cmd = 'qemu-img snapshot -d %s %s' % (snapshot, vol_path)
    try:
        runCmd(cmd)
        vol_xml = get_volume_xml(pool, vol)
        vol_path = get_volume_current_path(pool, vol)
        vol_json = toKubeJson(xmlToJson(vol_xml))
        vol_json = addSnapshots(vol_path, loads(vol_json))
        jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
        body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
        body = updateDescription(body)
        try:
            client.CustomObjectsApi().replace_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=vol, body=body)
        except ApiException as e:
            if e.reason == 'Conflict':
                logger.debug('**Other process updated %s, ignore this 409 error.' % vol) 
            else:
                logger.error(e)
                raise e   
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        report_failure(vol, jsondict, 'VirtletError', str(info[1]), GROUP, VERSION, VMD_PLURAL)

def revert_disk_internal_snapshot(params):
    vol, pool, snapshot = _get_param('--name', params), _get_param('--pool', params),
    _get_param('--snapshotname', params)
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=vol)
    vol_path = get_volume_current_path(pool, vol)
    cmd = 'qemu-img snapshot -a %s %s' % (snapshot, vol_path)
    try:
        runCmd(cmd)
        vol_xml = get_volume_xml(pool, vol)
        vol_path = get_volume_current_path(pool, vol)
        vol_json = toKubeJson(xmlToJson(vol_xml))
        vol_json = addSnapshots(vol_path, loads(vol_json))
        jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
        body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
        body = updateDescription(body)
        try:
            client.CustomObjectsApi().replace_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=VMD_PLURAL, name=vol, body=body)
        except ApiException as e:
            if e.reason == 'Conflict':
                logger.debug('**Other process updated %s, ignore this 409 error.' % vol) 
            else:
                logger.error(e)
                raise e         
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        report_failure(vol, jsondict, 'VirtletError', str(info[1]), GROUP, VERSION, VMD_PLURAL)
        
def revert_disk_external_snapshot(params):
#     jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=VMD_GROUP, version=VMD_VERSION, namespace='default', plural=VMD_PLURAL, name=vol)
    vol, pool, snapshot, leaves_str = _get_param('--name', params), _get_param('--pool', params),
    _get_param('--snapshotname', params), _get_param('--leaves', params)
    snapshot_path = get_volume_current_path(pool, snapshot)
    leaves = leaves_str.replace(' ', '').split(',')
    disks_to_delete = []
    for leaf in leaves:
        leaf_path = get_volume_current_path(pool, leaf)
        backing_chain = [leaf_path]
        backing_chain += DiskImageHelper.get_backing_files_tree(leaf_path)
        for backing_file in backing_chain:
            if backing_file == snapshot_path:
                break;
            else:
                disks_to_delete.append(backing_file)
    disks_to_delete = list(set(disks_to_delete))
    cmd1 = 'rm -f '
    for disk_to_delete in disks_to_delete:
        cmd1 = cmd1 + disk_to_delete + " "
    print(cmd1)
    runCmd(cmd1)
        
def addExceptionMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'waiting':{'message':message, 'reason':reason}}}}
        spec = jsondict['spec']
        if spec:
            spec['status'] = status
    return jsondict

def _get_param(key, params):
    try:
        index = params.index(key)
        return params[index+1]
    except ValueError as e:
        raise BadRequest('Wrong parameter %s' % key)
    except Exception as e:
        raise BadRequest(repr(e))

def _get_params(params):
    try:
        jsondict = {}
        for i, param in enumerate(params):
            print(i, len(params))
            if param.startswith('--'):
                if i < len(params)-1 and not params[i+1].startswith('--'):
                    jsondict[param.replace('--', '', 1)] = params[i+1]
                elif i < len(params)-1 and params[i+1].startswith('--'):
                    jsondict[param.replace('--', '', 1)] = True
                elif i == len(params)-1 and param.startswith('--'):
                    jsondict[param.replace('--', '', 1)] = True
                else:
                    continue
            else:
                continue
        return jsondict
    except Exception as e:
        raise BadRequest(repr(e))        
    
def _set_param(key, value, params):
    try:
        index = params.index(key)
        params[index+1] = value
    except ValueError as e:
        raise BadRequest('Wrong parameter %s' % key)
    except Exception as e:
        raise BadRequest(repr(e))

def _get_current(src_path):
    with open(src_path, "r") as f:
        config = json.load(f)
    return config.get('current')

def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace(
                    'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')
                    
def write_result_to_server(name, op, kind, plural, params):
    if op == 'create':
        logger.debug('Create %s %s, report to virtlet' % (kind, name))
        jsondict = {'spec': {'volume': {}, 'nodeName': HOSTNAME, 'status': {}},
                    'kind': kind, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
                    'apiVersion': '%s/%s' % (GROUP, VERSION)}
        
#             with open(get_pool_path(params.get('pool')) + '/' + name + '/config.json', "r") as f:
#                 config = json.load(f)
        vol_json = {'volume': get_vol_info_by_qemu(params.get('current'))}
        vol_json = add_spec_in_volume(vol_json, 'current', params.get('current'))
        vol_json = add_spec_in_volume(vol_json, 'disk', name)
        vol_json = add_spec_in_volume(vol_json, 'pool', params.get('pool'))
        jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
        body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')    
        try:
            client.CustomObjectsApi().create_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=plural, body=body)
        except ApiException as e:
            if e.reason == 'Conflict':
                logger.debug('**The %s %s already exists, update it.' % (kind, name))
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=GROUP,
                                                                              version=VERSION,
                                                                              namespace='default',
                                                                              plural=plural,
                                                                              name=name)
                jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
                body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.') 
                client.CustomObjectsApi().replace_namespaced_custom_object(
                   group=GROUP, version=VERSION, namespace='default', plural=plural, name=name, body=body)
            else:
                logger.error(e)
                raise e  
    elif op == 'delete':
        try:
            refresh_pool(params.get('pool'))
            jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=GROUP,
                                                                              version=VERSION,
                                                                              namespace='default',
                                                                              plural=plural,
                                                                              name=name)
            #             vol_xml = get_volume_xml(pool, name)
            #             vol_json = toKubeJson(xmlToJson(vol_xml))
            jsondict = updateJsonRemoveLifecycle(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            client.CustomObjectsApi().replace_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=plural, name=name, body=body)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**%s %s already deleted.' % (kind, name))
            else:
                logger.error(e)
                raise e   
        except:
            logger.error('Oops! ', exc_info=1)
        try:
            client.CustomObjectsApi().delete_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=plural, name=name, body=V1DeleteOptions())
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**%s %s already deleted.' % (kind, name))
            else:
                logger.error(e)
                raise e        

def create_and_start_vm_from_iso(params):
    metadata_name = _get_param('--name', params)
    network_config = _get_param('--network', params)
    try:
        operation_queue = ['virsh dommemstat --period %s --domain %s --config --live' % (str(5), metadata_name)]
        config_dict = _network_config_parser(network_config)
        operation_queue.extend( _get_network_operations_queue("createAndStartVMFromISO", config_dict, metadata_name))
        _set_param('--network', 'none', params)
        cmd = _unpackCmd('virt-install', params)
        runCmd(cmd)
        if is_vm_exists(metadata_name) and not is_vm_active(metadata_name):
            create(metadata_name)
        _runOperationQueue(operation_queue)
    except Exception as e:
        try:
            if is_vm_exists(metadata_name) and is_vm_active(metadata_name):
                destroy(metadata_name)
                time.sleep(0.5)
        except:
            logger.error('Oops! ', exc_info=1)
        raise e

def delete_vm(params):
    jsonDict = {'spec': {}}
    metadata_name = _get_param('--domain', params)
    if is_vm_exists(metadata_name) and is_vm_active(metadata_name):
        destroy(metadata_name)
        time.sleep(1)
    cmd = _unpackCmd('virsh undefine', params)
    try:
        runCmd(cmd)
    except Exception as e:
        if not is_vm_exists(metadata_name):
            logger.debug('VM %s has already been deleted.' % metadata_name)
        else:
            raise BadRequest('Delete VM %s failed! Error: %s' %(metadata_name, e))
    helper = K8sHelper(VM_KIND)
    helper.delete(metadata_name)
    return
    
def plug_nic(params):
    the_cmd_key = 'plugNIC'
    metadata_name = _get_param('--domain', params)
    network_config = _get_params(params)
    logger.debug(network_config)
    config_dict = _network_config_parser_json(the_cmd_key, network_config)
    logger.debug(config_dict)
    operation_queue = _get_network_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)
    
def unplug_nic(params):
    the_cmd_key = 'unplugNIC'
    metadata_name = _get_param('--domain', params)
    network_config = _get_params(params)
    logger.debug(network_config)
    config_dict = _network_config_parser_json(the_cmd_key, network_config)
    logger.debug(config_dict)
    operation_queue = _get_network_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)
    
def plug_disk(params):
    the_cmd_key = 'plugDisk'
    metadata_name = _get_param('--domain', params)
    disk_config = _get_params(params)
    logger.debug(disk_config)
    config_dict = _disk_config_parser_json(the_cmd_key, disk_config)
    logger.debug(config_dict)
    operation_queue = _get_disk_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)
    
def unplug_disk(params):
    the_cmd_key = 'unplugDisk'
    metadata_name = _get_param('--domain', params)
    disk_config = _get_params(params)
    logger.debug(disk_config)
    config_dict = _disk_config_parser_json(the_cmd_key, disk_config)
    logger.debug(config_dict)
    operation_queue = _get_disk_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)

def set_boot_order(params):
    the_cmd_key = 'setBootOrder'
    metadata_name = _get_param('--domain', params)
    config_dict = _get_params(params)
    logger.debug(config_dict)
    operation_queue = _get_redefine_vm_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)
    
def set_vnc_password(params):
    the_cmd_key = 'setVncPassword'
    metadata_name = _get_param('--domain', params)
    config_dict = _get_params(params)
    logger.debug(config_dict)
    operation_queue = _get_graphic_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)

def unset_vnc_password(params):
    the_cmd_key = 'unsetVncPassword'
    metadata_name = _get_param('--domain', params)
    config_dict = _get_params(params)
    logger.debug(config_dict)
    operation_queue = _get_graphic_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)

def set_guest_password(params):
    the_cmd_key = 'setGuestPassword'
    metadata_name = _get_param('--domain', params)
    config_dict = _get_params(params)
    logger.debug(config_dict)
    operation_queue = _get_vm_password_operations_queue(the_cmd_key, config_dict, metadata_name)
    _runOperationQueue(operation_queue)  
    
def dumpxml(params):
    name = _get_param('--name', params)
    jsonDict = {'spec': {'domain': {}, 'nodeName': HOSTNAME, 'status': {}}}
    vm_xml = get_xml(name)
    vm_power_state = vm_state(name).get(name)
    vm_json = toKubeJson(xmlToJson(vm_xml))
#     pprint(loads(vm_json))
    vm_json = updateDomain(loads(vm_json))
    vm_json = updateJsonRemoveLifecycle(jsonDict, vm_json)
    jsonDict = addPowerStatusMessage(vm_json, vm_power_state, 'The VM is %s' % vm_power_state)
    print(jsonDict)
    
def dump_l3_network_info(params):
    name = _get_param('--name', params)
    jsonDict = {'spec': {'data': {}, 'nodeName': HOSTNAME, 'type': 'l3network', 'status': {}}}
    jsonDict['spec']['data'] = get_l3_network_info(name) 
    jsonDict = addPowerStatusMessage(jsonDict, 'Ready', 'The resource is ready.')   
    # print(jsonDict)
    print(json.dumps(jsonDict))
    
def dump_l3_address_info(params):
    name = _get_param('--name', params)
    jsonDict = {'spec': {'data': {}, 'nodeName': HOSTNAME, 'type': 'l3address', 'status': {}}}
    jsonDict['spec']['data'] = get_address_set_info(name) 
    jsonDict = addPowerStatusMessage(jsonDict, 'Ready', 'The resource is ready.')   
    print(jsonDict)
    
def dump_l2_network_info(params):
    name = _get_param('--name', params)
    jsonDict = {'spec': {'data': {}, 'nodeName': HOSTNAME, 'type': 'l2network', 'status': {}}}
    jsonDict['spec']['data'] = get_l2_network_info(name) 
    jsonDict = addPowerStatusMessage(jsonDict, 'Ready', 'The resource is ready.')   
    print(jsonDict)
    
def delete_network():
    jsonDict = {'spec': {}}
    print(jsonDict)
    
def _runOperationQueue(operation_queue, interval = 1, raise_it = True):
    for operation in operation_queue:
        logger.debug(operation)
        if operation and operation.find('kubeovn-adm unbind-swport') != -1:
            runCmd(operation, False)
        else:
            runCmd(operation, raise_it)
        time.sleep(interval)

def _unpackCmd(cmd, params):
    retv = '%s' %(cmd)
    for param in params:
        retv += ' %s' %(param)
    logger.debug(retv)
    return retv
    
def _createNICXml(metadata_name, data):   
    '''
    Write NIC Xml file to DEFAULT_DEVICE_DIR dir.
    '''
    doc = Document()
    root = doc.createElement('interface')
    root.setAttribute('type', 'bridge')
    doc.appendChild(root)
    bandwidth = {}
    for k, v in data.items():
        if k == 'mac':
            node = doc.createElement(k)
            node.setAttribute('address', v)
            root.appendChild(node)
        elif k == 'source':
            node = doc.createElement(k)
            node.setAttribute('bridge', v)
            root.appendChild(node)
        elif k == 'virtualport':
            node = doc.createElement(k)
            node.setAttribute('type', v)
            root.appendChild(node)
        elif k == 'model':
            node = doc.createElement(k)
            node.setAttribute('type', v)
            root.appendChild(node)
        elif k == 'target':
            node = doc.createElement(k)
            node.setAttribute('dev', v)
            root.appendChild(node)
        elif k == 'inbound':
            bandwidth[k] = v
        elif k == 'outbound':
            bandwidth[k] = v
    
    if bandwidth:        
        node_bandwidth = doc.createElement('bandwidth')
        for k,v in bandwidth.items():
            sub_node = doc.createElement(k)
            sub_node.setAttribute('average', v)
            node_bandwidth.appendChild(sub_node)
            root.appendChild(node_bandwidth)        
            
    '''
    If DEFAULT_DEVICE_DIR not exists, create it.
    '''
    if not os.path.exists(constants.KUBEVMM_VM_DEVICES_DIR):
        os.makedirs(constants.KUBEVMM_VM_DEVICES_DIR, 0o711)
    file_path = '%s/%s-nic-%s.xml' % (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, data.get('mac').replace(':', ''))
    try:
        with open(file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='\t'))
    except:
        raise BadRequest('Execute plugNIC error: cannot create NIC XML file \'%s\'' % file_path)  
    
    return file_path

def _createDiskXml(metadata_name, data):   
    '''
    Write disk Xml file to DEFAULT_DEVICE_DIR dir.
    '''
    doc = Document()
    root = doc.createElement('disk')
    root.setAttribute('type', 'file')
    root.setAttribute('device', data.get('type') if data.get('type') else 'disk')
    doc.appendChild(root)
    driver = {}
    iotune = {}
    for k, v in data.items():
        if k == 'driver':
            driver[k] = v
        elif k == 'subdriver':
            driver[k] = v
        elif k == 'source':
            node = doc.createElement(k)
            node.setAttribute('file', v)
            root.appendChild(node)
        elif k == 'mode':
            node = doc.createElement(v)
            root.appendChild(node)
        elif k == 'target':
            node = doc.createElement(k)
            node.setAttribute('dev', v)
            root.appendChild(node)
        elif k == 'read-bytes-sec':
            iotune[k] = v
        elif k == 'write-bytes-sec':
            iotune[k] = v
        elif k == 'read-iops-sec':
            iotune[k] = v
        elif k == 'write-iops-sec':
            iotune[k] = v
    
    if driver:        
        node = doc.createElement('driver')
        node.setAttribute('name', driver.get('driver') if driver.get('driver') else 'qemu')
        node.setAttribute('type', driver.get('subdriver') if driver.get('subdriver') else 'qcow2')
        root.appendChild(node)
    
    if iotune:        
        vm_iotune = doc.createElement('iotune')
        for k,v in iotune.items():
            sub_node = doc.createElement(k)
            text = doc.createTextNode(v)
            sub_node.appendChild(text)
            vm_iotune.appendChild(sub_node)
            root.appendChild(vm_iotune)      
            
    '''
    If DEFAULT_DEVICE_DIR not exists, create it.
    '''
    if not os.path.exists(constants.KUBEVMM_VM_DEVICES_DIR):
        os.makedirs(constants.KUBEVMM_VM_DEVICES_DIR, 0o711)
    file_path = '%s/%s-disk-%s.xml' % (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, data.get('target'))
    try:
        with open(file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='\t'))
    except:
        raise BadRequest('Execute plugDisk error: cannot create disk XML file \'%s\'' % file_path)  
    
    return file_path

def _createGraphicXml(metadata_name, data, unset_vnc_password=False):   
    '''
    Write disk Xml file to DEFAULT_DEVICE_DIR dir.
    '''
    doc = Document()
    root = doc.createElement('graphics')
    root.setAttribute('type', 'vnc')
    if not unset_vnc_password and data.get('password'):
        root.setAttribute('passwd', data.get('password'))
    doc.appendChild(root)
    node = doc.createElement('listen')
    node.setAttribute('type', 'address')
    node.setAttribute('address', '0.0.0.0')
    root.appendChild(node)
    
    '''
    If DEFAULT_DEVICE_DIR not exists, create it.
    '''
    if not os.path.exists(constants.KUBEVMM_VM_DEVICES_DIR):
        os.makedirs(constants.KUBEVMM_VM_DEVICES_DIR, 0o711)
    file_path = '%s/%s-graphic.xml' % (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name)
    try:
        with open(file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='\t'))
    except:
        raise BadRequest('Execute plugDisk error: cannot create disk XML file \'%s\'' % file_path)  
    
    return file_path

# def _validate_network_params(data): 
#     if data:
#         for key in data.keys():
#             if key not in ['type', 'source', 'inbound', 'outbound', 'mac', 'ip', 'switch']:
#                 return False
#     else:
#         return False
#     return True

def _network_config_parser(data):
    retv = {}
    if data:
        split_it = data.split(',')
        for i in split_it:
            i = i.strip()
            if i.find('=') != -1:
                (k, v) = i.split('=')
                retv[k] = v
    if retv:
        net_type = retv.get('type')
        if not net_type:
            raise BadRequest('Network config error: no "type" parameter.')
        else:
            if net_type not in ['bridge', 'l2bridge', 'l3bridge']:
                raise BadRequest('Network config error: unsupported network "type" %s.' % retv['type'])
        source = retv.get('source')
        if not source:
            raise BadRequest('Network config error: no "source" parameter.')
        if 'mac' not in retv.keys():
            retv['mac'] = randomMAC()
        '''
        Add default params.
        '''
        if net_type in ['l2bridge', 'l3bridge']:
            retv['virtualport'] = 'openvswitch'
        retv['model'] = 'virtio'
        retv['target'] = 'fe%s' % (retv['mac'].replace(':', '')[2:])
    else:
        raise BadRequest('Network config error: no parameters or in wrong format, plz check it!')
    return retv   

def _network_config_parser_json(the_cmd_key, data):
    retv = {}
    if data:
        retv = data.copy()
        if _isUnplugNIC(the_cmd_key):
            if not retv.get('mac'):
                raise BadRequest('Network config error: no "mac" parameter.')
            return retv
        source = data.get('source')
        if not source:
            raise BadRequest('Network config error: no "source" parameter.')
        split_it = source.split(',')
        for i in split_it:
            i = i.strip()
            if i.find('=') != -1:
                (k, v) = i.split('=')
                retv[k] = v
    if retv:
        net_type = retv.get('type')
        if not net_type:
            raise BadRequest('Network config error: no "type" parameter.')
        else:
            if net_type not in ['bridge', 'l2bridge', 'l3bridge']:
                raise BadRequest('Network config error: unsupported network "type" %s.' % retv['type'])
        if 'mac' not in retv.keys():
            retv['mac'] = randomMAC()
        '''
        Add default params.
        '''
        if net_type in ['l2bridge', 'l3bridge']:
            retv['virtualport'] = 'openvswitch'
        retv['model'] = 'virtio'
        retv['target'] = 'fe%s' % (retv['mac'].replace(':', '')[2:])
    else:
        raise BadRequest('Network config error: no parameters or in wrong format, plz check it!')
    return retv

def _disk_config_parser_json(the_cmd_key, data):
    retv = {}
    if data:
        retv = data.copy()
        if _isUnplugDisk(the_cmd_key):
            if not retv.get('target'):
                raise BadRequest('Disk config error: no "target" parameter.')
            return retv
        source = data.get('source')
        if not source:
            raise BadRequest('Disk config error: no "source" parameter.')
    if retv:
        if not retv.get('target'):
                raise BadRequest('Disk config error: no "target" parameter.')
    else:
        raise BadRequest('Disk config error: no parameters or in wrong format, plz check it!')
    return retv
    
def _get_network_operations_queue(the_cmd_key, config_dict, metadata_name):
    if _isInstallVMFromISO(the_cmd_key) or _isInstallVMFromImage(the_cmd_key) or _isPlugNIC(the_cmd_key):
        if _isPlugNIC(the_cmd_key):
            args = ''
            if config_dict.get('live'):
                args = args + '--live '
            if config_dict.get('config'):
                args = args + '--config '
            if config_dict.get('persistent'):
                args = args + '--persistent '
            if config_dict.get('current'):
                args = args + '--current '
            if config_dict.get('force'):
                args = args + '--force '
        else:
            args = '--live --config'
        if config_dict.get('type') == 'bridge':
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, args)
            return [plugNICCmd]
        elif config_dict.get('type') == 'l2bridge':
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, args)
            return [plugNICCmd]
        elif config_dict.get('type') == 'l3bridge':
            if not config_dict.get('switch'):
                raise BadRequest('Network config error: no "switch" parameter.')
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, args)
            if _isPlugNIC(the_cmd_key) and not is_vm_active(metadata_name):
                unbindSwPortCmd = ''
                bindSwPortCmd = ''
            else:
                unbindSwPortCmd = 'kubeovn-adm unbind-swport --mac %s' % (config_dict.get('mac'))
                bindSwPortCmd = 'kubeovn-adm bind-swport --mac %s --switch %s --ip %s' % (config_dict.get('mac'), config_dict.get('switch'), config_dict.get('ip') if config_dict.get('ip') else 'dynamic')
            recordSwitchToFileCmd = 'echo "switch=%s" > %s/%s-nic-%s.cfg' % \
            (config_dict.get('switch'), constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
            recordIpToFileCmd = 'echo "ip=%s" >> %s/%s-nic-%s.cfg' % \
            (config_dict.get('ip') if config_dict.get('ip') else 'dynamic', constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
    #         recordVxlanToFileCmd = 'echo "vxlan=%s" >> %s/%s-nic-%s.cfg' % \
    #         (config_dict.get('vxlan') if config_dict.get('vxlan') else '-1', DEFAULT_DEVICE_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
            return [plugNICCmd, unbindSwPortCmd, bindSwPortCmd, recordSwitchToFileCmd, recordIpToFileCmd]
    elif _isUnplugNIC(the_cmd_key):
        args = ''
        if config_dict.get('live'):
            args = args + '--live '
        if config_dict.get('config'):
            args = args + '--config '
        if config_dict.get('persistent'):
            args = args + '--persistent '
        if config_dict.get('current'):
            args = args + '--current '
        if config_dict.get('force'):
            args = args + '--force '
        unplugNICCmd = _unplugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, args)
        net_cfg_file_path = '%s/%s-nic-%s.cfg' % \
                                (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
        if os.path.exists(net_cfg_file_path):
            unbindSwPortCmd = 'kubeovn-adm unbind-swport --mac %s' % (config_dict.get('mac'))
            return [unbindSwPortCmd, unplugNICCmd]
        else:
            return [unplugNICCmd]
    else:
        return []
    
def _get_disk_operations_queue(the_cmd_key, config_dict, metadata_name):
    args = ''
    if config_dict.get('live'):
        args = args + '--live '
    if config_dict.get('config'):
        args = args + '--config '
    if config_dict.get('persistent'):
        args = args + '--persistent '
    if config_dict.get('current'):
        args = args + '--current '
    if config_dict.get('force'):
        args = args + '--force '
    if _isPlugDisk(the_cmd_key):
        plugDiskCmd = _plugDeviceFromXmlCmd(metadata_name, 'disk', config_dict, args)
        return [plugDiskCmd]
    elif _isUnplugDisk(the_cmd_key):
        unplugDiskCmd = _unplugDeviceFromXmlCmd(metadata_name, 'disk', config_dict, args)
        return [unplugDiskCmd]
    else:
        return []
    
def _get_graphic_operations_queue(the_cmd_key, config_dict, metadata_name):
    args = ''
    if config_dict.get('live'):
        args = args + '--live '
    if config_dict.get('config'):
        args = args + '--config '
    if config_dict.get('persistent'):
        args = args + '--persistent '
    if config_dict.get('current'):
        args = args + '--current '
    if config_dict.get('force'):
        args = args + '--force '
    if _isSetVncPassword(the_cmd_key):
        plugDiskCmd = _updateDeviceFromXmlCmd(metadata_name, 'graphic', config_dict, args)
        return [plugDiskCmd]
    elif _isUnsetVncPassword(the_cmd_key):
        unplugDiskCmd = _updateDeviceFromXmlCmd(metadata_name, 'graphic', config_dict, args, unset_vnc_password=True)
        return [unplugDiskCmd]
    else:
        return []
    
def _get_redefine_vm_operations_queue(the_cmd_key, config_dict, metadata_name):
    if _isSetBootOrder(the_cmd_key):
        cmds = _redefineVMFromXmlCmd(metadata_name, 'boot_order', config_dict)
        return cmds
    else:
        return []

def _get_vm_password_operations_queue(the_cmd_key, config_dict, metadata_name):
    if _isSetGuestPassword(the_cmd_key):
        os_type = config_dict.get('os_type')
        user = config_dict.get('user')
        password = config_dict.get('password')
        boot_disk_path = get_boot_disk_path(metadata_name)
        if not os_type or os_type not in ['linux', 'windows']:
            raise BadRequest('Wrong parameters "os_type" %s.' % os_type)
        if not user or not password:
            raise BadRequest('Wrong parameters "user" or "password".')
        if not boot_disk_path:
            raise BadRequest('Cannot get boot disk of domain %s' % metadata_name)
        if os_type == 'linux':
            cmd = 'kubesds-adm customize --add %s --user %s --password %s ' % (boot_disk_path, user, password)
        else:
            cmd = 'virsh set-user-password --domain %s --user %s --password %s' % (metadata_name, user, password)
        return [cmd]
    else:
        return []
    
def _get_paths_from_diskspec(diskspec):
    paths = ''
    str_list = diskspec.split('=')
    for i in str_list:
        if i.startswith('/'):
            paths = paths + i.split(',')[0] + ' '
    return paths

# def _get_snapshot_operations_queue(jsondict, the_cmd_key, domain, metadata_name):
#     if _isCreateSnapshot(the_cmd_key):
#         jsondict = _del_field(jsondict, the_cmd_key, 'isExternal')
#         disk_spec = _get_field(jsondict, the_cmd_key, 'diskspec')
#         if not disk_spec:
#             raise BadRequest('Missing parameter "diskspec".')
#         jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
#         cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#         snapshot_paths = _get_paths_from_diskspec(disk_spec)
#         cmd1 = 'kubesds-adm updateDiskCurrent --type dir --current %s' % snapshot_paths
#         return ([cmd, cmd1], [])
#     elif _isMergeSnapshot(the_cmd_key):
#         domain_obj = Domain(_get_dom(domain))
#         (merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.merge_snapshot(metadata_name)
#         return ([merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd], [])
#     elif _isRevertVirtualMachine(the_cmd_key):
#         domain_obj = Domain(_get_dom(domain))
# #         (merge_snapshots_cmd, _, _) = domain_obj.merge_snapshot(metadata_name)
#         (unplug_disks_cmd, unplug_disks_rollback_cmd, plug_disks_cmd, plug_disks_rollback_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.revert_snapshot(metadata_name)
#         return ([unplug_disks_cmd, plug_disks_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd], [unplug_disks_rollback_cmd, plug_disks_rollback_cmd])
#     elif _isDeleteVMSnapshot(the_cmd_key):
#         domain_obj = Domain(_get_dom(domain))
#         (unplug_disks_cmd, unplug_disks_rollback_cmd, plug_disks_cmd, plug_disks_rollback_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.revert_snapshot(metadata_name, True)
#         return ([unplug_disks_cmd, plug_disks_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd], [unplug_disks_rollback_cmd, plug_disks_rollback_cmd])
#     else:
#         return ([], [])
    
# def _get_vmdi_operations_queue(jsondict, the_cmd_key, target, metadata_name):
#     operation_queue = []
#     rollback_operation_queue = []
# #     if _isConvertDiskToDiskImage(the_cmd_key) or _isCreateVmdi(the_cmd_key):
# # #         (operation_queue, rollback_operation_queue) = createVmdi(metadata_name, target)
# #         jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
# #         cmd = unpackCmdFromJson(jsondict, the_cmd_key)
# #         operation_queue.append(cmd)
# #         return (operation_queue, rollback_operation_queue)
#     if _isDeleteVmdi(the_cmd_key):
# #         (operation_queue, rollback_operation_queue) = deleteVmdi(metadata_name, target)
#         jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
#         cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#         operation_queue.append(cmd)
#     else:
#         return (operation_queue, rollback_operation_queue)
#     
# def _get_vmi_operations_queue(jsondict, the_cmd_key, target, metadata_name):
#     operation_queue = []
#     rollback_operation_queue = []
#     if _isConvertVMToImage(the_cmd_key) or _isCreateImage(the_cmd_key):
#         (operation_queue, rollback_operation_queue) = createVmi(metadata_name, target)
#         jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
#         cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#         operation_queue.append(cmd)
#         return (operation_queue, rollback_operation_queue)
#     elif _isDeleteImage(the_cmd_key):
#         (operation_queue, rollback_operation_queue) = deleteVmi(metadata_name, target)
#         jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
#         cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#         operation_queue.append(cmd)
#     else:
#         return (operation_queue, rollback_operation_queue)

def _plugDeviceFromXmlCmd(metadata_name, device_type, data, args):
    if device_type == 'nic':
        file_path = _createNICXml(metadata_name, data)
    elif device_type == 'disk':
        file_path = _createDiskXml(metadata_name, data)
    return 'virsh attach-device --domain %s --file %s %s' % (metadata_name, file_path, args)

def _updateDeviceFromXmlCmd(metadata_name, device_type, data, args, unset_vnc_password=False):
    if device_type == 'graphic':
        file_path = _createGraphicXml(metadata_name, data, unset_vnc_password)
    return 'virsh update-device --domain %s --file %s %s' % (metadata_name, file_path, args)

def _redefineVMFromXmlCmd(metadata_name, resource_type, data):
    if resource_type == 'boot_order':
        boot_order = data.get('order')
        if not boot_order:
            raise BadRequest('Missing parameter "order".')
        orders = boot_order.replace(' ', '').split(',')
        if not orders:
            raise BadRequest('Unsupported parameter "order=%s".' % boot_order)
        for order in orders:
            if not runCmd('virsh domblklist %s | grep %s' % (metadata_name, order)):
                raise BadRequest('Virtual machine %s has no device named "%s".' % (metadata_name, order))
        cmds = []
        cmd1 = 'virsh dumpxml %s > /tmp/%s.xml' % (metadata_name, metadata_name)
        cmd2 = 'sed -i \'/<os>/n;/<boot /{:a;d;n;/<os\/>/!ba}\' /tmp/%s.xml' %(metadata_name)
        cmd3 = 'sed -i \'/<domain /n;/<boot order=/{:a;d;n;/<\/domain>/!ba}\' /tmp/%s.xml' %(metadata_name)
        cmds.append(cmd1)
        cmds.append(cmd2)
        cmds.append(cmd3)
        i = 1
        for order in orders:
            cmds.append("sed -i \'/<devices>/n;/<target dev='\\''%s'\\''/a\      <boot order='\\''%d'\\''\/>\' /tmp/%s.xml" % (order, i, metadata_name))
            i = i+1
        cmds.append('virsh define --file /tmp/%s.xml' % (metadata_name))
        return cmds
    else:
        return []

def _unplugDeviceFromXmlCmd(metadata_name, device_type, data, args):
    if device_type == 'nic':
        file_path = '%s/%s-nic-%s.xml' % (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, data.get('mac').replace(':', ''))
        if not os.path.exists(file_path):
            if data.get('type') in ['bridge', 'l2bridge', 'l3bridge']:
                net_type = 'bridge'
            else:
                net_type = data.get('type')
            return 'virsh detach-interface --domain %s --type %s --mac %s %s' (metadata_name, net_type, data.get('mac'), args)
    elif device_type == 'disk':
        file_path = '%s/%s-disk-%s.xml' % (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, data.get('target'))
        if not os.path.exists(file_path):
            return 'virsh detach-disk --domain %s --target %s %s' % (metadata_name, data.get('target'), args)
    return 'virsh detach-device --domain %s --file %s %s' % (metadata_name, file_path, args)

def _createNICFromXml(metadata_name, jsondict, the_cmd_key):
    spec = jsondict['raw_object'].get('spec')
    lifecycle = spec.get('lifecycle')
    if not lifecycle:
        return
    '''
    Read parameters from lifecycle, add default value to some parameters.
    '''
    mac = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('mac')
    source = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('source')
    model = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('model')
#     target = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('target')
    if not source:
        raise BadRequest('Execute plugNIC error: missing parameter "source"!')
    if not mac:
        mac = randomMAC()
    if not model:
        model = 'virtio'
    lines = {}
    lines['mac'] = mac
    lines['source'] = source
    lines['virtualport'] = 'openvswitch'
    lines['model'] = model
    lines['target'] = '%s' % (mac.replace(':', ''))
    
    file_path = _createNICXml(metadata_name, lines)

    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]
    new_cmd_key = 'plugDevice'
    jsondict['raw_object']['spec']['lifecycle'][new_cmd_key] = {'file': file_path}
    return(jsondict, new_cmd_key, file_path)

def _deleteNICFromXml(metadata_name, jsondict, the_cmd_key):
    spec = jsondict['raw_object'].get('spec')
    lifecycle = spec.get('lifecycle')
    if not lifecycle:
        return
    '''
    Read parameters from lifecycle, add default value to some parameters.
    '''
    mac = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('mac')
    if not mac:
        raise BadRequest('Execute plugNIC error: missing parameter "mac"!')
    
    file_path = '%s/%s-nic-%s.xml' % (constants.KUBEVMM_VM_DEVICES_DIR, metadata_name, mac.replace(':', ''))
    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]
    new_cmd_key = 'unplugDevice'
    jsondict['raw_object']['spec']['lifecycle'][new_cmd_key] = {'file': file_path}
    return (jsondict, new_cmd_key, file_path)

def mvNICXmlToTmpDir(file_path):
    if file_path:
        runCmd('mv -f %s /tmp' % file_path)

def _isInstallVMFromISO(the_cmd_key):
    if the_cmd_key == "createAndStartVMFromISO":
        return True
    return False

def _isCreateSwitch(the_cmd_key):
    if the_cmd_key == "createSwitch":
        return True
    return False

def _isDeleteSwPort(the_cmd_key):
    if the_cmd_key == "deleteSwPort":
        return True
    return False   

def _isMergeSnapshot(the_cmd_key):
    if the_cmd_key == "mergeSnapshot":
        return True
    return False

def _isRevertVirtualMachine(the_cmd_key):
    if the_cmd_key == "revertVirtualMachine":
        return True
    return False

def _isCreateDiskExternalSnapshot(the_cmd_key):
    if the_cmd_key == "createDiskExternalSnapshot":
        return True
    return False

def _isDeleteVM(the_cmd_key):
    if the_cmd_key == "deleteVM":
        return True
    return False

def _isDeleteVMImage(the_cmd_key):
    if the_cmd_key == "deleteImage":
        return True
    return False

def _isDeleteVMSnapshot(the_cmd_key):
    if the_cmd_key == "deleteSnapshot":
        return True
    return False

def _isDeleteDisk(the_cmd_key):
    if the_cmd_key == "deleteDisk":
        return True
    return False

def _isDeleteDiskExternalSnapshot(the_cmd_key):
    if the_cmd_key == "deleteDiskExternalSnapshot":
        return True
    return False

def _isDeletePool(the_cmd_key):
    if the_cmd_key == "deletePool":
        return True
    return False

def _isDeleteDiskImage(the_cmd_key):
    if the_cmd_key == "deleteDiskImage":
        return True
    return False

def _isDeleteNetwork(the_cmd_key):
    if the_cmd_key == "deleteSwitch":
        return True
    return False

def _isDeleteBridge(the_cmd_key):
    if the_cmd_key == "deleteBridge":
        return True
    return False

def _isDeleteAddress(the_cmd_key):
    if the_cmd_key == "deleteAddress":
        return True
    return False

def _isSetVncPassword(the_cmd_key):
    if the_cmd_key == "setVncPassword":
        return True
    return False

def _isUnsetVncPassword(the_cmd_key):
    if the_cmd_key == "unsetVncPassword":
        return True
    return False

def _isSetBootOrder(the_cmd_key):
    if the_cmd_key == "setBootOrder":
        return True
    return False

def _isSetGuestPassword(the_cmd_key):
    if the_cmd_key == "setGuestPassword":
        return True
    return False

def _isPlugNIC(the_cmd_key):
    if the_cmd_key == "plugNIC":
        return True
    return False

def _isUnplugNIC(the_cmd_key):
    if the_cmd_key == "unplugNIC":
        return True
    return False

def _isPlugDisk(the_cmd_key):
    if the_cmd_key == "plugDisk":
        return True
    return False

def _isRevertDiskExternalSnapshot(the_cmd_key):
    if the_cmd_key == "revertDiskExternalSnapshot":
        return True
    return False

def _isUnplugDisk(the_cmd_key):
    if the_cmd_key == "unplugDisk":
        return True
    return False

def _isPlugDevice(the_cmd_key):
    if the_cmd_key == "plugDevice":
        return True
    return False

def _isUnplugDevice(the_cmd_key):
    if the_cmd_key == "unplugDevice":
        return True
    return False

def _isInstallVMFromImage(the_cmd_key):
    if the_cmd_key == "createAndStartVMFromImage":
        return True
    return False

def _isCreateImage(the_cmd_key):
    if the_cmd_key == "createImage":
        return True
    return False

def _isCreateVmdi(the_cmd_key):
    if the_cmd_key == "createDiskImage":
        return True
    return False

def _isCreateSnapshot(the_cmd_key):
    if the_cmd_key == "createSnapshot":
        return True
    return False

def _isCreateDiskImageFromDisk(the_cmd_key):
    if the_cmd_key == "createDiskImageFromDisk":
        return True
    return False

def _isConvertVMToImage(the_cmd_key):
    if the_cmd_key == "convertVMToImage":
        return True
    return False

def _isCreateDiskFromDiskImage(the_cmd_key):
    if the_cmd_key == "createDiskFromDiskImage":
        return True
    return False

def _isDeleteVmdi(the_cmd_key):
    if the_cmd_key == "deleteDiskImage":
        return True
    return False

def _isDeleteImage(the_cmd_key):
    if the_cmd_key == "deleteImage":
        return True
    return False

def _isCloneDisk(the_cmd_key):
    if the_cmd_key == "cloneDisk":
        return True
    return False

def _isResizeDisk(the_cmd_key):
    if the_cmd_key == "resizeDisk":
        return True
    return False

def main():
    help_msg = 'Usage: %s <create_disk_from_vmdi|create_disk_from_vmdi|create_vmdi|delete_vmdi|update-os|create_and_start_vm_from_iso \
    |delete_vm|plug_nic|unplug_nic|plug_disk|unplug_disk|set_boot_order|set_vnc_password|unset_vnc_password \
    |set_guest_password|dumpxml|dump_l3_network_info|dump_l3_address_info|dump_l2_network_info|delete_network \
    |--help>' % sys.argv[0]
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print(help_msg)
        sys.exit(1)
 
    params = sys.argv[2:]
    
    
#     if sys.argv[1] == 'create_vm_image_from_vm':
#         create_vm_image_from_vm(params['--name'], params['--domain'], params['--targetPool'])
#     elif sys.argv[1] == 'convert_image_to_vm':
#         convert_image_to_vm(params['--name'])
    if sys.argv[1] == 'create_vmdi_from_disk':
        create_vmdi_from_disk(params)
    elif sys.argv[1] == 'create_disk_from_vmdi':
        create_disk_from_vmdi(params)
#     elif sys.argv[1] == 'create_disk_snapshot':
#         create_disk_snapshot(params)
#     elif sys.argv[1] == 'delete_disk_snapshot':
#         delete_disk_snapshot(params)
#     elif sys.argv[1] == 'revert_disk_internal_snapshot':
#         revert_disk_internal_snapshot(params)
#     elif sys.argv[1] == 'revert_disk_external_snapshot':
#         revert_disk_external_snapshot(params)
#     elif sys.argv[1] == 'delete_image':
#         delete_image(params['--name'])
    elif sys.argv[1] == 'create_vmdi':
        create_vmdi(params)
    elif sys.argv[1] == 'delete_vmdi':
        delete_vmdi(params)
    elif sys.argv[1] == 'update-os':
        updateOS(params)
    elif sys.argv[1] == 'create_and_start_vm_from_iso':
        create_and_start_vm_from_iso(params)
    elif sys.argv[1] == 'delete_vm':
        delete_vm(params)
    elif sys.argv[1] == 'plug_nic':
        plug_nic(params)
    elif sys.argv[1] == 'unplug_nic':
        unplug_nic(params)
    elif sys.argv[1] == 'plug_disk':
        plug_disk(params)
    elif sys.argv[1] == 'unplug_disk':
        unplug_disk(params)
    elif sys.argv[1] == 'unplug_disk':
        unplug_disk(params)
    elif sys.argv[1] == 'set_boot_order':
        set_boot_order(params)
    elif sys.argv[1] == 'set_vnc_password':
        set_vnc_password(params)
    elif sys.argv[1] == 'unset_vnc_password':
        unset_vnc_password(params)
    elif sys.argv[1] == 'set_guest_password':
        set_guest_password(params)
    elif sys.argv[1] == 'dumpxml':
        dumpxml(params)
    elif sys.argv[1] == 'dump_l3_network_info':
        dump_l3_network_info(params)
    elif sys.argv[1] == 'dump_l3_address_info':
        dump_l3_address_info(params)
    elif sys.argv[1] == 'dump_l2_network_info':
        dump_l2_network_info(params)
    elif sys.argv[1] == 'delete_network':
        delete_network(params)
    elif sys.argv[1] == 'create_disk':
        create_disk(params)
    elif sys.argv[1] == 'create_pool':
        create_pool(params)
    elif sys.argv[1] == 'delete_disk':
        delete_disk(params)
    elif sys.argv[1] == 'delete_pool':
        delete_pool(params)
    else:
        print ('invalid argument!')
        print (help_msg)
        sys.exit(1)

if __name__ == '__main__':
    config.load_kube_config(config_file="/root/.kube/config")
    main()
    pass
