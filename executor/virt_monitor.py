import subprocess

import prometheus_client
import ConfigParser
import re
import os
import sys
from prometheus_client.core import CollectorRegistry
from prometheus_client import Gauge,start_http_server,Counter
import time
import threading
import inspect
import ctypes
from kubernetes import config
from json import loads, dumps

from utils import logger

# try:
#     import xml.etree.CElementTree as ET
# except:
#     import xml.etree.ElementTree as ET

# from utils.libvirt_util import list_active_vms, get_macs
from utils.utils import get_field_in_kubernetes_by_index, CDaemon, list_all_disks, runCmdRaiseException, get_hostname_in_lower_case, get_field_in_kubernetes_node

LOG = '/var/log/virtmonitor.log'
logger = logger.set_logger(os.path.basename(__file__), LOG)

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
SHARE_FS_MOUNT_POINT = config_raw.get('Storage', 'share_fs_mount_point')
VDISK_FS_MOUNT_POINT = config_raw.get('Storage', 'vdisk_fs_mount_point')
LOCAL_FS_MOUNT_POINT = config_raw.get('Storage', 'local_fs_mount_point')
BLOCK_FS_MOUNT_POINT = config_raw.get('Storage', 'block_fs_mount_point')

HOSTNAME = get_hostname_in_lower_case()

# vm_cpu_system_proc_rate = Gauge('vm_cpu_system_proc_rate', 'The CPU rate of running system processes in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_cpu_usr_proc_rate = Gauge('vm_cpu_usr_proc_rate', 'The CPU rate of running user processes in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_cpu_idle_rate = Gauge('vm_cpu_idle_rate', 'The CPU idle rate in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_mem_total_bytes = Gauge('vm_mem_total_bytes', 'The total memory bytes in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_mem_available_bytes = Gauge('vm_mem_available_bytes', 'The available memory bytes in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_mem_buffers_bytes = Gauge('vm_mem_buffers_bytes', 'The buffers memory bytes in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_mem_rate = Gauge('vm_mem_rate', 'The memory rate in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels"])
# vm_disk_read_requests_per_secend = Gauge('vm_disk_read_requests_per_secend', 'Disk read requests per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_disk_write_requests_per_secend = Gauge('vm_disk_write_requests_per_secend', 'Disk write requests per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_disk_read_bytes_per_secend = Gauge('vm_disk_read_bytes_per_secend', 'Disk read bytes per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_disk_write_bytes_per_secend = Gauge('vm_disk_write_bytes_per_secend', 'Disk write bytes per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_receive_packages_per_secend = Gauge('vm_network_receive_packages_per_secend', 'Network receive packages per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_receive_bytes_per_secend = Gauge('vm_network_receive_bytes_per_secend', 'Network receive bytes per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_receive_errors_per_secend = Gauge('vm_network_receive_errors_per_secend', 'Network receive errors per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_receive_drops_per_secend = Gauge('vm_network_receive_drops_per_secend', 'Network receive drops per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_send_packages_per_secend = Gauge('vm_network_send_packages_per_secend', 'Network send packages per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_send_bytes_per_secend = Gauge('vm_network_send_bytes_per_secend', 'Network send bytes per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_send_errors_per_secend = Gauge('vm_network_send_errors_per_secend', 'Network send errors per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# vm_network_send_drops_per_secend = Gauge('vm_network_send_drops_per_secend', 'Network send drops per second in virtual machine', \
#                                 ['zone', 'host', 'vm', "labels", 'device'])
# storage_pool_total_size_kilobytes = Gauge('storage_pool_total_size_kilobytes', 'Storage pool total size in kilobytes on host', \
#                                 ['zone', 'host', 'pool', 'type'])
# storage_pool_used_size_kilobytes = Gauge('storage_pool_used_size_kilobytes', 'Storage pool used size in kilobytes on host', \
#                                 ['zone', 'host', 'pool', 'type'])
# storage_disk_total_size_kilobytes = Gauge('storage_disk_total_size_kilobytes', 'Storage disk total size in kilobytes on host', \
#                                 ['zone', 'host', 'pool', 'type', 'disk'])
# storage_disk_used_size_kilobytes = Gauge('storage_disk_used_size_kilobytes', 'Storage disk used size in kilobytes on host', \
#                                 ['zone', 'host', 'pool', 'type', 'disk'])

# VMS_CACHE = []

