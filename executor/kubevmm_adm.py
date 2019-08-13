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
import socket

HOSTNAME = socket.gethostname()

try:
    version_file = '/etc/kubevmm/VERSION'
    with open(version_file, 'r') as fr:
        VERSION = fr.read().strip()
except:
    print('error: can not read \'VERSION\' file %s!' % version_file)
    sys.exit(1)
    
def run_virtctl():
    return runCmd('docker run -itd -h %s --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:%s bash virtctl.sh' % (HOSTNAME, VERSION))

def run_virtlet():
    return runCmd('docker run -itd -h %s --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:%s bash virtlet.sh' % (HOSTNAME, VERSION))

def start():
    print('starting services...')
    (virtctl_container_id, virtlet_container_id) = status()
    if not virtctl_container_id:
        (_, virtctl_err) = run_virtctl()
        if virtctl_err:
            print('warning: %s' % (virtctl_err))
            sys.exit(1)
    else:
        print('do noting: service \'virtctl\' is running in container \'%s\'' % str(virtctl_container_id))
    if not virtlet_container_id:
        (_, virtlet_err) = run_virtlet()
        if virtlet_err:
            print('warning: %s' % (virtlet_err))
            sys.exit(1)
    else:
        print('do noting: service \'virtlet\' is running in container \'%s\'' % str(virtlet_container_id))

def stop():
    print('stopping services...')
    (virtctl_container_id, virtlet_container_id) = status()
    if not virtctl_container_id:
        print('do noting: service \'virtctl\' is not running')
    else:
        (_, virtctl_err) = runCmd('docker stop %s; docker rm %s' % (virtctl_container_id, virtctl_container_id))
        if virtctl_err:
            print('warning: %s' % (virtctl_err))
            sys.exit(1)
    if not virtlet_container_id:
        print('do noting: service \'virtlet\' is not running') 
    else:
        (_, virtlet_err) = runCmd('docker stop %s; docker rm %s' % (virtlet_container_id, virtlet_container_id)) 
        if virtlet_err:
            print('warning: %s' % (virtlet_err))
            sys.exit(1)

def restart():
    stop()
    start()

def status(print_result=False):
    (virtctl_container_id, virtctl_err) = runCmd("docker ps | grep registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:%s | awk \'NR==1{print $1}\'" % VERSION)
    (virtlet_container_id, virtlet_err) = runCmd("docker ps | grep registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:%s | awk \'NR==1{print $1}\'" % VERSION)
    if virtctl_err:
        print('warning: %s' % (virtctl_err))
        sys.exit(1)
    if virtlet_err:
        print('warning: %s' % (virtlet_err))
        sys.exit(1)
    if print_result:
        if not virtctl_container_id:    
            print('service \'virtctl\' is not running')
        else:
            print('service \'virtctl\' is running in container \'%s\'' % str(virtctl_container_id))
        if not virtlet_container_id:
            print('service \'virtlet\' is not running')
        else:
            print('service \'virtlet\' is running in container \'%s\'' % str(virtlet_container_id))
    return (virtctl_container_id, virtlet_container_id)

def update(pack):
    print('updating from package \'%s\'' % pack)
    print('*step 1: checking package file')
    time.sleep(2)
    is_ready = os.path.isfile(pack)
    if not is_ready:
        print('error: wrong pack file')
        print('error: please check the path %s - not exists' % pack)
        sys.exit(1)
    print('    package file is ready, continue...')
    print('*step 2: unpacking .tar.gz file to /tmp dir')
    time.sleep(3)
    (_, step2_err) = runCmd('tar -zxvf %s -C %s' % (pack, '/tmp'))
    if step2_err:
        print('error: %s' % step2_err)
        print('error: unpack failed, aborting...')
        sys.exit(1)
    print('    unpack done, continue...')
    print('*step 3: checking package dir in /tmp')
    time.sleep(2)
    check_unpack_dir = os.path.isdir('/tmp/kubevmm-%s' % VERSION)
    if not check_unpack_dir:
        print('error: wrong directory')
        print('error: please check the path %s - not exists' % check_unpack_dir)
        sys.exit(1)
    print('    package dir is ready, continue...')
    print('*step 4: updating kubevmm')
    time.sleep(2)
    runCmd('bash /tmp/kubevmm-%s/install.sh --skip-adm' % VERSION, True)
    print('    update complete.')

def version():
    print(VERSION)
    
def view_bar(num, total):
    r = '\r[%s%s]' % ("#"*num, " "*(100-num))
    sys.stdout.write(r)
    sys.stdout.write(str(num)+'%')
    sys.stdout.flush()

def main():
    usage_msg = 'Usage: %s <service|--version|--help>\n' % sys.argv[0] + \
                '       %s service <start|stop|restart|status|update>\n\n' % sys.argv[0]
    help_subcommands = 'All support sub commands: \n' + \
                        '    service                           service management\n' + \
                        '    --version                         show kubevmm version\n' + \
                        '    --help                            print help\n\n'
    help_service = 'All support options in \'service\': \n' + \
                '    service  start                           start kubevmm services\n' + \
                '    service  stop                            stop kubevmm services\n' + \
                '    service  restart                         restart kubevmm services\n' + \
                '    service  status                          show kubevmm services\n' + \
                '    service  update                          update kubevmm services\n\n'
    help_msg = usage_msg + help_subcommands + help_service
    help_update = 'Name:\n' + \
                '    %s update [--target <package>]\n' % sys.argv[0] + \
                'Options:\n' + \
                '    --target <package>  absolute path of package file\n\n'
    if len(sys.argv) < 2:
        print(usage_msg)
        sys.exit(1)
        
    if sys.argv[1] == '--help':
        print(help_msg)
        sys.exit(1)
    elif sys.argv[1] == '--version':
        version()
    elif sys.argv[1] == 'service':
        if len(sys.argv) < 3:
            print('error: invalid options!\n')
            print(help_service)
            sys.exit(1)
        params = []
        for i in range(3, len(sys.argv)):
            params.append(sys.argv[i])
            i = i+i
        if sys.argv[2] == 'start':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(help_service)
                sys.exit(1)            
            start()
        elif sys.argv[2] == 'stop':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(help_service)
                sys.exit(1)   
            stop()
        elif sys.argv[2] == 'restart':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(help_service)
                sys.exit(1)   
            restart()
        elif sys.argv[2] == 'status':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(help_service)
                sys.exit(1)   
            status(True)
        elif sys.argv[2] == 'update':
            if len(params) == 1:
                if params[0] == '--help':
                    print(help_update)
                    sys.exit(1)
                else:
                    print('error: command \'update\' requires [--target <package absolute path>] option')
                    sys.exit(1)
            elif len(params) == 2:
                if params[0] != '--target':
                    print('error: command \'update\' requires [--target <package absolute path>] option')
                    sys.exit(1)
                pack = params[1]
                update(pack)
            else:
                print('error: command \'update\' requires [--target <package absolute path>] option')
                sys.exit(1) 
        else:
            print('error: invalid options!\n')
            print(help_service)            
    else:
        print('error: invalid sub commands!\n')
        print(help_subcommands)


'''
Run back-end command in subprocess.
'''
def runCmd(cmd, show_stdout=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        if show_stdout:
            while p.poll() is None: 
                r = p.stdout.readline().decode('utf-8')
                sys.stdout.write(r)
            return
        std_out = p.stdout.read()
        std_err = p.stderr.read()
        return (std_out.strip() if std_out else None, std_err.strip() if std_err else None)
    finally:
        p.stdout.close()
        p.stderr.close()

if __name__ == '__main__':
    main()
