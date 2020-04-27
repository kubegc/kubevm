'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''
from json import loads, load
import xmltodict

from libvirt_util import get_graphics, is_snapshot_exists, is_pool_exists, get_pool_path
import json

'''
Import python libs
'''
import re
import fcntl
import socket
import shlex
import errno
from functools import wraps
import os, sys, time, signal, atexit, subprocess
import threading
import random
import socket
import pprint
import datetime
import ConfigParser
from dateutil.tz import gettz
from pprint import pformat
from six import iteritems
from xml.etree import ElementTree
from collections import namedtuple

'''
Import third party libs
'''
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr

DEFAULT_TT_FILE_PATH = '/root/noVNC/websockify/token/token.conf'
RESOURCE_FILE_PATH = '/etc/kubevmm/resource'

def get_IP():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr

def modify_token(vm_name, op):
    file_dir = os.path.split(DEFAULT_TT_FILE_PATH)[0]
    print file_dir
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    lines = []
    if os.path.exists(DEFAULT_TT_FILE_PATH):
        with open(DEFAULT_TT_FILE_PATH, "r") as f:
            lines = f.readlines()

    with open(DEFAULT_TT_FILE_PATH, "w") as f:
        print 'debug'
        for line in lines:
            if line.strip('\n').split(':')[0] != vm_name:
                f.write(line)
        if op != 'Stopped':
            vnc_info = get_graphics(vm_name)
            if vnc_info['listen'] == '0.0.0.0':
                newline = vm_name + ': ' + get_IP() + ':' + vnc_info['port'] + '\n'
                f.write(newline)
            else:
                newline = vm_name + ': ' + vnc_info['listen'] + ':' + vnc_info['port'] +'\n'
                f.write(newline)

def get_l2_network_info(name):
    data = {'bridgeInfo': {}}
    '''
    Get bridge informations.
    '''
    data['bridgeInfo']['name'] = name
    data['bridgeInfo']['uuid'] = runCmdRaiseException('ovs-vsctl get bridge %s _uuid' % name)[0].strip()
    ports = runCmdRaiseException('ovs-vsctl get bridge %s ports' % name)[0].strip().replace('[', '').replace(']','').replace(' ','').split(',')
    list_ports = []
    for port in ports:
        a_port = {}
        a_port['uuid'] = port
        a_port['name'] = runCmdRaiseException('ovs-vsctl get port %s name' % port)[0].strip()
        a_port['vlan'] = runCmdRaiseException('ovs-vsctl get port %s tag' % port)[0].strip()
        list_interfaces = []
        interfaces = runCmdRaiseException('ovs-vsctl get port %s interfaces' % port)[0].strip().replace('[', '').replace(']','').replace(' ','').split(',')
        for interface in interfaces:
            a_interface = {}
            a_interface['uuid'] = interface
            a_interface['mac'] = runCmdRaiseException('ovs-vsctl get interface %s mac_in_use' % interface)[0].strip()
            a_interface['name'] = runCmdRaiseException('ovs-vsctl get interface %s name' % interface)[0].strip()
            list_interfaces.append(a_interface)
        a_port['interfaces'] = list_interfaces
        list_ports.append(a_port)
    data['bridgeInfo']['ports'] = list_ports
    return data

def qeury_and_prepare_by_path(path):
    runCmd('kubectl get vmd -o=jsonpath="{range .items[?(@.spec.volume.current==\"/mnt/localfs/pooldir/pooldir/diskdirclone/diskdirclone\")]}{.metadata.name}{\"\t\"}{.spec.nodeName}{\"\n\"}{end}"')

def get_l3_network_info(name):
    cfg = "/etc/kubevmm/config"
    if not os.path.exists(cfg):
        cfg = "/home/kubevmm/bin/config"
    config_raw = parser()
    config_raw.read(cfg)
    token = config_raw.get('Kubernetes', 'token_file')
    
    master_ip = runCmdRaiseException('cat %s | grep server |awk -F"server:" \'{print$2}\' | awk -F"https://" \'{print$2}\' | awk -F":" \'{print$1}\'' % token)[0].strip()
    nb_port = '6641'
#     sb_port = '6642'
    data = {'switchInfo': '', 'routerInfo': '', 'gatewayInfo': ''}
    '''
    Get switch informations.
    '''
    switchInfo = {'id': '', 'name': '', 'ports': []}
    lines = runCmdRaiseException('ovn-nbctl --db=tcp:%s:%s show %s' % (master_ip, nb_port, name))