vm_cpu_system_proc_rate = Gauge('vm_cpu_system_proc_rate', 'The CPU rate of running system processes in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_cpu_usr_proc_rate = Gauge('vm_cpu_usr_proc_rate', 'The CPU rate of running user processes in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_cpu_idle_rate = Gauge('vm_cpu_idle_rate', 'The CPU idle rate in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_mem_total_bytes = Gauge('vm_mem_total_bytes', 'The total memory bytes in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_mem_available_bytes = Gauge('vm_mem_available_bytes', 'The available memory bytes in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_mem_buffers_bytes = Gauge('vm_mem_buffers_bytes', 'The buffers memory bytes in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_mem_rate = Gauge('vm_mem_rate', 'The memory rate in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster"])
vm_disk_read_requests_per_secend = Gauge('vm_disk_read_requests_per_secend', 'Disk read requests per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_disk_write_requests_per_secend = Gauge('vm_disk_write_requests_per_secend', 'Disk write requests per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_disk_read_bytes_per_secend = Gauge('vm_disk_read_bytes_per_secend', 'Disk read bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_disk_write_bytes_per_secend = Gauge('vm_disk_write_bytes_per_secend', 'Disk write bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_receive_packages_per_secend = Gauge('vm_network_receive_packages_per_secend', 'Network receive packages per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_receive_bytes_per_secend = Gauge('vm_network_receive_bytes_per_secend', 'Network receive bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_receive_errors_per_secend = Gauge('vm_network_receive_errors_per_secend', 'Network receive errors per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_receive_drops_per_secend = Gauge('vm_network_receive_drops_per_secend', 'Network receive drops per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_send_packages_per_secend = Gauge('vm_network_send_packages_per_secend', 'Network send packages per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_send_bytes_per_secend = Gauge('vm_network_send_bytes_per_secend', 'Network send bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_send_errors_per_secend = Gauge('vm_network_send_errors_per_secend', 'Network send errors per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
vm_network_send_drops_per_secend = Gauge('vm_network_send_drops_per_secend', 'Network send drops per second in virtual machine', \
                                ['zone', 'host', 'vm', "owner", "router", "autoscalinggroup", "cluster", 'device'])
storage_pool_total_size_kilobytes = Gauge('storage_pool_total_size_kilobytes', 'Storage pool total size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type'])
storage_pool_used_size_kilobytes = Gauge('storage_pool_used_size_kilobytes', 'Storage pool used size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type'])
storage_disk_total_size_kilobytes = Gauge('storage_disk_total_size_kilobytes', 'Storage disk total size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type', 'disk'])
storage_disk_used_size_kilobytes = Gauge('storage_disk_used_size_kilobytes', 'Storage disk used size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type', 'disk'])

class KillableThread:
    def __init__(self, target, args=None):
        self.th = threading.Thread(target=target, args=args)
        self.kill_sema = threading.Semaphore(0)
        self.start_sema = threading.Semaphore(0)
        def daemon_thread(self):
            self.th.setDaemon(True)
            self.th.start()
            self.start_sema.release()
            self.kill_sema.acquire()
        self.guard = threading.Thread(target=daemon_thread, args=(self,))

    def start(self):
        self.guard.start()
        self.start_sema.acquire()

    def join(self, secs=None):
        self.th.join(secs)
        if not self.th.is_alive():
            self.kill_sema.release()

    def is_alive(self):
        return self.th.is_alive() and self.guard.is_alive()

    def kill(self):
        self.kill_sema.release()
        while self.guard.is_alive():
            pass

def collect_storage_metrics(zone):
    storages = {VDISK_FS_MOUNT_POINT: 'vdiskfs', SHARE_FS_MOUNT_POINT: 'nfs/glusterfs', \
                LOCAL_FS_MOUNT_POINT: 'localfs', BLOCK_FS_MOUNT_POINT: 'blockfs'}
    for mount_point, pool_type in storages.items():
        try:
            all_pool_storages = runCmdRaiseException('timeout 2 df -aT | grep %s | awk \'{print $3,$4,$7}\'' % mount_point)
            for pool_storage in all_pool_storages:
                t = KillableThread(target=get_pool_metrics,args=(pool_storage, pool_type, zone,))
                t.start()
                t.join(2)
                t.kill()
        except:
            logger.warning('Oops! ', exc_info=1)
            return
#             get_pool_metrics(pool_storage, pool_type, zone)

def get_pool_metrics(pool_storage, pool_type, zone):
#     global storage_pool_total_size_kilobytes 
#     global storage_pool_used_size_kilobytes 
    (pool_total, pool_used, pool_mount_point) = pool_storage.strip().split(' ') 
    storage_pool_total_size_kilobytes.labels(zone, HOSTNAME, pool_mount_point, pool_type).set(pool_total)
    storage_pool_used_size_kilobytes.labels(zone, HOSTNAME, pool_mount_point, pool_type).set(pool_used)
    collect_disk_metrics(pool_mount_point, pool_type, zone)

def collect_disk_metrics(pool_mount_point, pool_type, zone):
    if pool_type in ['vdiskfs', 'nfs/glusterfs', 'localfs']:
        disk_list = list_all_disks(pool_mount_point, 'f')
        disk_type = 'file'
    else:
        disk_list = list_all_disks(pool_mount_point, 'l')
        disk_type = 'block'
    for disk in disk_list:
        get_vdisk_metrics(pool_mount_point, disk_type, disk, zone)
#         t = threading.Thread(target=get_vdisk_metrics,args=(pool_mount_point, disk_type, disk, zone,))
#         t.setDaemon(True)
#         t.start()
#         t.join()
#     vdisk_fs_list = list_all_vdisks(VDISK_FS_MOUNT_POINT, 'f')
#     for disk in vdisk_fs_list:
#         t1 = threading.Thread(target=get_vdisk_metrics,args=(disk, zone,))
#         t1.setDaemon(True)
#         t1.start()
#     local_fs_list = list_all_vdisks(LOCAL_FS_MOUNT_POINT, 'f')
#     for disk in local_fs_list:
#         t1 = threading.Thread(target=get_vdisk_metrics,args=(disk, zone,))
#         t1.setDaemon(True)
#         t1.start()
#     resource_utilization = {'host': HOSTNAME, 'vdisk_metrics': {}}
def get_vdisk_metrics(pool_mount_point, disk_type, disk, zone):
#     global storage_disk_total_size_kilobytes 
#     global storage_disk_used_size_kilobytes 
    try:
        output = loads(runCmdRaiseException('timeout 2 qemu-img info -U --output json %s' % (disk), use_read=True))
#     output = loads()
#     print(output)
    except:
        output = {}
    if output:
        virtual_size = float(output.get('virtual-size')) / 1024 if output.get('virtual-size') else 0.00
        actual_size = float(output.get('actual-size')) / 1024 if output.get('actual-size') else 0.00
        storage_disk_total_size_kilobytes.labels(zone, HOSTNAME, pool_mount_point, disk_type, disk).set(virtual_size)
        storage_disk_used_size_kilobytes.labels(zone, HOSTNAME, pool_mount_point, disk_type, disk).set(actual_size)

def runCmdAndGetOutput(cmd):
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for line in std_out:
                msg = msg + line
            return msg
        if std_err:
            return ''
    except Exception:
        return ''
    finally:
        p.stdout.close()
        p.stderr.close()

def get_disks_spec(domain):
    output = runCmdAndGetOutput('virsh domblklist %s' % domain)
    lines = output.splitlines()
    specs = []
    for i in range(2, len(lines)):
        spec = []
        kv = lines[i].split()
        if len(kv) == 2:
            spec.append(kv[0])
            spec.append(kv[1])
            specs.append(spec)
    return specs

def list_active_vms():
    output = runCmdAndGetOutput('virsh list')
    lines = output.splitlines()
    if (len(lines) < 2):
        return []
    vms = []
    for line in lines[2:]:
        if (len(line.split()) == 3):
            vms.append(line.split()[1])
    return vms

def list_all_vms():
    output = runCmdAndGetOutput('virsh list --all')
    lines = output.splitlines()
    if (len(lines) < 2):
        return []
    vms = []
    for line in lines[2:]:
        if (len(line.split()) >= 1):
            vms.append(line.split()[1])
    return vms

def get_macs(vm):
    if not vm:
        return []
    lines = runCmdRaiseException('timeout 2 virsh domiflist %s | awk \'NR>2{print $5}\'' % (vm))
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    macs = []
    for line in lines:
        line = line.strip()
        if line:
            macs.append(line)
    return macs

def collect_vm_metrics(zone):
    try:
        vm_list = list_active_vms()
        all_vm = list_all_vms()
        
#         print(vm_list)
#         global VMS_CACHE
        vm_stopped = []
#         if VMS_CACHE:
        print(all_vm)
        print(vm_list)
        if all_vm:
            vm_stopped = list(set(all_vm).difference(set(vm_list)))
            print(vm_stopped)
#         VMS_CACHE = vm_list
# #         print(VMS_CACHE)
        for vm in vm_list:
            t = KillableThread(target=get_vm_metrics,args=(vm, zone,))
            t.start()
            t.join(2)
            t.kill()
        for vm in vm_stopped:
            t = KillableThread(target=zero_vm_metrics,args=(vm, zone,))
            t.start()
            t.join(2)
            t.kill()            
    except:
        logger.warning('Oops! ', exc_info=1)
        return        
#         get_vm_metrics(vm, zone)
        
def get_vm_metrics(vm, zone):
    
#     global vm_cpu_system_proc_rate
#     global vm_cpu_usr_proc_rate 
#     global vm_cpu_idle_rate 
#     global vm_mem_total_bytes 
#     global vm_mem_available_bytes 
#     global vm_mem_buffers_bytes 
#     global vm_mem_rate 
#     global vm_disk_read_requests_per_secend 
#     global vm_disk_write_requests_per_secend 
#     global vm_disk_read_bytes_per_secend 
#     global vm_disk_write_bytes_per_secend 
#     global vm_network_receive_packages_per_secend 
#     global vm_network_receive_bytes_per_secend 
#     global vm_network_receive_errors_per_secend 
#     global vm_network_receive_drops_per_secend 
#     global vm_network_send_packages_per_secend 
#     global vm_network_send_bytes_per_secend 
#     global vm_network_send_errors_per_secend 
#     global vm_network_send_drops_per_secend 

    config.load_kube_config(config_file=TOKEN)
    labels = get_field_in_kubernetes_by_index(vm, GROUP, VERSION, PLURAL, ['metadata', 'labels'])
#     labels_str = dumps(labels)
    resource_utilization = {'vm': vm, 'cpu_metrics': {}, 'mem_metrics': {},
                            'disks_metrics': [], 'networks_metrics': [], 'cluster': labels.get('cluster'), 'router': labels.get('router'),
                            'owner': labels.get('owner'), 'autoscalinggroup': labels.get('autoscalinggroup')}
#     cpus = len(get_vcpus(vm)[0])
#     print(cpus)
    cpu_stats = runCmdRaiseException('timeout 2 virsh cpu-stats --total %s' % vm)
    cpu_time = 0.00
    cpu_system_time = 0.00
    cpu_user_time = 0.00
    for line in cpu_stats:
        if line.find('cpu_time') != -1:
            p1 = r'^(\s*cpu_time\s*)([\S*]+)\s*(\S*)'
            m1 = re.match(p1, line)
            if m1:
                cpu_time = float(m1.group(2))
        elif line.find('system_time') != -1:
            p1 = r'^(\s*system_time\s*)([\S*]+)\s*(\S*)'
            m1 = re.match(p1, line)
            if m1:
                cpu_system_time = float(m1.group(2))
        elif line.find('user_time') != -1:
            p1 = r'^(\s*user_time\s*)([\S*]+)\s*(\S*)'
            m1 = re.match(p1, line)
            if m1:
                cpu_user_time = float(m1.group(2))
    if cpu_time and cpu_system_time and cpu_user_time:
        resource_utilization['cpu_metrics']['cpu_system_rate'] = '%.2f' % (cpu_system_time / cpu_time)
        resource_utilization['cpu_metrics']['cpu_user_rate'] = '%.2f' % (cpu_user_time / cpu_time)
        resource_utilization['cpu_metrics']['cpu_idle_rate'] = \
        '%.2f' % (100 - ((cpu_user_time + cpu_system_time) / cpu_time))
    else:
        resource_utilization['cpu_metrics']['cpu_system_rate'] = '%.2f' % (0.00)
        resource_utilization['cpu_metrics']['cpu_user_rate'] = '%.2f' % (0.00)
        resource_utilization['cpu_metrics']['cpu_idle_rate'] = '%.2f' % (0.00)
    mem_stats = runCmdRaiseException('timeout 2 virsh dommemstat %s' % vm)
    mem_actual = 0.00
    mem_unused = 0.00
    mem_available = 0.00
    for line in mem_stats:
        if line.find('unused') != -1:
            mem_unused = float(line.split(' ')[1].strip()) * 1024
        elif line.find('available') != -1:
            mem_available = float(line.split(' ')[1].strip()) * 1024
        elif line.find('actual') != -1:
            mem_actual = float(line.split(' ')[1].strip()) * 1024
    resource_utilization['mem_metrics']['mem_unused'] = '%.2f' % (mem_unused)
    resource_utilization['mem_metrics']['mem_available'] = '%.2f' % (mem_available)
    if mem_unused and mem_available and mem_actual:
        mem_buffers = abs(mem_actual - mem_available)
        resource_utilization['mem_metrics']['mem_buffers'] = '%.2f' % (mem_buffers)
        resource_utilization['mem_metrics']['mem_rate'] = \
        '%.2f' % (abs(mem_available - mem_unused - mem_buffers) / mem_available * 100)
    else:
        resource_utilization['mem_metrics']['mem_buffers'] = '%.2f' % (0.00)
        resource_utilization['mem_metrics']['mem_rate'] = '%.2f' % (0.00)
    disks_spec = get_disks_spec(vm)
    for disk_spec in disks_spec:
        disk_metrics = {}
        disk_device = disk_spec[0]
        disk_metrics['device'] = disk_device
        stats1 = {}
        stats2 = {}
        # logger.debug('virsh domblkstat --device %s --domain %s' % (disk_device, vm))
        blk_dev_stats1 = runCmdRaiseException('timeout 2 virsh domblkstat --device %s --domain %s' % (disk_device, vm))
        for line in blk_dev_stats1:
            if line.find('rd_req') != -1:
                stats1['rd_req'] = float(line.split(' ')[2].strip())
            elif line.find('rd_bytes') != -1:
                stats1['rd_bytes'] = float(line.split(' ')[2].strip())
            elif line.find('wr_req') != -1:
                stats1['wr_req'] = float(line.split(' ')[2].strip())
            elif line.find('wr_bytes') != -1:
                stats1['wr_bytes'] = float(line.split(' ')[2].strip())
        time.sleep(0.1)
        blk_dev_stats2 = runCmdRaiseException('timeout 2 virsh domblkstat --device %s --domain %s' % (disk_device, vm))
        for line in blk_dev_stats2:
            if line.find('rd_req') != -1:
                stats2['rd_req'] = float(line.split(' ')[2].strip())
            elif line.find('rd_bytes') != -1:
                stats2['rd_bytes'] = float(line.split(' ')[2].strip())
            elif line.find('wr_req') != -1:
                stats2['wr_req'] = float(line.split(' ')[2].strip())
            elif line.find('wr_bytes') != -1:
                stats2['wr_bytes'] = float(line.split(' ')[2].strip())
        disk_metrics['disk_read_requests_per_secend'] = '%.2f' % ((stats2['rd_req'] - stats1['rd_req']) / 0.1) \
        if (stats2['rd_req'] - stats1['rd_req']) > 0 else '%.2f' % (0.00)
        disk_metrics['disk_read_bytes_per_secend'] = '%.2f' % ((stats2['rd_bytes'] - stats1['rd_bytes']) / 0.1) \
        if (stats2['rd_bytes'] - stats1['rd_bytes']) > 0 else '%.2f' % (0.00)
        disk_metrics['disk_write_requests_per_secend'] = '%.2f' % ((stats2['wr_req'] - stats1['wr_req']) / 0.1) \
        if (stats2['wr_req'] - stats1['wr_req']) > 0 else '%.2f' % (0.00)
        disk_metrics['disk_write_bytes_per_secend'] = '%.2f' % ((stats2['wr_bytes'] - stats1['wr_bytes']) / 0.1) \
        if (stats2['wr_bytes'] - stats1['wr_bytes']) > 0 else '%.2f' % (0.00)
        resource_utilization['disks_metrics'].append(disk_metrics)
    macs = get_macs(vm)
    for mac in macs:
        net_metrics = {}
        net_metrics['device'] = mac.encode('utf-8')
        stats1 = {}
        stats2 = {}
        net_dev_stats1 = runCmdRaiseException('timeout 2 virsh domifstat --interface %s --domain %s' % (mac, vm))
        for line in net_dev_stats1:
            if line.find('rx_bytes') != -1:
                stats1['rx_bytes'] = float(line.split(' ')[2].strip())
            elif line.find('rx_packets') != -1:
                stats1['rx_packets'] = float(line.split(' ')[2].strip())
            elif line.find('tx_packets') != -1:
                stats1['tx_packets'] = float(line.split(' ')[2].strip())
            elif line.find('tx_bytes') != -1:
                stats1['tx_bytes'] = float(line.split(' ')[2].strip())
            elif line.find('rx_drop') != -1:
                stats1['rx_drop'] = float(line.split(' ')[2].strip())
            elif line.find('rx_errs') != -1:
                stats1['rx_errs'] = float(line.split(' ')[2].strip())
            elif line.find('tx_errs') != -1:
                stats1['tx_errs'] = float(line.split(' ')[2].strip())
            elif line.find('tx_drop') != -1:
                stats1['tx_drop'] = float(line.split(' ')[2].strip())
        time.sleep(0.1)
        net_dev_stats2 = runCmdRaiseException('timeout 2 virsh domifstat --interface %s --domain %s' % (mac, vm))
        for line in net_dev_stats2:
            if line.find('rx_bytes') != -1:
                stats2['rx_bytes'] = float(line.split(' ')[2].strip())
            elif line.find('rx_packets') != -1:
                stats2['rx_packets'] = float(line.split(' ')[2].strip())
            elif line.find('tx_packets') != -1:
                stats2['tx_packets'] = float(line.split(' ')[2].strip())
            elif line.find('tx_bytes') != -1:
                stats2['tx_bytes'] = float(line.split(' ')[2].strip())
            elif line.find('rx_drop') != -1:
                stats2['rx_drop'] = float(line.split(' ')[2].strip())
            elif line.find('rx_errs') != -1:
                stats2['rx_errs'] = float(line.split(' ')[2].strip())
            elif line.find('tx_errs') != -1:
                stats2['tx_errs'] = float(line.split(' ')[2].strip())
            elif line.find('tx_drop') != -1:
                stats2['tx_drop'] = float(line.split(' ')[2].strip())
        net_metrics['network_read_packages_per_secend'] = '%.2f' % ((stats2['rx_packets'] - stats1['rx_packets']) / 0.1) \
        if (stats2['rx_packets'] - stats1['rx_packets']) > 0 else '%.2f' % (0.00)
        net_metrics['network_read_bytes_per_secend'] = '%.2f' % ((stats2['rx_bytes'] - stats1['rx_bytes']) / 0.1) \
        if (stats2['rx_bytes'] - stats1['rx_bytes']) > 0 else '%.2f' % (0.00)
        net_metrics['network_write_packages_per_secend'] = '%.2f' % ((stats2['tx_packets'] - stats1['tx_packets']) / 0.1) \
        if (stats2['tx_packets'] - stats1['tx_packets']) > 0 else '%.2f' % (0.00)
        net_metrics['network_write_bytes_per_secend'] = '%.2f' % ((stats2['tx_bytes'] - stats1['tx_bytes']) / 0.1) \
        if (stats2['tx_bytes'] - stats1['tx_bytes']) > 0 else '%.2f' % (0.00)
        net_metrics['network_read_errors_per_secend'] = '%.2f' % ((stats2['rx_errs'] - stats1['rx_errs']) / 0.1) \
        if (stats2['rx_errs'] - stats1['rx_errs']) > 0 else '%.2f' % (0.00)
        net_metrics['network_read_drops_per_secend'] = '%.2f' % ((stats2['rx_drop'] - stats1['rx_drop']) / 0.1) \
        if (stats2['rx_drop'] - stats1['rx_drop']) > 0 else '%.2f' % (0.00)
        net_metrics['network_write_errors_per_secend'] = '%.2f' % ((stats2['tx_errs'] - stats1['tx_errs']) / 0.1) \
        if (stats2['tx_errs'] - stats1['tx_errs']) > 0 else '%.2f' % (0.00)
        net_metrics['network_write_drops_per_secend'] = '%.2f' % ((stats2['tx_drop'] - stats1['tx_drop']) / 0.1) \
        if (stats2['tx_drop'] - stats1['tx_drop']) > 0 else '%.2f' % (0.00)
        resource_utilization['networks_metrics'].append(net_metrics)  
    vm_cpu_system_proc_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['cpu_metrics']['cpu_system_rate'])
    vm_cpu_usr_proc_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['cpu_metrics']['cpu_user_rate'])
    vm_cpu_idle_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['cpu_metrics']['cpu_idle_rate'])
    vm_mem_total_bytes.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_available'])
    vm_mem_available_bytes.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_unused'])
    vm_mem_buffers_bytes.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_buffers'])
    vm_mem_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_rate'])
    for disk_metrics in resource_utilization['disks_metrics']:
        vm_disk_read_requests_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_read_requests_per_secend'])
        vm_disk_read_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_read_bytes_per_secend'])
        vm_disk_write_requests_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_write_requests_per_secend'])
        vm_disk_write_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_write_bytes_per_secend'])
    for net_metrics in resource_utilization['networks_metrics']:
        vm_network_receive_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_bytes_per_secend'])
        vm_network_receive_drops_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_drops_per_secend'])
        vm_network_receive_errors_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_errors_per_secend'])
        vm_network_receive_packages_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_packages_per_secend'])
        vm_network_send_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_bytes_per_secend'])
        vm_network_send_drops_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_drops_per_secend'])
        vm_network_send_errors_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_errors_per_secend'])
        vm_network_send_packages_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_packages_per_secend'])
    return resource_utilization

def zero_vm_metrics(vm, zone):
    
    config.load_kube_config(config_file=TOKEN)
    labels = get_field_in_kubernetes_by_index(vm, GROUP, VERSION, PLURAL, ['metadata', 'labels'])
#     labels_str = dumps(labels)
    resource_utilization = {'vm': vm, 'cpu_metrics': {}, 'mem_metrics': {},
                            'disks_metrics': [], 'networks_metrics': [], 'cluster': labels.get('cluster'), 'router': labels.get('router'),
                            'owner': labels.get('owner'), 'autoscalinggroup': labels.get('autoscalinggroup')}
    resource_utilization['cpu_metrics']['cpu_system_rate'] = '%.2f' % (0.00)
    resource_utilization['cpu_metrics']['cpu_user_rate'] = '%.2f' % (0.00)
    resource_utilization['cpu_metrics']['cpu_idle_rate'] = '%.2f' % (0.00)
    mem_unused = 0.00
    mem_available = 0.00
    resource_utilization['mem_metrics']['mem_unused'] = '%.2f' % (mem_unused)
    resource_utilization['mem_metrics']['mem_available'] = '%.2f' % (mem_available)
    resource_utilization['mem_metrics']['mem_buffers'] = '%.2f' % (0.00)
    resource_utilization['mem_metrics']['mem_rate'] = '%.2f' % (0.00)
    disks_spec = get_disks_spec(vm)
    for disk_spec in disks_spec:
        disk_metrics = {}
        disk_device = disk_spec[0]
        disk_metrics['device'] = disk_device
        disk_metrics['disk_read_requests_per_secend'] =  '%.2f' % (0.00)
        disk_metrics['disk_read_bytes_per_secend'] = '%.2f' % (0.00)
        disk_metrics['disk_write_requests_per_secend'] = '%.2f' % (0.00)
        disk_metrics['disk_write_bytes_per_secend'] = '%.2f' % (0.00)
        resource_utilization['disks_metrics'].append(disk_metrics)
    macs = get_macs(vm)
    for mac in macs:
        net_metrics = {}
        net_metrics['device'] = mac.encode('utf-8')
        net_metrics['network_read_packages_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_read_bytes_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_write_packages_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_write_bytes_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_read_errors_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_read_drops_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_write_errors_per_secend'] = '%.2f' % (0.00)
        net_metrics['network_write_drops_per_secend'] = '%.2f' % (0.00)
        resource_utilization['networks_metrics'].append(net_metrics)  
    vm_cpu_system_proc_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['cpu_metrics']['cpu_system_rate'])
    vm_cpu_usr_proc_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['cpu_metrics']['cpu_user_rate'])
    vm_cpu_idle_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['cpu_metrics']['cpu_idle_rate'])
    vm_mem_total_bytes.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_available'])
    vm_mem_available_bytes.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_unused'])
    vm_mem_buffers_bytes.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_buffers'])
    vm_mem_rate.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster')).set(resource_utilization['mem_metrics']['mem_rate'])
    for disk_metrics in resource_utilization['disks_metrics']:
        vm_disk_read_requests_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_read_requests_per_secend'])
        vm_disk_read_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_read_bytes_per_secend'])
        vm_disk_write_requests_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_write_requests_per_secend'])
        vm_disk_write_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), disk_metrics['device']).set(disk_metrics['disk_write_bytes_per_secend'])
    for net_metrics in resource_utilization['networks_metrics']:
        vm_network_receive_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_bytes_per_secend'])
        vm_network_receive_drops_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_drops_per_secend'])
        vm_network_receive_errors_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_errors_per_secend'])
        vm_network_receive_packages_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_read_packages_per_secend'])
        vm_network_send_bytes_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_bytes_per_secend'])
        vm_network_send_drops_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_drops_per_secend'])
        vm_network_send_errors_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_errors_per_secend'])
        vm_network_send_packages_per_secend.labels(zone, HOSTNAME, vm, labels.get('owner'), labels.get('router'), labels.get('autoscalinggroup'), labels.get('cluster'), net_metrics['device']).set(net_metrics['network_write_packages_per_secend'])
    return resource_utilization

