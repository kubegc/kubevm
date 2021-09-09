# -*- coding: utf-8 -*-
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''

'''
Import python libs
'''
import os
import sys
import time
import threading
from threading import Thread
from json import loads

'''
Import third party libs
'''
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.client import V1DeleteOptions
from libvirt import libvirtError

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
from utils import logger
from utils import constants
from utils.exception import InternalServerError, NotFound, Forbidden, BadRequest
from utils.conf_parser import UserDefinedParser
from utils.kubernetes_event_utils import KubernetesEvent
from services.executor import Executor
from services.convertor import toCmds

from utils.misc import get_label_selector, report_failure

TOKEN = constants.KUBERNETES_TOKEN_FILE    
logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTCTL_LOG)

create_vm_mutex = threading.Lock()            
start_vm_mutex = threading.Lock()
stop_vm_mutex = threading.Lock()
reboot_vm_mutex = threading.Lock()
destroy_vm_mutex = threading.Lock()
delete_vm_mutex = threading.Lock()
reset_vm_mutex = threading.Lock()
suspend_vm_mutex = threading.Lock()
migrate_vm_mutex = threading.Lock()

def main():
    '''将Kubernetes资源监听器运行在python子进程里.
    '''
    logger.debug("---------------------------------------------------------------------------------")
    logger.debug("------------------------Welcome to Virtctl Daemon.-------------------------------")
    logger.debug("------Copyright (2021, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn,wuheng@otcaix.iscas.ac.cn-----------")
    logger.debug("---------------------------------------------------------------------------------")

    logger.debug("Loading configurations in 'constants.py' ...")
    logger.debug("All support CMDs are:")
    logger.debug(UserDefinedParser().get_all_support_cmds())
    try:
        thread_1 = Thread(target=doWatch, args=(constants.KUBERNETES_PLURAL_VM, constants.KUBERNETES_KIND_VM,))
        thread_1.daemon = True
        thread_1.name = 'vm_watcher'
        thread_1.start()
        thread_2 = Thread(target=doWatch, args=(constants.KUBERNETES_PLURAL_VMD, constants.KUBERNETES_KIND_VMD,))
        thread_2.daemon = True
        thread_2.name = 'vm_disk_watcher'
        thread_2.start()
        thread_3 = Thread(target=doWatch, args=(constants.KUBERNETES_PLURAL_VMDI, constants.KUBERNETES_KIND_VMDI,))
        thread_3.daemon = True
        thread_3.name = 'vm_disk_image_watcher'
        thread_3.start()
        thread_4 = Thread(target=doWatch, args=(constants.KUBERNETES_PLURAL_VMDSN, constants.KUBERNETES_KIND_VMDSN,))
        thread_4.daemon = True
        thread_4.name = 'vm_disk_snapshot_watcher'
        thread_4.start()
        thread_5 = Thread(target=doWatch, args=(constants.KUBERNETES_PLURAL_VMN, constants.KUBERNETES_KIND_VMN,))
        thread_5.daemon = True
        thread_5.name = 'vm_network_watcher'
        thread_5.start()
        thread_6 = Thread(target=doWatch, args=(constants.KUBERNETES_PLURAL_VMP, constants.KUBERNETES_KIND_VMP,))
        thread_6.daemon = True
        thread_6.name = 'vm_pool_watcher'
        thread_6.start()
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
    except:
        logger.error('Oops! ', exc_info=1)
        
def doWatch(plural, k8s_object_kind):
    '''监听器的请求处理逻辑，请求封装在{'spec': {'lifecycle': {...}}}里。\
    lifecycle通过解析器convertor解析，并与constatns里的配置项匹配，转化成invoke cmd和query cmd。\
    处理器executor用于顺序执行invoke cmd和query cmd。 \
    executor的结果如果符合json规范，并包含关键字{'spec': {...}}，则会被写回到Kubernetes里。
    
    '''
    while True:
        watcher = watch.Watch()
        kwargs = {}
        kwargs['label_selector'] = get_label_selector()
        kwargs['watch'] = True
        kwargs['timeout_seconds'] = int(constants.KUBERNETES_WATCHER_TIME_OUT)
        try:
            for jsondict in watcher.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                        group=constants.KUBERNETES_GROUP, version=constants.KUBERNETES_API_VERSION, plural=plural, **kwargs):
                thread = Thread(target=doExecutor,args=(plural, k8s_object_kind, jsondict))
                thread.daemon = True
                thread.name = 'do_executor'
                thread.start()
        except Exception as e:
    #             master_ip = change_master_and_reload_config(fail_times)
            config.load_kube_config(config_file=TOKEN)
    #             fail_times += 1
    #             logger.debug('retrying another master %s, retry times: %d' % (master_ip, fail_times))
            info=sys.exc_info()
            logger.warning('Oops! ', exc_info=1)
