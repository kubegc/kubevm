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
from xml.dom.minidom import Document
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
from utils.utils import get_l3_network_info, randomMAC, ExecuteException, updateJsonRemoveLifecycle, addPowerStatusMessage, addExceptionMessage, report_failure, deleteLifecycleInJson, randomUUID, now_to_timestamp, now_to_datetime, now_to_micro_time, get_hostname_in_lower_case, UserDefinedEvent

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
PLURAL_VM_NETWORK = config_raw.get('VirtualMachineNetwork', 'plural')
VERSION_VM_NETWORK = config_raw.get('VirtualMachineNetwork', 'version')
GROUP_VM_NETWORK = config_raw.get('VirtualMachineNetwork', 'group')

FORCE_SHUTDOWN_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'stopVMForce')
RESET_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'resetVM')

PLURAL_STORAGE_POOL = config_raw.get('UITStoragePool', 'plural')
VERSION_STORAGE_POOL = config_raw.get('UITStoragePool', 'version')
GROUP_STORAGE_POOL = config_raw.get('UITStoragePool', 'group')

PLURAL_UIT_DISK = config_raw.get('UITDisk', 'plural')
VERSION_UIT_DISK = config_raw.get('UITDisk', 'version')
GROUP_UIT_DISK = config_raw.get('UITDisk', 'group')

PLURAL_UIT_SNAPSHOT = config_raw.get('UITSnapshot', 'plural')
VERSION_UIT_SNAPSHOT = config_raw.get('UITSnapshot', 'version')
GROUP_UIT_SNAPSHOT = config_raw.get('UITSnapshot', 'group')

DEFAULT_STORAGE_DIR = config_raw.get('DefaultStorageDir', 'default')
DEFAULT_DEVICE_DIR = config_raw.get('DefaultDeviceDir', 'default')

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
ALL_SUPPORT_CMDS_WITH_POOL_FIELD = {}
ALL_SUPPORT_CMDS_WITH_SNAME_FIELD = {}

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
        elif string.find(k, 'WithPoolNameField') != -1:
            ALL_SUPPORT_CMDS_WITH_POOL_FIELD = dict(ALL_SUPPORT_CMDS_WITH_POOL_FIELD, **v)
        elif string.find(k, 'WithSnameField') != -1:
            ALL_SUPPORT_CMDS_WITH_SNAME_FIELD = dict(ALL_SUPPORT_CMDS_WITH_SNAME_FIELD, **v)

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
        thread_6 = Thread(target=storagePoolWatcher)
        thread_6.daemon = True
        thread_6.name = 'vm_storage_pool_watcher'
        thread_6.start()
        thread_7 = Thread(target=uitDiskWatcher)
        thread_7.daemon = True
        thread_7.name = 'uit_disk_watcher'
        thread_7.start()
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
        thread_6.join()
        thread_7.join()
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
        try:
            operation_type = jsondict.get('type')
            logger.debug(operation_type)
            metadata_name = getMetadataName(jsondict)
            logger.debug('metadata name: %s' % metadata_name)
            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)
            if the_cmd_key and operation_type != 'DELETED':
                if _isInstallVMFromImage(the_cmd_key):
                    template_path = _get_field(jsondict, the_cmd_key, 'cdrom')
                    if not os.path.exists(template_path):
                        raise ExecuteException('VirtctlError', "Template file %s not exists, cannot copy from it!" % template_path)
                    new_vm_path = '%s/%s.qcow2' % (DEFAULT_STORAGE_DIR, metadata_name)
                    jsondict = _updateRootDiskInJson(jsondict, the_cmd_key, new_vm_path)
                if _isDeleteVM(the_cmd_key):
                    if not is_vm_exists(metadata_name):
                        logger.debug('***VM %s already deleted!***' % metadata_name)
                        continue
                if _isPlugNIC(the_cmd_key):
                    network_type = _get_field(jsondict, the_cmd_key, 'type')
                    if network_type == 'ovsbridge':
                        (jsondict, the_cmd_key, file_path) = createNICFromXml(metadata_name, jsondict, the_cmd_key)
                if _isUnplugNIC(the_cmd_key):
                    network_type = _get_field(jsondict, the_cmd_key, 'type')
                    if network_type == 'ovsbridge':
                        (jsondict, the_cmd_key, file_path) = deleteNICFromXml(metadata_name, jsondict, the_cmd_key)
                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = unpackCmdFromJson(jsondict, the_cmd_key)
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
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
                try:
                    event.registerKubernetesEvent()
                except:
                    logger.error('Oops! ', exc_info=1)
    #             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
    #             body = jsondict['raw_object']
    #             jsondict1 = client.CustomObjectsApi().get_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name)
    #             logger.debug(jsondict1)
    #             logger.debug(body)
    #             try:
    #                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
    #             except:
    #                 logger.warning('Oops! ', exc_info=1)
                try:
            #             print(jsondict)
                    if operation_type == 'ADDED':
                        if _isInstallVMFromISO(the_cmd_key):
                            if cmd:
                                runCmd(cmd)
                            if is_vm_exists(metadata_name) and not is_vm_active(metadata_name):
                                create(metadata_name)
                        elif _isInstallVMFromImage(the_cmd_key):
        #                     if os.path.exists(new_vm_path):
        #                         raise Exception("File %s already exists, copy abolish!" % new_vm_path)
                            runCmd('cp %s %s' %(template_path, new_vm_path))
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
                            elif _isPlugDevice(the_cmd_key):
                                if cmd:
                                    try:
                                        runCmd(cmd)
                                    except ExecuteException, e:
                                        if 'file_path' in dir():
                                            if 'network_type' in dir() and network_type == 'ovsbridge':
                                                mvNICXmlToTmpDir(file_path)
                                        raise e            
                            elif _isUnplugDevice(the_cmd_key):
                                if cmd:
                                    runCmd(cmd)
                                if 'file_path' in dir():
                                    if 'network_type' in dir() and network_type == 'ovsbridge':
                                        mvNICXmlToTmpDir(file_path)
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
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)
        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)
                