#     if not (len(lines) -1) % 4 == 0:
#         raise Exception('ovn-nbctl --db=tcp:%s:%s show %s error: wrong return value %s' % (master_ip, nb_port, name, lines))
    if lines:
        (_, switchInfo['id'], switchInfo['name']) = str.strip(lines[0].replace('(', '').replace(')', '')).split(' ')
        ports = lines[1:]
        portsInfo = []
        list_ports = []
        a_port = []
        _start = False
        for i in ports:
            if i.find('port ') != -1 and not _start:
                _start = True
                a_port.append(i)
            elif i.find('port ') != -1 and _start:
                list_ports.append(a_port)
                a_port = []
                a_port.append(i)
            elif i == ports[-1]:
                a_port.append(i)
                list_ports.append(a_port)
            else:
                a_port.append(i)
        for a_port in list_ports:
            portInfo = {'name': '', 'addresses': [], 'type': '', 'router_port':''}
            for line in a_port:
                if line.find('port ') != -1:
                    (_, portInfo['name']) = str.strip(line).split(' ')
                elif line.find('type:') != -1:
                    (_, portInfo['type']) = str.strip(line).split(': ')
                elif line.find('addresses:') != -1:
                    (_, portInfo['addresses']) = str.strip(line).split(': ')
                elif line.find('router-port:') != -1:
                    (_, portInfo['router_port']) = str.strip(line).split(': ')
                elif line.find('tag:') != -1:
                    (_, portInfo['tag']) = str.strip(line).split(': ')
            portsInfo.append(portInfo)
        switchInfo['ports'] = portsInfo
    data['switchInfo'] = switchInfo
    '''
    Get router informations.
    '''
    routerInfo = {'id': '', 'name': '', 'ports': []}
    lines = runCmdRaiseException('ovn-nbctl --db=tcp:%s:%s show %s-router' % (master_ip, nb_port, name))
    if lines:
        (_, routerInfo['id'], routerInfo['name']) = str.strip(lines[0].replace('(', '').replace(')', '')).split(' ')
        ports = lines[1:]
        portsInfo = []
        list_ports = []
        a_port = []
        _start = False
        for i in ports:
            if i.find('port ') != -1 and not _start:
                _start = True
                a_port.append(i)
            elif i.find('port ') != -1 and _start:
                list_ports.append(a_port)
                a_port = []
                a_port.append(i)
            elif i == ports[-1]:
                a_port.append(i)
                list_ports.append(a_port)
            else:
                a_port.append(i)
        for a_port in list_ports:
            portInfo = {'name': '', 'mac': '', 'networks': []}
            for line in a_port:
                if line.find('port ') != -1:
                    (_, portInfo['name']) = str.strip(line).split(' ')
                elif line.find('mac:') != -1:
                    (_, portInfo['mac']) = str.strip(line).split(': ')
                elif line.find('networks:') != -1:
                    (_, portInfo['networks']) = str.strip(line).split(': ')
            portsInfo.append(portInfo)
        routerInfo['ports'] = portsInfo
    data['routerInfo'] = routerInfo
    '''
    Get gateway informations.
    '''
    gatewayInfo = {'id': '', 'server_mac': '', 'router': '', 'server_id': '', 'lease_time': ''}
    switchId = switchInfo.get('id')
#     if not switchId:
#         raise Exception('ovn-nbctl --db=tcp:%s:%s show %s error: no id found!' % (master_ip, nb_port, name))
    if switchId:
        cmd = 'ovn-nbctl --db=tcp:%s:%s show %s | grep dhcpv4id | awk -F"dhcpv4id-%s-" \'{print$2}\''% (master_ip, nb_port, name, name)
    #     print(cmd)
        lines = runCmdRaiseException(cmd)
#         if not lines:
#             raise Exception('error occurred: ovn-nbctl --db=tcp:%s:%s list DHCP_Options  | grep -B 3 "%s"  | grep "_uuid" | awk -F":" \'{print$2}\'' % (master_ip, nb_port, switchId))
        if lines:
            gatewayInfo['id'] = lines[0].strip()
            cmd = 'ovn-nbctl --db=tcp:%s:%s dhcp-options-get-options %s' % (master_ip, nb_port, gatewayInfo['id'])
        #     print(cmd)
            lines = runCmdRaiseException(cmd)
            for line in lines:
                if line.find('server_mac') != -1:
                    (_, gatewayInfo['server_mac']) = line.strip().split('=')
                elif line.find('router') != -1:
                    (_, gatewayInfo['router']) = line.strip().split('=')
                elif line.find('server_id') != -1:
                    (_, gatewayInfo['server_id']) = line.strip().split('=')
                elif line.find('lease_time') != -1:
                    (_, gatewayInfo['lease_time']) = line.strip().split('=')
    data['gatewayInfo'] = gatewayInfo
    return data

def get_address_set_info(name):
    cfg = "/etc/kubevmm/config"
    if not os.path.exists(cfg):
        cfg = "/home/kubevmm/bin/config"
    config_raw = parser()
    config_raw.read(cfg)
    token = config_raw.get('Kubernetes', 'token_file')
    
    master_ip = runCmdRaiseException('cat %s | grep server |awk -F"server:" \'{print$2}\' | awk -F"https://" \'{print$2}\' | awk -F":" \'{print$1}\'' % token)[0].strip()
    nb_port = '6641'
    data = {'addressInfo': ''}
    addressInfo = {'_uuid': '', 'addresses': [], 'external_ids': {}, 'name': ''}
    cmd = 'ovn-nbctl --db=tcp:%s:%s list Address_Set %s' % (master_ip, nb_port, name)
    lines = runCmdRaiseException(cmd)
    for line in lines:
        if line.find('_uuid') != -1:
            (_, addressInfo['_uuid']) = line.strip().split(': ')
        elif line.find('addresses') != -1:
            (_, addressInfo['addresses']) = line.strip().split(': ')
        elif line.find('external_ids') != -1:
            (_, addressInfo['external_ids']) = line.strip().split(': ')
        elif line.find('name') != -1:
            (_, addressInfo['name']) = line.strip().split(': ')
    data['addressInfo'] = addressInfo
    return data

def get_field_in_kubernetes_node(name, index):
    try:
        v1_node_list = client.CoreV1Api().list_node(label_selector='host=%s' % name)
        jsondict = v1_node_list.to_dict()
        items = jsondict.get('items')
        if items:
            return get_field(items[0], index)
        else:
            return None
    except:
        return None

def get_field_in_kubernetes_by_index(name, group, version, plural, index):
    try:
        if not index or not list(index):
            return None
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name)
        return get_field(jsondict, index)
    except:
        return None
    
def get_node_name_from_kubernetes(group, version, namespace, plural, metadata_name):
    try:
        jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
            group=group, version=version, namespace=namespace, plural=plural, name=metadata_name)
    except ApiException, e:
        if e.reason == 'Not Found':
            return None
        else:
            raise e
    return jsonStr['metadata']['labels']['host']