#             vMWatcher(group=GROUP_VM, version=VERSION_VM, plural=PLURAL_VM)
            time.sleep(3)
            continue
        finally:
            watcher.stop()
        
def doExecutor(plural, k8s_object_kind, jsondict):
    operation_type = jsondict.get('type')
    logger.debug(operation_type)
    metadata_name = _getMetadataName(jsondict)
    logger.debug('metadata name: %s' % metadata_name)
    '''convertor'''
    (policy, the_cmd_key, prepare_cmd, invoke_cmd, query_cmd) = toCmds(jsondict)
    if the_cmd_key:
        _acquire_mutex_lock(the_cmd_key)
    try:
        if the_cmd_key and operation_type != 'DELETED':
            logger.debug("cmd key: %s, prepare cmd: %s, invoke cmd: %s, query cmd: %s" % (the_cmd_key, prepare_cmd, invoke_cmd, query_cmd))
            '''delete lifecycle in Kubernetes'''
            delete_lifecycle_in_kubernetes(plural, metadata_name)
            '''create Kubernetes event'''
            event_id = _getEventId(jsondict)
            event = KubernetesEvent(metadata_name, the_cmd_key, k8s_object_kind, event_id)
            event.create_event(constants.KUBEVMM_EVENT_LIFECYCLE_DOING, constants.KUBEVMM_EVENT_TYPE_NORMAL)
            try:
                if invoke_cmd:
                    '''executor'''
                    executor = Executor(policy, prepare_cmd, invoke_cmd, query_cmd)
                    _, data = executor.execute()
                '''write result'''
                write_result_to_kubernetes(plural, metadata_name, data)
                '''update Kubernetes event'''
                event.update_evet(constants.KUBEVMM_EVENT_LIFECYCLE_DONE, constants.KUBEVMM_EVENT_TYPE_NORMAL)
            except libvirtError:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    report_failure(metadata_name, jsondict, 'LibvirtError', str(info[1]), constants.KUBERNETES_GROUP, constants.KUBERNETES_API_VERSION, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
                event.update_evet(constants.KUBEVMM_EVENT_LIFECYCLE_DONE, constants.KUBEVMM_EVENT_TYPE_ERROR)
            except Exception as e:
                logger.error('Oops! ', exc_info=1)
                info=sys.exc_info()
                try:
                    if hasattr(e, 'reason'):
                        report_failure(metadata_name, jsondict, e.reason, e.message, constants.KUBERNETES_GROUP, constants.KUBERNETES_API_VERSION, plural)
                    else:
                        report_failure(metadata_name, jsondict, 'Exception', str(info[1]), constants.KUBERNETES_GROUP, constants.KUBERNETES_API_VERSION, plural)
                except:
                    logger.warning('Oops! ', exc_info=1)
                event.update_evet(constants.KUBEVMM_EVENT_LIFECYCLE_DONE, constants.KUBEVMM_EVENT_TYPE_ERROR)
            finally:
                if the_cmd_key:
                    _release_mutex_lock(the_cmd_key)
    except Exception as e:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        try:
            if hasattr(e, 'reason'):
                report_failure(metadata_name, jsondict, e.reason, e.message, constants.KUBERNETES_GROUP, constants.KUBERNETES_API_VERSION, plural)
            else:
                report_failure(metadata_name, jsondict, 'Exception', str(info[1]), constants.KUBERNETES_GROUP, constants.KUBERNETES_API_VERSION, plural)
        except:
            logger.warning('Oops! ', exc_info=1)

def _getMetadataName(jsondict):
    '''获取metadata name
    Returns:
        str: metadata name in Kubernetes
        
    '''
    metadata = jsondict['raw_object']['metadata']
    metadata_name = metadata.get('name')
    if metadata_name:
        return metadata_name
    else:
        raise BadRequest('FATAL ERROR! No metadata name!')
    
def _getEventId(jsondict):
    '''获取event id
    Returns:
        str: event id
    '''
    metadata = jsondict['raw_object'].get('metadata')
    labels = metadata.get('labels')
    logger.debug(labels)
    return labels.get('eventId') if labels.get('eventId') else '-1'

def _acquire_mutex_lock(the_cmd_key):
    if the_cmd_key == constants.CREATE_AND_START_VM_FROM_ISO_CMD or the_cmd_key == constants.CREATE_VM_CMD:
        create_vm_mutex.acquire()
    elif the_cmd_key == constants.START_VM_CMD:
        start_vm_mutex.acquire()
    elif the_cmd_key == constants.STOP_VM_CMD:
        stop_vm_mutex.acquire()
    elif the_cmd_key == constants.REBOOT_VM_CMD:
        reboot_vm_mutex.acquire()
    elif the_cmd_key == constants.STOP_VM_FORCE_CMD:
        destroy_vm_mutex.acquire()
    elif the_cmd_key == constants.DELETE_VM_CMD:
        delete_vm_mutex.acquire()
    elif the_cmd_key == constants.RESET_VM_CMD:
        reset_vm_mutex.acquire()
    elif the_cmd_key == constants.SUSPEND_VM_CMD:
        suspend_vm_mutex.acquire()
    elif the_cmd_key == constants.MIGRATE_VM_CMD:
        migrate_vm_mutex.acquire()
     
def _release_mutex_lock(the_cmd_key):
    if the_cmd_key == constants.CREATE_AND_START_VM_FROM_ISO_CMD or the_cmd_key == constants.CREATE_VM_CMD:
        create_vm_mutex.release()
    elif the_cmd_key == constants.START_VM_CMD:
        start_vm_mutex.release()
    elif the_cmd_key == constants.STOP_VM_CMD:
        stop_vm_mutex.release()
    elif the_cmd_key == constants.REBOOT_VM_CMD:
        reboot_vm_mutex.release()
    elif the_cmd_key == constants.STOP_VM_FORCE_CMD:
        destroy_vm_mutex.release()
    elif the_cmd_key == constants.DELETE_VM_CMD:
        delete_vm_mutex.release()
    elif the_cmd_key == constants.RESET_VM_CMD:
        reset_vm_mutex.release()
    elif the_cmd_key == constants.SUSPEND_VM_CMD:
        suspend_vm_mutex.release()
    elif the_cmd_key == constants.MIGRATE_VM_CMD:
        migrate_vm_mutex.release()

def write_result_to_kubernetes(plural, name, data):
    '''将executor的处理结果写回到Kubernetes里，处理结果必须是json格式，\
    并且符合{'spec':{...}}规范，如果传{'spec':{}}则代表从Kubernetes中删除该对象。
    '''
    jsonDict = None
    try:
        # involved_object_name actually is nodeerror occurred during processing json data from apiserver
        try:
            jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
                group=constants.KUBERNETES_GROUP, version=constants.KUBERNETES_API_VERSION, namespace='default', plural=plural, name=name)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**Object %s already deleted.' % name)
                return
            else:
                raise e
        jsonDict = jsonStr.copy()
        logger.debug(data)
        try:
            data = loads(data)
        except:
            logger.debug('Cannot write result to Kubernetes, because the output cannot convert to json')
        if isinstance(data, dict) and data.get('spec'):
            if data['spec']:
                jsonDict['spec'] = data['spec']
                try:
                    client.CustomObjectsApi().replace_namespaced_custom_object(
                        group=constants.KUBERNETES_GROUP, version=constants.KUBERNETES_API_VERSION, namespace='default', plural=plural, name=name, body=jsonDict)
                except ApiException as e:
                    if e.reason == 'Conflict':
                        logger.debug('**Other process updated %s, ignore this 409 message.' % name)
                        return
                    else:
                        raise e
            else:
                try:
                    client.CustomObjectsApi().delete_namespaced_custom_object(
                        group=constants.KUBERNETES_GROUP, version=constants.KUBERNETES_API_VERSION, namespace='default', plural=plural, name=name, body=V1DeleteOptions())
                except ApiException as e:
                    if e.reason == 'Not Found':
                        logger.debug('**Object %s already deleted, ignore this 404 message.' % name)
                        return
                    else:
                        raise e
        elif isinstance(data, dict) and not data.get('spec'):
            Forbidden('Wrong format in cmd results, only support "dict" with "spec" item, e.g. {"spec": {...}}. Please check the output of query cmd if exists, or the output of invoke cmd.')
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        raise InternalServerError('Write result to apiserver failed: %s %s' % (info[0], info[1]))