# def set_vm_mem_period(vm, sec):
#     runCmdRaiseException('virsh dommemstat --period %s --domain %s --config --live' % (str(sec), vm))
    
# def get_resource_collector_threads():
#     config.load_kube_config(config_file=TOKEN)
#     zone = get_field_in_kubernetes_node(HOSTNAME, ['metadata', 'labels', 'zone'])
#     print(zone)
#     while True:
#         vm_list = list_active_vms()
#         for vm in vm_list:
#             t = threading.Thread(target=collect_vm_metrics,args=(vm,zone,))
#             t.setDaemon(True)
#             t.start()
#         t1 = threading.Thread(target=collect_storage_metrics,args=(zone,))
#         t1.setDaemon(True)
#         t1.start()
# #         nfs_vdisk_list = list_all_vdisks('/var/lib/libvirt/cstor')
# #         for nfs_vdisk in nfs_vdisk_list:
# #             t2 = threading.Thread(target=collect_disk_metrics,args=(nfs_vdisk,zone,))
# #             t2.setDaemon(True)
# #             t2.start()
#         time.sleep(5)
        
class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=022, verbose=1):
        CDaemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name
        
    def run(self, output_fn, **kwargs):
        logger.debug("---------------------------------------------------------------------------------")
        logger.debug("------------------------Welcome to Monitor Daemon.-------------------------------")
        logger.debug("------Copyright (2019, ) Institute of Software, Chinese Academy of Sciences------")
        logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn,liuhe18@otcaix.iscas.ac.cn----------")
        logger.debug("--------------------------------wuheng@otcaix.iscas.ac.cn------------------------")
        logger.debug("---------------------------------------------------------------------------------")
        start_http_server(19998)
