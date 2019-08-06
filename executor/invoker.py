'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''

'''
Import python libs
'''
import os
import sys
import subprocess
import ConfigParser
import socket
import string
import traceback
from datetime import datetime
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
from utils.libvirt_util import get_volume_xml, undefine_with_snapshot, destroy, undefine, create, setmem, setvcpus, is_vm_active, is_vm_exists, is_volume_exists, is_snapshot_exists
from utils import logger
from utils.uit_utils import is_block_dev_exists
from utils.utils import ExecuteException, updateJsonRemoveLifecycle, addPowerStatusMessage, addExceptionMessage, report_failure, deleteLifecycleInJson, randomUUID, now_to_timestamp, now_to_datetime, now_to_micro_time, get_hostname_in_lower_case, UserDefinedEvent

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
FORCE_SHUTDOWN_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'stopVMForce')
RESET_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'resetVM')

DEFAULT_STORAGE_DIR = config_raw.get('DefaultStorageDir', 'default')

LABEL = 'host=%s' % (get_hostname_in_lower_case())

TIMEOUT = config_raw.get('WatcherTimeout', 'timeout')

LOG = '/var/log/virtctl.log'

logger = logger.set_logger(os.path.basename(__file__), LOG)

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
    logger.debug("------------------------Welcome to Virtlet Daemon.-------------------------------")
    logger.debug("------Copyright (2019, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn,liuhe18@otcaix.iscas.ac.cn----------")
    logger.debug("--------------------------------wuheng@otcaix.iscas.ac.cn------------------------")
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
        
def vMWatcher(group=GROUP_VM, version=VERSION_VM, plural=PLURAL_VM):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=group, version=version, plural=plural, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        the_cmd_key = _getCmdKey(jsondict)
        logger.debug('cmd key is: %s' % the_cmd_key)
        if the_cmd_key and operation_type != 'DELETED':
            involved_object_name = metadata_name
            involved_object_kind = 'VirtualMachine'
            event_metadata_name = randomUUID()
            event_type = 'Normal'
            status = 'Doing(Success)'
            reporter = 'virtctl'
            event_id = _getEventId(jsondict)
            time_now = now_to_datetime()
            time_start = time_now
            time_end = time_now
            message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
            event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
            try:
                event.registerKubernetesEvent()
            except:
                logger.error('Oops! ', exc_info=1)
            jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
            if _isInstallVMFromImage(the_cmd_key):
                template_path = _get_field(jsondict, the_cmd_key, 'cdrom')
                if not os.path.exists(template_path):
                    raise ExecuteException('VirtctlError', "Template file %s not exists, cannot copy from it!" % template_path)
                new_vm_path = '%s/%s.qcow2' % (DEFAULT_STORAGE_DIR, metadata_name)
                runCmd('cp %s %s' %(template_path, new_vm_path))
                jsondict = _updateRootDiskInJson(jsondict, the_cmd_key, new_vm_path)                
            cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
#             body = jsondict['raw_object']
#             jsondict1 = client.CustomObjectsApi().get_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name)
#             logger.debug(jsondict1)
#             logger.debug(body)
#             try:
#                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
#             except:
#                 logger.error('Oops! ', exc_info=1)
            try:
        #             print(jsondict)
                if operation_type == 'ADDED':
                    if _isInstallVMFromISO(the_cmd_key):
                        if cmd:
                            runCmd(cmd)
                        if is_vm_exists(metadata_name) and not is_vm_active(metadata_name):
                            create(metadata_name)
                    elif _isInstallVMFromImage(the_cmd_key):
                        if cmd: 
                            runCmd(cmd)
                        if is_vm_exists(metadata_name) and not is_vm_active(metadata_name):
                            create(metadata_name)
                    else:
                        if cmd:
                            runCmd(cmd)
                elif operation_type == 'MODIFIED':
                    if is_vm_exists(metadata_name):
                        if _isDeleteVM(the_cmd_key):
                            if is_vm_active(metadata_name):
                                destroy(metadata_name)   
                            if cmd:
                                runCmd(cmd)  
                        # add support python file real path to exec
                        else:
                            if cmd:
                                runCmd(cmd)
                elif operation_type == 'DELETED':
                    logger.debug('Delete custom object by client.')
