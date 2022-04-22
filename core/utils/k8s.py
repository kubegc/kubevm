import socket
import time
import traceback
import operator
from json import dumps

import os, sys
from sys import exit

from kubernetes import client, config
from kubernetes.client import V1DeleteOptions
from kubernetes.client.rest import ApiException
import logging
import logging.handlers
from core.virtmonitor.virt_monitor_in_docker import PLURAL_VMP
from core.virtlet.services.os_event_handler import PLURAL_VM_DISK,\
    PLURAL_VM_DISK_IMAGE

try:
    from utils import constants
    from utils.exception import BadRequest
except:
    import constants
    from exception import BadRequest

TOKEN = constants.KUBERNETES_TOKEN_FILE
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

config.load_kube_config(config_file=TOKEN)

LOG = '/var/log/kubesds.log'

RETRY_TIMES = 15


def set_logger(header, fn):
    logger = logging.getLogger(header)

    handler1 = logging.StreamHandler()
    handler2 = logging.handlers.RotatingFileHandler(filename=fn, maxBytes=10000000, backupCount=10)

    logger.setLevel(logging.DEBUG)
    handler1.setLevel(logging.ERROR)
    handler2.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(name)s %(lineno)s %(levelname)s %(message)s")
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger


k8s_logger = set_logger(os.path.basename(__file__), LOG)

resources = {}
kind_plural = {VM_KIND:VM_PLURAL, VMP_KIND:VMP_PLURAL, VMD_KIND:VMD_PLURAL, 
               VMDI_KIND:VMDI_PLURAL, VMDSN_KIND:VMDSN_PLURAL}
for kind,plural in kind_plural.items():
    resource = {}
    resource['version'] = VERSION
    resource['group'] = GROUP
    resource['plural'] = plural
    resources[kind] = resource


def get(name, kind):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=resources[kind]['group'],
                                                                      version=resources[kind]['version'],
                                                                      namespace='default',
                                                                      plural=resources[kind]['plural'],
                                                                      name=name)
    return jsondict


def create(name, data, kind):
    hostname = get_hostname_in_lower_case()
    jsondict = {'spec': {'volume': {}, 'nodeName': hostname, 'status': {}},
                'kind': kind, 'metadata': {'labels': {'host': hostname}, 'name': name},
                'apiVersion': '%s/%s' % (resources[kind]['group'], resources[kind]['version'])}

    jsondict = updateJsonRemoveLifecycle(jsondict, data)
    body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')

    return client.CustomObjectsApi().create_namespaced_custom_object(
        group=resources[kind]['group'], version=resources[kind]['version'], namespace='default',
        plural=resources[kind]['plural'], body=body)


def update(name, data, kind):
    return client.CustomObjectsApi().replace_namespaced_custom_object(
        group=resources[kind]['group'], version=resources[kind]['version'], namespace='default',
        plural=resources[kind]['plural'], name=name, body=data)


def delete(name, data, kind):
    k8s_logger.debug('deleteVMBackupdebug %s' % name)
    return client.CustomObjectsApi().delete_namespaced_custom_object(
        group=resources[kind]['group'], version=resources[kind]['version'], namespace='default',
        plural=resources[kind]['plural'], name=name, body=data)


def addPowerStatusMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions': {'state': {'waiting': {'message': message, 'reason': reason}}}}
        spec = get_spec(jsondict)
        if spec:
            spec['status'] = status
    return jsondict


def get_spec(jsondict):
    spec = jsondict.get('spec')
    if not spec:
        raw_object = jsondict.get('raw_object')
        if raw_object:
            spec = raw_object.get('spec')
    return spec


def deleteLifecycleInJson(jsondict):
    if jsondict:
        spec = get_spec(jsondict)
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
    return jsondict


def updateJsonRemoveLifecycle(jsondict, body):
    if jsondict:
        spec = get_spec(jsondict)
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(body)
    return jsondict


def hasLifeCycle(jsondict):
    if jsondict:
        spec = get_spec(jsondict)
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                return True
    return False


def removeLifecycle(jsondict):
    if jsondict:
        spec = get_spec(jsondict)
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
    return jsondict


def get_hostname_in_lower_case():
    return 'vm.%s' % socket.gethostname().lower()


def changeNode(jsondict, newNodeName):
    if jsondict:
        jsondict['metadata']['labels']['host'] = newNodeName
        spec = get_spec(jsondict)
        if spec:
            nodeName = spec.get('nodeName')
            if nodeName:
                spec['nodeName'] = newNodeName
    return jsondict


