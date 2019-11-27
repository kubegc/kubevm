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
from json import loads, load
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
from utils.libvirt_util import get_boot_disk_path, get_xml, vm_state, _get_dom, is_snapshot_exists, is_volume_in_use, get_volume_xml, \
    undefine_with_snapshot, destroy, \
    undefine, create, setmem, setvcpus, is_vm_active, is_vm_exists, is_volume_exists, is_snapshot_exists, \
    is_pool_exists, _get_pool_info, get_pool_info, get_vol_info_by_qemu
from utils import logger
from utils.uit_utils import is_block_dev_exists
from utils.utils import get_address_set_info, get_spec, get_field_in_kubernetes_by_index, deleteVmi, createVmi, deleteVmdi, createVmdi, updateDescription, updateJsonRemoveLifecycle, \
    updateDomain, Domain, get_l2_network_info, get_l3_network_info, randomMAC, ExecuteException, \
    updateJsonRemoveLifecycle, \
    addPowerStatusMessage, addExceptionMessage, report_failure, deleteLifecycleInJson, randomUUID, now_to_timestamp, \
    now_to_datetime, now_to_micro_time, get_hostname_in_lower_case, UserDefinedEvent, report_success, \
    add_spec_in_volume


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
PLURAL_VM_NETWORK = config_raw.get('VirtualMachineNetwork', 'plural')
VERSION_VM_NETWORK = config_raw.get('VirtualMachineNetwork', 'version')
GROUP_VM_NETWORK = config_raw.get('VirtualMachineNetwork', 'group')

PLURAL_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'plural')
VERSION_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'version')
GROUP_VM_DISK_IMAGE = config_raw.get('VirtualMachineDiskImage', 'group')

PLURAL_VM_DISK_SNAPSHOT = config_raw.get('VirtualMachineDiskSnapshot', 'plural')
VERSION_VM_DISK_SNAPSHOT = config_raw.get('VirtualMachineDiskSnapshot', 'version')
GROUP_VM_DISK_SNAPSHOT = config_raw.get('VirtualMachineDiskSnapshot', 'group')

FORCE_SHUTDOWN_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'stopVMForce')
RESET_VM = config_raw.get('VirtualMachineSupportCmdsWithDomainField', 'resetVM')

PLURAL_VM_POOL = config_raw.get('VirtualMahcinePool', 'plural')
VERSION_VM_POOL = config_raw.get('VirtualMahcinePool', 'version')
GROUP_VM_POOL = config_raw.get('VirtualMahcinePool', 'group')

DEFAULT_STORAGE_DIR = config_raw.get('DefaultStorageDir', 'default')
DEFAULT_DEVICE_DIR = config_raw.get('DefaultDeviceDir', 'default')
DEFAULT_SNAPSHOT_DIR = config_raw.get('DefaultSnapshotDir', 'snapshot')
DEFAULT_VMD_TEMPLATE_DIR = config_raw.get('DefaultVirtualMachineDiskTemplateDir', 'vmdi')

DEFAULT_VM_TEMPLATE_DIR = config_raw.get('DefaultTemplateDir', 'default')

L2NETWORKSUPPORTCMDS = []
for k,v in config_raw.items('L2NetworkSupportCmdsWithNameField'):
    L2NETWORKSUPPORTCMDS.append(k)
L3NETWORKSUPPORTCMDS = []
for k,v in config_raw.items('L3NetworkSupportCmdsWithNameField'):
    L3NETWORKSUPPORTCMDS.append(k)
for k,v in config_raw.items('L3NetworkSupportCmdsWithSwitchField'):
    L3NETWORKSUPPORTCMDS.append(k)

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
        thread_6 = Thread(target=vMDiskSnapshotWatcher)
        thread_6.daemon = True
        thread_6.name = 'vm_disk_snapshot_watcher'
        thread_6.start()
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
                (jsondict, operations_queue) \
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
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
                                        
#                                 file_path = '%s/%s-*' % (DEFAULT_DEVICE_DIR, metadata_name)
#                                 mvNICXmlToTmpDir(file_path)
                            # add support python file real path to exec
                    '''
                    Run operations
                    '''
                    if operations_queue:
                        for operation in operations_queue:
                            logger.debug(operation)
                            if operation.find('kubeovn-adm unbind-swport') != -1:
                                try:
                                    runCmd(operation)
                                except:
                                    pass
                            else:
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
                    if not _isDeleteVM(the_cmd_key) and not _isMigrateVM(the_cmd_key):
                        write_result_to_server(group, version, 'default', plural, metadata_name)
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
                # logger.debug(jsondict)
                if not pool_name:
                    pool_name = get_field_in_kubernetes_by_index(metadata_name, group, version, plural, ['spec', 'volume', 'pool'])
                    logger.debug(pool_name)
                if _isCreateDiskFromDiskImage(the_cmd_key):