def vMDiskWatcher(group=GROUP_VM_DISK, version=VERSION_VM_DISK, plural=PLURAL_VM_DISK):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        try:
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
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
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
    #                 logger.warning('Oops! ', exc_info=1)
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
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)
        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)
                
def vMImageWatcher(group=GROUP_VMI, version=VERSION_VMI, plural=PLURAL_VMI):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=group, version=version, plural=plural, **kwargs):
        try:
            # logger.debug(jsondict)
            operation_type = jsondict.get('type')
            logger.debug(operation_type)
            metadata_name = getMetadataName(jsondict)
            logger.debug('metadata name: %s' % metadata_name)
            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)
            if the_cmd_key and operation_type != 'DELETED':
                if _isCreateImage(the_cmd_key):
                    jsondict = addDefaultSettings(jsondict, the_cmd_key)
                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = unpackCmdFromJson(jsondict, the_cmd_key)
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
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, the_cmd_key, event_type)
                try:
                    event.registerKubernetesEvent()
                except:
                    logger.error('Oops! ', exc_info=1)
    #             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
    #             body = jsondict['raw_object']
    #             try:
    #                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
    #             except:
    #                 logger.warning('Oops! ', exc_info=1)
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
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)
        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)
        
def vMSnapshotWatcher(group=GROUP_VM_SNAPSHOT, version=VERSION_VM_SNAPSHOT, plural=PLURAL_VM_SNAPSHOT):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=group, version=version, plural=plural, **kwargs):
        try:
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
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
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
    #                 logger.warning('Oops! ', exc_info=1)
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
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)
        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)

def vMBlockDevWatcher(group=GROUP_BLOCK_DEV_UIT, version=VERSION_BLOCK_DEV_UIT, plural=PLURAL_BLOCK_DEV_UIT):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        try:
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
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
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
    #                 logger.warning('Oops! ', exc_info=1)
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
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)
        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)
            