def replaceData(jsondict):
    all_kind = {'VirtualMachine': 'domain',
                'VirtualMachinePool': 'pool',
                'VirtualMachineDisk': 'volume',
                'VirtualMachineDiskImage': 'volume',
                'VirtualMachineDiskSnapshot': 'volume',
                'VirtualMachineBackup': 'backup'}

    mkind = jsondict['kind']
    mn = jsondict['metadata']['name']
    k8s = K8sHelper(mkind)
    current = k8s.get(mn)

    host = jsondict['metadata']['labels']['host']
    # nodename = jsondicts[i]['metadata']['labels']['host']
    changeNode(current, host)

    if jsondict:
        key = all_kind[mkind]
        if 'spec' in jsondict.keys() and isinstance(jsondict['spec'], dict) and key in jsondict['spec'].keys():
            data = jsondict['spec'][key]
            if current:
                current['spec'][key] = data

    return current


def get_node_name(jsondict):
    if jsondict:
        return jsondict['metadata']['labels']['host']
    return None

def list_node():
    for i in range(RETRY_TIMES):
        try:
            config.load_kube_config(TOKEN)
            jsondict = client.CoreV1Api().list_node().to_dict()
            return jsondict
        except ApiException as e:
            if e.reason == 'Not Found':
                return False
            else:
                time.sleep(3)
        except Exception as e:
            if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                    'ApiException') != -1:
                config.load_kube_config(TOKEN)
            k8s_logger.debug(traceback.format_exc())
            k8s_logger.debug("sleep 3 sec")
            time.sleep(3)
    raise BadRequest('can not get node info from k8s.')