#                     image_name = _get_field(jsondict, the_cmd_key, "sourceImage")
#                     source_pool_name = get_field_in_kubernetes_by_index(image_name, group, version, PLURAL_VM_DISK_IMAGE, ['spec', 'volume', 'pool'])
#                     jsondict = _set_field(jsondict, the_cmd_key, 'sourcePool', source_pool_name)
                    pool_name = _get_field(jsondict, the_cmd_key, 'targetPool')
                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                # logger.debug(jsondict)
                cmd = unpackCmdFromJson(jsondict, the_cmd_key)
                if cmd.find('backing-vol-format') >= 0:
                    cmd = cmd.replace('backing-vol-format', 'backing_vol_format')
                if cmd.find('backing-vol') >= 0:
                    cmd = cmd.replace('backing-vol', 'backing_vol')
                if cmd.find('full-copy') >= 0:
                    cmd = cmd.replace('full-copy', 'full_copy')
    #             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
    #             body = jsondict['raw_object']
    #             try:
    #                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
    #             except:
    #                 logger.warning('Oops! ', exc_info=1)
                try:
                    if not disk_type or not pool_name:
                        raise ExecuteException('VirtctlError', "parameters \"type\" and \"pool\" must be set")
                    if operation_type == 'ADDED':
                        if cmd:
                            if cmd.find("kubesds-adm") >= 0:
                                logger.debug(cmd)
                                _, data = None, None
                                if not is_kubesds_disk_exists(disk_type, pool_name, metadata_name):
                                    _, data = runCmdWithResult(cmd)
                                else:
                                    _, data = get_kubesds_disk_info(disk_type, pool_name, metadata_name)
                            else:
                                runCmd(cmd)
                                _, data = get_kubesds_disk_info(disk_type, pool_name, metadata_name)
                    elif operation_type == 'MODIFIED':
                        _, data = None, None
                        try:
                            if cmd.find("kubesds-adm") >= 0:
                                result, data = runCmdWithResult(cmd, raise_it=False)
                                if result['code'] != 0:
                                    raise ExecuteException('virtctl', 'error when operate volume ' + result['msg'])
                            else:
                                logger.debug(cmd)
                                runCmd(cmd)
                                _, data = get_kubesds_disk_info(disk_type, pool_name, metadata_name)
                        except Exception, e:
                            if _isDeleteDisk(the_cmd_key) and result['code'] != 221 and not is_kubesds_disk_exists(disk_type, pool_name, metadata_name):
                                logger.warning("***Disk %s not exists, delete it from virtlet" % metadata_name)
                                # jsondict = deleteLifecycleInJson(jsondict)
                                # try:
                                #     modifyStructure(metadata_name, jsondict, group, version, plural)
                                # except Exception:
                                #     pass
                                # time.sleep(0.5)
                                # if the disk path is alive, do not delete (the reason maybe caused by give the wrong poolname)
                                DISK_PATH = get_disk_path_from_server(metadata_name)
                                if DISK_PATH is None or not os.path.exists(DISK_PATH):
                                    deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                else:
                                    raise e
                            else:
                                raise e
                        # update disk info
                        if _isCloneDisk(the_cmd_key) or _isCreateDiskFromDiskImage(the_cmd_key):
                            # uus disk type register to server by hand
                            _, data = get_kubesds_disk_info(disk_type, pool_name, metadata_name)
                            newname = getCloneDiskName(the_cmd_key, jsondict)
                            _, newdata = get_kubesds_disk_info(disk_type, pool_name, newname)
                            addResourceToServer(the_cmd_key, jsondict, newname, newdata, group, version, plural)
                        elif _isDeleteDisk(the_cmd_key):
                            try:
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            except:
                                pass
#                     elif operation_type == 'DELETED':
#                         if pool_name and is_volume_exists(metadata_name, pool_name):
#                             if cmd:
#                                 runCmd(cmd)
#                         else:
#                             raise ExecuteException('VirtctlError', 'No vol %s in pool %s!' % (metadata_name, pool_name))
                    status = 'Done(Success)'
                    if not _isDeleteDisk(the_cmd_key) and not _isCloneDisk(the_cmd_key):
                        write_result_to_server(group, version, 'default', plural, metadata_name, data=data)
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
                sourcePool = _get_field(jsondict, the_cmd_key, 'sourcePool')
                if not sourcePool:
                    sourcePool = get_field_in_kubernetes_by_index(metadata_name, group, version, plural, ['spec', 'volume', 'pool'])
                    jsondict = _set_field(jsondict, the_cmd_key, 'sourcePool', sourcePool)
#                 (jsondict, operation_queue, rollback_operation_queue) \
#                     = _vmdi_prepare_step(the_cmd_key, jsondict, metadata_name)
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
                                # jsondict = deleteLifecycleInJson(jsondict)
                                # modifyStructure(metadata_name, jsondict, group, version, plural)
                                # time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
#                     elif operation_type == 'DELETED':
#                         if cmd:
#                             runCmd(cmd)
#                         '''
#                         Run operations
#                         '''
#                         if operation_queue:
#                             index = 0
#                             for operation in operation_queue:
#                                 logger.debug(operation)
#                                 try:
#                                     runCmd(operation)
#                                 except ExecuteException, e:
#                                     if index >= len(rollback_operation_queue):
#                                         index = len(rollback_operation_queue)
#                                     operations_rollback_queue = rollback_operation_queue[:index]
#                                     operations_rollback_queue.reverse()
#                                     for operation in operations_rollback_queue:
#                                         logger.debug("do rollback: %s" % operation)
#                                         try:
#                                             runCmd(operation)
#                                         except:
#                                             logger.debug('Oops! ', exc_info=1)
#                                     raise e
#                                 index += 1
#                                 time.sleep(1)
                    status = 'Done(Success)'
                    if not _isDeleteDiskImage(the_cmd_key):
                        write_result_to_server(group, version, 'default', plural, metadata_name)
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
                