def vMNetworkWatcher(group=GROUP_VM_NETWORK, version=VERSION_VM_NETWORK, plural=PLURAL_VM_NETWORK):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        try:
            operation_type = jsondict.get('type')
            logger.debug(operation_type)
            metadata_name = getMetadataName(jsondict)
            logger.debug('metadata name: %s' % metadata_name)
            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)
            if the_cmd_key and operation_type != 'DELETED':
                involved_object_name = metadata_name
                involved_object_kind = 'VirtualMachineNetwork'
                event_metadata_name = randomUUID()
                event_type = 'Normal'
                status = 'Doing(Success)'
                reporter = 'virtctl'
                event_id = _getEventId(jsondict)
                time_now = now_to_datetime()
                time_start = time_now
                time_end = time_now
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
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
    #                 logger.warning('Oops! ', exc_info=1)
                try:
                    if operation_type == 'ADDED':
                        if cmd:
                            runCmd(cmd)
                    elif operation_type == 'MODIFIED':
                        if cmd:
                            runCmd(cmd)
                    elif operation_type == 'DELETED':
                        if cmd:
                            runCmd(cmd)
                    status = 'Done(Success)'
                    write_result_to_server(GROUP_VM_NETWORK, VERSION_VM_NETWORK, 'default', PLURAL_VM_NETWORK, metadata_name)
                except libvirtError:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info=sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)
        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)

def storagePoolWatcher(group=GROUP_STORAGE_POOL, version=VERSION_STORAGE_POOL, plural=PLURAL_STORAGE_POOL):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        try:
            logger.debug(dumps(jsondict))

            operation_type = jsondict.get('type')
            logger.debug(operation_type)

            metadata_name = getMetadataName(jsondict)
            logger.debug('metadata name: %s' % metadata_name)

            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)

            if the_cmd_key and operation_type != 'DELETED':
                involved_object_name = metadata_name
                involved_object_kind = 'UITStoragePool'
                event_metadata_name = randomUUID()
                event_type = 'Normal'
                status = 'Doing(Success)'
                reporter = 'virtctl'
                event_id = _getEventId(jsondict)
                time_now = now_to_datetime()
                time_start = time_now
                time_end = time_now
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (
                involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id,
                (time_end - time_start).total_seconds())
                event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name,
                                         involved_object_kind, message, the_cmd_key, event_type)
                try:
                    event.registerKubernetesEvent()
                except:
                    logger.error('Oops! ', exc_info=1)

                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = get_cmd(jsondict, the_cmd_key)
                try:
                    if cmd is None:
                        break
                    result, data = None, None
                    if operation_type == 'ADDED':
                        result, data = runCmdWithResult(cmd)

                    elif operation_type == 'MODIFIED':
                        result, data = runCmdWithResult(cmd)
                    write_result_to_server(GROUP_STORAGE_POOL, VERSION_STORAGE_POOL, 'default', PLURAL_STORAGE_POOL,
                                           involved_object_name, result, data)

                    if result['code'] == 0:
                        # Verify successful operation, if success countinue, else raise exception
#                         verifyUITStoragePoolOperation(the_cmd_key, cmd)
                        status = 'Done(Success)'

                    else:
                        raise ExecuteException(the_cmd_key+" exec error", result['msg'])
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info = sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info = sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)

        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)


def uitDiskWatcher(group=GROUP_UIT_DISK, version=VERSION_UIT_DISK, plural=PLURAL_UIT_DISK):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        try:
            logger.debug(dumps(jsondict))

            operation_type = jsondict.get('type')
            logger.debug(operation_type)

            metadata_name = getMetadataName(jsondict)
            logger.debug('metadata name: %s' % metadata_name)

            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)

            if the_cmd_key and operation_type != 'DELETED':
                involved_object_name = metadata_name
                involved_object_kind = 'NodeStoragePool'
                event_metadata_name = randomUUID()
                event_type = 'Normal'
                status = 'Doing(Success)'
                reporter = 'virtctl'
                event_id = _getEventId(jsondict)
                time_now = now_to_datetime()
                time_start = time_now
                time_end = time_now
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (
                    involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id,
                    (time_end - time_start).total_seconds())
                event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name,
                                         involved_object_kind, message, the_cmd_key, event_type)
                try:
                    event.registerKubernetesEvent()
                except:
                    logger.error('Oops! ', exc_info=1)

                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = get_cmd(jsondict, the_cmd_key)
                try:
                    if cmd is None:
                        break
                    result, data = None, None
                    if operation_type == 'ADDED':
                        result, data = runCmdWithResult(cmd)

                    elif operation_type == 'MODIFIED':
                        result, data = runCmdWithResult(cmd)
                    write_result_to_server(GROUP_UIT_DISK, VERSION_UIT_DISK, 'default', PLURAL_UIT_DISK,
                                           involved_object_name, result, data)

                    if result['code'] == 0:
#                         verifyUITDiskOperation(the_cmd_key, cmd)
                        status = 'Done(Success)'
                    else:
                        raise ExecuteException(result['code'], result['msg'])
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info = sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info = sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)

        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)

def uitSnapshotWatcher(group=GROUP_VM_SNAPSHOT, version=VERSION_UIT_SNAPSHOT, plural=PLURAL_UIT_SNAPSHOT):
    watcher = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    kwargs['timeout_seconds'] = int(TIMEOUT)
    for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                   group=group, version=version, plural=plural, **kwargs):
        try:
            logger.debug(dumps(jsondict))

            operation_type = jsondict.get('type')
            logger.debug(operation_type)

            metadata_name = getMetadataName(jsondict)
            logger.debug('metadata name: %s' % metadata_name)

            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)

            if the_cmd_key and operation_type != 'DELETED':
                involved_object_name = metadata_name
                involved_object_kind = 'UITSnapshot'
                event_metadata_name = randomUUID()
                event_type = 'Normal'
                status = 'Doing(Success)'
                reporter = 'virtctl'
                event_id = _getEventId(jsondict)
                time_now = now_to_datetime()
                time_start = time_now
                time_end = time_now
                message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (
                    involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id,
                    (time_end - time_start).total_seconds())
                event = UserDefinedEvent(event_metadata_name, time_start, time_end, involved_object_name,
                                         involved_object_kind, message, the_cmd_key, event_type)
                try:
                    event.registerKubernetesEvent()
                except:
                    logger.error('Oops! ', exc_info=1)

                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = get_cmd(jsondict, the_cmd_key)
                try:
                    if cmd is None:
                        break
                    result, data = None, None
                    if operation_type == 'ADDED':
                        result, data = runCmdWithResult(cmd)

                    elif operation_type == 'MODIFIED':
                        result, data = runCmdWithResult(cmd)
                    write_result_to_server(GROUP_UIT_SNAPSHOT, VERSION_UIT_SNAPSHOT, 'default', PLURAL_UIT_SNAPSHOT,
                                           involved_object_name, result, data)

                    if result['code'] == 0:
#                         verifyUITDiskOperation(the_cmd_key, cmd)
                        status = 'Done(Success)'
                    else:
                        raise ExecuteException(result['code'], result['msg'])
                except ExecuteException, e:
                    logger.error('Oops! ', exc_info=1)
                    info = sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                except:
                    logger.error('Oops! ', exc_info=1)
                    info = sys.exc_info()
                    try:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
                    except:
                        logger.warning('Oops! ', exc_info=1)
                    status = 'Done(Error)'
                    event_type = 'Warning'
                    event.set_event_type(event_type)
                finally:
                    if the_cmd_key and operation_type != 'DELETED':
                        time_end = now_to_datetime()
                        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' % (involved_object_kind, involved_object_name, the_cmd_key, status, reporter, event_id, (time_end - time_start).total_seconds())
                        event.set_message(message)
                        event.set_time_end(time_end)
                        try:
                            event.updateKubernetesEvent()
                        except:
                            logger.warning('Oops! ', exc_info=1)

        except:
            logger.debug("error occurred during processing json data from apiserver")
            logger.warning('Oops! ', exc_info=1)

def get_cmd(jsondict, the_cmd_key):
    cmd = None
    if _isCreatePool(the_cmd_key) and 'poolType' in jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].keys():
        poolType = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['poolType']
        if poolType != None:
            del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]['poolType']
            realCmd = ALL_SUPPORT_CMDS[the_cmd_key] + '-' + poolType
            cmd = unpackCmdFromJson(jsondict, the_cmd_key)
            cmd = cmd.replace(ALL_SUPPORT_CMDS[the_cmd_key], realCmd)
            logger.debug(cmd)
    else:
        cmd = unpackCmdFromJson(jsondict, the_cmd_key)
    if cmd is None:
        raise Exception("error: can't get cmd")
    logger.debug(cmd)
    return cmd

