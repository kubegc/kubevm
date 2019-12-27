import subprocess

import prometheus_client
import ConfigParser
import re
import os
from prometheus_client import Gauge,start_http_server,Counter
import time
import threading
from kubernetes import config
from json import loads

from utils import logger

try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET

from utils.utils import list_all_disks, runCmdRaiseException, get_hostname_in_lower_case, get_field_in_kubernetes_node

LOG = '/var/log/virtlet.log'
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
SHARE_FS_MOUNT_POINT = config_raw.get('Storage', 'share_fs_mount_point')
VDISK_FS_MOUNT_POINT = config_raw.get('Storage', 'vdisk_fs_mount_point')
LOCAL_FS_MOUNT_POINT = config_raw.get('Storage', 'local_fs_mount_point')
BLOCK_FS_MOUNT_POINT = config_raw.get('Storage', 'block_fs_mount_point')

HOSTNAME = get_hostname_in_lower_case()

vm_cpu_system_proc_rate = Gauge('vm_cpu_system_proc_rate', 'The CPU rate of running system processes in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_cpu_usr_proc_rate = Gauge('vm_cpu_usr_proc_rate', 'The CPU rate of running user processes in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_cpu_idle_rate = Gauge('vm_cpu_idle_rate', 'The CPU idle rate in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_mem_total_bytes = Gauge('vm_mem_total_bytes', 'The total memory bytes in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_mem_available_bytes = Gauge('vm_mem_available_bytes', 'The available memory bytes in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_mem_buffers_bytes = Gauge('vm_mem_buffers_bytes', 'The buffers memory bytes in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_mem_rate = Gauge('vm_mem_rate', 'The memory rate in virtual machine', \
                                ['zone', 'host', 'vm'])
vm_disk_read_requests_per_secend = Gauge('vm_disk_read_requests_per_secend', 'Disk read requests per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_disk_write_requests_per_secend = Gauge('vm_disk_write_requests_per_secend', 'Disk write requests per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_disk_read_bytes_per_secend = Gauge('vm_disk_read_bytes_per_secend', 'Disk read bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_disk_write_bytes_per_secend = Gauge('vm_disk_write_bytes_per_secend', 'Disk write bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_receive_packages_per_secend = Gauge('vm_network_receive_packages_per_secend', 'Network receive packages per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_receive_bytes_per_secend = Gauge('vm_network_receive_bytes_per_secend', 'Network receive bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_receive_errors_per_secend = Gauge('vm_network_receive_errors_per_secend', 'Network receive errors per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_receive_drops_per_secend = Gauge('vm_network_receive_drops_per_secend', 'Network receive drops per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_send_packages_per_secend = Gauge('vm_network_send_packages_per_secend', 'Network send packages per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_send_bytes_per_secend = Gauge('vm_network_send_bytes_per_secend', 'Network send bytes per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_send_errors_per_secend = Gauge('vm_network_send_errors_per_secend', 'Network send errors per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
vm_network_send_drops_per_secend = Gauge('vm_network_send_drops_per_secend', 'Network send drops per second in virtual machine', \
                                ['zone', 'host', 'vm', 'device'])
storage_pool_total_size_kilobytes = Gauge('storage_pool_total_size_kilobytes', 'Storage pool total size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type'])
storage_pool_used_size_kilobytes = Gauge('storage_pool_used_size_kilobytes', 'Storage pool used size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type'])
storage_disk_total_size_kilobytes = Gauge('storage_disk_total_size_kilobytes', 'Storage disk total size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type', 'disk'])
storage_disk_used_size_kilobytes = Gauge('storage_disk_used_size_kilobytes', 'Storage disk used size in kilobytes on host', \
                                ['zone', 'host', 'pool', 'type', 'disk'])

def collect_storage_metrics(zone):
    storages = {VDISK_FS_MOUNT_POINT: 'vdiskfs', SHARE_FS_MOUNT_POINT: 'nfs/glusterfs', \
                LOCAL_FS_MOUNT_POINT: 'localfs', BLOCK_FS_MOUNT_POINT: 'blockfs'}
    for mount_point, pool_type in storages.items():
        all_pool_storages = runCmdRaiseException('df -aT | grep %s | awk \'{print $3,$4,$7}\'' % mount_point)
        for pool_storage in all_pool_storages:
            t = threading.Thread(target=get_pool_metrics,args=(pool_storage, pool_type, zone,))
            t.setDaemon(True)
            t.start()
            t.join()

def get_pool_metrics(pool_storage, pool_type, zone):
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
    try:
        output = loads(runCmdRaiseException('qemu-img info -U --output json %s' % (disk), use_read=True))
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

def get_macs(vm):
    if not vm:
        return []
    runCmdAndGetOutput('virsh dumpxml %s > /tmp/%s.xml' % (vm, vm))
    tree = ET.parse('/tmp/%s.xml' % vm)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    macs = []
    captionList = root.findall("devices")
    for caption in captionList:
        interfaces = caption.findall("interface")
        for interface in interfaces:
            mac_element = interface.find("mac")
            if "address" in mac_element.keys():
                macs.append(mac_element.get("address"))
    return macs

def collect_vm_metrics(zone):
    vm_list = list_active_vms()
    for vm in vm_list:
        t = threading.Thread(target=get_vm_metrics,args=(vm, zone,))
        t.setDaemon(True)
        t.start()
        t.join()
        
def get_vm_metrics(vm, zone):
    resource_utilization = {'vm': vm, 'cpu_metrics': {}, 'mem_metrics': {},
                            'disks_metrics': [], 'networks_metrics': []}
#     cpus = len(get_vcpus(vm)[0])
#     print(cpus)
    cpu_stats = runCmdRaiseException('virsh cpu-stats --total %s' % vm)
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
    mem_stats = runCmdRaiseException('virsh dommemstat %s' % vm)
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
        blk_dev_stats1 = runCmdRaiseException('virsh domblkstat --device %s --domain %s' % (disk_device, vm))
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
        blk_dev_stats2 = runCmdRaiseException('virsh domblkstat --device %s --domain %s' % (disk_device, vm))
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
        net_dev_stats1 = runCmdRaiseException('virsh domifstat --interface %s --domain %s' % (mac, vm))
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
        net_dev_stats2 = runCmdRaiseException('virsh domifstat --interface %s --domain %s' % (mac, vm))
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
    vm_cpu_system_proc_rate.labels(zone, HOSTNAME, vm).set(resource_utilization['cpu_metrics']['cpu_system_rate'])
    vm_cpu_usr_proc_rate.labels(zone, HOSTNAME, vm).set(resource_utilization['cpu_metrics']['cpu_user_rate'])
    vm_cpu_idle_rate.labels(zone, HOSTNAME, vm).set(resource_utilization['cpu_metrics']['cpu_idle_rate'])
    vm_mem_total_bytes.labels(zone, HOSTNAME, vm).set(resource_utilization['mem_metrics']['mem_available'])
    vm_mem_available_bytes.labels(zone, HOSTNAME, vm).set(resource_utilization['mem_metrics']['mem_unused'])
    vm_mem_buffers_bytes.labels(zone, HOSTNAME, vm).set(resource_utilization['mem_metrics']['mem_buffers'])
    vm_mem_rate.labels(zone, HOSTNAME, vm).set(resource_utilization['mem_metrics']['mem_rate'])
    for disk_metrics in resource_utilization['disks_metrics']:
        vm_disk_read_requests_per_secend.labels(zone, HOSTNAME, vm, disk_metrics['device']).set(disk_metrics['disk_read_requests_per_secend'])
        vm_disk_read_bytes_per_secend.labels(zone, HOSTNAME, vm, disk_metrics['device']).set(disk_metrics['disk_read_bytes_per_secend'])
        vm_disk_write_requests_per_secend.labels(zone, HOSTNAME, vm, disk_metrics['device']).set(disk_metrics['disk_write_requests_per_secend'])
        vm_disk_write_bytes_per_secend.labels(zone, HOSTNAME, vm, disk_metrics['device']).set(disk_metrics['disk_write_bytes_per_secend'])
    for net_metrics in resource_utilization['networks_metrics']:
        vm_network_receive_bytes_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_read_bytes_per_secend'])
        vm_network_receive_drops_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_read_drops_per_secend'])
        vm_network_receive_errors_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_read_errors_per_secend'])
        vm_network_receive_packages_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_read_packages_per_secend'])
        vm_network_send_bytes_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_write_bytes_per_secend'])
        vm_network_send_drops_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_write_drops_per_secend'])
        vm_network_send_errors_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_write_errors_per_secend'])
        vm_network_send_packages_per_secend.labels(zone, HOSTNAME, vm, net_metrics['device']).set(net_metrics['network_write_packages_per_secend'])
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
        
def main():
    start_http_server(19998)
    config.load_kube_config(config_file=TOKEN)
    zone = get_field_in_kubernetes_node(HOSTNAME, ['metadata', 'labels', 'zone'])
    while True:
        collect_vm_metrics(zone)
        collect_storage_metrics(zone)
        time.sleep(10)
        
if __name__ == '__main__':
    main()
    # print get_disks_spec('vmtest222')
#     import pprint
#     set_vm_mem_period('vm010', 5)
#     pprint.pprint(collect_vm_metrics("vm010"))