def vMDiskSnapshotWatcher(group=GROUP_VM_DISK_SNAPSHOT, version=VERSION_VM_DISK_SNAPSHOT, plural=PLURAL_VM_DISK_SNAPSHOT):
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
                involved_object_kind = 'VirtualMachineDiskSnapshot'
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
                vol_name = _get_field(jsondict, the_cmd_key, 'vol')
                jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
                cmd = unpackCmdFromJson(jsondict, the_cmd_key)
    #             jsondict = _injectEventIntoLifecycle(jsondict, event.to_dict())
    #             body = jsondict['raw_object']
    #             try:
    #                 client.CustomObjectsApi().replace_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural, name=metadata_name, body=body)
    #             except:
    #                 logger.warning('Oops! ', exc_info=1)
                try:
                    if disk_type is None or pool_name is None or vol_name is None:
                        raise ExecuteException('VirtctlError', "parameters \"type\", \"pool\" and \"vol\" must be set")
                    if operation_type == 'ADDED':
                        _, data = None, None
                        if not is_kubesds_disk_snapshot_exists(disk_type, pool_name, vol_name, metadata_name):
                            _, data = runCmdWithResult(cmd)
                        else:
                            _, data = get_kubesds_disk_snapshot_info(disk_type, pool_name, vol_name, metadata_name)
                    elif operation_type == 'MODIFIED':
                        try:
                            backing_file = get_backing_file_from_k8s(metadata_name)
                            logger.debug(backing_file)
                            if backing_file is None and not os.path.isfile(backing_file):
                                raise ExecuteException('', 'error: cant get backing file from k8s.')
                            _, data = None, None
                            _, data = runCmdWithResult('%s --backing_file %s' % (cmd, backing_file))
                            # if is_kubesds_disk_snapshot_exists(disk_type, pool_name, vol_name, os.path.basename(backing_file)):
                            #     _, data = runCmdWithResult('%s --backing_file %s' % (cmd, backing_file))
                            # else:
                            #     _, data = get_kubesds_disk_snapshot_info(disk_type, pool_name, vol_name, metadata_name)
                        except Exception, e:
                            if _isDeleteDiskExternalSnapshot(the_cmd_key):
                                if backing_file is None or not os.path.isfile(backing_file):
                                    logger.warning("***Disk snapshot %s not exists, delete it from virtlet" % metadata_name)
                                    # jsondict = deleteLifecycleInJson(jsondict)
                                    # modifyStructure(metadata_name, jsondict, group, version, plural)
                                    # time.sleep(0.5)
                                    deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
#                     elif operation_type == 'DELETED':
#                         if cmd:
#                             runCmd(cmd)
                    status = 'Done(Success)'
                    if _isDeleteDiskExternalSnapshot(the_cmd_key):
                        if data:
                            if 'delete_ss' in data.keys() and data['delete_ss']:
                                for delete_ss in data['delete_ss']:
                                    try:
                                        deleteStructure(delete_ss, V1DeleteOptions(), group, version, plural)
                                    except ApiException, e:
                                        if e.reason == 'Not Found':
                                            logger.debug('**Object %s already deleted.' % delete_ss)
                            if 'need_to_modify' in data.keys() and data['need_to_modify']:
                                try:
                                    modify_snapshot(data['pool'], data['disk'], data['need_to_modify'], group, version, plural)
                                except Exception:
                                    pass
                    else:
                        write_result_to_server(group, version, 'default', plural, metadata_name, data=data,
                                               the_cmd_key=the_cmd_key)
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
                                # jsondict = deleteLifecycleInJson(jsondict)
                                # modifyStructure(metadata_name, jsondict, group, version, plural)
                                # time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
#                     elif operation_type == 'DELETED':
#                         if is_vm_active(metadata_name):
#                             destroy(metadata_name)
#                         if cmd:
#                             runCmd(cmd)
                    status = 'Done(Success)'
                    if not _isDeleteVMImage(the_cmd_key):
                        write_result_to_server(group, version, 'default', plural, metadata_name)
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
                (jsondict, snapshot_operations_queue, snapshot_operations_rollback_queue) = _vm_snapshot_prepare_step(the_cmd_key, jsondict, metadata_name)
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
                                # jsondict = deleteLifecycleInJson(jsondict)
                                # modifyStructure(metadata_name, jsondict, group, version, plural)
                                # time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
                    '''
                    Run snapshot operations
                    '''
                    if snapshot_operations_queue:
                        index = 0
                        for operation in snapshot_operations_queue:
                            logger.debug(operation)
                            try:
                                runCmd(operation)
                            except ExecuteException, e:
                                if index >= len(snapshot_operations_rollback_queue):
                                    index = len(snapshot_operations_rollback_queue)
                                snapshot_operations_rollback_queue = snapshot_operations_rollback_queue[:index]
                                snapshot_operations_rollback_queue.reverse()
                                for operation in snapshot_operations_rollback_queue:
                                    logger.debug("do rollback: %s" % operation)
                                    try:
                                        runCmd(operation)
                                    except:
                                        logger.debug('Oops! ', exc_info=1)
                                raise e
                            index += 1
                            time.sleep(1)