#                     if is_vm_exists(metadata_name):
#                         if is_vm_active(metadata_name):
#                             destroy(metadata_name)
#                         cmd = unpackCmdFromJson(jsondict)
#                         if cmd:
#                             runCmd(cmd)
                status = 'Done(Success)'
            except libvirtError:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            except ExecuteException, e:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)         
            except:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            finally:
                if the_cmd_key and operation_type != 'DELETED':
                    time_end = now_to_datetime()
                    message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                    event.set_message(message)
                    event.set_time_end(time_end)
                    try:
                        event.updateKubernetesEvent()
                    except:
                        logger.error('Oops! ', exc_info=1)
                
def vMDiskWatcher(group=GROUP_VM_DISK, version=VERSION_VM_DISK, plural=PLURAL_VM_DISK):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        the_cmd_key = _getCmdKey(jsondict)
        logger.debug('cmd key is: %s' % the_cmd_key)
        if the_cmd_key and operation_type != 'DELETED':
            involved_object_name = metadata_name
            involved_object_kind = 'VirtualMachineDisk'
            event_metadata_name = randomUUID()
            event_type = 'Normal'
            status = 'Doing(Success)'
            reporter = 'virtctl'
            event_id = _getEventId(jsondict)
            time_now = now_to_datetime()
            time_start = time_now
            time_end = time_now
            message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
            event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
            try:
                event.registerKubernetesEvent()
            except:
                logger.error('Oops! ', exc_info=1)
            pool_name = _get_field(jsondict, the_cmd_key, 'pool')
            jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
            cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
#             body = jsondict['raw_object']
#             try:
#                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
#             except:
#                 logger.error('Oops! ', exc_info=1)
            try:
                if operation_type == 'ADDED':
                    if cmd:
                        runCmd(cmd)
                elif operation_type == 'MODIFIED':
                    if pool_name and is_volume_exists(metadata_name, pool_name):
                        if cmd: 
                            runCmd(cmd)
                        if _isCloneDisk(the_cmd_key) or _isResizeDisk(the_cmd_key):
                            vol_xml = get_volume_xml(pool_name, metadata_name)
                            vol_json = toKubeJson(xmlToJson(vol_xml))
                            vol_json = updateJsonRemoveLifecycle(jsondict, loads(vol_json))
                            body = addPowerStatusMessage(vol_json, 'Ready', 'The resource is ready.')
                            _reportResutToVirtlet(metadata_name, body, group, version, plural)
                    else:
                        raise ExecuteException('VirtctlError', 'No vol %s in pool %s!' % (metadata_name, pool_name))
                elif operation_type == 'DELETED':
                    if pool_name and is_volume_exists(metadata_name, pool_name):
                        if cmd: 
                            runCmd(cmd)   
                    else:
                        raise ExecuteException('VirtctlError', 'No vol %s in pool %s!' % (metadata_name, pool_name))
                status = 'Done(Success)'
            except libvirtError:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            except ExecuteException, e:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)    
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)          
            except:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            finally:
                if the_cmd_key and operation_type != 'DELETED':
                    time_end = now_to_datetime()
                    message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                    event.set_message(message)
                    event.set_time_end(time_end)
                    try:
                        event.updateKubernetesEvent()
                    except:
                        logger.error('Oops! ', exc_info=1)
                
def vMImageWatcher(group=GROUP_VMI, version=VERSION_VMI, plural=PLURAL_VMI):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=group, version=version, plural=plural, **kwargs):
        # logger.debug(jsondict)
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        the_cmd_key = _getCmdKey(jsondict)
        logger.debug('cmd key is: %s' % the_cmd_key)
        if the_cmd_key and operation_type != 'DELETED':
            involved_object_name = metadata_name
            involved_object_kind = 'VirtualMachineImage'
            event_metadata_name = randomUUID()
            event_type = 'Normal'
            status = 'Doing(Success)'
            reporter = 'virtctl'
            event_id = _getEventId(jsondict)
            time_now = now_to_datetime()
            time_start = time_now
            time_end = time_now
            message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
            event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
            try:
                event.registerKubernetesEvent()
            except:
                logger.error('Oops! ', exc_info=1)
            jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
            if _isCreateImage(the_cmd_key):
                jsondict = addDefaultSettings(jsondict, the_cmd_key)
            cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
