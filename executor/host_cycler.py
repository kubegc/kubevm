'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''

'''
Import python libs
'''
import os, sys, time, datetime, socket, subprocess, time, traceback
import ConfigParser
from dateutil.tz import gettz
from json import dumps
from json import loads
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf

'''
Import third party libs
'''
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client.models.v1_node_status import V1NodeStatus
from kubernetes.client.models.v1_node_condition import V1NodeCondition
from kubernetes.client.models.v1_node_daemon_endpoints import V1NodeDaemonEndpoints
from kubernetes.client.models.v1_node_system_info import V1NodeSystemInfo
from kubernetes.client.models.v1_node import V1Node
from kubernetes.client.models.v1_node_spec import V1NodeSpec
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_node_address import V1NodeAddress

'''
Import local libs
'''
# sys.path.append('%s/utils/libvirt_util.py' % (os.path.dirname(os.path.realpath(__file__))))
from utils.libvirt_util import get_xml, vm_state, freecpu, freemem, node_info, list_active_vms, list_vms, destroy, undefine, is_vm_active, start
from utils.utils import change_master_and_reload_config, updateDescription, addPowerStatusMessage, updateDomain, CDaemon, runCmd, get_field_in_kubernetes_by_index, get_hostname_in_lower_case, get_node_name_from_kubernetes, get_ha_from_kubernetes
from utils import logger

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
PLURAL = config_raw.get('VirtualMachine', 'plural')
VERSION = config_raw.get('VirtualMachine', 'version')
GROUP = config_raw.get('VirtualMachine', 'group')

DEFAULT_JSON_BACKUP_DIR = config_raw.get('DefaultJsonBackupDir', 'default')
HOSTNAME = get_hostname_in_lower_case()

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

def main():
#     restart_service = False
    ha_check = True
    fail_times = 0
    while True:
        try:
            host = client.CoreV1Api().read_node_status(name=HOSTNAME)
            node_watcher = HostCycler()
            host.status = node_watcher.get_node_status()
            client.CoreV1Api().replace_node_status(name=HOSTNAME, body=host)
            if ha_check:
                for vm in list_vms():
                    _check_vm_by_hosting_node(GROUP, VERSION, PLURAL, vm)
                    _check_ha_and_autostart_vm(GROUP, VERSION, PLURAL, vm)
                    _check_vm_power_state(GROUP, VERSION, PLURAL, vm)
                ha_check = False
#             if restart_service:
#                 runCmd('kubevmm-adm service restart')
#                 restart_service = False
            fail_times = 0
            time.sleep(8)
        except Exception, e:
            logger.debug(repr(e))
            if repr(e).find('Connection refused') != -1 or repr(e).find('No route to host') != -1:
                logger.debug('in here!')
                master_ip = change_master_and_reload_config(fail_times)
                config.load_kube_config(config_file=TOKEN)
                fail_times += 1
                logger.debug('retrying another master %s, retry times: %d' % (master_ip, fail_times))
            logger.error('Oops! ', exc_info=1)
            time.sleep(8)
#             restart_service = True
            continue
        
def _check_vm_by_hosting_node(group, version, plural, metadata_name):
    try:
        logger.debug('1.Doing hosting node verification for VM: %s' % metadata_name)
        node_name = get_node_name_from_kubernetes(group, version, 'default', plural, metadata_name)
        if not node_name:
            logger.debug('Delete VM %s because it is not hosting by the Kubernetes cluster.' % (metadata_name))
            if is_vm_active(metadata_name):
                destroy(metadata_name)
                time.sleep(1)
            undefine(metadata_name)    
        elif node_name != get_hostname_in_lower_case():
            logger.debug('Delete VM %s because it is now hosting by another node %s.' % (metadata_name, node_name))
            _backup_json_to_file(group, version, 'default', plural, metadata_name)
            if is_vm_active(metadata_name):
                destroy(metadata_name)
                time.sleep(1)
            undefine(metadata_name)    
    except:
        logger.error('Oops! ', exc_info=1)
        