#                     elif operation_type == 'DELETED':
# #                         if vm_name and is_snapshot_exists(metadata_name, vm_name):
#                         if cmd:
#                             runCmd(cmd)
                    status = 'Done(Success)'
                    if not _isDeleteVMSnapshot(the_cmd_key):
                        write_result_to_server(group, version, 'default', plural, metadata_name)
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
                            if _isDeleteNetwork(the_cmd_key) or _isDeleteBridge(the_cmd_key):
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                        except Exception, e:
                            if _isDeleteNetwork(the_cmd_key) or _isDeleteBridge(the_cmd_key):
                                logger.warning("***Network %s not exists, delete it from virtlet" % metadata_name)
                                # jsondict = deleteLifecycleInJson(jsondict)
                                # modifyStructure(metadata_name, jsondict, group, version, plural)
                                # time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
                    elif operation_type == 'DELETED':
                        if cmd:
                            runCmd(cmd)
                    status = 'Done(Success)'
                    if not _isDeleteNetwork(the_cmd_key) and not _isDeleteBridge(the_cmd_key) and not _isDeleteAddress(the_cmd_key):
                        if _isCreateBridge(the_cmd_key) or _isSetBridgeVlan(the_cmd_key):
                            name = _get_field(jsondict, the_cmd_key, "name")
                        write_result_to_server(group, version, 'default', plural, metadata_name, the_cmd_key=the_cmd_key, obj_name=name)
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
                try:
                    if operation_type == 'ADDED':
                        # judge pool path exist or not

                        # POOL_PATH = getPoolPathWhenCreate(jsondict)
                        # # file_dir = os.path.split(POOL_PATH)[0]
                        # if not os.path.isdir(POOL_PATH):
                        #     os.makedirs(POOL_PATH)
                        if not is_kubesds_pool_exists(pool_type, pool_name):
                            _, poolJson = runCmdWithResult(cmd)
                            logger.debug('create pool')
                        else:
                            _, poolJson = get_kubesds_pool_info(pool_type, pool_name)
                            logger.debug('get pool info')
                    elif operation_type == 'MODIFIED':
                        try:
                            if _isDeletePool(the_cmd_key):
                                result, _ = runCmdWithResult(cmd, raise_it=False)
                                # fix pool type not match
                                if result['code'] == 0:
                                    deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                                else:
                                    raise ExecuteException('virtctl', 'error when delete pool ' + result['msg'])
                            else:
                                if pool_type == 'uus':
                                    pass
                                else:
                                    runCmd(cmd)
                        except Exception, e:
                            # only two case has exception when delete pool
                            # case 1: pool exist but not pool type not match(code is 221)
                            # case 2: pool not exist, only this case delete pool info from api server
                            if _isDeletePool(the_cmd_key) and result['code'] != 221 and not is_kubesds_pool_exists(pool_type, pool_name):
                                logger.warning("***Pool %s not exists, delete it from virtlet" % metadata_name)
                                # jsondict = deleteLifecycleInJson(jsondict)
                                # modifyStructure(metadata_name, jsondict, group, version, plural)
                                # time.sleep(0.5)
                                deleteStructure(metadata_name, V1DeleteOptions(), group, version, plural)
                            else:
                                raise e
                        if not _isDeletePool(the_cmd_key):
                            result, poolJson = get_kubesds_pool_info(pool_type, pool_name)
                    # elif operation_type == 'DELETED':
                    #     if is_pool_exists(pool_name):
                    #         runCmd(cmd)
                    #     else:
                    #         raise ExecuteException('VirtctlError', 'Not exist '+pool_name+' pool!')
                    status = 'Done(Success)'
                    if not _isDeletePool(the_cmd_key):
                        write_result_to_server(group, version, 'default', plural,
                                               metadata_name, {'code': 0, 'msg': 'success'}, poolJson)
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


def get_disk_path_from_server(metadata_name):
    logger.debug("try get disk path from server")
    try:
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
            group=GROUP_VM_DISK, version=VERSION_VM_DISK, namespace='default', plural=PLURAL_VM_DISK,
            name=metadata_name)
        if 'volume' in jsondict['spec'].keys():
            return jsondict['spec']['volume']['current']
    except ApiException, e:
        if e.reason == 'Not Found':
            logger.debug('**Object %s already deleted.' % metadata_name)
            return
        else:
            raise e
    return None

def is_kubesds_pool_exists(type, pool):
    result, _ = runCmdWithResult('kubesds-adm showPool --type %s --pool %s' % (type, pool), False)
    if result['code'] == 0:
        return True
    return False