#             body = jsondict['raw_object']
#             try:
#                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
#             except:
#                 logger.error('Oops! ', exc_info=1)
            try:
                if operation_type == 'ADDED':
                    if _isCreateImage(the_cmd_key):
                        if cmd:
                            runCmd(cmd)
                        if is_vm_exists(metadata_name):
                            if is_vm_active(metadata_name):
                                destroy(metadata_name)
                            runCmd('/usr/bin/vmm convert_vm_to_image --name %s' % metadata_name)
                    else:
                        if cmd:
                            runCmd(cmd)
                elif operation_type == 'MODIFIED':
                    if cmd:
                        runCmd(cmd)
                elif operation_type == 'DELETED':
                    if is_vm_active(metadata_name):
                        destroy(metadata_name)
                    if cmd:
                        runCmd(cmd)
                status = 'Done(Success)'
            except libvirtError:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type) 
            except ExecuteException, e:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)    
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)          
            except:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            finally:
                if the_cmd_key and operation_type != 'DELETED':
                    time_end = now_to_datetime()
                    message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                    event.set_message(message)
                    event.set_time_end(time_end)
                    try:
                        event.updateKubernetesEvent()
                    except:
                        logger.error('Oops! ', exc_info=1)
        
def vMSnapshotWatcher(group=GROUP_VM_SNAPSHOT, version=VERSION_VM_SNAPSHOT, plural=PLURAL_VM_SNAPSHOT):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=group, version=version, plural=plural, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        the_cmd_key = _getCmdKey(jsondict)
        logger.debug('cmd key is: %s' % the_cmd_key)
        if the_cmd_key and operation_type != 'DELETED':
            involved_object_name = metadata_name
            involved_object_kind = 'VirtualMachineSnapshot'
            event_metadata_name = randomUUID()
            event_type = 'Normal'
            status = 'Doing(Success)'
            reporter = 'virtctl'
            event_id = _getEventId(jsondict)
            time_now = now_to_datetime()
            time_start = time_now
            time_end = time_now
            message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
            event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
            try:
                event.registerKubernetesEvent()
            except:
                logger.error('Oops! ', exc_info=1)
            vm_name = _get_field(jsondict, the_cmd_key, 'domain')
            jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
            cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
#             body = jsondict['raw_object']
#             try:
#                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
#             except:
#                 logger.error('Oops! ', exc_info=1)
            try:
                if operation_type == 'ADDED':
                    if cmd:
                        runCmd(cmd)
                elif operation_type == 'MODIFIED':
                    if vm_name and is_snapshot_exists(metadata_name, vm_name):
                        if cmd: 
                            runCmd(cmd)
                elif operation_type == 'DELETED':
                    if vm_name and is_snapshot_exists(metadata_name, vm_name):
                        if cmd: 
                            runCmd(cmd)  
                status = 'Done(Success)'
            except libvirtError:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type) 
            except ExecuteException, e:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)    
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)           
            except:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            finally:
                if the_cmd_key and operation_type != 'DELETED':
                    time_end = now_to_datetime()
                    message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                    event.set_message(message)
                    event.set_time_end(time_end)
                    try:
                        event.updateKubernetesEvent()
                    except:
                        logger.error('Oops! ', exc_info=1)

