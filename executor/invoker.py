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
import re
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
from utils.libvirt_util import _get_dom, is_snapshot_exists, is_volume_in_use, get_volume_xml, undefine_with_snapshot, destroy, \
    undefine, create, setmem, setvcpus, is_vm_active, is_vm_exists, is_volume_exists, is_snapshot_exists, \
    is_pool_exists, _get_pool_info
from utils import logger
from utils.uit_utils import is_block_dev_exists
from utils.utils import Domain, get_l3_network_info, randomMAC, ExecuteException, updateJsonRemoveLifecycle, \
    addPowerStatusMessage, addExceptionMessage, report_failure, deleteLifecycleInJson, randomUUID, now_to_timestamp, \
    now_to_datetime, now_to_micro_time, get_hostname_in_lower_case, UserDefinedEvent, report_success


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

PLURAL_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'plural')
VERSION_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'version')
GROUP_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'group')


FORCE_SHUTDOWN_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'stopVMForce')
RESET_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'resetVM')

PLURAL_VM_POOL = config_raw.get('VirtualMahcinePool', 'plural')
VERSION_VM_POOL = config_raw.get('VirtualMahcinePool', 'version')
GROUP_VM_POOL = config_raw.get('VirtualMahcinePool', 'group')

PLURAL_UIT_POOL = config_raw.get('UITStoragePool', 'plural')
VERSION_UIT_POOL = config_raw.get('UITStoragePool', 'version')
GROUP_UIT_POOL = config_raw.get('UITStoragePool', 'group')

PLURAL_UIT_DISK = config_raw.get('UITDisk', 'plural')
VERSION_UIT_DISK = config_raw.get('UITDisk', 'version')
GROUP_UIT_DISK = config_raw.get('UITDisk', 'group')

PLURAL_UIT_SNAPSHOT = config_raw.get('UITSnapshot', 'plural')
VERSION_UIT_SNAPSHOT = config_raw.get('UITSnapshot', 'version')
GROUP_UIT_SNAPSHOT = config_raw.get('UITSnapshot', 'group')

DEFAULT_STORAGE_DIR = config_raw.get('DefaultStorageDir', 'default')
DEFAULT_DEVICE_DIR = config_raw.get('DefaultDeviceDir', 'default')
DEFAULT_SNAPSHOT_DIR = config_raw.get('DefaultSnapshotDir', 'snapshot')
DEFAULT_VMD_TEMPLATE_DIR = config_raw.get('DefaultVirtualMachineDiskTemplateDir', 'vmdi')

DEFAULT_VM_TEMPLATE_DIR = config_raw.get('DefaultTemplateDir', 'default')

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
ALL_SUPPORT_CMDS_WITH_POOLNAME_FIELD = {}
ALL_SUPPORT_CMDS_WITH_SNAME_FIELD = {}
ALL_SUPPORT_CMDS_WITH_SWITCH_FIELD = {}
ALL_SUPPORT_CMDS_WITH_POOL_FIELD = {}

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
            ALL_SUPPORT_CMDS_WITH_POOLNAME_FIELD = dict(ALL_SUPPORT_CMDS_WITH_POOLNAME_FIELD, **v)
        elif string.find(k, 'WithSnameField') != -1:
            ALL_SUPPORT_CMDS_WITH_SNAME_FIELD = dict(ALL_SUPPORT_CMDS_WITH_SNAME_FIELD, **v)
        elif string.find(k, 'WithSwitchField') != -1:
            ALL_SUPPORT_CMDS_WITH_SWITCH_FIELD = dict(ALL_SUPPORT_CMDS_WITH_SWITCH_FIELD, **v)
        elif string.find(k, 'WithPoolField') != -1:
            ALL_SUPPORT_CMDS_WITH_POOL_FIELD = dict(ALL_SUPPORT_CMDS_WITH_POOL_FIELD, **v)
            
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
        thread_5 = Thread(target=vMDiskImageWatcher)
        thread_5.daemon = True
        thread_5.name = 'vm_disk_image_watcher'
        thread_5.start()
#         thread_5 = Thread(target=vMBlockDevWatcher)
#         thread_5.daemon = True
#         thread_5.name = 'vm_block_dev_watcher'
#         thread_5.start()
        thread_9 = Thread(target=vMNetworkWatcher)
        thread_9.daemon = True
        thread_9.name = 'vm_network_watcher'
        thread_9.start()
        thread_10 = Thread(target=vMPoolWatcher)
        thread_10.daemon = True
        thread_10.name = 'vm_pool_watcher'
        thread_10.start()
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
#         thread_6.join()
#         thread_7.join()
#         thread_8.join()
        thread_9.join()
        thread_10.join()
    except:
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
            if the_cmd_key and operation_type != 'DELETED':