def _check_ha_and_autostart_vm(group, version, plural, metadata_name):
    try:
        logger.debug('2.Doing HA verification for VM: %s' % metadata_name)
        ha = get_ha_from_kubernetes(group, version, 'default', plural, metadata_name)
        if ha:
            logger.debug('Autostart HA VM: %s.' % (metadata_name))
            if not is_vm_active(metadata_name):
                start(metadata_name)
    except:
        logger.error('Oops! ', exc_info=1)
        
def _check_vm_power_state(group, version, plural, metadata_name):
    try:
        logger.debug('3.Check the power state of VM: %s' % metadata_name)
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=GROUP, version=VERSION, namespace='default', plural=PLURAL, name=metadata_name)
    except ApiException, e:
        if e.reason == 'Not Found':
            logger.debug('**VM %s already deleted, ignore this 404 error.' % metadata_name)
    except Exception, e:
        logger.error('Oops! ', exc_info=1)
    vm_xml = get_xml(metadata_name)
    vm_power_state = vm_state(metadata_name).get(metadata_name)
    vm_json = toKubeJson(xmlToJson(vm_xml))
    vm_json = updateDomain(loads(vm_json))
    jsondict = updateDomainStructureAndDeleteLifecycleInJson(jsondict, vm_json)
    body = addPowerStatusMessage(jsondict, vm_power_state, 'The VM is %s' % vm_power_state)
    try:
        modifyVM(group, version, plural, metadata_name, body)
    except ApiException, e:
        if e.reason == 'Not Found':
            logger.debug('**VM %s already deleted, ignore this 404.' % metadata_name)
        if e.reason == 'Conflict':
            logger.debug('**Other process updated %s, ignore this 409.' % metadata_name)
        else:
            logger.error('Oops! ', exc_info=1)
    except Exception, e:
        logger.error('Oops! ', exc_info=1)
    

def _backup_json_to_file(group, version, namespace, plural, metadata_name):
    try:
        jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
            group=group, version=version, namespace=namespace, plural=plural, name=metadata_name)
    except ApiException, e:
        if e.reason == 'Not Found':
            logger.debug('**VM %s already deleted.' % metadata_name)
            return
        else:
            raise e
    if not os.path.exists(DEFAULT_JSON_BACKUP_DIR):
        os.mkdir(DEFAULT_JSON_BACKUP_DIR)
    backup_file = '%s/%s.json' % (DEFAULT_JSON_BACKUP_DIR, metadata_name)
    with open(backup_file, "w") as f1:
        f1.write(dumps(jsonStr))

def modifyVM(group, version, plural, name, body):
    body = updateDescription(body)
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv
        
def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace(
                    'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')
                    
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

class HostCycler:
    
    def __init__(self):
        self.node_status = V1NodeStatus(addresses=self.get_status_address(), allocatable=self.get_status_allocatable(), 
                            capacity=self.get_status_capacity(), conditions=self.get_status_condition(),
                            daemon_endpoints=self.get_status_daemon_endpoints(), node_info=self.get_status_node_info())
        self.node = V1Node(api_version='v1', kind='Node', metadata=self.get_object_metadata(), spec=self.get_node_spec(), status=self.node_status)
        self.__node = self.node
        self.__node_status = self.node_status

    def get_node(self):
        return self.__node

    def get_node_status(self):
        return self.__node_status

    def _format_mem_to_Mi(self, mem):
        return int(round(int(mem))) if int(round(int(mem))) > 0 else 0
    
    def get_node_spec(self):
        return V1NodeSpec()
    
    def get_object_metadata(self):
        return V1ObjectMeta(annotations=[], name=HOSTNAME, uid='', labels=[], resource_version='', self_link='')
    
    def get_status_address(self):
        ip = socket.gethostbyname(socket.gethostname())
        node_status_address1 = V1NodeAddress(address=ip, type='InternalIP')
        node_status_address2 = V1NodeAddress(address=HOSTNAME, type='Hostname')
        return [node_status_address1, node_status_address2]
    
    def get_status_allocatable(self):
        try:
            cpu_allocatable = freecpu()
            if int(cpu_allocatable) <= 0:
                cpu_allocatable = 0
        except:
            cpu_allocatable = 0
        try:
            mem_allocatable = '%sMi' % str(self._format_mem_to_Mi(freemem()))
        except:
            mem_allocatable = '0Mi'
        try:
            active_vms = list_active_vms()
        except:
            active_vms = []
        return {'cpu': str(cpu_allocatable), 'memory': mem_allocatable, 'pods': str(40 - len(active_vms)) if 40 - len(active_vms) >= 0 else 0}
    
    def get_status_capacity(self):
        try:
            node_info_dict = node_info()
        except:
            node_info_dict = {}
        if node_info_dict:
            cpu_capacity = node_info_dict.get('cpus')
            mem_capacity = self._format_mem_to_Mi(node_info_dict.get('phymemory'))
            return {'cpu': str(cpu_capacity), 'memory': str(mem_capacity)+'Mi', 'pods': '40'}
        else:
            return {'cpu': 0, 'memory': '0Mi', 'pods': '40'}
    
    def get_status_daemon_endpoints(self):
        return V1NodeDaemonEndpoints(kubelet_endpoint={'port':0})

    def get_status_condition(self):
        time_zone = gettz('Asia/Shanghai')
        now = datetime.datetime.now(tz=time_zone)