def is_kubesds_disk_exists(type, pool, vol):
    result, _ = runCmdWithResult('kubesds-adm showDisk --type %s --pool %s' % (type, pool), False)
    if result['code'] == 0:
        return True
    return False

def is_kubesds_disk_snapshot_exists(type, pool, vol, name):
    result, _ = runCmdWithResult('kubesds-adm showDiskSnapshot --type %s --pool %s --vol %s --name %s' % (type, pool, vol, name), False)
    if result['code'] == 0:
        return True
    return False

def get_kubesds_pool_info(type, pool):
    return runCmdWithResult('kubesds-adm showPool --type %s --pool %s' % (type, pool))

def get_kubesds_disk_info(type, pool, vol):
    return runCmdWithResult('kubesds-adm showDisk --type %s --pool %s --vol %s' % (type, pool, vol), raise_it=False)

def get_kubesds_disk_snapshot_info(type, pool, vol, name):
    return runCmdWithResult('kubesds-adm showDiskSnapshot --type %s --pool %s --vol %s --name %s' % (type, pool, vol, name), raise_it=False)

def deleteStructure(name, body, group, version, plural):
    retv = client.CustomObjectsApi().delete_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def get_backing_file_from_k8s(name):
    try:
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
            group=GROUP_VM_DISK_SNAPSHOT, version=VERSION_VM_DISK_SNAPSHOT, namespace='default', plural=PLURAL_VM_DISK_SNAPSHOT, name=name)
        return jsondict['spec']['volume']['full_backing_filename']
    except Exception:
        return None

def write_result_to_server(group, version, namespace, plural, name, result=None, data=None, the_cmd_key=None, obj_name=None):
    jsonDict = None
    try:
        # involved_object_name actually is nodeerror occurred during processing json data from apiserver
        try:
            jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
                group=group, version=version, namespace=namespace, plural=plural, name=name)
        except ApiException, e:
            if e.reason == 'Not Found':
                logger.debug('**Object %s already deleted.' % name)
                return
            else:
                raise e
        # logger.debug(dumps(jsonStr))
#         logger.debug("node name is: " + name)
        jsonDict = jsonStr.copy()
        
        if plural == PLURAL_VM_NETWORK:
            if the_cmd_key in L3NETWORKSUPPORTCMDS:
                if the_cmd_key.endswith('Address'):
                    net_type = 'l3address'
                    retv = get_address_set_info(name)
                else:
                    net_type = 'l3network'
                    retv = get_l3_network_info(name)
            else:
                net_type = 'l2network'
                if obj_name:
                    retv = get_l2_network_info(obj_name)
                else:
                    retv = get_l2_network_info(name)
            jsonDict['spec'] = {'nodeName': get_hostname_in_lower_case(), 'data': retv, 'type': net_type}
        elif plural == PLURAL_VM_POOL:
            jsonDict['spec']['pool'] = data
        elif plural == PLURAL_VM_DISK:   
            jsonDict['spec']['volume'] = data
        elif plural == PLURAL_VM_DISK_SNAPSHOT:
            if _isRevertDiskExternalSnapshot(the_cmd_key) or _isCreateDiskExternalSnapshot(the_cmd_key):
                modify_disk(data['pool'], data['disk'], GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
            if _isCreateDiskExternalSnapshot(the_cmd_key):
                jsonDict['spec']['volume'] = data
        elif plural == PLURAL_VM:
            vm_xml = get_xml(name)
            vm_power_state = vm_state(name).get(name)
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            vm_json = updateJsonRemoveLifecycle(jsonDict, vm_json)
            jsonDict = addPowerStatusMessage(vm_json, vm_power_state, 'The VM is %s' % vm_power_state)

        if result:
            jsonDict = addPowerStatusMessage(jsonDict, result.get('code'), result.get('msg'))
        elif plural != PLURAL_VM:
            jsonDict = addPowerStatusMessage(jsonDict, 'Ready', 'The resource is ready.')
        if jsonDict['spec'].get('lifecycle'):
            del jsonDict['spec']['lifecycle']
        jsonDict = updateDescription(jsonDict)
        try:
            client.CustomObjectsApi().replace_namespaced_custom_object(
                group=group, version=version, namespace='default', plural=plural, name=name, body=jsonDict)
        except ApiException, e:
            if e.reason == 'Conflict':
                logger.debug('**Other process updated %s, ignore this 409 error.' % name)
                return
            else:
                raise e
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        raise ExecuteException('VirtctlError', 'write result to apiserver failure: %s' % info[1])

def modify_disk(pool, name, group, version, plural):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
                                                                      version=version,
                                                                      namespace='default',
                                                                      plural=plural,
                                                                      name=name)
    if os.path.isfile(get_pool_info(pool)['path'] + '/' + name + '/config.json'):
        with open(get_pool_info(pool)['path'] + '/' + name + '/config.json', "r") as f:
            config = load(f)
            vol_json = {'volume': get_vol_info_by_qemu(config['current'])}
            logger.debug(config['current'])
            vol_json = add_spec_in_volume(vol_json, 'current', config['current'])
            vol_json = add_spec_in_volume(vol_json, 'disk', name)
            vol_json = add_spec_in_volume(vol_json, 'pool', pool)
        jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
        body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
        try:
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            logger.debug(traceback.format_exc())
            if e.reason == 'Conflict':
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
                                                                                  version=version,
                                                                                  namespace='default',
                                                                                  plural=plural,
                                                                                  name=name)
                jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
                body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                modifyStructure(name, body, group, version, plural)
            else:
                logger.error(e)

