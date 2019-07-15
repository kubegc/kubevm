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
from utils.libvirt_util import freecpu, freemem, node_info
from utils.utils import CDaemon
from utils import logger

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

cfg = "%s/default.cfg" % os.path.dirname(os.path.realpath(__file__))
config_raw = parser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
HOSTNAME = socket.gethostname()

logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=022, verbose=1):
        CDaemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name
 
    def run(self, output_fn, **kwargs):
        config.load_kube_config(config_file=TOKEN)
        try:
            main()
        except:
            traceback.print_exc()

def daemonize():
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print help_msg
        sys.exit(1)
    p_name = 'virtlet_host_cycler'
    pid_fn = '/var/run/virtlet_host_cycler_daemon.pid'
    log_fn = '/var/log/virtlet.log'
    err_fn = '/var/log/virtlet_error.log'
    cD1 = ClientDaemon(p_name, pid_fn, stderr=err_fn, verbose=1)
 
    if sys.argv[1] == 'start':
        cD1.start(log_fn)
    elif sys.argv[1] == 'stop':
        cD1.stop()
    elif sys.argv[1] == 'restart':
        cD1.restart(log_fn)
    elif sys.argv[1] == 'status':
        alive = cD1.is_running()
        if alive:
            print 'process [%s] is running ......' % cD1.get_pid()
        else:
            print 'daemon process [%s] stopped' %cD1.name
    else:
        print 'invalid argument!'
        print help_msg

def main():
    while True:
        host = client.CoreV1Api().read_node_status(name='node12')
        node_watcher = HostCycler()
        host.status = node_watcher.get_node_status()
        client.CoreV1Api().replace_node_status(name='node12', body=host)
        time.sleep(8)

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

    def _format_mem_to_mb(self, mem):
        return int(round(int(mem) / 1000))
    
    '''
    Run back-end command in subprocess.
    '''
    def runCmd(self, cmd):
        std_err = None
        if not cmd:
            return
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            std_out = p.stdout.readlines()
            std_err = p.stderr.readlines()
            return str.strip(std_out[0]) if std_out else ''
        finally:
            p.stdout.close()
            p.stderr.close()

    def get_node_spec(self):
        return V1NodeSpec()
    
    def get_object_metadata(self):
        return V1ObjectMeta(annotations=[], name=socket.gethostname(), uid='', labels=[], resource_version='', self_link='')
    
    def get_status_address(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        node_status_address1 = V1NodeAddress(address=ip, type='InternalIP')
        node_status_address2 = V1NodeAddress(address=hostname, type='Hostname')
        return [node_status_address1, node_status_address2]
    
    def get_status_allocatable(self):
        cpu_allocatable = freecpu()
        mem_allocatable = self._format_mem_to_mb(freemem())
        return {'cpu': str(cpu_allocatable), 'memory': str(mem_allocatable)}
    
    def get_status_capacity(self):
        node_info_dict = node_info()
        cpu_capacity = node_info_dict.get('cpus')
        mem_capacity = self._format_mem_to_mb(node_info_dict.get('phymemory'))
        return {'cpu': str(cpu_capacity), 'memory': str(mem_capacity)}
    
    def get_status_daemon_endpoints(self):
        return V1NodeDaemonEndpoints(kubelet_endpoint={'port':0})

    def get_status_condition(self):
        time_zone = gettz('Asia/Shanghai')
        now = datetime.datetime.now(tz=time_zone)
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
        ARCHITECTURE = self.runCmd('uname -m')
        BOOT_ID = self.runCmd('cat /sys/class/dmi/id/product_uuid')
        RUNTIME_VERSION = 'QEMU-KVM://%s' % (self.runCmd('/usr/libexec/qemu-kvm -version | awk \'NR==1 {print $4}\''))
        KERNEL_VERSION = self.runCmd('cat /proc/sys/kernel/osrelease')
        KUBE_PROXY_VERSION = self.runCmd('kubelet --version | awk \'{print $2}\'')
        KUBELET_VERSION = KUBE_PROXY_VERSION
        MACHINE_ID = BOOT_ID
        OPERATING_SYSTEM = self.runCmd('cat /proc/sys/kernel/ostype')
        OS_IMAGE = self.runCmd('cat /etc/os-release | grep PRETTY_NAME | awk -F"\\"" \'{print$2}\'')
        SYSTEM_UUID = BOOT_ID
        return V1NodeSystemInfo(architecture=ARCHITECTURE, boot_id=BOOT_ID, container_runtime_version=RUNTIME_VERSION, \
                     kernel_version=KERNEL_VERSION, kube_proxy_version=KUBE_PROXY_VERSION, kubelet_version=KUBELET_VERSION, \
                     machine_id=MACHINE_ID, operating_system=OPERATING_SYSTEM, os_image=OS_IMAGE, system_uuid=SYSTEM_UUID)
        
    node = property(get_node, "node's docstring")
    node_status = property(get_node_status, "node_status's docstring")

if __name__ == "__main__":
    daemonize()
