'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''

'''
Import python libs
'''
import fcntl
import errno
from functools import wraps
import os, sys, time, signal, atexit, subprocess
import threading
import random
import socket
import datetime
from dateutil.tz import gettz
from pprint import pformat
from six import iteritems

'''
Import third party libs
'''
from kubernetes import client
from kubernetes.client.rest import ApiException

def get_l3_network_info(name):
    data = {'switchInfo': '', 'routerInfo': '', 'gatewayInfo': ''}
    '''
    Get switch informations.
    '''
    switchInfo = {'id': '', 'name': '', 'ports': []}
    lines = runCmdRaiseException('ovn-nbctl show %s' % name)
    if not (len(lines) -1) % 4 == 0:
        raise Exception('ovn-nbctl show %s error: wrong return value %s' % (name, lines))
    (_, switchInfo['id'], switchInfo['name']) = str.strip(lines[0].replace('(', '').replace(')', '')).split(' ')
    ports = lines[1:]
    portsInfo = []
    for i in range(4, len(ports)+1):
        portInfo = {}
        (_, portInfo['name']) = str.strip(ports[i-4]).split(' ')
        (_, portInfo['type']) = str.strip(ports[i-3]).split(': ')
        (_, portInfo['addresses']) = str.strip(ports[i-2]).split(': ')
        (_, portInfo['router_port']) = str.strip(ports[i-1]).split(': ')
        portsInfo.append(portInfo)
        i += 4
    switchInfo['ports'] = portsInfo
    data['switchInfo'] = switchInfo
    '''
    Get router informations.
    '''
    routerInfo = {'id': '', 'name': '', 'ports': []}
    lines = runCmdRaiseException('ovn-nbctl show r4%s' % name)
    if not (len(lines) -1) % 3 == 0:
        raise Exception('ovn-nbctl show r4%s error: wrong return value %s' % (name, lines))
    (_, routerInfo['id'], routerInfo['name']) = str.strip(lines[0].replace('(', '').replace(')', '')).split(' ')
    ports = lines[1:]
    portsInfo = []
    for i in range(3, len(ports)+1):
        portInfo = {}
        (_, portInfo['name']) = str.strip(ports[i-4]).split(' ')
        (_, portInfo['mac']) = str.strip(ports[i-2]).split(': ')
        (_, portInfo['networks']) = str.strip(ports[i-1]).split(': ')
        portsInfo.append(portInfo)
        i += 3
    routerInfo['ports'] = portsInfo
    data['routerInfo'] = routerInfo
    '''
    Get gateway informations.
    '''
    gatewayInfo = {'id': '', 'server_mac': '', 'router': '', 'server_id': '', 'lease_time': ''}
    switchId = switchInfo.get('id')
    if not switchId:
        raise Exception('ovn-nbctl show %s error: no id found!' % (name))
    gatewayId = runCmdRaiseException('ovn-nbctl list DHCP_Options  | grep -B 3 "%s"  | grep "_uuid" | awk -F":" \'{print$2}\'' % switchId)[0].strip()
    print(data)
    

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

def runCmdRaiseException(cmd):
    std_err = None
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_err:
            raise ExecuteException('VirtctlError', std_err)
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
    body = addExceptionMessage(jsondict, error_reason, error_message)
    retv = client.CustomObjectsApi().replace_namespaced_custom_object(
        group=group, version=version, namespace='default', plural=plural, name=name, body=body)
    return retv

def _getSpec(jsondict):
    spec = jsondict.get('spec')
    if not spec:
        raw_object = jsondict.get('raw_object')
        if raw_object:
            spec = raw_object.get('spec')
    return spec    

def deleteLifecycleInJson(jsondict):
    if jsondict:
        spec = _getSpec(jsondict)
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
    return jsondict

def updateJsonRemoveLifecycle(jsondict, body):
    if jsondict:
        spec = _getSpec(jsondict)
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
            spec.update(body)
    return jsondict
        
def addPowerStatusMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'waiting':{'message':message, 'reason':reason}}}}
        spec = _getSpec(jsondict)
        if spec:
            spec['status'] = status
    return jsondict

def addExceptionMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'waiting':{'message':message, 'reason':reason}}}}
        spec = _getSpec(jsondict)
        if spec:
            spec['status'] = status
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
    get_l3_network_info('ttt')