def modify_snapshot(pool, disk, ss_path, group, version, plural):
    if os.path.isfile(ss_path):
        name = os.path.basename(ss_path)
        volume = get_vol_info_by_qemu(ss_path)
        volume['pool'] = pool
        volume['disk'] = disk
        vol_json = {'volume': volume}

        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
                                                                          version=version,
                                                                          namespace='default',
                                                                          plural=plural,
                                                                          name=name)
        jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
        body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
        try:
            modifyStructure(name, body, group, version, plural)
        except ApiException, e:
            if e.reason == 'Conflict':
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
                                                                                  version=version,
                                                                                  namespace='default',
                                                                                  plural=plural,
                                                                                  name=name)
                jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
                body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                modifyStructure(name, body, group, version, plural)
            else:
                logger.error(e)

def modifyStructure(name, body, group, version, plural):
    body = updateDescription(body)
    try:
        retv = client.CustomObjectsApi().replace_namespaced_custom_object(
            group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    except ApiException, e:
        if e.reason == 'Conflict':
            logger.debug('**Other process updated %s, ignore this 409 error.' % name)
            return None
        else:
            raise e
    return retv

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
    operations_queue = []
    balloon_operation_queue = []
    network_operations_queue = []
    disk_operations_queue = []
    graphic_operations_queue = []
    redefine_vm_operations_queue = []
    vm_password_operations_queue = []
    if _isInstallVMFromISO(the_cmd_key):
        balloon_operation_queue = ['virsh dommemstat --period %s --domain %s --config --live' % (str(5), metadata_name)]
        '''
        Parse network configurations
        '''
        network_config = _get_field(jsondict, the_cmd_key, 'network')
        config_dict = _network_config_parser(network_config)
        logger.debug(config_dict)
        network_operations_queue = _get_network_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = _set_field(jsondict, the_cmd_key, 'network', 'none')
    if _isInstallVMFromImage(the_cmd_key):
        balloon_operation_queue = ['virsh dommemstat --period %s --domain %s --config --live' % (str(5), metadata_name)]
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
    if _isSetVncPassword(the_cmd_key) or _isUnsetVncPassword(the_cmd_key):
        '''
        Parse graphic configurations
        '''
        config_dict = _get_fields(jsondict, the_cmd_key)
        logger.debug(config_dict)
        graphic_operations_queue = _get_graphic_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)
    if _isSetBootOrder(the_cmd_key):
        config_dict = _get_fields(jsondict, the_cmd_key)
        logger.debug(config_dict)
        redefine_vm_operations_queue = _get_redefine_vm_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)      
    if _isSetGuestPassword(the_cmd_key):
        config_dict = _get_fields(jsondict, the_cmd_key)
        logger.debug(config_dict)
        vm_password_operations_queue = _get_vm_password_operations_queue(the_cmd_key, config_dict, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)     
    operations_queue.extend(balloon_operation_queue)
    operations_queue.extend(network_operations_queue)
    operations_queue.extend(disk_operations_queue)
    operations_queue.extend(graphic_operations_queue)
    operations_queue.extend(redefine_vm_operations_queue)
    operations_queue.extend(vm_password_operations_queue)
    return (jsondict, operations_queue)

def _vm_snapshot_prepare_step(the_cmd_key, jsondict, metadata_name):
    domain = _get_field(jsondict, the_cmd_key, "domain")
    isExternal = _get_field(jsondict, the_cmd_key, "isExternal")
    if not isExternal:
        return (jsondict, [], [])
    elif isExternal and is_vm_active(domain) and not _isCreateSnapshot(the_cmd_key):
        raise ExecuteException('VirtctlError', '400, Bad Request. Cannot operate external snapshot when vm is running.')
    (snapshot_operations_queue, snapshot_operations_rollback_queue) = _get_snapshot_operations_queue(jsondict, the_cmd_key, domain, metadata_name)
    jsondict = deleteLifecycleInJson(jsondict)
    return (jsondict, snapshot_operations_queue, snapshot_operations_rollback_queue)

def _vmdi_prepare_step(the_cmd_key, jsondict, metadata_name):
    target = _get_field(jsondict, the_cmd_key, "target")
    if not target:
        raise ExecuteException('VirtctlError', 'Missing parameter "target".')
    (operation_queue, rollback_operation_queue) = _get_vmdi_operations_queue(jsondict, the_cmd_key, target, metadata_name)
    jsondict = deleteLifecycleInJson(jsondict)
    return (jsondict, operation_queue, rollback_operation_queue)

def _vmi_prepare_step(the_cmd_key, jsondict, metadata_name):
    operation_queue = []
    rollback_operation_queue = []
    target = _get_field(jsondict, the_cmd_key, "target")
    if target:
        (operation_queue, rollback_operation_queue) = _get_vmi_operations_queue(jsondict, the_cmd_key, target, metadata_name)
        jsondict = deleteLifecycleInJson(jsondict)
    return (jsondict, operation_queue, rollback_operation_queue)