#         registry = CollectorRegistry(auto_describe=False)
        config.load_kube_config(config_file=TOKEN)
        zone = get_field_in_kubernetes_node(HOSTNAME, ['metadata', 'labels', 'zone'])
        while True:
#             init(registry)
            collect_vm_metrics(zone)
            collect_storage_metrics(zone)
            time.sleep(10)
        
def daemonize():
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print help_msg
        sys.exit(1)
    p_name = 'virtmonitor'
    pid_fn = '/var/run/virtmonitor_daemon.pid'
    log_fn = '/var/log/virtmonitor.log'
    err_fn = '/var/log/virtmonitor.log'
    cD = ClientDaemon(p_name, pid_fn, stderr=err_fn, verbose=1)
 
    if sys.argv[1] == 'start':
        cD.start(log_fn)
    elif sys.argv[1] == 'stop':
        cD.stop()
    elif sys.argv[1] == 'restart':
        cD.restart(log_fn)
    elif sys.argv[1] == 'status':
        alive = cD.is_running()
        if alive:
            print 'process [%s] is running ......' % cD.get_pid()
        else:
            print 'daemon process [%s] stopped' %cD.name
    else:
        print 'invalid argument!'
        print help_msg    
        
if __name__ == '__main__':
    daemonize()
#     start_http_server(19998)
#     config.load_kube_config(config_file=TOKEN)
#     zone = get_field_in_kubernetes_node(HOSTNAME, ['metadata', 'labels', 'zone'])
#     while True:
#         collect_vm_metrics(zone)
# #         collect_storage_metrics(zone)
#         time.sleep(10)    
#     print(get_macs("vm006"))
    # print get_disks_spec('vmtest222')
#     import pprint
#     set_vm_mem_period('vm010', 5)
#     pprint.pprint(collect_vm_metrics("vm010"))