def write_result_to_server(group, version, namespace, plural, name, result=None, data=None):
    jsonDict = None
    try:
        # involved_object_name actually is nodeerror occurred during processing json data from apiserver
        jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
            group=group, version=version, namespace=namespace, plural=plural, name=name)
        # logger.debug(dumps(jsonStr))
        logger.debug("node name is: " + name)
        jsonDict = jsonStr.copy()

        if group == GROUP_STORAGE_POOL:
            jsonDict['spec']['virtualMachineUITPool'] = {'result': result, 'data': data}
        elif group == GROUP_UIT_DISK:
            jsonDict['spec']['virtualMachineUITDisk'] = {'result': result, 'data': data}
        elif group == GROUP_VM_NETWORK:
            jsonDict['spec']['VirtualMachineNetwork'] = {'type': 'layer3', 'data': get_l3_network_info(name)}
        if result:
            jsonDict = addPowerStatusMessage(jsonDict, result.get('code'), result.get('msg'))
        else:
            jsonDict = addPowerStatusMessage(jsonDict, 'Ready', 'The resource is ready.')
        del jsonDict['spec']['lifecycle']
        client.CustomObjectsApi().replace_namespaced_custom_object(
            group=group, version=version, namespace='default', plural=plural, name=name, body=jsonDict)

    except:
        logger.debug("error occurred during write result to apiserver")
        logger.error('Oops! ', exc_info=1)
        raise ExecuteException('VirtctlError', 'write result to apiserver failure')

def verifyUITStoragePoolOperation(the_cmd_key, cmd):
    success = False
    kv = {}
    for i in range(len(cmd.split()) / 2):
        kv[cmd.split()[i * 2].replace('--', '')] = cmd.split()[i * 2 + 1]

    result, data = runCmdWithResult('cstor-cli pool-list')
    if result['code'] != 0:
        raise ExecuteException(the_cmd_key + " exec error", 'verifyUITStoragePoolOperation failure')

    if the_cmd_key == 'createPool':
        # cstor-cli pooladd-localfs --poolname test --url localfs:///dev/sdb:/pool
        for pooldata in result['data']:
            if pooldata['poolname'] == kv['poolname']:
                success = True
                break
    elif the_cmd_key == 'deletePool':
        success = True
        for pooldata in data:
            if pooldata['poolname'] == kv['poolname']:
                success = False
    else:
        success = True
    if not success:
        raise ExecuteException(the_cmd_key + " exec error", 'UITStoragePoolOperation not really successful,'
                                                            ' '+the_cmd_key + ' operation has bug!!!')

def verifyUITDiskOperation(the_cmd_key, cmd):
    success = False
    kv = {}
    for i in range(len(cmd.split()) / 2):
        kv[cmd.split()[i * 2].replace('--', '')] = cmd.split()[i * 2 + 1]

    result, data = runCmdWithResult('cstor-cli vdisk-show --poolname '+kv['poolname']+' --name '+kv['name'])
    if result['code'] != 0 and the_cmd_key != 'deleteUITDisk':
        raise ExecuteException(the_cmd_key + " exec error", 'verifyUITDiskOperation failure')

    if the_cmd_key == 'createUITDisk' or the_cmd_key == 'expandUITDisk':
        if data['name'] == kv['name'] and data['poolname'] == kv['poolname'] and data['size'] == kv['size']:
            success = True
    elif the_cmd_key == 'deleteUITDisk':
        if result['code'] == 0:
            raise ExecuteException(the_cmd_key + " exec error", 'verifyUITDiskOperation failure')
    elif the_cmd_key == 'snapshotUITDisk':
        result, data = runCmdWithResult('cstor-cli vdisk-show-ss --poolname '+kv['poolname']+
                                        ' --name '+kv['name']+' --sname '+kv['sname'])
        if kv['cstor-cli'] == 'vdisk-add-ss':
            if result['code'] == 0 and data['name'] == kv['name'] and data['poolname'] == kv['poolname'] and data['sname'] == kv['sname']:
                success = True
        elif kv['cstor-cli'] == 'vdisk-rr-ss':
            if result['code'] == 0:
                success = True
        elif kv['cstor-cli'] == 'vdisk-rm-ss':
            if result['code'] != 0:
                success = True
    else:
        success = True
    if not success:
        raise ExecuteException(the_cmd_key + " exec error", 'UITDiskOperation not really successful,'
                                                            ' ' + the_cmd_key + ' operation has bug!!!')

def _isCreatePool(the_cmd_key):
    if the_cmd_key == "createUITPool":
        return True
    return False