def get_ha_from_kubernetes(group, version, namespace, plural, metadata_name):
    try:
        jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
            group=group, version=version, namespace=namespace, plural=plural, name=metadata_name)
    except ApiException, e:
        if e.reason == 'Not Found':
            return False
        else:
            raise e
    if 'ha' in jsonStr['metadata']['labels'].keys():
        return True
    else:
        return False
    
def get_field(jsondict, index):
    retv = None
    '''
    Iterate keys in 'spec' structure and map them to real CMDs in back-end.
    Note that only the first CMD will be executed.
    '''
    contents = jsondict
    for layer in index[:-1]:
#         print(contents)
        contents = contents.get(layer)
    if not contents:
        return None
    for k, v in contents.items():
        if k == index[-1]:
            retv = v
    return retv

def getCmdKey(jsondict):
    spec = get_spec(jsondict)
    the_cmd_keys = []
    if spec:
        '''
        Iterate keys in 'spec' structure and map them to real CMDs in back-end.
        Note that only the first CMD will be executed.
        '''
        lifecycle = spec.get('lifecycle')
        if not lifecycle:
            return None
        keys = lifecycle.keys()
        for key in keys:
            the_cmd_keys.append(key)
    return the_cmd_keys[0] if the_cmd_keys else None
    
def get_volume_snapshots(path):
    cmd = 'qemu-img info -U %s' % path
    try:
        std_out = runCmdRaiseException(cmd)
    except:
        cmd = 'qemu-img info %s' % path
        std_out = runCmdRaiseException(cmd)
    start = False
    snapshots = {'snapshot': []}
    for line in std_out:
        line = line.strip()
        if line.startswith('ID  '):
            start = True
            continue
        if line.startswith('Format '):
            break;
        if start:
            data = re.split('\s+', line)
            if len(data) == 6:
                snapshot = {}
                snapshot['id'] = data[0].strip()
                snapshot['name'] = data[1].strip()
                snapshot['date'] = '%s %s' % (data[3].strip(), data[4].strip())
                snapshots['snapshot'].append(snapshot)
                continue
            else:
                pass
    return snapshots

def singleton(pid_filename):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            pid = str(os.getpid())
            pidfile = open(pid_filename, 'a+')
            try:
                fcntl.flock(pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                return
            pidfile.seek(0)
            pidfile.truncate()
            pidfile.write(pid)
            pidfile.flush()
            pidfile.seek(0)

            ret = f(*args, **kwargs)

            try:
                pidfile.close()
            except IOError, err:
                if err.errno != 9:
                    return
            os.remove(pid_filename)
            return ret
        return decorated
    return decorator

def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        return False
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            return False
    else:
        return True

def get_hostname_in_lower_case():
    cfg = "/etc/kubevmm/config"
    if not os.path.exists(cfg):
        cfg = "/home/kubevmm/bin/config"
    config_raw = parser()
    config_raw.read(cfg)
    prefix = config_raw.get('Kubernetes', 'hostname_prefix')
    if prefix == 'vm':
        return 'vm.%s' % socket.gethostname().lower()
    else:
        return socket.gethostname().lower()
    
def normlize(s):
    return s[:1].upper() + s[1:]

def now_to_datetime():
    time_zone = gettz('Asia/Shanghai')
    return datetime.datetime.now(tz=time_zone)

def now_to_micro_time():
    time_zone = gettz('Asia/Shanghai')
    dt = datetime.datetime.now(tz=time_zone)
    return time.mktime(dt.timetuple()) + dt.microsecond / 1000000.0
    
def now_to_timestamp(digits = 10):
    time_stamp = time.time()
    digits = 10 ** (digits -10)
    time_stamp = int(round(time_stamp*digits))
    return time_stamp

class RotatingOperation: 
    def __init__(self):
        pass
    
    def option(self):
        pass
    
    def rotating_option(self):
        pass

'''
Switch string in file
Parameters:
    x: target file.
    y: replaced value.
    z: replacement value.
    s:
        { 1: only replace 1th match.
          'g': replace all matches.
        }
'''
def string_switch(x,y,z,s=1):
    with open(x, "r") as f:
        lines = f.readlines()
 
    with open(x, "w") as f_w:
        n = 0
        if s == 1:
            for line in lines:
                if y in line:
                    line = line.replace(y,z)
                    f_w.write(line)
                    n += 1
                    break
                f_w.write(line)
                n += 1
            for i in range(n,len(lines)):
                f_w.write(lines[i])
        elif s == 'g':
            for line in lines:
                if y in line:
                    line = line.replace(y,z)
                f_w.write(line)

'''
Run back-end command in subprocess.
'''
def runCmd(cmd):
    std_err = None
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            return str.strip(std_out[0])
        else:
            return std_out
    finally:
        p.stdout.close()
        p.stderr.close()

def runCmdRaiseException(cmd, head='VirtctlError', use_read=False):
    std_err = None
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        if use_read:
            std_out = p.stdout.read()
            std_err = p.stderr.read()
        else:
            std_out = p.stdout.readlines()
            std_err = p.stderr.readlines()
        if std_err:
            raise ExecuteException(head, std_err)
        return std_out
    finally:
        p.stdout.close()
        p.stderr.close()

def report_failure(name, jsondict, error_reason, error_message, group, version, plural):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                      version=version, 
                                                                      namespace='default', 
                                                                      plural=plural, 
                                                                      name=name)
    jsondict = deleteLifecycleInJson(jsondict)
    jsondict = updateDescription(jsondict)
    body = addExceptionMessage(jsondict, error_reason, error_message)
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def report_success(name, jsondict, success_reason, success_message, group, version, plural):
    jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group,
                                                                      version=version,
                                                                      namespace='default',
                                                                      plural=plural,
                                                                      name=name)
    jsondict = deleteLifecycleInJson(jsondict)
    jsondict = updateDescription(jsondict)
    body = addPowerStatusMessage(jsondict, success_reason, success_message)
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

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

