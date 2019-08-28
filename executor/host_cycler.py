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

'''
Import third party libs
'''
from kubernetes import client, config
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
from utils.libvirt_util import freecpu, freemem, node_info, list_active_vms
from utils.utils import CDaemon, runCmd, get_hostname_in_lower_case
from utils import logger

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

cfg = "/etc/kubevmm/config"
if not os.path.exists(cfg):
    cfg = "/home/kubevmm/bin"
config_raw = parser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
HOSTNAME = get_hostname_in_lower_case()

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

def main():
    while True:
        try:
            host = client.CoreV1Api().read_node_status(name=HOSTNAME)
            node_watcher = HostCycler()
            host.status = node_watcher.get_node_status()
            client.CoreV1Api().replace_node_status(name=HOSTNAME, body=host)
            time.sleep(8)
        except:
            logger.error('Oops! ', exc_info=1)

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
        return int(round(int(mem)))
    
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
        cpu_allocatable = freecpu()
        mem_allocatable = self._format_mem_to_Mi(freemem())
        active_vms = list_active_vms()
        return {'cpu': str(cpu_allocatable), 'memory': str(mem_allocatable)+'Mi', 'pods': str(40 - len(active_vms)) if 40 - len(active_vms) >= 0 else 0}
    
    def get_status_capacity(self):
        node_info_dict = node_info()
        cpu_capacity = node_info_dict.get('cpus')
        mem_capacity = self._format_mem_to_Mi(node_info_dict.get('phymemory'))
        return {'cpu': str(cpu_capacity), 'memory': str(mem_capacity)+'Mi', 'pods': '40'}
    
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
        KUBE_PROXY_VERSION = 'v1.14.1'
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