class K8sHelper(object):
    def __init__(self, kind):
        self.kind = kind

    def exist(self, name):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=resources[self.kind]['group'],
                                                                                  version=resources[self.kind][
                                                                                      'version'],
                                                                                  namespace='default',
                                                                                  plural=resources[self.kind]['plural'],
                                                                                  name=name)
                return True
            except ApiException as e:
                if e.reason == 'Not Found':
                    return False
                else:
                    time.sleep(3)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not get %s %s response from k8s.' % (self.kind, name))

    def get(self, name):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=resources[self.kind]['group'],
                                                                                  version=resources[self.kind][
                                                                                      'version'],
                                                                                  namespace='default',
                                                                                  plural=resources[self.kind]['plural'],
                                                                                  name=name)
                return jsondict
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)

        raise BadRequest('can not get %s %s on k8s.' % (self.kind, name))

    def get_data(self, name, key):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=resources[self.kind]['group'],
                                                                                  version=resources[self.kind][
                                                                                      'version'],
                                                                                  namespace='default',
                                                                                  plural=resources[self.kind]['plural'],
                                                                                  name=name)
                if 'spec' in jsondict.keys() and isinstance(jsondict['spec'], dict) and key in jsondict['spec'].keys():
                    return jsondict['spec'][key]
                return None
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                time.sleep(3)
        raise BadRequest('can not get %s %s on k8s.' % (self.kind, name))

    def get_create_jsondict(self, name, key, data):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                hostname = get_hostname_in_lower_case()
                jsondict = {'spec': {'volume': {}, 'nodeName': hostname, 'status': {}},
                            'kind': self.kind, 'metadata': {'labels': {'host': hostname}, 'name': name},
                            'apiVersion': '%s/%s' % (resources[self.kind]['group'], resources[self.kind]['version'])}

                jsondict = updateJsonRemoveLifecycle(jsondict, {key: data})
                body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                return body
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                time.sleep(3)
        raise BadRequest('can not get %s %s data on k8s.' % (self.kind, name))

    def create(self, name, key, data):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                if self.exist(name):
                    return
                hostname = get_hostname_in_lower_case()
                jsondict = {'spec': {'volume': {}, 'nodeName': hostname, 'status': {}},
                            'kind': self.kind, 'metadata': {'labels': {'host': hostname}, 'name': name},
                            'apiVersion': '%s/%s' % (resources[self.kind]['group'], resources[self.kind]['version'])}

                jsondict = updateJsonRemoveLifecycle(jsondict, {key: data})
                body = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')

                return client.CustomObjectsApi().create_namespaced_custom_object(
                    group=resources[self.kind]['group'], version=resources[self.kind]['version'], namespace='default',
                    plural=resources[self.kind]['plural'], body=body)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        error_print(500, 'can not create %s %s on k8s.' % (self.kind, name))

    def add_label(self, name, domain):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                if not self.exist(name):
                    return
                jsondict = self.get(name)
                jsondict['metadata']['labels']['domain'] = domain
                # jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                # jsondict = updateJsonRemoveLifecycle(jsondict, {key: data})
                return client.CustomObjectsApi().replace_namespaced_custom_object(
                    group=resources[self.kind]['group'], version=resources[self.kind]['version'], namespace='default',
                    plural=resources[self.kind]['plural'], name=name, body=jsondict)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not modify %s %s on k8s.' % (self.kind, name))

    def update(self, name, key, data):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                if not self.exist(name):
                    return
                jsondict = self.get(name)
                if 'spec' in jsondict.keys() and isinstance(jsondict['spec'], dict) and key in jsondict['spec'].keys() \
                        and operator.eq(jsondict['spec'][key], data) == 0:
                    return
                jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                jsondict = updateJsonRemoveLifecycle(jsondict, {key: data})
                return client.CustomObjectsApi().replace_namespaced_custom_object(
                    group=resources[self.kind]['group'], version=resources[self.kind]['version'], namespace='default',
                    plural=resources[self.kind]['plural'], name=name, body=jsondict)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not modify %s %s on k8s.' % (self.kind, name))

    def updateAll(self, name, jsondict):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                if not self.exist(name):
                    return
                jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                jsondict = deleteLifecycleInJson(jsondict)
                return client.CustomObjectsApi().replace_namespaced_custom_object(
                    group=resources[self.kind]['group'], version=resources[self.kind]['version'], namespace='default',
                    plural=resources[self.kind]['plural'], name=name, body=jsondict)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not modify %s %s on k8s.' % (self.kind, name))

    def createAll(self, name, jsondict):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                if self.exist(name):
                    return
                jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                jsondict = deleteLifecycleInJson(jsondict)
                return client.CustomObjectsApi().create_namespaced_custom_object(
                    group=resources[self.kind]['group'], version=resources[self.kind]['version'], namespace='default',
                    plural=resources[self.kind]['plural'], body=jsondict)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not modify %s %s on k8s.' % (self.kind, name))

    def delete(self, name):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                k8s_logger.debug('deleteVMBackupdebug %s' % name)
                return client.CustomObjectsApi().delete_namespaced_custom_object(
                    group=resources[self.kind]['group'], version=resources[self.kind]['version'], namespace='default',
                    plural=resources[self.kind]['plural'], name=name, body=V1DeleteOptions())
            except ApiException as e:
                if e.reason == 'Not Found':
                    return
                else:
                    time.sleep(3)
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)

                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not delete %s %s on k8s.' % (self.kind, name))

    def delete_lifecycle(self, name):
        for i in range(RETRY_TIMES):
            try:
                config.load_kube_config(TOKEN)
                if not self.exist(name):
                    return
                jsondict = self.get(name)
                if hasLifeCycle(jsondict):
                    jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
                    jsondict = removeLifecycle(jsondict)
                    return client.CustomObjectsApi().replace_namespaced_custom_object(
                        group=resources[self.kind]['group'], version=resources[self.kind]['version'],
                        namespace='default',
                        plural=resources[self.kind]['plural'], name=name, body=jsondict)
                else:
                    return
            except Exception as e:
                if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1 or repr(e).find(
                        'ApiException') != -1:
                    config.load_kube_config(TOKEN)
                k8s_logger.debug(traceback.format_exc())
                k8s_logger.debug("sleep 3 sec")
                time.sleep(3)
        raise BadRequest('can not delete lifecycle %s %s on k8s.' % (self.kind, name))

    def change_node(self, name, newNodeName):
        if not self.exist(name):
            return
        jsondict = self.get(name)
        if jsondict:
            jsondict = addPowerStatusMessage(jsondict, 'Ready', 'The resource is ready.')
            jsondict['metadata']['labels']['host'] = newNodeName
            spec = get_spec(jsondict)
            if spec:
                nodeName = spec.get('nodeName')
                if nodeName:
                    spec['nodeName'] = newNodeName
            self.updateAll(name, jsondict)


def error_print(code, msg, data=None):
    if data is None:
        print(dumps({"result": {"code": code, "msg": msg}, "data": {}}))
        exit(1)
    else:
        print(dumps({"result": {"code": code, "msg": msg}, "data": data}))
        exit(1)


if __name__ == '__main__':
    # data = {
    #     'domain': 'cloudinit',
    #     'pool': 'migratepoolnodepool22'
    # }
    helper = K8sHelper(VMP_KIND)
    # backup_helper.create('backup1', 'backup', data)
#     print(backup_helper.add_label('vmbackup2', 'cloudinit'))

#     print get_all_node_ip()
#     get_pools_by_path('/var/lib/libvirt/cstor/1709accf174vccaced76b0dbfccdev/1709accf174vccaced76b0dbfccdev')
# k8s = K8sHelper('VirtualMachineDisk')
# disk1 = k8s.get('disk33333clone')
# print dumps(disk1)
# k8s.delete('disk33333clone1')
# k8s.create('disk33333clone1', 'volume', disk1['spec']['volume'])
# disk1['spec']['volume']['filename'] = 'lalalalalalala'
# k8s.update('disk33333clone1', 'volume', disk1['spec']['volume'])