def _isCreateSwitch(the_cmd_key):
    if the_cmd_key == "createSwitch":
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
    spec = get_spec(jsondict)
    lifecycle = spec.get('lifecycle')

    if lifecycle:
        return lifecycle['createPool']['target']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No metadata name!')

def getPoolType(the_cmd_key, jsondict):
    spec = get_spec(jsondict)
    lifecycle = spec.get('lifecycle')
    
    if lifecycle and 'type' in lifecycle[the_cmd_key].keys():
        return lifecycle[the_cmd_key]['type']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No found pool type!')


def getDesturi(the_cmd_key, jsondict):
    spec = get_spec(jsondict)
    lifecycle = spec.get('lifecycle')

    if lifecycle and 'desturi' in lifecycle[the_cmd_key].keys():
        return lifecycle[the_cmd_key]['desturi']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No found desturi!')

def getCloneDiskName(the_cmd_key, jsondict):
    spec = get_spec(jsondict)
    lifecycle = spec.get('lifecycle')

    if lifecycle:
        return lifecycle[the_cmd_key]['newname']
    else:
        raise ExecuteException('VirtctlError', 'FATAL ERROR! No found clone disk name!')

def forceUsingMetadataName(metadata_name, the_cmd_key, jsondict):
    spec = get_spec(jsondict)
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
        spec = get_spec(jsondict)
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

def addResourceToServer(the_cmd_key, jsondict, newname, newdata, group, version, plural):
    jsoncopy = jsondict.copy()
    jsoncopy['raw_object']['kind'] = 'VirtualMachineDisk'
    jsoncopy['raw_object']['metadata']['kind'] = 'VirtualMachineDisk'
    jsoncopy['raw_object']['metadata']['name'] = newname
    jsoncopy['raw_object']['spec']['volume'] = newdata
    del jsoncopy['raw_object']['metadata']['resourceVersion']
    if jsoncopy['raw_object']['spec'].get('lifecycle'):
        del jsoncopy['raw_object']['spec']['lifecycle']
    jsoncopy = jsoncopy.get('raw_object')
    try:
        body = updateDescription(jsoncopy)
        client.CustomObjectsApi().create_namespaced_custom_object(group=group, version=version, namespace='default', plural=plural,  body=body)
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        raise ExecuteException('VirtctlError', 'write result to apiserver failure: %s' % info[1])

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

def _isCreateDiskExternalSnapshot(the_cmd_key):
    if the_cmd_key == "createDiskExternalSnapshot":
        return True
    return False

def _isDeleteVM(the_cmd_key):
    if the_cmd_key == "deleteVM":
        return True
    return False

def _isMigrateVM(the_cmd_key):
    if the_cmd_key == "migrateVM":
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

def _isCreateBridge(the_cmd_key):
    if the_cmd_key == "createBridge":
        return True
    return False

def _isSetBridgeVlan(the_cmd_key):
    if the_cmd_key == "setBridgeVlan":
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

# def _isConvertDiskImageToDisk(the_cmd_key):
#     if the_cmd_key == "convertDiskImageToDisk":
#         return True
#     return False

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
    spec = get_spec(jsondict)
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
    spec = get_spec(jsondict)
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return None
        if the_cmd_key:
            spec['lifecycle'][the_cmd_key][field] = value
    return jsondict 

def _del_field(jsondict, the_cmd_key, field):
    spec = get_spec(jsondict)
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
                    del spec['lifecycle'][the_cmd_key][k]
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
    if not os.path.exists(DEFAULT_DEVICE_DIR):
        os.makedirs(DEFAULT_DEVICE_DIR, 0711)
    file_path = '%s/%s-graphic.xml' % (DEFAULT_DEVICE_DIR, metadata_name)
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
                raise ExecuteException('VirtctlError', 'Network config error: no "switch" parameter.')
            plugNICCmd = _plugDeviceFromXmlCmd(metadata_name, 'nic', config_dict, args)
            if _isPlugNIC(the_cmd_key) and not is_vm_active(metadata_name):
                unbindSwPortCmd = ''
                bindSwPortCmd = ''
            else:
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
                                (DEFAULT_DEVICE_DIR, metadata_name, config_dict.get('mac').replace(':', ''))
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
            raise ExecuteException('VirtctlError', 'Wrong parameters "os_type" %s.' % os_type)
        if not user or not password:
            raise ExecuteException('VirtctlError', 'Wrong parameters "user" or "password".')
        if not boot_disk_path:
            raise ExecuteException('VirtctlError', 'Cannot get boot disk of domain %s' % metadata_name)
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