def delete_lifecycle_in_kubernetes(plural, name):
    '''删除lifecycle结构，避免推送程序更新Kubernetes时再次进入lifecycle的处理逻辑。
    '''
    jsonDict = None
    try:
        try:
            jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
                group=constants.KUBERNETES_GROUP, version=constants.KUBERNETES_API_VERSION, namespace='default', plural=plural, name=name)
        except ApiException as e:
            if e.reason == 'Not Found':
                logger.debug('**Object %s already deleted.' % name)
                return
            else:
                raise e
        # logger.debug(dumps(jsonStr))
#         logger.debug("node name is: " + name)
        jsonDict = jsonStr.copy()
        if jsonDict['spec'].get('lifecycle'):
            del jsonDict['spec']['lifecycle']
#         jsonDict = updateDescription(jsonDict)
        client.CustomObjectsApi().replace_namespaced_custom_object(
            group=constants.KUBERNETES_GROUP, version=constants.KUBERNETES_API_VERSION, namespace='default', plural=plural, name=name, body=jsonDict)
    except:
        logger.error('Oops! ', exc_info=1)
        info=sys.exc_info()
        raise InternalServerError('Write result to apiserver failed: %s %s' % (info[0], info[1]))

if __name__ == '__main__':
    config.load_kube_config(config_file=constants.KUBERNETES_TOKEN_FILE)
    main()