#                 _vm_priori_step(the_cmd_key, jsondict)
                (jsondict, network_operations_queue, disk_operations_queue) \
                    = _vm_prepare_step(the_cmd_key, jsondict, metadata_name)
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
                        if _isInstallVMFromISO(the_cmd_key) or _isInstallVMFromImage(the_cmd_key):
                            if cmd:
                                runCmd(cmd)
                            if is_vm_exists(metadata_name) and not is_vm_active(metadata_name):
                                create(metadata_name)
                            time.sleep(2)
                        else:
                            if cmd:
                                runCmd(cmd)
                        '''
                        Run network operations
                        '''
                        if network_operations_queue:
                            for operation in network_operations_queue:
                                logger.debug(operation)
                                if operation.find('kubeovn-adm unbind-swport') != -1:
                                    try:
                                        runCmd(operation)
                                    except:
                                        pass
                                else:
                                    runCmd(operation)
                                time.sleep(1)
                    elif operation_type == 'MODIFIED':
#                         if not is_vm_exists(metadata_name):
#                             raise ExecuteException('VirtctlError', '404, Not Found. VM %s not exists.' % metadata_name)
                        if _isDeleteVM(the_cmd_key):
                            if is_vm_active(metadata_name):
                                destroy(metadata_name)
                                time.sleep(1)
                        try:
                            runCmd(cmd)
                        except Exception, e:
                            if _isDeleteVM(the_cmd_key) and not is_vm_exists(metadata_name):
                                logger.warning("***VM %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e
                                        
#                                 file_path = '%s/%s-*' % (DEFAULT_DEVICE_DIR, metadata_name)
#                                 mvNICXmlToTmpDir(file_path)
                            # add support python file real path to exec
                        '''
                        Run network operations
                        '''
                        if network_operations_queue:
                            for operation in network_operations_queue:
                                logger.debug(operation)
                                runCmd(operation)
                                time.sleep(1)
                        '''
                        Run disk operations
                        '''
                        if disk_operations_queue:
                            for operation in disk_operations_queue:
                                logger.debug(operation)
                                runCmd(operation)
                                time.sleep(1)
#                     elif operation_type == 'DELETED':
#                         logger.debug('Delete custom object by client.')
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
                    if _isInstallVMFromISO(the_cmd_key) or _isInstallVMFromImage(the_cmd_key):
                        try:
                            if is_vm_exists(metadata_name) and is_vm_active(metadata_name):
                                destroy(metadata_name)
                                time.sleep(0.5)
                        except:
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
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
                disk_type = _get_field(jsondict, the_cmd_key, 'type')
                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = unpackCmdFromJson(jsondict, the_cmd_key)
    #             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
    #             body = jsondict['raw_object']
    #             try:
    #                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
    #             except:
    #                 logger.warning('Oops! ', exc_info=1)
                try:
                    if disk_type is None or pool_name is None:
                        raise ExecuteException('VirtctlError', "disk type and pool must be set")
                    if operation_type == 'ADDED':
                        if cmd:
                            result, data = None, None
                            if not is_kubesds_disk_exists(disk_type, pool_name, metadata_name):
                                result, data = runCmdWithResult(cmd)
                                if result['code'] != 0:
                                    raise ExecuteException('VirtctlError', result['msg'])
                            else:
                                result, data = get_kubesds_disk_info(disk_type, pool_name, metadata_name)
                            vol_json = updateJsonRemoveLifecycle(jsondict, data)
                            body = addPowerStatusMessage(vol_json, 'Ready', 'The resource is ready.')
                            _reportResutToVirtlet(metadata_name, body, group, version, plural)
                    elif operation_type == 'MODIFIED':
                        result, data = None, None
                        try:
                            result, data = runCmdWithResult(cmd)
                            if result['code'] != 0:
                                raise ExecuteException('VirtctlError', result['msg'])
                        except Exception, e:
                            if _isDeleteDisk(the_cmd_key) and not is_kubesds_disk_exists(disk_type, pool_name, metadata_name):
                                logger.warning("***Disk %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e
                        # update disk info
                        if _isResizeDisk(the_cmd_key):
                            vol_json = updateJsonRemoveLifecycle(jsondict, data)
                            body = addPowerStatusMessage(vol_json, 'Ready', 'The resource is ready.')
                            _reportResutToVirtlet(metadata_name, body, group, version, plural)
                        elif _isCloneDisk(the_cmd_key):
                            if disk_type == 'uus':
                                # uus disk type register to server by hand
                                result, data = get_kubesds_disk_info(disk_type, pool_name, metadata_name)
                                if result['code'] == 0:
                                    newname = getCloneDiskName(the_cmd_key, jsondict)
                                    jsoncopy = jsondict.copy()
                                    jsoncopy['kind'] = 'VirtualMachineDisk'
                                    jsoncopy['metadata']['kind'] = 'VirtualMachineDisk'
                                    jsoncopy['metadata']['name'] = newname
                                    del jsoncopy['metadata']['resourceVersion']
                                    del jsoncopy['spec']['lifecycle']
                                    jsoncopy['spec']['volume'] = data
                                    addResourceToServer(newname, jsoncopy, group, version, plural)
                            else:
                                # other disk type auto register to server
                                vol_json = deleteLifecycleInJson(jsondict)
                                body = addPowerStatusMessage(vol_json, 'Ready', 'The resource is ready.')
                                _reportResutToVirtlet(metadata_name, body, group, version, plural)
                        elif _isDeleteDisk(the_cmd_key) and disk_type == 'uus':
                            deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
#                     elif operation_type == 'DELETED':
#                         if pool_name and is_volume_exists(metadata_name, pool_name):
#                             if cmd:
#                                 runCmd(cmd)
#                         else:
#                             raise ExecuteException('VirtctlError', 'No vol %s in pool %s!' % (metadata_name, pool_name))
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
                
def vMDiskImageWatcher(group=GROUP_VM_DISK_IMAGE, version=VERSION_VM_DISK_IMAGE, plural=PLURAL_VM_DISK_IMAGE):
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('metadata name: %s' % metadata_name)
            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)
            if the_cmd_key and operation_type != 'DELETED':
                involved_object_name = metadata_name
                involved_object_kind = 'VirtualMachineDiskImage'
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
                        try:
                            runCmd(cmd)
                        except Exception, e:
                            if _isDeleteDiskImage(the_cmd_key):
                                logger.warning("***Disk image %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e
#                     elif operation_type == 'DELETED':
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
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
            operation_type = jsondict.get('type')
            logger.debug(operation_type)
            metadata_name = getMetadataName(jsondict)
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
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
                        try:
                            runCmd(cmd)
                        except Exception, e:
                            if _isDeleteImage(the_cmd_key):
                                logger.warning("***VM image %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e
#                     elif operation_type == 'DELETED':
#                         if is_vm_active(metadata_name):
#                             destroy(metadata_name)
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
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
                if not vm_name:
                    raise ExecuteException('VirtctlError', 'error: no "domain" parameter')
                if not is_vm_exists(vm_name):
                    raise ExecuteException('VirtctlError', '404, Not Found. VM %s not exists.' % vm_name)
                (jsondict, snapshot_operations_queue) = _vm_snapshot_prepare_step(the_cmd_key, jsondict, metadata_name)
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
                        try:
                            runCmd(cmd)
                        except Exception, e:
                            if _isDeleteVMSnapshot(the_cmd_key) and not _snapshot_file_exists(metadata_name):
                                logger.warning("***VM snapshot %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e
                        '''
                        Run snapshot operations
                        '''
                        if snapshot_operations_queue:
                            for operation in snapshot_operations_queue:
                                logger.debug(operation)
                                runCmd(operation)
                                time.sleep(1)
#                     elif operation_type == 'DELETED':
# #                         if vm_name and is_snapshot_exists(metadata_name, vm_name):
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
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
                if not _isDeleteSwPort(the_cmd_key):
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
                        try:
                            runCmd(cmd)
                        except Exception, e:
                            if _isDeleteNetwork(the_cmd_key):
                                logger.warning("***Network %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

def vMPoolWatcher(group=GROUP_VM_POOL, version=VERSION_VM_POOL, plural=PLURAL_VM_POOL):
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
        except:
            logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('metadata name: %s' % metadata_name)
            the_cmd_key = _getCmdKey(jsondict)
            logger.debug('cmd key is: %s' % the_cmd_key)
            if the_cmd_key and operation_type != 'DELETED':
                involved_object_name = metadata_name
                involved_object_kind = 'VirtualMachinePool'
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
                pool_name = metadata_name
                pool_type = getPoolType(the_cmd_key, jsondict)
                logger.debug("pool_name is :"+pool_name)
                logger.debug("pool_type is :" + pool_type)
                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = unpackCmdFromJson(jsondict, the_cmd_key)
                if cmd is None:
                    break
                try:
                    if operation_type == 'ADDED':
                        # judge pool path exist or not

                        # POOL_PATH = getPoolPathWhenCreate(jsondict)
                        # # file_dir = os.path.split(POOL_PATH)[0]
                        # if not os.path.isdir(POOL_PATH):
                        #     os.makedirs(POOL_PATH)
                        result, poolJson = None, None
                        if not is_kubesds_pool_exists(pool_type, pool_name):
                            result, poolJson = runCmdWithResult(cmd)
                            logger.debug('create pool')
                        else:
                            result, poolJson = get_kubesds_pool_info(pool_type, pool_name)
                            logger.debug('get pool info')
                        if result['code'] == 0:
                            write_result_to_server(group, version, 'default', plural,
                                                   involved_object_name, {'code': 0, 'msg': 'success'}, poolJson)
                            try:
                                report_success(metadata_name, jsondict, 'success',
                                               'has exist ' + pool_name + ' pool!', group, version, plural)
                            except:
                                logger.warning('Oops! report_success fail', exc_info=1)
                        else:
                            raise ExecuteException('VirtctlError', result['msg'])
                    elif operation_type == 'MODIFIED':
                        try:
                            if the_cmd_key == 'deletePool':
                                result, data = runCmdWithResult(cmd)
                                if result['code'] != 0:
                                    raise ExecuteException('VirtctlError', result['msg'])
                                else:
                                    deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                    return
                            else:
                                if pool_type == 'uus':
                                    pass
                                else:
                                    runCmd(cmd)
                        except Exception, e:
                            if _isDeletePool(the_cmd_key) and not is_kubesds_pool_exists(pool_type, pool_name):
                                logger.warning("***Pool %s not exists, delete it from virtlet" % metadata_name)
                                jsondict = deleteLifecycleInJson(jsondict)
                                modifyStructure(metadata_name, jsondict, group, version, plural)
                                time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                continue
                            else:
                                raise e

                        result, poolJson = get_kubesds_pool_info(pool_type, pool_name)
                        write_result_to_server(group, version, 'default', plural,
                                            involved_object_name, {'code': 0, 'msg': 'success'}, poolJson)
                        try:
                            report_success(metadata_name, jsondict, 'success', the_cmd_key + pool_name + ' pool success!', group, version, plural)
                        except:
                            logger.warning('Oops! report_success fail', exc_info=1)
                    # elif operation_type == 'DELETED':
                    #     if is_pool_exists(pool_name):
                    #         runCmd(cmd)
                    #     else:
                    #         raise ExecuteException('VirtctlError', 'Not exist '+pool_name+' pool!')
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
        except ExecuteException, e:
            logger.error('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, e.reason, e.message, group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        except:
            logger.warning('Oops! ', exc_info=1)
            info=sys.exc_info()
            try:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

def is_kubesds_pool_exists(type, pool):
    result, poolJson = runCmdWithResult('kubesds-adm showPool --type ' + type + ' --pool ' + pool)
    if result['code'] == 0:
        return True
    return False

def is_kubesds_disk_exists(type, pool, vol):
    result, poolJson = runCmdWithResult('kubesds-adm showDisk --type ' + type + ' --pool ' + pool + ' --vol ' + vol)
    if result['code'] == 0:
        return True
    return False

def get_kubesds_pool_info(type, pool):
    return runCmdWithResult('kubesds-adm showPool --type ' + type + ' --pool ' + pool)

def get_kubesds_disk_info(type, pool, vol):
    return runCmdWithResult('kubesds-adm showDisk --type ' + type + ' --pool ' + pool + ' --vol ' + vol)

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

def modifyStructure(name, body, group, version, plural):
    if body.get('raw_object'):
        body = body.get('raw_object')
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def deleteStructure(name, body, group, version, plural):
    retv = client.CustomObjectsApi().delete_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def write_result_to_server(group, version, namespace, plural, name, result=None, data=None):
    jsonDict = None
    try:
        # involved_object_name actually is nodeerror occurred during processing json data from apiserver
        jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
            group=group, version=version, namespace=namespace, plural=plural, name=name)
        # logger.debug(dumps(jsonStr))
#         logger.debug("node name is: " + name)
        jsonDict = jsonStr.copy()

        if plural == PLURAL_UIT_POOL:
            jsonDict['spec']['virtualMachineUITPool'] = {'result': result, 'data': data}
        elif plural == PLURAL_UIT_DISK:
            jsonDict['spec']['virtualMachineUITDisk'] = {'result': result, 'data': data}
        elif plural == PLURAL_UIT_SNAPSHOT:
            if 'virtualMachineUITSnapshot' in jsonDict['spec'].keys():
                if data:
                    jsonDict['spec']['virtualMachineUITSnapshot'] = {'result': result, 'data': data}
                else:
                    jsonDict['spec']['virtualMachineUITSnapshot']['result'] = result
            else:
                jsonDict['spec']['virtualMachineUITSnapshot'] = {'result': result, 'data': data}
        elif plural == PLURAL_VM_NETWORK:
            jsonDict['spec']['VirtualMachineNetwork'] = {'type': 'layer3', 'data': get_l3_network_info(name)}
        elif plural == PLURAL_VM_POOL:
            jsonDict['spec']['pool'] = data

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

def _vm_priori_step(the_cmd_key, jsondict):
    if _isPlugDisk(the_cmd_key):
        vmd_path = _get_field(jsondict, the_cmd_key, 'source')
        if not vmd_path:
            raise ExecuteException('VirtctlError', 'Config error: no "source" parameter.')
        if is_volume_in_use(path=vmd_path):
            raise ExecuteException('VirtctlError', "Cannot plug disk in use %s." % vmd_path)
        if os.path.split(vmd_path)[0] == DEFAULT_VMD_TEMPLATE_DIR:
            raise ExecuteException('VirtctlError', "Cannot plug disk image %s." % vmd_path)
        
def _vm_prepare_step(the_cmd_key, jsondict, metadata_name):    
    network_operations_queue = []
    disk_operations_queue = []
    if _isInstallVMFromISO(the_cmd_key):
        '''
        Parse network configurations
        '''
        network_config = _get_field(jsondict, the_cmd_key, 'network')
        config_dict = _network_config_parser(network_config)
        logger.debug(config_dict)
        network_operations_queue = _get_network_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = _set_field(jsondict, the_cmd_key, 'network', 'none')
    if _isInstallVMFromImage(the_cmd_key):
        template_path = _get_field(jsondict, the_cmd_key, 'cdrom')
        if not os.path.exists(template_path):
            raise ExecuteException('VirtctlError', "Template file %s not exists, cannot copy from it!" % template_path)
        (new_vm_path, jsondict) = _updateRootDiskInJson(jsondict, the_cmd_key, metadata_name)
#         if os.path.exists(new_vm_path):
#             raise ExecuteException('VirtctlError', '409, Conflict. File %s already exists, aborting copy.' % new_vm_path)
        runCmd('cp %s %s' %(template_path, new_vm_path))
        '''
        Parse network configurations
        '''
        network_config = _get_field(jsondict, the_cmd_key, 'network')
        config_dict = _network_config_parser(network_config)
        logger.debug(config_dict)
        network_operations_queue = _get_network_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = _set_field(jsondict, the_cmd_key, 'network', 'none')
    if _isPlugNIC(the_cmd_key) or _isUnplugNIC(the_cmd_key):
        '''
        Parse network configurations
        '''
        network_config = _get_fields(jsondict, the_cmd_key)
        logger.debug(network_config)
        config_dict = _network_config_parser_json(the_cmd_key, network_config)
        logger.debug(config_dict)
        network_operations_queue = _get_network_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)
    if _isPlugDisk(the_cmd_key) or _isUnplugDisk(the_cmd_key):
        '''
        Parse disk configurations
        '''
        disk_config = _get_fields(jsondict, the_cmd_key)
        logger.debug(disk_config)
        config_dict = _disk_config_parser_json(the_cmd_key, disk_config)
        logger.debug(config_dict)
        disk_operations_queue = _get_disk_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)
    return (jsondict, network_operations_queue, disk_operations_queue)

def _vm_snapshot_prepare_step(the_cmd_key, jsondict, metadata_name):
    snapshot_operations_queue = []
    if _isMergeSnapshot(the_cmd_key) or _isRevertVirtualMachine(the_cmd_key):
        domain = _get_field(jsondict, the_cmd_key, "domain")
        snapshot_operations_queue = _get_snapshot_operations_queue(the_cmd_key, domain, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)
    return (jsondict, snapshot_operations_queue)

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

def _isDeleteSwPort(the_cmd_key):
    if the_cmd_key == "deleteSwPort":
        return True
    return False    

def getMetadataName(jsondict):
    metadata = jsondict['raw_object']['metadata']
    metadata_name = metadata.get('name')
    if metadata_name:
        return metadata_name
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No metadata name!')

def getPoolPathWhenCreate(jsondict):
    spec = jsondict['raw_object']['spec']
    lifecycle = spec.get('lifecycle')

    if lifecycle:
        return lifecycle['createPool']['target']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No metadata name!')

def getPoolType(the_cmd_key, jsondict):
    spec = jsondict['raw_object']['spec']
    lifecycle = spec.get('lifecycle')

    if lifecycle:
        return lifecycle[the_cmd_key]['type']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No found pool type!')

def getCloneDiskName(the_cmd_key, jsondict):
    spec = jsondict['raw_object']['spec']
    lifecycle = spec.get('lifecycle')

    if lifecycle:
        return lifecycle[the_cmd_key]['newname']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No found clone disk name!')

def forceUsingMetadataName(metadata_name, the_cmd_key, jsondict):
    spec = jsondict['raw_object']['spec']
    lifecycle = spec.get('lifecycle')
    if lifecycle:
        if the_cmd_key in ALL_SUPPORT_CMDS_WITH_NAME_FIELD:
            lifecycle[the_cmd_key]['name'] = metadata_name    
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_DOMAIN_FIELD:
            lifecycle[the_cmd_key]['domain'] = metadata_name
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_VOL_FIELD:
            lifecycle[the_cmd_key]['vol'] = metadata_name
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_SNAPNAME_FIELD:
            lifecycle[the_cmd_key]['snapshotname'] = metadata_name
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_POOLNAME_FIELD:
            lifecycle[the_cmd_key]['poolname'] = metadata_name
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_SNAME_FIELD:
            lifecycle[the_cmd_key]['sname'] = metadata_name
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_SWITCH_FIELD:
            lifecycle[the_cmd_key]['switch'] = metadata_name
        elif the_cmd_key in ALL_SUPPORT_CMDS_WITH_POOL_FIELD:
            lifecycle[the_cmd_key]['pool'] = metadata_name
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

def addResourceToServer(new_name, body, group, version, plural):
    body = body.get('raw_object')
    try:
        client.CustomObjectsApi().create_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=new_name, body=body)
    except:
        logger.error('Oops! ', exc_info=1)

'''
Install VM from ISO.
'''
def _isInstallVMFromISO(the_cmd_key):
    if the_cmd_key == "createAndStartVMFromISO":
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

def _isDeleteVM(the_cmd_key):
    if the_cmd_key == "deleteVM":
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

'''
Get event id.
'''
def _getEventId(jsondict):
    metadata = jsondict['raw_object'].get('metadata')
    labels = metadata.get('labels')
    logger.debug(labels)
    return labels.get('eventId') if labels.get('eventId') else '-1'

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

def _get_fields(jsondict, the_cmd_key):
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
            retv = lifecycle.get(the_cmd_key)
    return retv  

def _set_field(jsondict, the_cmd_key, field, value):
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
                    jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k] = value
    return jsondict 

def _del_field(jsondict, the_cmd_key, field):
    spec = jsondict['raw_object'].get('spec')
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return jsondict
        if the_cmd_key:
            contents = lifecycle.get(the_cmd_key)
            for k, v in contents.items():
                if k == field:
                    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k]
    return jsondict
        
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
    if not os.path.exists(DEFAULT_DEVICE_DIR):
        os.makedirs(DEFAULT_DEVICE_DIR, 0711)
    file_path = '%s/%s-nic-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, data.get('mac').replace(':', ''))
    try:
        with open(file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='\t'))
    except:
        raise ExecuteException('VirtctlError', 'Execute plugNIC error: cannot create NIC XML file \'%s\'' % file_path)  
    
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
        elif k == 'read_bytes_sec':
            iotune[k] = v
        elif k == 'write_bytes_sec':
            iotune[k] = v
        elif k == 'read_iops_sec':
            iotune[k] = v
        elif k == 'write_iops_sec':
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
    if not os.path.exists(DEFAULT_DEVICE_DIR):
        os.makedirs(DEFAULT_DEVICE_DIR, 0711)
    file_path = '%s/%s-disk-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, data.get('target'))
    try:
        with open(file_path, 'w') as f:
            f.write(doc.toprettyxml(indent='\t'))
    except:
        raise ExecuteException('VirtctlError', 'Execute plugDisk error: cannot create disk XML file \'%s\'' % file_path)  
    
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
            raise ExecuteException('VirtctlError', 'Network config error: no "type" parameter.')
        else:
            if net_type not in ['bridge', 'l2bridge', 'l3bridge']:
                raise ExecuteException('VirtctlError', 'Network config error: unsupported network "type" %s.' % retv['type'])
        source = retv.get('source')
        if not source:
            raise ExecuteException('VirtctlError', 'Network config error: no "source" parameter.')
        if not retv.has_key('mac'):
            retv['mac'] = randomMAC()
        '''
        Add default params.
        '''
        if net_type in ['l2bridge', 'l3bridge']:
            retv['virtualport'] = 'openvswitch'
        retv['model'] = 'virtio'
        retv['target'] = 'fe%s' % (retv['mac'].replace(':', '')[2:])
    else:
        raise ExecuteException('VirtctlError', 'Network config error: no parameters or in wrong format, plz check it!')
    return retv