def _get_snapshot_operations_queue(jsondict, the_cmd_key, domain, metadata_name):
    if _isCreateSnapshot(the_cmd_key):
        jsondict = _del_field(jsondict, the_cmd_key, 'isExternal')
        disk_spec = _get_field(jsondict, the_cmd_key, 'diskspec')
        if not disk_spec:
            raise ExecuteException('VirtctlError', 'Missing parameter "diskspec".')
        jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
        cmd = unpackCmdFromJson(jsondict, the_cmd_key)
        snapshot_paths = _get_paths_from_diskspec(disk_spec)
        cmd1 = 'kubesds-adm updateDiskCurrent --type dir --current %s' % snapshot_paths
        return ([cmd, cmd1], [])
    elif _isMergeSnapshot(the_cmd_key):
        domain_obj = Domain(_get_dom(domain))
        (merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.merge_snapshot(metadata_name)
        return ([merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd], [])
    elif _isRevertVirtualMachine(the_cmd_key):
        domain_obj = Domain(_get_dom(domain))
#         (merge_snapshots_cmd, _, _) = domain_obj.merge_snapshot(metadata_name)
        (unplug_disks_cmd, unplug_disks_rollback_cmd, plug_disks_cmd, plug_disks_rollback_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.revert_snapshot(metadata_name)
        return ([unplug_disks_cmd, plug_disks_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd], [unplug_disks_rollback_cmd, plug_disks_rollback_cmd])
    elif _isDeleteVMSnapshot(the_cmd_key):
        domain_obj = Domain(_get_dom(domain))
        (unplug_disks_cmd, unplug_disks_rollback_cmd, plug_disks_cmd, plug_disks_rollback_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd) = domain_obj.revert_snapshot(metadata_name, True)
        return ([unplug_disks_cmd, plug_disks_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd], [unplug_disks_rollback_cmd, plug_disks_rollback_cmd])
    else:
        return ([], [])
    
def _get_vmdi_operations_queue(jsondict, the_cmd_key, target, metadata_name):
    operation_queue = []
    rollback_operation_queue = []
#     if _isConvertDiskToDiskImage(the_cmd_key) or _isCreateVmdi(the_cmd_key):
# #         (operation_queue, rollback_operation_queue) = createVmdi(metadata_name, target)
#         jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
#         cmd = unpackCmdFromJson(jsondict, the_cmd_key)
#         operation_queue.append(cmd)
#         return (operation_queue, rollback_operation_queue)
    if _isDeleteVmdi(the_cmd_key):
#         (operation_queue, rollback_operation_queue) = deleteVmdi(metadata_name, target)
        jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
        cmd = unpackCmdFromJson(jsondict, the_cmd_key)
        operation_queue.append(cmd)
    else:
        return (operation_queue, rollback_operation_queue)
    
def _get_vmi_operations_queue(jsondict, the_cmd_key, target, metadata_name):
    operation_queue = []
    rollback_operation_queue = []
    if _isConvertVMToImage(the_cmd_key) or _isCreateImage(the_cmd_key):
        (operation_queue, rollback_operation_queue) = createVmi(metadata_name, target)
        jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
        cmd = unpackCmdFromJson(jsondict, the_cmd_key)
        operation_queue.append(cmd)
        return (operation_queue, rollback_operation_queue)
    elif _isDeleteImage(the_cmd_key):
        (operation_queue, rollback_operation_queue) = deleteVmi(metadata_name, target)
        jsondict = forceUsingMetadataName(metadata_name, the_cmd_key, jsondict)
        cmd = unpackCmdFromJson(jsondict, the_cmd_key)
        operation_queue.append(cmd)
    else:
        return (operation_queue, rollback_operation_queue)

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
            raise ExecuteException('VirtctlError', 'Missing parameter "order".')
        orders = boot_order.replace(' ', '').split(',')
        if not orders:
            raise ExecuteException('VirtctlError', 'Unsupported parameter "order=%s".' % boot_order)
        for order in orders:
            if not runCmd('virsh domblklist %s | grep %s' % (metadata_name, order)):
                raise ExecuteException('VirtctlError', 'Virtual machine %s has no device named "%s".' % (metadata_name, order))
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
        file_path = '%s/%s-nic-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, data.get('mac').replace(':', ''))
        if not os.path.exists(file_path):
            if data.get('type') in ['bridge', 'l2bridge', 'l3bridge']:
                net_type = 'bridge'
            else:
                net_type = data.get('type')
            return 'virsh detach-interface --domain %s --type %s --mac %s %s' (metadata_name, net_type, data.get('mac'), args)
    elif device_type == 'disk':
        file_path = '%s/%s-disk-%s.xml' % (DEFAULT_DEVICE_DIR, metadata_name, data.get('target'))
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
                            raise ExecuteException('VirtctlError', '400, Bad Request. Non-supported parameter "%s".' % v)
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
        if key.startswith("_"):
            key = str(key).replace('_', '')
        if key == 'leaves':
            return ('--%s' % key.replace('_', '-'), value.replace(' ', ''))
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
            logger.debug(std_out)
        if std_err:
            logger.error(std_err)
            raise ExecuteException('VirtctlError', std_err)
        return std_out
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
def runCmdWithResult(cmd, raise_it=True):
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
            msg = msg.replace("'", '"')
            logger.debug(msg)
            try:
                result = loads(msg)
                # print result
                if result['result']['code'] != 0 and raise_it:
                    raise ExecuteException('VirtctlError', result['result']['msg'])
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