def vMBlockDevWatcher(group=GROUP_BLOCK_DEV_UIT, version=VERSION_BLOCK_DEV_UIT, plural=PLURAL_BLOCK_DEV_UIT):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        operation_type = jsondict.get('type')
        logger.debug(operation_type)
        metadata_name = getMetadataName(jsondict)
        logger.debug('metadata name: %s' % metadata_name)
        the_cmd_key = _getCmdKey(jsondict)
        logger.debug('cmd key is: %s' % the_cmd_key)
        if the_cmd_key and operation_type != 'DELETED':
            involved_object_name = metadata_name
            involved_object_kind = 'VirtualMachineBlockDev'
            event_metadata_name = randomUUID()
            event_type = 'Normal'
            status = 'Doing(Success)'
            reporter = 'virtctl'
            event_id = _getEventId(jsondict)
            time_now = now_to_datetime()
            time_start = time_now
            time_end = time_now
            message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
            event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
            try:
                event.registerKubernetesEvent()
            except:
                logger.error('Oops! ', exc_info=1)
            jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
            cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
#             body = jsondict['raw_object']
#             try:
#                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
#             except:
#                 logger.error('Oops! ', exc_info=1)
            try:
                if operation_type == 'ADDED':
                    if cmd:
                        runCmd(cmd)
                elif operation_type == 'MODIFIED':
                    if is_block_dev_exists('/dev/%s/%s' % (metadata_name, metadata_name)):
                        if cmd: 
                            runCmd(cmd)
                elif operation_type == 'DELETED':
                    if is_block_dev_exists('/dev/%s/%s' % (metadata_name, metadata_name)):
                        if cmd: 
                            runCmd(cmd)   
                status = 'Done(Success)'
            except libvirtError:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            except ExecuteException, e:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)    
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)          
            except:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                except:
                    logger.error('Oops! ', exc_info=1)
                status = 'Done(Error)'
                event_type = 'Warning' 
                event.set_event_type(event_type)
            finally:
                if the_cmd_key and operation_type != 'DELETED':
                    time_end = now_to_datetime()
                    message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventid:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                    event.set_message(message)
                    event.set_time_end(time_end)
                    try:
                        event.updateKubernetesEvent()
                    except:
                        logger.error('Oops! ', exc_info=1)

def getMetadataName(jsondict):
    metadata = jsondict['raw_object']['metadata']
    metadata_name = metadata.get('name')
    if metadata_name:
        return metadata_name
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No metadata name!') 

def forceUsingMetadataName(metadata_name, the_cmd_key, jsondict):
    spec = jsondict['raw_object']['spec']
    lifecycle = spec.get('lifecycle')
    if the_cmd_key in ALL_SUPPORT_CMDS_WITH_NAME_FIELD:
        lifecycle[the_cmd_key]['name'] = metadata_name    
    elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_DOMAIN_FIELD:
        lifecycle[the_cmd_key]['domain'] = metadata_name
    elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_VOL_FIELD:
        lifecycle[the_cmd_key]['vol'] = metadata_name
    elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_SNAPNAME_FIELD:
        lifecycle[the_cmd_key]['snapshotname'] = metadata_name
    return jsondict

def _injectEventIntoLifecycle(jsondict, eventdict):
    if jsondict:
        spec = jsondict['raw_object']['spec']
#         metadata = jsondict['raw_object']['metadata']
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                spec['lifecycle']['event'] = eventdict
#         if metadata:
#             resource_version = metadata.get('resourceVersion')
#             if resource_version:
#                 del metadata['resourceVersion']
    return jsondict

def _reportResutToVirtlet(metadata_name, body, group, version, plural):
    body = body.get('raw_object')
    try:
        client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
    except:
        logger.error('Oops! ', exc_info=1)

'''
Install VM from ISO.
'''
def _isInstallVMFromISO(the_cmd_key):
    if the_cmd_key == "createAndStartVMFromISO":
        return True
    return False

def _isDeleteVM(the_cmd_key):
    if the_cmd_key == "deleteVM":
        return True
    return False

'''
Get event id.
'''
def _getEventId(jsondict):
    metadata = jsondict['raw_object'].get('metadata')
    labels = metadata.get('labels')
    logger.debug(labels)
    return labels.get('eventid') if labels.get('eventid') else '-1'