def _network_config_parser_json(the_cmd_key, data):
    retv = {}
    if data:
        retv = data.copy()
        if _isUnplugNIC(the_cmd_key):
            if not retv.get('mac'):
                raise ExecuteException('VirtctlError', 'Network config error: no "mac" parameter.')
            return retv
        source = data.get('source')
        if not source:
            raise ExecuteException('VirtctlError', 'Network config error: no "source" parameter.')
        split_it = source.split(',')
        for i in split_it:
            i = i.strip()
            if i.find('=') != -1:
                (k, v) = i.split('=')
                retv[k] = v
    if retv:
        net_type = retv.get('type')
        if not net_type:
            raise ExecuteException('VirtctlError', 'Network config error: no "type" parameter.')
        else:
            if net_type not in ['bridge', 'l2bridge', 'l3bridge']:
                raise ExecuteException('VirtctlError', 'Network config error: unsupported network "type" %s.' % retv['type'])
        if not retv.has_key('mac'):
            retv['mac'] = randomMAC()
        '''
        Add default params.
        '''
        if net_type in ['l2bridge', 'l3bridge']:
            retv['virtualport'] = 'openvswitch'
        retv['model'] = 'virtio'
        retv['target'] = 'fe%s' % (retv['mac'].replace(':', '')[2:])
    else:
        raise ExecuteException('VirtctlError', 'Network config error: no parameters or in wrong format, plz check it!')
    return retv