def updateDescription(jsondict):
    if jsondict:
        spec = get_spec(jsondict)    
        if spec:
            spec['description'] = {'lastOperationTimeStamp': int(round(time.time()*1000))}
    return jsondict

def updateNodeName(jsondict):
    if jsondict:
        spec = get_spec(jsondict)    
        if spec:
            jsondict['spec']['nodeName'] = get_hostname_in_lower_case()
    return jsondict    
        
def addPowerStatusMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'waiting':{'message':message, 'reason':reason}}}}
        spec = get_spec(jsondict)
        if spec:
            spec['status'] = status
            spec['powerstate'] = reason
    return jsondict

def addExceptionMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'waiting':{'message':message, 'reason':reason}}}}
        spec = get_spec(jsondict)
        if spec:
            spec['status'] = status
    return jsondict

# def addPowerStatusMessage(jsondict, reason, message):
#     if jsondict:
#         status = {'conditions':{'state':{'powerstate':{'message':message, 'reason':reason}}}}
#         status1 = {'powerstate':{'message':message, 'reason':reason}}
#         spec = get_spec(jsondict)
#         if spec:
#             if not status.has_key('conditions'):
#                 spec['status'].update(status)
#             else:
#                 spec['status']['conditions']['state'].update(status1)
#     return jsondict
# 
# def addExceptionMessage(jsondict, reason, message):
#     if jsondict:
#         status = {'conditions':{'state':{'exception':{'message':message, 'reason':reason}}}}
#         status1 = {'exception':{'message':message, 'reason':reason}}
#         spec = get_spec(jsondict)
#         if spec:
#             if not status.has_key('conditions'):
#                 spec['status'].update(status)
#             else:
#                 spec['status']['conditions']['state'].update(status1)
#     return jsondict

def addSnapshots(vol_path, jsondict):
    snapshot_json = get_volume_snapshots(vol_path)
    jsondict['volume'].update(snapshot_json)
    return jsondict

def add_spec_in_volume(jsondict, field, value):
    jsondict['volume'][field] = value
    return jsondict

def updateDomainBackup(vm_json):
    domain = vm_json.get('domain')
    if domain:
        os = domain.get('os')
        if os:
            boot = os.get('boot')
            if boot:
                os['boot'] = _addListToSpecificField(boot)
        domain['os'] = os
        sec_label = domain.get('seclabel')
        if sec_label:
            domain['seclabel'] = _addListToSpecificField(sec_label)
        devices = domain.get('devices')
        if devices:
            channel = devices.get('channel')
            if channel:
                devices['channel'] = _addListToSpecificField(channel)
            graphics = devices.get('graphics')
            if graphics:
                devices['graphics'] = _addListToSpecificField(graphics)   
            video = devices.get('video')
            if video:
                devices['video'] = _addListToSpecificField(video) 
            _interface = devices.get('_interface')
            if _interface:
                devices['_interface'] = _addListToSpecificField(_interface)  
            console = devices.get('console')
            if console:
                devices['console'] = _addListToSpecificField(console)  
            controller = devices.get('controller')
            if controller:
                devices['controller'] = _addListToSpecificField(controller)  
            rng = devices.get('rng')
            if rng:
                devices['rng'] = _addListToSpecificField(rng)  
            serial = devices.get('serial')
            if serial:
                devices['serial'] = _addListToSpecificField(serial)  
            disk = devices.get('disk')
            if disk:
                devices['disk'] = _addListToSpecificField(disk)
        domain['devices'] = devices
    return vm_json

def update_vm_json(jsonstr):
    json = jsonstr.replace('_interface', 'interface').replace('_transient', 'transient').replace(
        'suspend_to_mem', 'suspend-to-mem').replace('suspend_to_disk', 'suspend-to-disk').replace(
            'on_crash', 'on-crash').replace('on_poweroff', 'on-poweroff').replace('on_reboot', 'on-reboot').replace(
            'nested_hv', 'nested-hv').replace('read_bytes_sec', 'read-bytes-sec').replace(
                'write_bytes_sec', 'write-bytes-sec').replace('"_', '"@').replace("'_", "'@").replace(
                        'text', '#text').replace('\'', '"')
    return json

def iterate_dict(area, i=0):
#     result = {}
    for k,v in area.items():
        if isinstance(v, int):
            area[k] = "%d" % v
#             area[k] = "+1-{}".format(v)
        if isinstance(area[k], dict):
            iterate_dict(area[k], i+1)
        if isinstance(area[k], list):
            for j in area[k]:
                if isinstance(j, dict):
                    iterate_dict(j, i+1)
    return area

def trans_dict_to_xml(jsdict):
    xml=''
    try:
        xml = xmltodict.unparse(jsdict,encoding='utf-8',pretty=True)
#         pprint.pprint(xml)
    except:
        xml = xmltodict.unparse({'domain':jsdict},encoding='utf-8',pretty=True)
#         pprint.pprint(xml)
    finally:
#         print(xml)
        return xml

def updateDomain(jsondict):
    with open('%s/../arraylist.cfg' % os.path.dirname(__file__)) as fr:
        for line in fr:
            l = str.strip(line)
            alist = l.split('-')
            _userDefinedOperationInList('domain', jsondict, alist)
    return jsondict

def updateDomainSnapshot(jsondict):
    with open('%s/../arraylist.cfg' % os.path.dirname(__file__)) as fr:
        for line in fr:
            l = str.strip(line)
            alist = l.split('-')
            _userDefinedOperationInList('domainsnapshot', jsondict, alist)
    return jsondict