'''
Get the CMD key.
'''
def _getCmdKey(jsondict):
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return None
        the_cmd_keys = []
        keys = lifecycle.keys()
        for key in keys:
            if key in ALL_SUPPORT_CMDS.keys():
                '''
                Priority 1st -- Force shutdown out of control VM.
                '''
                if key == FORCE_SHUTDOWN_VM:
                    the_cmd_keys.insert(0, key)
                    break;
                elif key == RESET_VM:
                    the_cmd_keys.insert(0, key)
                    break;
                else:
                    the_cmd_keys.append(key)
    return the_cmd_keys[0] if the_cmd_keys else None

'''
Install VM from image.
'''
def _isInstallVMFromImage(the_cmd_key):
    if the_cmd_key == "createAndStartVMFromImage":
        return True
    return False

def _isCreateImage(the_cmd_key):
    if the_cmd_key == "createImage":
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
    
def _get_field(jsondict, the_cmd_key, field):
    retv = None
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return None
        if the_cmd_key:
            contents = lifecycle.get(the_cmd_key)
            for k, v in contents.items():
                if k == field:
                    retv = v
    return retv    
        
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

def addDefaultSettings(jsondict, the_cmd_key):
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['virt_type'] = "kvm"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['memory'] = "1024"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['vcpus'] = "1"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['graphics'] = "vnc,listen=0.0.0.0"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['network'] = "default"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['os_variant'] = "rhel7"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['noautoconsole'] = "True"
        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['boot'] = "hd"
        logger.debug(jsondict)
        return jsondict    
        

def _updateRootDiskInJson(jsondict, the_cmd_key, new_vm_path):
    '''
    Get target VM name from Json.
    '''
    spec = jsondict['raw_object'].get('spec')
    if spec:
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return
        if the_cmd_key:
            contents = lifecycle.get(the_cmd_key)
            if contents:
                for k, v in contents.items():
                    if k == "disk":
                        tmp = v.replace('ROOTDISK', new_vm_path)
                        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k] = tmp
                    elif k == 'cdrom':
                        del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k]
                    else:
                        continue
    return jsondict    

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
    elif value == 'False':
        return ('', '')
    else:
        return ('--%s' % key.replace('_', '-'), value)
   

'''
Unpack the CMD that will be executed in Json format.
'''
def unpackCmdFromJson(jsondict, the_cmd_key):
    cmd = None
    if jsondict:
        spec = jsondict['raw_object'].get('spec')
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return cmd
        '''
        Get the CMD body from 'dict' structure.
        '''
        if the_cmd_key:
            cmd_head = ALL_SUPPORT_CMDS.get(the_cmd_key)
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
#             msg = ''
#             for index,line in enumerate(std_out):
#                 if not str.strip(line):
#                     continue
#                 if index == len(std_out) - 1:
#                     msg = msg + str.strip(line) + '. '
#                 else:
#                     msg = msg + str.strip(line) + ', '
#             logger.debug(str.strip(msg))
            logger.debug(std_out)
        if std_err:
#             msg = ''
#             for index, line in enumerate(std_err):
#                 if not str.strip(line):
#                     continue
#                 if index == len(std_err) - 1:
#                     msg = msg + str.strip(line) + '. ' + '***More details in %s***' % LOG
#                 else:
#                     msg = msg + str.strip(line) + ', '
            logger.error(std_err)
#             raise ExecuteException('VirtctlError', str.strip(msg))
            raise ExecuteException('VirtctlError', std_err)
#         return (str.strip(std_out[0]) if std_out else '', str.strip(std_err[0]) if std_err else '')
        return
    finally:
        p.stdout.close()
        p.stderr.close()

# '''
# Run back-end command in subprocess.
# '''
# def runCmdAndCheckReturnCode(cmd):
#     std_err = None
#     if not cmd:
#         logger.debug('No CMD to execute.')
#         return
#     try:
#         result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
#         logger.debug(result)
#     except Exception:
#         raise ExecuteException('VmmError', "Cmd: %s failed!" %cmd)
        #         return (str.strip(std_out[0]) if std_out else '', str.strip(std_err[0]) if std_err else '')

if __name__ == '__main__':
    config.load_kube_config(config_file=TOKEN)
    main()
#     test()
