'''
Copyright (2019, ) Institute of Software, Chinese Academy of 

@author: wuheng@otcaix.iscas.ac.cn
@author: wuyuewen@otcaix.iscas.ac.cn
'''

import sys
import os
import time
import json
import subprocess
import traceback
import shutil
import socket
import signal

from utils.utils import pid_exists

HOSTNAME = socket.gethostname()

try:
    with open('VERSION', 'r') as fr:
        VERSION = fr.read().strip()
except:
    print('error: upload \'VERSION\' file failed!')
    sys.exit(1)
    
try:
    with open('/var/run/virtctl_in_docker.pid', 'r') as fr:
        virtctl_pid = int(fr.read().strip())
    if not pid_exists(virtctl_pid):
        virtctl_pid = -1
except:
    virtctl_pid = -1
    
try:
    with open('/var/run/virtlet_in_docker.pid', 'r') as fr:
        virtlet_pid = int(fr.read().strip())
    if not pid_exists(virtlet_pid):
        virtlet_pid = -1
except:
    virtlet_pid = -1
    
def run_virtctl():
    return runCmd('docker run -itd -h %s --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v%s bash virtctl.sh' % (HOSTNAME, VERSION))

def run_virtlet():
    return runCmd('docker run -itd -h %s --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v%s bash virtlet.sh' % (HOSTNAME, VERSION))

def start():
    if virtctl_pid == -1:
        run_virtctl()
    else:
        print('service \'virtctl\' is running in pid <%s>' % str(virtctl_pid))
    if virtlet_pid == -1:
        run_virtlet()
    else:
        print('service \'virtlet\' is running in pid <%s>' % str(virtlet_pid))

def stop():
    if virtctl_pid == -1:
        print('service \'virtctl\' is not running')
    else:
        os.kill(virtctl_pid, signal.SIGINT)
    if virtlet_pid == -1:
        print('service \'virtlet\' is not running') 
    else:
        os.kill(virtlet_pid, signal.SIGINT)   

def restart():
    stop()
    start()

def status():
    if virtctl_pid == -1:    
        print('service \'virtctl\' is not running')
    else:
        print('service \'virtctl\' is running in pid <%s>' % str(virtctl_pid))
    if virtlet_pid == -1:
        print('service \'virtlet\' is not running')
    else:
        print('service \'virtlet\' is running in pid <%s>' % str(virtlet_pid))

def update(pack):
    pass

def version():
    print(VERSION)

def main():
    usage_msg = 'Usage: %s <start|stop|restart|status|update|--version|--help>\n' % sys.argv[0]
    help_msg = 'All support commands: \n' + \
                '    start                           start kubevmm services\n' + \
                '    stop                            stop kubevmm services\n' + \
                '    restart                         restart kubevmm services\n' + \
                '    status                          show kubevmm services\n' + \
                '    update                          update kubevmm services\n' + \
                '    --version                         show kubevmm version\n' + \
                '    --help                            print help\n\n'
    help_update = 'Name:\n' + \
                '    %s update [--target <package>]\n' % sys.argv[0] + \
                'Options:\n' + \
                '    --target <package>  update package file\n\n'
    if len(sys.argv) < 2:
        print(usage_msg)
        sys.exit(1)
    if sys.argv[1] == '--help':
        print(help_msg)
        sys.exit(1)
 
    params = []
    for i in range(2, len(sys.argv)):
        params.append(sys.argv[i])
        i = i+i
    
    if sys.argv[1] == 'start':
        if len(params) != 0:
            print('error: invalid arguments!')
            print(usage_msg)
            sys.exit(1)            
        start()
    elif sys.argv[1] == 'stop':
        if len(params) != 0:
            print('error: invalid arguments!')
            print(usage_msg)
            sys.exit(1)   
        stop()
    elif sys.argv[1] == 'restart':
        if len(params) != 0:
            print('error: invalid arguments!')
            print(usage_msg)
            sys.exit(1)   
        restart()
    elif sys.argv[1] == 'status':
        if len(params) != 0:
            print('error: invalid arguments!')
            print(usage_msg)
            sys.exit(1)   
        status()
    elif sys.argv[1] == 'update':
        if len(params) == 1:
            if params[0] == '--help':
                print(help_update)
                sys.exit(1)
            else:
                print('error: command \'update\' requires [--target <package>] option')
                sys.exit(1)
        elif len(params) == 2:
            if params[0] != '--target':
                print('error: command \'update\' requires [--target <package>] option')
                sys.exit(1)
            pack = params[1]
            update(pack)
        else:
            print('error: command \'update\' requires [--target <package>] option')
            sys.exit(1)   
    elif sys.argv[1] == '--version':
        version()
    else:
        print('error: invalid arguments!')
        print(usage_msg)


'''
Run back-end command in subprocess.
'''
def runCmd(cmd):
    std_err = None
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.read()
        std_err = p.stderr.read()
        if std_out:
#             msg = ''
#             for index,line in enumerate(std_out):
#                 if not str.strip(line):
#                     continue
#                 if index == len(std_out) - 1:
#                     msg = msg + str.strip(line) + '. '
#                 else:
#                     msg = msg + str.strip(line) + ', '
#             logger.debug(str.strip(msg))
            print(std_out)
        if std_err:
#             msg = ''
#             for index, line in enumerate(std_err):
#                 if not str.strip(line):
#                     continue
#                 if index == len(std_err) - 1:
#                     msg = msg + str.strip(line) + '. ' + '***More details in %s***' % LOG
#                 else:
#                     msg = msg + str.strip(line) + ', '
#             raise ExecuteException('VirtctlError', str.strip(msg))
            print(std_err)
#             sys.exit(1)
#         return (str.strip(std_out[0]) if std_out else '', str.strip(std_err[0]) if std_err else '')
#         sys.exit(0)
        return
    finally:
        p.stdout.close()
        p.stderr.close()


# def run(cmd):
#     try:
#         result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
#         logger.debug(result)
#         print result
#     except Exception:
#         traceback.format_exc()
#         print(sys.exc_info())
#         raise ExecuteException('vmmError', sys.exc_info()[1])


if __name__ == '__main__':
    main()