def _disk_config_parser_json(the_cmd_key, data):
    retv = {}
    if data:
        retv = data.copy()
        if _isUnplugDisk(the_cmd_key):
            if not retv.get('target'):
                raise ExecuteException('VirtctlError', 'Disk config error: no "target" parameter.')
            return retv
        source = data.get('source')
        if not source:
            raise ExecuteException('VirtctlError', 'Disk config error: no "source" parameter.')
    if retv:
        if not retv.get('target'):
                raise ExecuteException('VirtctlError', 'Disk config error: no "target" parameter.')
    else:
        raise ExecuteException('VirtctlError', 'Disk config error: no parameters or in wrong format, plz check it!')
    return retv

def _get_network_operations_queue(the_cmd_key, config_dict, metadata_name):
    if _isInstallVMFromISO(the_cmd_key) or _isInstallVMFromImage(the_cmd_key) or _isPlugNIC(the_cmd_key):
        if _isPlugNIC(the_cmd_key):
            if config_dict.get('live'):
                live = '--live'
            else:
                live = ''
            if config_dict.get('config'):
                config = '--config'
            else:
                config = ''
        else:
            live = '--live'
            config = '--config'
        if config_dict.get('type') == 'bridge':
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, live, config)
            return [plugNICCmd]
        elif config_dict.get('type') == 'l2bridge':
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, live, config)
            return [plugNICCmd]
        elif config_dict.get('type') == 'l3bridge':
            if not config_dict.get('switch'):
                raise ExecuteException('VirtctlError', 'Network config error: no "switch" parameter.')
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, live, config)
            unbindSwPortCmd = 'kubeovn-adm unbind-swport --mac %s' % (config_dict.get('mac'))
            bindSwPortCmd = '%s --mac %s --switch %s --ip %s' % (ALL_SUPPORT_CMDS.get('bindSwPort'), config_dict.get('mac'), config_dict.get('switch'), config_dict.get('ip') if config_dict.get('ip') else 'dynamic')
            recordSwitchToFileCmd = 'echo "switch=%s" > %s/%s-nic-%s.cfg' % \
            (config_dict.get('switch'), DEFAULT_DEVICE_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
            recordIpToFileCmd = 'echo "ip=%s" >> %s/%s-nic-%s.cfg' % \
            (config_dict.get('ip') if config_dict.get('ip') else 'dynamic', DEFAULT_DEVICE_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
    #         recordVxlanToFileCmd = 'echo "vxlan=%s" >> %s/%s-nic-%s.cfg' % \
    #         (config_dict.get('vxlan') if config_dict.get('vxlan') else '-1', DEFAULT_DEVICE_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
            return [plugNICCmd, unbindSwPortCmd, bindSwPortCmd, recordSwitchToFileCmd, recordIpToFileCmd]
    elif _isUnplugNIC(the_cmd_key):
        if config_dict.get('live'):
            live = '--live'
        else:
            live = ''
        if config_dict.get('config'):
            config = '--config'
        else:
            config = ''
        unplugNICCmd = _unplugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, live, config)
        net_cfg_file_path = '%s/%s-nic-%s.cfg' % \
                                (DEFAULT_DEVICE_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
        if os.path.exists(net_cfg_file_path):
            unbindSwPortCmd = 'kubeovn-adm unbind-swport --mac %s' % (config_dict.get('mac'))
            return [unbindSwPortCmd, unplugNICCmd]
        else:
            return [unplugNICCmd]
        
def _get_disk_operations_queue(the_cmd_key, config_dict, metadata_name):
    if config_dict.get('live'):
        live = '--live'
    else:
        live = ''
    if config_dict.get('config'):
        config = '--config'
    else:
        config = ''
    if _isPlugDisk(the_cmd_key):
        plugDiskCmd = _plugDeviceFromXmlCmd(metadata_name, 'disk', config_dict, live, config)
        return [plugDiskCmd]
    elif _isUnplugDisk(the_cmd_key):
        unplugDiskCmd = _unplugDeviceFromXmlCmd(metadata_name, 'disk', config_dict, live, config)
        return [unplugDiskCmd]
    
def _get_snapshot_operations_queue(the_cmd_key, domain, metadata_name):
    if _isMergeSnapshot(the_cmd_key):
        domain_obj = Domain(_get_dom(domain))
        (merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.merge_snapshot(metadata_name)
        return [merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd]
    elif _isRevertVirtualMachine(the_cmd_key):
        domain_obj = Domain(_get_dom(domain))
        (merge_snapshots_cmd, _, _) = domain_obj.merge_snapshot(metadata_name)
        (revert_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.revert_snapshot(metadata_name)
        return [merge_snapshots_cmd, revert_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd]

def _plugDeviceFromXmlCmd(metadata_name, device_type, data, live, config):
    if device_type == 'nic':
        file_path = _createNICXml(metadata_name, data)
    elif device_type == 'disk':
        file_path = _createDiskXml(metadata_name, data)
    return 'virsh attach-device --domain %s --file %s %s %s' % (metadata_name, file_path, live, config)

def _unplugDeviceFromXmlCmd(metadata_name, device_type, data, live, config):
    if device_type == 'nic':
        file_path = '%s/%s-nic-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, data.get('mac').replace(':', ''))
        if not os.path.exists(file_path):
            file_path = _createNICXml(metadata_name, data)
    elif device_type == 'disk':
        file_path = '%s/%s-disk-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, data.get('target'))
        if not os.path.exists(file_path):
            file_path = _createDiskXml(metadata_name, data)
    return 'virsh detach-device --domain %s --file %s %s %s' % (metadata_name, file_path, live, config)

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
        raise ExecuteException('VirtctlError', 'Execute plugNIC error: missing parameter "source"!')
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
        raise ExecuteException('VirtctlError', 'Execute plugNIC error: missing parameter "mac"!')
    
    file_path = '%s/%s-nic-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, mac.replace(':', ''))
    del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key]
    new_cmd_key = 'unplugDevice'
    jsondict['raw_object']['spec']['lifecycle'][new_cmd_key] = {'file': file_path}
    return (jsondict, new_cmd_key, file_path)

def mvNICXmlToTmpDir(file_path):
    if file_path:
        runCmd('mv -f %s /tmp' % file_path)

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
    
def _updateRootDiskInJson(jsondict, the_cmd_key, metadata_name):
    '''
    Get target VM name from Json.
    '''
    new_path = None
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
                        p1 = r'^(\s*ROOTDISK\s*=\s*)([^,^\s*]+)\s*'
                        p2 = r'^\s*ROOTDISK'
                        m1 = re.match(p1,v)
                        if m1:
                            string_to_remove = m1.group(1)
                            new_path = m1.group(2)
                            new_v = v.replace(string_to_remove, '')
                        elif re.match(p2,v):
                            new_path = '%s/%s' % (DEFAULT_STORAGE_DIR, metadata_name)
                            new_v = v.replace('ROOTDISK', new_path)
                        else:
                            raise ExecuteException('VirtctlError', '400, Bad Reqeust. Non-supported parameter "%s".' % v)
                        jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k] = new_v
                    elif k == 'cdrom':
                        del jsondict['raw_object']['spec']['lifecycle'][the_cmd_key][k]
                    else:
                        continue
    return (new_path, jsondict)    

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

def _snapshot_file_exists(snapshot):
    xml_file = '%s.xml' % (snapshot)
    for _,_,files in os.walk(DEFAULT_SNAPSHOT_DIR, topdown = False):
        if xml_file in files:
            return True
        else:
            return False
    return False


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
def runCmdIgnoreError(cmd):
    std_err = None
    if not cmd:
#         logger.debug('No CMD to execute.')
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            logger.debug(std_out)
        if std_err:
            logger.warning(std_err)
        return
    finally:
        p.stdout.close()
        p.stderr.close()

'''
Run back-end command in subprocess.
'''
def runCmdWithResult(cmd):
    std_err = None
    logger.debug(cmd)
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
            msg = msg.replace("'", '"')
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
                raise ExecuteException('VirtctlError', error_msg)
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