def _addListToSpecificField(data):
    if isinstance(data, list):
        return data
    else:
        return [data]

'''
Cautions! Do not modify this function because it uses reflections!
'''    
def _userDefinedOperationInList(field, jsondict, alist):
    jsondict = jsondict[field]
    tmp = jsondict
    do_it = False
    for index, value in enumerate(alist):
        if index == 0:
            if value != field:
                break;
            continue
        tmp = tmp.get(value)
        if not tmp:
            do_it = False
            break;
        do_it = True
    if do_it:
        tmp2 = None
        for index, value in enumerate(alist):
            if index == 0:
                tmp2 = 'jsondict'
            else:
                tmp2 = '{}[\'{}\']'.format(tmp2, value)
        exec('{} = {}').format(tmp2, _addListToSpecificField(tmp))
    return
    
class ExecuteException(Exception):
    def __init__(self, reason, message):
        self.reason = reason
        self.message = message       

class KubevmmException(Exception):
    def __init__(self, reason, message):
        self.reason = reason
        self.message = message      

def randomUUID():
    u = [random.randint(0, 255) for ignore in range(0, 16)]
    u[6] = (u[6] & 0x0F) | (4 << 4)
    u[8] = (u[8] & 0x3F) | (2 << 6)
    return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2,
                     "%02x" * 6]) % tuple(u)