def _isCreateUITSnapshot(the_cmd_key):
    if the_cmd_key == "createUITSnapshot":
        return True
    return False

def _isDeleteUITSnapshot(the_cmd_key):
    if the_cmd_key == "deleteUITSnapshot":
        return True
    return False
def _isRecoveryUITSnapshot(the_cmd_key):
    if the_cmd_key == "recoveryUITSnapshot":
        return True
    return False

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
    elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_POOL_FIELD:
        lifecycle[the_cmd_key]['poolname'] = metadata_name
    elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_SNAME_FIELD:
        lifecycle[the_cmd_key]['sname'] = metadata_name
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

def _isPlugNIC(the_cmd_key):
    if the_cmd_key == "plugNIC":
        return True
    return False

def _isUnplugNIC(the_cmd_key):
    if the_cmd_key == "unplugNIC":
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
                    
def createNICFromXml(metadata_name, jsondict, the_cmd_key):
    spec = jsondict['raw_object'].get('spec')
    if spec:    
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return
        '''
        Read parameters from lifecycle, add default value to some parameters.
        '''
        mac = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('mac')
        source = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('source')
        model = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('model')
        if not source:
            raise ExecuteException('VirtctlError', 'Execute plugNIC error: missing parameter \'source\'!')
        if not mac:
            mac = randomMAC()
        if not model:
            model = 'virtio'
        lines = {}
        lines['mac'] = mac
        lines['source'] = source
        lines['virtualport'] = 'openvswitch'
        lines['model'] = model
    
    '''
    Write NIC Xml file to DEFAULT_DEVICE_DIR dir.
    '''
    doc = Document()
    root = doc.createElement('interface')
    root.setAttribute('type', 'bridge')
    doc.appendChild(root)
    for k, v in lines.items():
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
    '''
    If DEFAULT_DEVICE_DIR not exists, create it.
    '''
    if not os.path.exists(DEFAULT_DEVICE_DIR):
        os.makedirs(DEFAULT_DEVICE_DIR, 0711)
    file_path = '%s/%s-nic-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, mac.replace(':', ''))
    try:
        with open(file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='\t'))
    except:
        raise ExecuteException('VirtctlError', 'Execute plugNIC error: cannot create NIC XML file \'%s\'' % file_path)
    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]
    new_cmd_key = 'plugDevice'
    jsondict['raw_object']['spec']['lifecycle'][new_cmd_key] = {'file': file_path}
    return(jsondict, new_cmd_key, file_path)

def deleteNICFromXml(metadata_name, jsondict, the_cmd_key):
    spec = jsondict['raw_object'].get('spec')
    if spec:    
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return
        '''
        Read parameters from lifecycle, add default value to some parameters.
        '''
        mac = jsondict['raw_object']['spec']['lifecycle'][the_cmd_key].get('mac')
        if not mac:
            raise ExecuteException('VirtctlError', 'Execute plugNIC error: missing parameter \'mac\'!')
    
    file_path = '%s/%s-nic-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, mac.replace(':', ''))
    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]
    new_cmd_key = 'unplugDevice'
    jsondict['raw_object']['spec']['lifecycle'][new_cmd_key] = {'file': file_path}
    return (jsondict, new_cmd_key, file_path)

def mvNICXmlToTmpDir(file_path):
    if file_path:
        runCmd('mv %s /tmp' % file_path)

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

'''
Run back-end command in subprocess.
'''
def runCmdWithResult(cmd):
    std_err = None
    if not cmd:
        #         logger.debug('No CMD to execute.')
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for index, line in enumerate(std_out):
                if not str.strip(line):
                    continue
                msg = msg + str.strip(line)
            msg = str.strip(msg)
            logger.debug(msg)
            try:
                result = loads(msg)
                # print result
                return result['result'], result['data']
            except Exception:
                error_msg = ''
                for index, line in enumerate(std_err):
                    if not str.strip(line):
                        continue
                    error_msg = error_msg + str.strip(line)
                error_msg = str.strip(error_msg)
                logger.error(error_msg)
                raise ExecuteException('cmd exec failure', error_msg)
        if std_err:
            logger.error(std_err)
            raise ExecuteException('VirtctlError', std_err)
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
    # runCmdWithResult('cstor-cli dev-list --type localfs --url all')
#     test()