#         now = datetime.datetime
        condition1 = V1NodeCondition(last_heartbeat_time=now, last_transition_time=now, message="virtlet has sufficient memory available", \
                            reason="VirtletHasSufficientMemory", status="False", type="MemoryPressure")
        condition2 = V1NodeCondition(last_heartbeat_time=now, last_transition_time=now, message="virtlet has no disk pressure", \
                            reason="VirtletHasNoDiskPressure", status="False", type="DiskPressure")
        condition3 = V1NodeCondition(last_heartbeat_time=now, last_transition_time=now, message="virtlet has sufficient PID available", \
                            reason="VirtletHasSufficientPID", status="False", type="PIDPressure")
        condition4 = V1NodeCondition(last_heartbeat_time=now, last_transition_time=now, message="virtlet is posting ready status", \
                            reason="VirtletReady", status="True", type="Ready")    
        return [condition1, condition2, condition3, condition4]
    
#         node_status = V1NodeStatus(conditions=[condition1, condition2, condition3, condition4], daemon_endpoints=daemon_endpoints, \
#                                    node_info=node_info)
#         self.node.status = node_status
#         client.CoreV1Api().replace_node_status(name="node11", body=self.node)
        
    def get_status_node_info(self):
        ARCHITECTURE = runCmd('uname -m')
        BOOT_ID = runCmd('cat /sys/class/dmi/id/product_uuid')
        RUNTIME_VERSION = 'QEMU-KVM://%s' % (runCmd('/usr/bin/qemu-img --version | awk \'NR==1 {print $3}\''))
        KERNEL_VERSION = runCmd('cat /proc/sys/kernel/osrelease')
#         KUBE_PROXY_VERSION = runCmd('kubelet --version | awk \'{print $2}\'')
        KUBE_PROXY_VERSION = 'v1.16.2'
        KUBELET_VERSION = KUBE_PROXY_VERSION
        MACHINE_ID = BOOT_ID
        OPERATING_SYSTEM = runCmd('cat /proc/sys/kernel/ostype')
        OS_IMAGE = runCmd('cat /etc/os-release | grep PRETTY_NAME | awk -F"\\"" \'{print$2}\'')
        SYSTEM_UUID = BOOT_ID
        return V1NodeSystemInfo(architecture=ARCHITECTURE, boot_id=BOOT_ID, container_runtime_version=RUNTIME_VERSION, \
                     kernel_version=KERNEL_VERSION, kube_proxy_version=KUBE_PROXY_VERSION, kubelet_version=KUBELET_VERSION, \
                     machine_id=MACHINE_ID, operating_system=OPERATING_SYSTEM, os_image=OS_IMAGE, system_uuid=SYSTEM_UUID)
        
    node = property(get_node, "node's docstring")
    node_status = property(get_node_status, "node_status's docstring")

if __name__ == "__main__":
    config.load_kube_config(config_file=TOKEN)
    main()