def randomMAC():
    mac = [ 0x52, 0x54, 0x00,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def createVmi(metadata_name, target):
    if not is_pool_exists(target):
        raise ExecuteException('Wrong "target" %s: no such directory.' % target)
    path = get_pool_path(target)
    return (['echo "vmi = %s" >> %s' % (path, RESOURCE_FILE_PATH)], 
            ['sed -i \'/vmi = %s/d\' %s' % (path, RESOURCE_FILE_PATH)])

def deleteVmi(metadata_name, target):
    if not is_pool_exists(target):
        raise ExecuteException('Wrong "target" %s: no such directory.' % target)
    path = get_pool_path(target)
    return (['sed -i \'/vmi = %s/d\' %s' % (path, RESOURCE_FILE_PATH)], 
            ['echo "vmi = %s" >> %s' % (path, RESOURCE_FILE_PATH)])

def createVmdi(metadata_name, target):
    if not is_pool_exists(target):
        raise ExecuteException('Wrong "target" %s: no such directory.' % target)
    path = get_pool_path(target)
    return (['echo "vmdi = %s" >> %s' % (path, RESOURCE_FILE_PATH)], 
            ['sed -i \'/vmdi = %s/d\' %s' % (path, RESOURCE_FILE_PATH)])

def deleteVmdi(metadata_name, target):
    if not is_pool_exists(target):
        raise ExecuteException('Wrong "target" %s: no such directory.' % target)
    path = get_pool_path(target)
    return (['sed -i \'/vmdi = %s/d\' %s' % (path, RESOURCE_FILE_PATH)], 
            ['echo "vmdi = %s" >> %s' % (path, RESOURCE_FILE_PATH)])

class Domain(object):
    def __init__(self, libvirt_domain):
        self.libvirt_domain = libvirt_domain
        self.name = libvirt_domain.name()
        self.libvirt_snapshot = None

    def get_disks(self):
        """ Gets all domain disk as namedtuple('DiskInfo', ['device', 'file', 'format']) """
        # root node
        root = ElementTree.fromstring(self.libvirt_domain.XMLDesc())

        # search <disk type='file' device='disk'> entries
        disks = root.findall("./devices/disk[@device='disk']")

        # for every disk get drivers, sources and targets
        drivers = [disk.find("driver").attrib for disk in disks]
        sources = [disk.find("source").attrib for disk in disks]
        targets = [disk.find("target").attrib for disk in disks]

        # iterate drivers, sources and targets
        if len(drivers) != len(sources) != len(targets):
            raise RuntimeError("Drivers, sources and targets lengths are different %s:%s:%s" % (
                len(drivers), len(sources), len(targets)))

        disk_info = namedtuple('DiskInfo', ['device', 'file', 'format'])

        # all disks info
        disks_info = []

        for i in range(len(sources)):
            disks_info.append(disk_info(targets[i]["dev"], sources[i]["file"], drivers[i]["type"]))

        return disks_info
    
    def get_snapshot_disks(self, snapshot):
        """ Gets all domain disk as namedtuple('DiskInfo', ['device', 'file', 'format']) """
        # root node
        root = ElementTree.fromstring(self.libvirt_domain.snapshotLookupByName(snapshot).getXMLDesc())
        
        # search <disk type='file' device='disk'> entries
        disks = root.findall("./disks/disk[@snapshot='external']")

        # for every disk get drivers, sources and targets
        drivers = [disk.find("driver").attrib for disk in disks]
        sources = [disk.find("source").attrib for disk in disks]
        targets = [disk.attrib for disk in disks]

        # iterate drivers, sources and targets
        if len(drivers) != len(sources) != len(targets):
            raise RuntimeError("Drivers, sources and targets lengths are different %s:%s:%s" % (
                len(drivers), len(sources), len(targets)))

        disk_info = namedtuple('DiskInfo', ['device', 'file', 'format'])

        # all disks info
        disks_info = []

        for i in range(len(sources)):
            disks_info.append(disk_info(targets[i]["name"], sources[i]["file"], drivers[i]["type"]))

        return disks_info
    
    def verify_disk_write_lock(self, file_path):
        backing_file = DiskImageHelper.get_backing_file(file_path, True)
        return backing_file
    
    def merge_snapshot(self, base):
        """ Merges base to snapshot and removes old disk files """
        disks = self.get_disks()
        snapshot_disks = self.get_snapshot_disks(base)
        disks_to_remove = []
        merge_snapshots_cmd = ''
        disks_to_remove_cmd = ''
        snapshots_to_delete_cmd = ''
        for disk in disks:
            current_disk_files = [disk.file]
            current_disk_files += (DiskImageHelper.get_backing_files_tree(disk.file))
            if len(current_disk_files) == 1:
                continue
            base_disk = ''
            for snapshot_disk in snapshot_disks:
                if snapshot_disk.file == disk.file:
                    raise ExecuteException('VirtctlError', '400, Bad Request! Cannot merge current disk %s to itself.' % snapshot_disk.file)
                elif snapshot_disk.file in current_disk_files:
                    base_disk = DiskImageHelper.get_backing_file(snapshot_disk.file)
                else:
                    continue
            if not base_disk:
#                 disks_to_remove.append(a_disk for a_disk in current_disk_files)
                continue
            else:
                start_it = False
                for a_disk in current_disk_files:
                    if a_disk == disk.file and a_disk != base_disk:
                        start_it = True
                    elif a_disk == base_disk:
                        break;
                    elif start_it:
                        disks_to_remove.append(a_disk)
                    else:
                        continue
                merge_snapshots_cmd += 'virsh blockpull --domain %s --path %s --base %s --wait;' % (self.name, disk.file, base_disk)
        for disk_to_remove in disks_to_remove:
            self.verify_disk_write_lock(disk_to_remove)
            disks_to_remove_cmd += 'rm -f %s;' % disk_to_remove
            snapshot_name = os.path.basename(disk_to_remove)
            if not is_snapshot_exists(snapshot_name, self.name):
                snapshot_name = os.path.splitext(os.path.basename(disk_to_remove))[1][1:] \
                if len(os.path.splitext(os.path.basename(disk_to_remove))) == 2 else None
            if snapshot_name and is_snapshot_exists(snapshot_name, self.name):
                if snapshots_to_delete_cmd.find('--snapshotname %s' % snapshot_name) != -1:
                    continue
                else:
                    snapshots_to_delete_cmd += 'virsh snapshot-delete --domain %s --snapshotname %s --metadata;' % (self.name, snapshot_name)
            # remove old disk device files without current ones
        return (merge_snapshots_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd)
    
    def revert_snapshot(self, snapshot, revert_to_backing_file=False):
        """ Revert snapshot and removes invalid snapshots and their disk files """
        disks = self.get_disks()
        snapshot_disks = self.get_snapshot_disks(snapshot)
        unplug_disks_cmd = ''
        unplug_disks_rollback_cmd = ''
        plug_disks_cmd = ''
        plug_disks_rollback_cmd = ''
        disks_to_remove = []
#         revert_snapshot_cmd = 'virsh snapshot-revert --domain %s --snapshotname %s' % (self.name, snapshot)
        disks_to_remove_cmd = ''
        snapshots_to_delete_cmd = ''
        for disk in disks:
            current_disk_files = [disk.file]
            current_disk_files += (DiskImageHelper.get_backing_files_tree(disk.file))
            if len(current_disk_files) == 1:
                continue
            base_disk = ''
            base_disk_target = ''
            for snapshot_disk in snapshot_disks:
                if snapshot_disk.file == disk.file and not revert_to_backing_file:
                    raise ExecuteException('VirtctlError', '400, Bad Request! Cannot revert current disk %s to itself.' % snapshot_disk.file)
                elif snapshot_disk.file in current_disk_files:
                    if revert_to_backing_file:
                        base_disk = DiskImageHelper.get_backing_file(snapshot_disk.file)
                    else:
                        base_disk = snapshot_disk.file
                    base_disk_target = snapshot_disk.device
                else:
                    continue
            if not base_disk:
#                 disks_to_remove.append(a_disk for a_disk in current_disk_files)
                continue
            else:
                start_it = False
                current_disk_files.reverse()
                for a_disk in current_disk_files:
                    if a_disk == base_disk:
                        start_it = True
                    elif a_disk == disk.file:
                        disks_to_remove.append(a_disk)
                        break;
                    elif start_it:
                        self.verify_disk_write_lock(a_disk)
                        disks_to_remove.append(a_disk)
                    else:
                        continue
                unplug_disks_cmd += 'virsh detach-disk --domain %s --target %s --config;' % (self.name, disk.file)
                unplug_disks_rollback_cmd += 'virsh attach-disk --subdriver qcow2 --domain %s --source %s --target %s --config;' % (self.name, disk.file, disk.device)
                plug_disks_cmd += 'virsh attach-disk --subdriver qcow2 --domain %s --source %s --target %s --config;' % (self.name, base_disk, base_disk_target)
                plug_disks_rollback_cmd += 'virsh detach-disk --domain %s --target %s --config;' % (self.name, base_disk)
        for disk_to_remove in disks_to_remove:
            disks_to_remove_cmd += 'rm -f %s;' % disk_to_remove
            snapshot_name = os.path.basename(disk_to_remove)
            if not is_snapshot_exists(snapshot_name, self.name):
                snapshot_name = os.path.splitext(os.path.basename(disk_to_remove))[1][1:] \
                if len(os.path.splitext(os.path.basename(disk_to_remove))) == 2 else None
            if snapshot_name and is_snapshot_exists(snapshot_name, self.name):
                if snapshots_to_delete_cmd.find('--snapshotname %s' % snapshot_name) != -1:
                    continue
                else:
                    snapshots_to_delete_cmd += 'virsh snapshot-delete --domain %s --snapshotname %s --metadata;' % (self.name, snapshot_name)
            # remove old disk device files without current ones
        return (unplug_disks_cmd, unplug_disks_rollback_cmd, plug_disks_cmd, plug_disks_rollback_cmd, disks_to_remove_cmd, snapshots_to_delete_cmd)
    
class DiskImageHelper(object):
    @staticmethod
    def get_backing_file(file, raise_it=False):
        """ Gets backing file for disk image """
        get_backing_file_cmd = "qemu-img info %s" % file
        try:
            out = runCmdRaiseException(get_backing_file_cmd, use_read=True)
        except Exception, e:
            if raise_it:
                raise e
            get_backing_file_cmd = "qemu-img info -U %s" % file
            out = runCmdRaiseException(get_backing_file_cmd, use_read=True)
        lines = out.decode('utf-8').split('\n')
        for line in lines:
            if re.search("backing file:", line):
                return str(line.strip().split()[2])
        return None

    @staticmethod
    def get_backing_files_tree(file):
        """ Gets all backing files (snapshot tree) for disk image """
        backing_files = []
        backing_file = DiskImageHelper.get_backing_file(file)
        while backing_file is not None:
            backing_files.append(backing_file)
            backing_file = DiskImageHelper.get_backing_file(backing_file)
        return backing_files

    @staticmethod
    def set_backing_file(backing_file, file):
        """ Sets backing file for disk image """
        set_backing_file_cmd = "qemu-img rebase -u -b %s %s" % (backing_file, file)
        runCmdRaiseException(set_backing_file_cmd)
        
def get_rebase_backing_file_cmds(source_dir, target_dir):
    source_config_file = '%s/config.json' % (source_dir)
    with open(source_config_file, "r") as f:
        config = load(f)
    source_current = config.get('current')
    backing_chain = DiskImageHelper.get_backing_files_tree(source_current)
    set_backing_file_cmd = []
    if backing_chain:
        backing_chain = backing_chain[:-1]
        backing_chain.reverse()
        backing_chain.append(source_current)
        for disk_file in backing_chain:
            new_backing = DiskImageHelper.get_backing_file(disk_file).replace(source_dir, target_dir)
            new_file = disk_file.replace(source_dir, target_dir)
            cmd = 'qemu-img rebase -u -b %s %s' % (new_backing, new_file)
            set_backing_file_cmd.append(cmd.encode('utf-8'))
    else:
        raise ExecuteException('VirtctlError', 'Cannot find backing files of %s' % source_current)
    return set_backing_file_cmd

def check_vdiskfs_by_disk_path(path):
    all_path = []
    if path.find("--disk") >= 0:
        for disk in path.split("--disk"):
            all_path.append(disk.split(',')[0])
    else:
        all_path.append(path)

    is_vdiskfs = False
    for disk_path in all_path:
        result, data = runCmdWithResult('kubesds-adm showDiskPool --path %s' % disk_path, False)
        if data and 'pooltype' in data.keys():
            if data['pooltype'] == 'vdiskfs':
                is_vdiskfs = True
    return is_vdiskfs

'''
Run back-end command in subprocess.
'''
def runCmdWithResult(cmd, raise_it=True):
    std_err = None
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
                raise ExecuteException('VirtctlError', error_msg)
        if std_err:
            raise ExecuteException('VirtctlError', std_err)
    finally:
        p.stdout.close()
        p.stderr.close()

def get_sn_chain(ss_path):
    return runCmdWithResult('qemu-img info -U --backing-chain --output json %s' % ss_path)

def get_disk_snapshots(ss_path):
    ss_chain = get_sn_chain(ss_path)
    snapshots = []
    for disk_info in ss_chain:
        if disk_info['filename'] != ss_path:
            snapshots.append(disk_info['filename'])
    return snapshots

def list_all_disks(path, disk_type = 'f'):
    try:
        return runCmdRaiseException("find %s -type %s ! -name '*.json' ! -name '*.temp' ! -name 'content' ! -name '.*' ! -name '*.xml' ! -name '*.pem' | grep -v overlay2" % (path, disk_type))
    except:
        return []

class UserDefinedEvent(object):
    
    swagger_types = {
        'event_metadata_name': 'str',
        'time_start': 'datetime',
        'time_end': 'datetime',
        'involved_object_name': 'str',
        'involved_object_kind': 'str',
        'message': 'str',
        'reason': 'str',
        'event_type': 'str'
    }
    
    def __init__(self, event_metadata_name, time_start, time_end, involved_object_name, involved_object_kind, message, reason, event_type):
        self.event_metadata_name = event_metadata_name
        self.time_start = time_start
        self.time_end = time_end
        self.involved_object_name = involved_object_name
        self.involved_object_kind = involved_object_kind
        self.message = message
        self.reason = reason
        self.event_type = event_type
        
    def registerKubernetesEvent(self):
        '''
        More details please @See: 
            https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Event.md
        '''
        involved_object = client.V1ObjectReference(name=self.involved_object_name, kind=self.involved_object_kind, namespace='default')
        metadata = client.V1ObjectMeta(name=self.event_metadata_name, namespace='default')
        body = client.V1Event(first_timestamp=self.time_start, last_timestamp=self.time_end, metadata=metadata, involved_object=involved_object, message=self.message, reason=self.reason, type=self.event_type)
        client.CoreV1Api().replace_namespaced_event(self.event_metadata_name, 'default', body, pretty='true')
        
    def updateKubernetesEvent(self):
        '''
        More details please @See: 
            https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Event.md
        '''
        involved_object = client.V1ObjectReference(name=self.involved_object_name, kind=self.involved_object_kind, namespace='default')
        metadata = client.V1ObjectMeta(name=self.event_metadata_name, namespace='default')
        body = client.V1Event(first_timestamp=self.time_start, last_timestamp=self.time_end, metadata=metadata, involved_object=involved_object, message=self.message, reason=self.reason, type=self.event_type)
        client.CoreV1Api().replace_namespaced_event(self.event_metadata_name, 'default', body, pretty='true')

    def get_event_metadata_name(self):
        return self.__event_metadata_name


    def get_time_start(self):
        return self.__time_start


    def get_time_end(self):
        return self.__time_end


    def get_involved_object_name(self):
        return self.__involved_object_name


    def get_involved_object_kind(self):
        return self.__involved_object_kind


    def get_message(self):
        return self.__message


    def get_reason(self):
        return self.__reason


    def get_event_type(self):
        return self.__event_type


    def set_event_metadata_name(self, value):
        self.__event_metadata_name = value


    def set_time_start(self, value):
        self.__time_start = value


    def set_time_end(self, value):
        self.__time_end = value


    def set_involved_object_name(self, value):
        self.__involved_object_name = value


    def set_involved_object_kind(self, value):
        self.__involved_object_kind = value


    def set_message(self, value):
        self.__message = value


    def set_reason(self, value):
        self.__reason = value


    def set_event_type(self, value):
        self.__event_type = value


    def del_event_metadata_name(self):
        del self.__event_metadata_name


    def del_time_start(self):
        del self.__time_start


    def del_time_end(self):
        del self.__time_end


    def del_involved_object_name(self):
        del self.__involved_object_name


    def del_involved_object_kind(self):
        del self.__involved_object_kind


    def del_message(self):
        del self.__message


    def del_reason(self):
        del self.__reason


    def del_event_type(self):
        del self.__event_type
        
    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    event_metadata_name = property(get_event_metadata_name, set_event_metadata_name, del_event_metadata_name, "event_metadata_name's docstring")
    time_start = property(get_time_start, set_time_start, del_time_start, "time_start's docstring")
    time_end = property(get_time_end, set_time_end, del_time_end, "time_end's docstring")
    involved_object_name = property(get_involved_object_name, set_involved_object_name, del_involved_object_name, "involved_object_name's docstring")
    involved_object_kind = property(get_involved_object_kind, set_involved_object_kind, del_involved_object_kind, "involved_object_kind's docstring")
    message = property(get_message, set_message, del_message, "message's docstring")
    reason = property(get_reason, set_reason, del_reason, "reason's docstring")
    event_type = property(get_event_type, set_event_type, del_event_type, "event_type's docstring")

class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            time.sleep(1)

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()


class CDaemon:
    '''
    a generic daemon class.
    usage: subclass the CDaemon class and override the run() method
    stderr:
    verbose:
    save_path:
    '''
    def __init__(self, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=022, verbose=1):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = save_path
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True
 
    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
 
        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)
 
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
 
        sys.stdout.flush()
        sys.stderr.flush()
 
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        if self.stderr:
            se = file(self.stderr, 'a+', 0)
        else:
            se = so
 
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
 
        def sig_handler(signum, frame):
            self.daemon_alive = False
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)
 
        if self.verbose >= 1:
            print 'daemon process started ...'
 
        atexit.register(self.del_pid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)
 
    def get_pid(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid
 
    def del_pid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
 
    def start(self, *args, **kwargs):
        if self.verbose >= 1:
            print 'ready to starting ......'
        #check for a pid file to see if the daemon already runs
        pid = self.get_pid()
        if pid:
            msg = 'pid file %s already exists, is it already running?\n'
            sys.stderr.write(msg % self.pidfile)
            sys.exit(1)
        #start the daemon
        self.daemonize()
        self.run(*args, **kwargs)
 
    def stop(self):
        if self.verbose >= 1:
            print 'stopping ...'
        pid = self.get_pid()
        if not pid:
            msg = 'pid file [%s] does not exist. Not running?\n' % self.pidfile
            sys.stderr.write(msg)
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            return
        #try to kill the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError, err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
            if self.verbose >= 1:
                print 'Stopped!'
 
    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)
 
    def is_running(self):
        pid = self.get_pid()
        #print(pid)
        return pid and os.path.exists('/proc/%d' % pid)
 
    def run(self, *args, **kwargs):
        'NOTE: override the method in subclass'
        print 'base class run()'

