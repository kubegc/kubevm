# -*- coding: utf-8 -*-
'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
@author: liuhe18@otcaix.iscas.ac.cn
'''
import json

'''
Import python libs
'''
import time
import traceback
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
from utils.libvirt_util import get_pool_path, get_volume_path, refresh_pool, get_volume_xml, get_snapshot_xml, is_vm_exists, get_xml, \
    vm_state, _get_all_pool_path, get_vol_info_by_qemu
from utils import logger
from utils import constants
from utils.misc import create_custom_object, delete_custom_object, get_custom_object, update_custom_object, add_spec_in_volume, updateDescription, addSnapshots, get_volume_snapshots, runCmdRaiseException, \
    addPowerStatusMessage, updateDomainSnapshot, updateDomain, report_failure, get_hostname_in_lower_case, \
    DiskImageHelper

GROUP = constants.KUBERNETES_GROUP
VERSION = constants.KUBERNETES_API_VERSION
VM_KIND = constants.KUBERNETES_KIND_VM
VMD_KIND = constants.KUBERNETES_KIND_VMD
VMDSN_KIND = constants.KUBERNETES_KIND_VMDSN
VMDI_KIND = constants.KUBERNETES_KIND_VMDI
VMSN_KIND = constants.KUBERNETES_KIND_VMSN
VMDEV_KIND = constants.KUBERNETES_KIND_VMDEV
VMI_KIND = constants.KUBERNETES_KIND_VMI

TOKEN = constants.KUBERNETES_TOKEN_FILE
PLURAL_VM = constants.KUBERNETES_PLURAL_VM
PLURAL_VM_DISK = constants.KUBERNETES_PLURAL_VMD
PLURAL_VM_DISK_SS = constants.KUBERNETES_PLURAL_VMDSN
PLURAL_VM_DISK_IMAGE = constants.KUBERNETES_PLURAL_VMDI
LIBVIRT_XML_DIR = constants.KUBEVMM_LIBVIRT_VM_XML_DIR

HOSTNAME = get_hostname_in_lower_case()
logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTLET_LOG)


def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)


def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
        'interface', '_interface').replace('transient', '_transient').replace(
        'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk',
                                                                                      'suspend_to_disk')


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
            jsondict = get_custom_object(group, version, plural, name)
            #             vol_xml = get_volume_xml(pool, name)
            #             vol_json = toKubeJson(xmlToJson(vol_xml))
            jsondict = updateJsonRemoveLifecycle(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            update_custom_object(group, version, plural, name, body)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM disk %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm disk %s, report to virtlet' % name)
            delete_custom_object(group, version, plural, name)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM disk %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
    elif event == "Create":
        try:
            logger.debug('Create vm disk %s, report to virtlet' % name)
            jsondict = {'spec': {'volume': {}, 'nodeName': HOSTNAME, 'status': {}},
                        'kind': VMD_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
                        'apiVersion': '%s/%s' % (group, version)}
            with open(get_pool_path(pool) + '/' + name + '/config.json', "r") as f:
                config = json.load(f)
                volume = get_vol_info_by_qemu(config['current'])
                volume["pool"] = config['pool']
                volume["poolname"] = pool
                volume["uni"] = config['current']
                volume['disk'] = name
                volume['current'] = config['current']
                vol_json = {'volume': volume}
                vol_json = add_spec_in_volume(vol_json, 'current', config['current'])
            jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            try:
                create_custom_object(group, version, plural, body)
            except ApiException as e:
                logger.error(e)

        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                jsondict = get_custom_object(group, version, plural, name)
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    elif event == "Modify":
        try:
            logger.debug('Modify vm disk %s current, report to virtlet' % name)
            jsondict = get_custom_object(group, version, plural, name)
            with open(get_pool_path(pool) + '/' + name + '/config.json', "r") as f:
                config = json.load(f)
                volume = get_vol_info_by_qemu(config['current'])
                volume["pool"] = config['pool']
                volume["poolname"] = pool
                volume["uni"] = config['current']
                volume['disk'] = name
                volume['current'] = config['current']
                vol_json = {'volume': volume}
                logger.debug(config['current'])
                vol_json = add_spec_in_volume(vol_json, 'current', config['current'])
            jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            try:
                update_custom_object(group, version, plural, name, body)
            except ApiException as e:
                logger.error(e)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                jsondict = get_custom_object(group, version, plural, name)
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    else:
        refresh_pool(pool)
        jsondict = get_custom_object(group, version, plural, name)
        try:
            pass
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)

# def myVmVolSnapshotEventHandler(event, pool, ss_path, name, group, version, plural):
#     #     print(jsondict)
#     if event == "Delete":
#         try:
#             refresh_pool(pool)
#             jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                               version=version,
#                                                                               namespace='default',
#                                                                               plural=plural,
#                                                                               name=name)
#             #             vol_xml = get_volume_xml(pool, name)
#             #             vol_json = toKubeJson(xmlToJson(vol_xml))
#             jsondict = updateJsonRemoveLifecycle(jsondict, {})
#             body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#             modifyStructure(name, body, group, version, plural)
#         except ApiException as e:
#             if e.reason == 'Not Found':
#                 logger.debug('**VM disk %s already deleted, ignore this 404 error.' % name)
#             else:
#                 info = sys.exc_info()
#                 try:
#                     report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#                 except:
#                     logger.warning('Oops! ', exc_info=1)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)
#         try:
#             logger.debug('Delete vm disk snapshot %s, report to virtlet' % name)
#             deleteStructure(name, V1DeleteOptions(), group, version, plural)
#         except ApiException as e:
#             if e.reason == 'Not Found':
#                 logger.debug('**VM disk snapshot %s already deleted, ignore this 404 error.' % name)
#             else:
#                 info = sys.exc_info()
#                 try:
#                     report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#                 except:
#                     logger.warning('Oops! ', exc_info=1)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)
#     elif event == "Create":
#         try:
#             logger.debug('Create vm disk snapshot %s, report to virtlet' % name)
#             jsondict = {'spec': {'volume': {}, 'nodeName': HOSTNAME, 'status': {}},
#                         'kind': VMDSN_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
#                         'apiVersion': '%s/%s' % (group, version)}
#
#             volume = get_vol_info_by_qemu(ss_path)
#             volume["poolname"] = pool
#             volume["uni"] = ss_path
#             volume['disk'] = name
#             volume['current'] = ss_path
#             vol_json = {'volume': volume}
#             current = DiskImageHelper.get_backing_file(ss_path)
#             vol_json = add_spec_in_volume(vol_json, 'current', current)
#             jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
#             body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#             try:
#                 createStructure(body, group, version, plural)
#             except ApiException as e:
#                 if e.reason == 'Conflict':
#                     jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                                       version=version,
#                                                                                       namespace='default',
#                                                                                       plural=plural,
#                                                                                       name=name)
#                     jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
#                     body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#                     modifyStructure(name, body, group, version, plural)
#                 else:
#                     logger.error(e)
#
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                                   version=version,
#                                                                                   namespace='default',
#                                                                                   plural=plural,
#                                                                                   name=name)
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.error('Oops! ', exc_info=1)
#     elif event == "Modify":
#         try:
#             logger.debug('Modify vm disk snapshot %s current, report to virtlet' % name)
#             jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                               version=version,
#                                                                               namespace='default',
#                                                                               plural=plural,
#                                                                               name=name)
#             volume = get_vol_info_by_qemu(ss_path)
#             volume["poolname"] = pool
#             volume["uni"] = ss_path
#             volume['disk'] = name
#             volume['current'] = ss_path
#             vol_json = {'volume': volume}
#             current = DiskImageHelper.get_backing_file(ss_path)
#             vol_json = add_spec_in_volume(vol_json, 'current', current)
#             jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
#             body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#             try:
#                 modifyStructure(name, body, group, version, plural)
#             except ApiException as e:
#                 if e.reason == 'Conflict':
#                     jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                                       version=version,
#                                                                                       namespace='default',
#                                                                                       plural=plural,
#                                                                                       name=name)
#                     jsondict = updateJsonRemoveLifecycle(jsondict, vol_json)
#                     body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#                     modifyStructure(name, body, group, version, plural)
#                 else:
#                     logger.error(e)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                                   version=version,
#                                                                                   namespace='default',
#                                                                                   plural=plural,
#                                                                                   name=name)
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.error('Oops! ', exc_info=1)
#     else:
#         refresh_pool(pool)
#         jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
#                                                                           version=version,
#                                                                           namespace='default',
#                                                                           plural=plural,
#                                                                           name=name)
#         try:
#             pass
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)

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
            logger.debug("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
            # filename = os.path.basename(event.src_path)
            # if filename == 'config.json':
            #     with open(event.src_path, "r") as f:
            #         config = json.load(f)
            #     vol = config['name']
            #     try:
            #         myVmVolEventHandler('Create', self.pool, vol, self.group, self.version, self.plural)
            #     except ApiException:
            #         logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            # filename = os.path.basename(event.src_path)
            # if filename == 'config.json':
            #     vol = os.path.basename(os.path.dirname(event.src_path))
            #     try:
            #         myVmVolEventHandler('Delete', self.pool, vol, self.group, self.version, self.plural)
            #     except ApiException:
            #         logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
            logger.debug("directory modified:{0}".format(event.src_path))
        else:
            pass
#             logger.debug("file modified:{0}".format(event.src_path))
            # filename = os.path.basename(event.src_path)
            # if filename == 'config.json':
            #     logger.debug("change config.json file: %s" % event.src_path)
            #     with open(event.src_path, "r") as f:
            #         config = json.load(f)
            #     vol = config['name']
            #     try:
            #         myVmVolEventHandler('Modify', self.pool, vol, self.group, self.version, self.plural)
            #     except ApiException:
            #         logger.error('Oops! ', exc_info=1)

                # maybe rebase current, try modify current snapshot
                # try:
                #     myVmVolSnapshotEventHandler('Modify', self.pool, config['current'],
                #                 os.path.basename(config['current']), self.group, self.version, self.plural)
                # except ApiException:
                #     logger.error('Oops! ', exc_info=1)


def myVmSnapshotEventHandler(event, vm, name, group, version, plural):
    #     print(jsondict)
    if event == "Delete":
        try:
            jsondict = get_custom_object(group, version, plural, name)
            #             snap_xml = get_snapshot_xml(vm, name)
            #             snap_json = toKubeJson(xmlToJson(snap_xml))
            #             snap_json = updateDomainSnapshot(loads(snap_json))
            jsondict = updateJsonRemoveLifecycle(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            update_custom_object(group, version, plural, name, body)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM snapshot %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm snapshot %s, report to virtlet' % name)
            delete_custom_object(group, version, plural, name)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM snapshot %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
    elif event == "Create":
        try:
            logger.debug('Create vm snapshot %s, report to virtlet' % name)
            jsondict = {'spec': {'domainsnapshot': {}, 'nodeName': HOSTNAME, 'status': {}},
                        'kind': VMSN_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
                        'apiVersion': '%s/%s' % (group, version)}
            snap_xml = get_snapshot_xml(vm, name)
            snap_json = toKubeJson(xmlToJson(snap_xml))
            snap_json = updateDomainSnapshot(loads(snap_json))
            jsondict = updateJsonRemoveLifecycle(jsondict, snap_json)
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            try:
                create_custom_object(group, version, plural, body)
            except ApiException as e:
                logger.error(e)

        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                jsondict = get_custom_object(group, version, plural, name)
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    else:
        try:
            jsondict = get_custom_object(group, version, plural, name)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
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
            logger.debug("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path, event.dest_path))
            dirs, snap_file = os.path.split(event.dest_path)
            _, vm = os.path.split(dirs)
            snap, file_type = os.path.splitext(snap_file)
            if file_type == '.xml':
                try:
                    myVmSnapshotEventHandler('Create', vm, snap, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))

    #             dirs,snap_file = os.path.split(event.src_path)
    #             _,vm = os.path.split(dirs)
    #             snap, file_type = os.path.splitext(snap_file)
    #             if file_type == '.xml':
    #                 try:
    #                     myVmSnapshotEventHandler('Create', vm, snap, self.group, self.version, self.plural)
    #                 except ApiException:
    #                     logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            dirs, snap_file = os.path.split(event.src_path)
            _, vm = os.path.split(dirs)
            snap, file_type = os.path.splitext(snap_file)
            if file_type == '.xml':
                try:
                    myVmSnapshotEventHandler('Delete', vm, snap, self.group, self.version, self.plural)
                except ApiException:
                    logger.error('Oops! ', exc_info=1)

    def on_modified(self, event):
        if event.is_directory:
            logger.debug("directory modified:{0}".format(event.src_path))
        else:
            logger.debug("file modified:{0}".format(event.src_path))


# def myVmBlockDevEventHandler(event, name, group, version, plural):
#     #     print(jsondict)
#     if event == "Delete":
#         try:
#             jsondict = get_custom_object(group, version, plural, name)
#             #             block_json = get_block_dev_json(name)
#             jsondict = updateJsonRemoveLifecycle(jsondict, {})
#             body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#             update_custom_object(group, version, plural, name, body)
#         except ApiException as e:
#             if e.reason == 'Not Found':
#                 logger.debug('**VM block device %s already deleted, ignore this 404 error.' % name)
#             else:
#                 info = sys.exc_info()
#                 try:
#                     report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#                 except:
#                     logger.warning('Oops! ', exc_info=1)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)
#         try:
#             logger.debug('Delete vm block %s, report to virtlet' % name)
#             delete_custom_object(group, version, plural, name)
#         except ApiException as e:
#             if e.reason == 'Not Found':
#                 logger.debug('**VM block %s already deleted, ignore this 404 error.' % name)
#             else:
#                 info = sys.exc_info()
#                 try:
#                     report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#                 except:
#                     logger.warning('Oops! ', exc_info=1)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)
#     elif event == "Create":
#         try:
#             logger.debug('Create vm block %s, report to virtlet' % name)
#             jsondict = {'spec': {'REPLACE': {}, 'nodeName': HOSTNAME, 'status': {}},
#                         'kind': VMDEV_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
#                         'apiVersion': '%s/%s' % (group, version)}
#             block_json = get_block_dev_json(name)
#             jsondict = updateJsonRemoveLifecycle(jsondict, loads(block_json))
#             body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
#             try:
#                 create_custom_object(group, version, plural, body)
#             except ApiException as e:
#                 logger.error(e)
# 
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 jsondict = get_custom_object(group, version, plural, name)
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.error('Oops! ', exc_info=1)
#     else:
#         try:
#             jsondict = get_custom_object(group, version, plural, name)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)
# 
# 
# class VmBlockDevEventHandler(FileSystemEventHandler):
#     def __init__(self, field, target, group, version, plural):
#         FileSystemEventHandler.__init__(self)
#         self.field = field
#         self.target = target
#         self.group = group
#         self.version = version
#         self.plural = plural
# 
#     def on_moved(self, event):
#         if event.is_directory:
#             logger.debug("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
#         else:
#             logger.debug("file moved from {0} to {1}".format(event.src_path, event.dest_path))
# 
#     def on_created(self, event):
#         if event.is_directory:
#             logger.debug("directory created:{0}".format(event.src_path))
#         else:
#             logger.debug("file created:{0}".format(event.src_path))
#             path, block = os.path.split(event.src_path)
#             if is_block_dev_exists(event.src_path) and path != "/dev/mapper":
#                 try:
#                     myVmBlockDevEventHandler('Create', block, self.group, self.version, self.plural)
#                 except ApiException:
#                     logger.error('Oops! ', exc_info=1)
# 
#     def on_deleted(self, event):
#         if event.is_directory:
#             logger.debug("directory deleted:{0}".format(event.src_path))
#         else:
#             logger.debug("file deleted:{0}".format(event.src_path))
#             path, block = os.path.split(event.src_path)
#             #             if is_block_dev_exists(event.src_path):
#             if path == '/dev/pts':
#                 logger.debug('Ignore devices %s' % event.src_path)
#             else:
#                 try:
#                     myVmBlockDevEventHandler('Delete', block, self.group, self.version, self.plural)
#                 except ApiException:
#                     logger.error('Oops! ', exc_info=1)
# 
#     def on_modified(self, event):
#         if event.is_directory:
#             #             logger.debug("directory modified:{0}".format(event.src_path))
#             pass
#         else:
#             #             logger.debug("file modified:{0}".format(event.src_path))
#             pass

def _solve_conflict_in_VM(name, group, version, plural):
    for i in range(1, 6):
        try:
            jsondict = get_custom_object(group, version, plural, name)
            jsondict['metadata']['labels']['host'] = HOSTNAME
            vm_xml = get_xml(name)
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            body = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            body = addNodeName(jsondict)
            update_custom_object(group, version, plural, name, body)
            return
        except Exception as e:
            if i == 5:
                raise e

def myVmLibvirtXmlEventHandler(event, name, xml_path, group, version, plural):
    #     print(jsondict)
    if event == "Create":
        try:
            logger.debug('***Create VM %s from back-end, report to virtlet***' % name)
            jsondict = {'spec': {'domain': {}, 'nodeName': HOSTNAME, 'status': {}},
                        'kind': VM_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
                        'apiVersion': '%s/%s' % (group, version)}
            vm_xml = get_xml(name)
            vm_power_state = vm_state(name).get(name)
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            jsondict = addPowerStatusMessage(jsondict, vm_power_state, 'The VM is %s' % vm_power_state)
            body = addNodeName(jsondict)
            try:
                create_custom_object(group, version, plural, body)
            except ApiException as e:
                if e.reason == 'Conflict':
                    _solve_conflict_in_VM(name, group, version, plural)
                else:
                    logger.error(e)

        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                jsondict = get_custom_object(group, version, plural, name)
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    elif event == "Modify":
        jsondict = get_custom_object(group, version, plural, name)
        try:
            if jsondict['metadata']['labels']['host'] != HOSTNAME:
                logger.debug('VM %s is migrating, ignore modify.' % name)
                return
            logger.debug('***Modify VM %s from back-end, report to virtlet***' % name)
            vm_xml = get_xml(name)
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            body = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            update_custom_object(group, version, plural, name, body)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
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
        logger.debug('***Delete VM %s, ignore it***' % name)
#         time.sleep(1)
#         try:
#             jsondict = get_custom_object(group, version, plural, name)
#             if jsondict['metadata']['labels']['host'] != HOSTNAME:
#                 logger.debug('VM %s is migrating or ha, ignore delete.' % name)
#                 return
#             #             vm_xml = get_xml(name)
#             #             vm_json = toKubeJson(xmlToJson(vm_xml))
#             #             vm_json = updateDomain(loads(vm_json))
#             body = updateDomainStructureAndDeleteLifecycleInJson(jsondict, {})
#             update_custom_object(group, version, plural, name, body)
#         except ApiException as e:
#             if e.reason == 'Not Found':
#                 logger.debug('**VM %s already deleted, ignore this 404 error.' % name)
#             else:
#                 info = sys.exc_info()
#                 try:
#                     report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#                 except:
#                     logger.warning('Oops! ', exc_info=1)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)
#         try:
#             delete_custom_object(group, version, plural, name)
#         #                 vm_xml = get_xml(name)
#         #                 vm_json = toKubeJson(xmlToJson(vm_xml))
#         #                 vm_json = updateDomain(loads(vm_json))
#         #                 jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
#         #                 body = addExceptionMessage(jsondict, 'VirtletError', 'VM has been deleted in back-end.')
#         #                 modifyStructure(name, body, group, version, plural)
#         except ApiException as e:
#             if e.reason == 'Not Found':
#                 logger.debug('**VM %s already deleted, ignore this 404 error.' % name)
#             else:
#                 info = sys.exc_info()
#                 try:
#                     report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#                 except:
#                     logger.warning('Oops! ', exc_info=1)
#         except:
#             logger.error('Oops! ', exc_info=1)
#             info = sys.exc_info()
#             try:
#                 report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
#             except:
#                 logger.warning('Oops! ', exc_info=1)


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
            logger.debug("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path, event.dest_path))
            _, name = os.path.split(event.dest_path)
            vm, file_type = os.path.splitext(name)
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
            _, name = os.path.split(event.src_path)
            vm, file_type = os.path.splitext(name)
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
            _, name = os.path.split(event.src_path)
            vm, file_type = os.path.splitext(name)
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
                        'kind': VMDI_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
                        'apiVersion': '%s/%s' % (group, version)}
            vmd_xml = get_volume_xml(pool, name)
            vol_path = get_volume_path(pool, name)
            vmd_json = toKubeJson(xmlToJson(vmd_xml))
            vmd_json = addSnapshots(vol_path, loads(vmd_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vmd_json)
            jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            body = addNodeName(jsondict)
            try:
                create_custom_object(group, version, plural, body)
            except ApiException as e:
                logger.error(e)

        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                jsondict = get_custom_object(group, version, plural, name)
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    elif event == "Delete":
        try:
            '''
            Refresh pool manually
            '''
            refresh_pool(pool)
            jsondict = get_custom_object(group, version, plural, name)
            #             with open(xml_path, 'r') as fr:
            #                 vm_xml = fr.read()
            #             vmd_json = toKubeJson(xmlToJson(vm_xml))
            #             vmd_json = updateDomain(loads(vmd_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            update_custom_object(group, version, plural, name, body)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM disk image %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm disk image %s, report to virtlet' % name)
            delete_custom_object(group, version, plural, name)
        #                 jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vmd_json)
        #                 body = addExceptionMessage(jsondict, 'VirtletError', 'VM has been deleted in back-end.')
        #                 modifyStructure(name, body, group, version, plural)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM disk image %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)


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
            logger.debug("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path, event.dest_path))
            vmdi = os.path.split(event.src_path)[1]
            try:
                myVmdImageLibvirtXmlEventHandler('Create', vmdi, self.pool, event.dest_path, self.group, self.version,
                                                 self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_created(self, event):
        if event.is_directory:
            logger.debug("directory created:{0}".format(event.src_path))
        else:
            logger.debug("file created:{0}".format(event.src_path))
            vmdi = os.path.split(event.src_path)[1]
            try:
                myVmdImageLibvirtXmlEventHandler('Create', vmdi, self.pool, event.src_path, self.group, self.version,
                                                 self.plural)
            except ApiException:
                logger.error('Oops! ', exc_info=1)

    def on_deleted(self, event):
        if event.is_directory:
            logger.debug("directory deleted:{0}".format(event.src_path))
        else:
            logger.debug("file deleted:{0}".format(event.src_path))
            vmdi = os.path.split(event.src_path)[1]
            try:
                myVmdImageLibvirtXmlEventHandler('Delete', vmdi, self.pool, event.src_path, self.group, self.version,
                                                 self.plural)
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
                        'kind': VMI_KIND, 'metadata': {'labels': {'host': HOSTNAME}, 'name': name},
                        'apiVersion': '%s/%s' % (group, version)}
            with open(xml_path, 'r') as fr:
                vm_xml = fr.read()
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            body = addNodeName(jsondict)
            try:
                create_custom_object(group, version, plural, body)
            except ApiException as e:
                logger.error(e)

        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                jsondict = get_custom_object(group, version, plural, name)
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.error('Oops! ', exc_info=1)
    elif event == "Modify":
        jsondict = get_custom_object(group, version, plural, name)
        try:
            logger.debug('Modify vm image %s, report to virtlet' % name)
            with open(xml_path, 'r') as fr:
                vm_xml = fr.read()
            vm_json = toKubeJson(xmlToJson(vm_xml))
            vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            #             logger.debug(body)
            update_custom_object(group, version, plural, name, body)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
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
            jsondict = get_custom_object(group, version, plural, name)
            #             with open(xml_path, 'r') as fr:
            #                 vm_xml = fr.read()
            #             vm_json = toKubeJson(xmlToJson(vm_xml))
            #             vm_json = updateDomain(loads(vm_json))
            jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, {})
            body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            update_custom_object(group, version, plural, name, body)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM image %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)
        try:
            logger.debug('Delete vm image %s, report to virtlet' % name)
            delete_custom_object(group, version, plural, name)
        #                 jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
        #                 body = addExceptionMessage(jsondict, 'VirtletError', 'VM has been deleted in back-end.')
        #                 modifyStructure(name, body, group, version, plural)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**VM image %s already deleted, ignore this 404 error.' % name)
            else:
                info = sys.exc_info()
                try:
                    report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
        except:
            logger.error('Oops! ', exc_info=1)
            info = sys.exc_info()
            try:
                report_failure(name, jsondict, 'VirtletError', str(info[1]), group, version, plural)
            except:
                logger.warning('Oops! ', exc_info=1)


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
            logger.debug("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger.debug("file moved from {0} to {1}".format(event.src_path, event.dest_path))
            _, name = os.path.split(event.dest_path)
            vmi, file_type = os.path.splitext(name)
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
            _, name = os.path.split(event.src_path)
            vmi, file_type = os.path.splitext(name)
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
            _, name = os.path.split(event.src_path)
            vmi, file_type = os.path.splitext(name)
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
        #         os.makedirs(ob[1], 0x0711)
        #         try:
        #             runCmdRaiseException('virsh pool-create-as --name %s --type dir --target %s' % (ob[0], ob[1]))
        #         except:
        #             os.removedirs(ob[1])
        #             logger.error('Oops! ', exc_info=1)
        #     event_handler = VmVolEventHandler(ob[0], ob[1], GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
        #     observer.schedule(event_handler,ob[1],True)
        # for ob in SYSTEM_VOL_DIRS:
        #     if not os.path.exists(ob[1]):
        #         os.makedirs(ob[1], 0x0711)
        #     event_handler = VmVolEventHandler(ob[0], ob[1], GROUP_VM_DISK, VERSION_VM_DISK, PLURAL_VM_DISK)
        #     observer.schedule(event_handler,ob[1],True)
#         for ob in SNAP_DIRS:
#             if not os.path.exists(ob[1]):
#                 os.makedirs(ob[1], 0x0711)
#             event_handler = VmSnapshotEventHandler(ob[0], ob[1], GROUP_VM_SNAPSHOT, VERSION_VM_SNAPSHOT,
#                                                    PLURAL_VM_SNAPSHOT)
#             observer.schedule(event_handler, ob[1], True)
        #         for ob in BLOCK_DEV_DIRS:
        #             if not os.path.exists(ob[1]):
        #                 os.makedirs(ob[1], 0x0711)
        #             event_handler = VmBlockDevEventHandler(ob[0], ob[1], GROUP_BLOCK_DEV_UIT, VERSION_BLOCK_DEV_UIT, PLURAL_BLOCK_DEV_UIT)
        #             observer.schedule(event_handler,ob[1],True)
        for ob in constants.KUBEVMM_LIBVIRT_VM_XML_DIR:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0x0711)
            event_handler = VmLibvirtXmlEventHandler(ob[0], ob[1], GROUP, VERSION, PLURAL_VM)
            observer.schedule(event_handler, ob[1], True)
#         for ob in TEMPLATE_DIRS:
#             if not os.path.exists(ob[1]):
#                 os.makedirs(ob[1], 0x0711)
#             event_handler = ImageLibvirtXmlEventHandler(ob[0], ob[1], GROUP_VMI, VERSION_VMI, PLURAL_VMI)
#             observer.schedule(event_handler, ob[1], True)
        for ob in constants.KUBEVMM_DEFAULT_VMDI_DIR:
            if not os.path.exists(ob[1]):
                os.makedirs(ob[1], 0x0711)
                try:
                    runCmdRaiseException('virsh pool-create-as --name %s --type dir --target %s' % (ob[0], ob[1]))
                except:
                    os.removedirs(ob[1])
                    logger.error('Oops! ', exc_info=1)
            event_handler = VmdImageLibvirtXmlEventHandler(ob[0], ob[1], GROUP, VERSION,
                                                           PLURAL_VM_DISK_IMAGE)
            observer.schedule(event_handler, ob[1], True)
        observer.start()

        OLD_PATH_WATCHERS = {}
        while True:
            try:
                paths = _get_all_pool_path()
                for pool_name, pool_path in paths.items():
                    content_file = '%s/content' % pool_path
                    if os.path.exists(content_file):
                        with open(content_file, 'r') as fr:
                            pool_content = fr.read().strip()
                        if pool_content != 'vmd':
                            del paths[pool_name]
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
                        event_handler = VmVolEventHandler(pool, paths[pool], GROUP, VERSION,
                                                          PLURAL_VM_DISK)
                        watcher = observer.schedule(event_handler, paths[pool], True)
                        OLD_PATH_WATCHERS[paths[pool]] = watcher
            except Exception as e:
                logger.debug(traceback.print_exc())
                logger.debug("error occur when watch all storage pool")
                time.sleep(3)

            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except:
        logger.warning('Oops! ', exc_info=1)
    observer.join()


if __name__ == "__main__":
    config.load_kube_config(config_file=TOKEN)
    while True:
        try:
            main()
        except Exception as e:
            if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1:
                config.load_kube_config(config_file=TOKEN)
            info=sys.exc_info()
            logger.error('Oops! ', exc_info=1)
            time.sleep(5)
            continue