if __name__ == '__main__':
#     cfg = "/etc/kubevmm/config"
#     if not os.path.exists(cfg):
#         cfg = "/home/kubevmm/bin/config"
#     config_raw = parser()
#     config_raw.read(cfg)
#     TOKEN = config_raw.get('Kubernetes', 'token_file')
#     config.load_kube_config(config_file=TOKEN)
#     print(get_field_in_kubernetes_by_index('wyw123', 'cloudplus.io', 'v1alpha3', 'virtualmachinedisks', ['volume', 'format_specific', 'data', 'refcount_bits']))
#     pprint.pprint(get_l3_network_info("switch1"))
    check_vdiskfs_by_disk_path('/var/lib/libvirt/cstor/8c8a012b6092487f8cd6745735bf28a2/8c8a012b6092487f8cd6745735bf28a2/vmtest111disk1/vmtest111disk1')
#     pprint.pprint(get_l2_network_info("br-native"))
#     from libvirt_util import _get_dom
#     domain = Domain(_get_dom("950646e8c17a49d0b83c1c797811e004"))
#     try:
#     print(get_rebase_backing_file_cmds("/var/lib/libvirt/pooltest3/wyw123/", "/var/lib/libvirt/pooltest4/wyw123/"))
# #         print(domain.merge_snapshot("snapshot3"))
# #         print(domain.revert_snapshot("snapshot3"))
#     except Exception, e:
#         print e.message
#     volume = {'volume': {"allocation": {"_unit": "bytes","text": 200704}}}
#     volume.get('volume').update(get_volume_snapshots('/var/lib/libvirt/images/test1.qcow2'))
#     print(volume)
#     print(get_volume_snapshots('/var/lib/libvirt/images/test4.qcow2'))