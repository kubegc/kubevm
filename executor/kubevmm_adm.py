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
    
def check_version(ignore_warning=False):
    (virtctl_running_version, _) = runCmd('docker ps | grep \"bash virtctl\" | awk \'{print $2}\' | awk -F\':\' \'{if(NF>1) print $2}\'')
    if not virtctl_running_version:
        (virtctl_running_version, _) = runCmd('docker ps | grep registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl | awk \'{print $2}\' | awk -F\':\' \'{if(NF>1) print $2}\'')
    (virtlet_running_version, _) = runCmd('docker ps | grep \"bash virtlet\" | awk \'{print $2}\' | awk -F\':\' \'{if(NF>1) print $2}\'')
    if not virtlet_running_version:
        (virtlet_running_version, _) = runCmd('docker ps | grep registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet | awk \'{print $2}\' | awk -F\':\' \'{if(NF>1) print $2}\'')
    if not ignore_warning and virtctl_running_version and virtctl_running_version != VERSION or not ignore_warning and virtlet_running_version and virtlet_running_version != VERSION:
        print('warning: mismatch version detected!') 
        (style_1, style_2, style_3, style_4) = ('\033[1;42m', '\033[0m', '\033[1;42m', '\033[0m')
        if virtctl_running_version != VERSION:
            style_1 = '\033[1;43m'
            style_2 = '\033[0m'
        if virtlet_running_version != VERSION:
            style_3 = '\033[1;43m'
            style_4 = '\033[0m'
        print('warning: \'kubevmm-adm(\033[1;42m%s\033[0m)\' mismatch with \'virtctl(%s%s%s)\' & \'virtlet(%s%s%s)\'' % (VERSION, style_1, virtctl_running_version, style_2, style_3, virtlet_running_version, style_4))
        print('\033[1;46m*strongly suggest do: %s service update\033[0m \n' % sys.argv[0])
    return (virtctl_running_version, virtlet_running_version)
    
def run_virtctl(update_stuff=False, version=VERSION):
    if update_stuff:
        script = 'virtctl-update-stuff.sh'
    else:
        script = 'virtctl.sh'
    return runCmd('docker run -itd --restart=always  --privileged=true --cap-add=sys_admin  -h %s --net=host -v /etc/kubevmm:/etc/kubevmm -v /etc/libvirt:/etc/libvirt -v /etc/sysconfig/cstor:/etc/sysconfig/cstor -v /dev:/dev -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/lib64:/usr/lib64 -v /usr/bin:/usr/bin -v /usr/lib/uraid:/usr/lib/uraid -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:%s bash %s' % (HOSTNAME, version, script))

def run_virtlet(update_stuff=False, version=VERSION):
    if update_stuff:
        script = 'virtlet-update-stuff.sh'
    else:
        script = 'virtlet.sh'
    return runCmd('docker run -itd --restart=always  --privileged=true --cap-add=sys_admin  -h %s --net=host -v /etc/kubevmm:/etc/kubevmm -v /etc/libvirt:/etc/libvirt -v /etc/sysconfig/cstor:/etc/sysconfig/cstor -v /dev:/dev -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/lib64:/usr/lib64 -v /usr/bin:/usr/bin -v /usr/lib/uraid:/usr/lib/uraid -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:%s bash %s' % (HOSTNAME, version, script))

def start(ignore_warning=False, update_stuff=False, version=VERSION):
    virtctl_err = None
    virtlet_err = None
    (virtctl_container_id, virtctl_running_version, virtlet_container_id, virtlet_running_version) = status(ignore_warning=ignore_warning)
    print('starting kubevmm(%s) services...' % version)
    time.sleep(3)
    if not virtctl_container_id:
        (_, virtctl_err) = run_virtctl(update_stuff=update_stuff, version=version)
        if virtctl_err:
            print('warning: %s\n' % (virtctl_err))
    else:
        if virtctl_running_version != version:
            print('error: a different version of service \'virtctl(%s)\' is running in container \'%s\'\n' % (virtctl_running_version, str(virtctl_container_id)))
        else:
            print('do noting: service \'virtctl\' is running in container \'%s\'' % str(virtctl_container_id))
    if not virtlet_container_id:
        (_, virtlet_err) = run_virtlet(update_stuff=update_stuff, version=version)
        if virtlet_err:
            print('warning: %s\n' % (virtlet_err))
    else:
        if virtlet_running_version != version:
            print('error: a different version of service \'virtlet(%s)\' is running in container \'%s\'\n' % (virtlet_running_version, str(virtlet_container_id)))
        else:
            print('do noting: service \'virtlet\' is running in container \'%s\'\n' % str(virtlet_container_id))
    runCmd('kubesds-rpc start')
    if virtctl_err or virtlet_err:
        sys.exit(1)

def stop(ignore_warning=False):
    virtctl_err = None
    virtlet_err = None
    (virtctl_container_id, virtctl_running_version, virtlet_container_id, virtlet_running_version) = status(ignore_warning=ignore_warning)
    print('stopping kubevmm services...')
    if not virtctl_container_id:
        print('do noting: service \'virtctl\' is not running')
    else:
        print('>>> stopping \'virtctl\' in container \'%s\'...' % (str(virtctl_container_id)))
        (_, virtctl_err) = runCmd('docker stop %s; docker rm %s' % (virtctl_container_id, virtctl_container_id))
        if virtctl_err:
            print('warning: %s\n' % (virtctl_err))
    if not virtlet_container_id:
        print('do noting: service \'virtlet\' is not running\n') 
    else:
        print('>>> stopping \'virtlet\' in container \'%s\'...\n' % (str(virtlet_container_id)))
        (_, virtlet_err) = runCmd('docker stop %s; docker rm %s' % (virtlet_container_id, virtlet_container_id)) 
        if virtlet_err:
            print('warning: %s\n' % (virtlet_err))
    runCmd('kubesds-rpc stop')
    if virtctl_err or virtlet_err:
        sys.exit(1)
        
def restart_kubesds_rpc(ignore_warning=False):
    (_, _err) = runCmd('kubesds-rpc restart')
    if _err and not ignore_warning:
        print('warning: %s\n' % (_err))
        sys.exit(1)

def restart(ignore_warning=False):
    stop(ignore_warning=ignore_warning)
    start(ignore_warning=ignore_warning)
    restart_kubesds_rpc(ignore_warning=ignore_warning)

def status(print_result=False, ignore_warning=False):
    (virtctl_running_version, virtlet_running_version) = check_version(ignore_warning=ignore_warning)
    (virtctl_container_id, virtctl_err) = runCmd("docker ps | grep \"bash virtctl\" | awk \'NR==1{print $1}\'")
    if not virtctl_container_id:
        (virtctl_container_id, virtctl_err) = runCmd("docker ps | grep registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl | awk \'NR==1{print $1}\'")
    (virtlet_container_id, virtlet_err) = runCmd("docker ps | grep \"bash virtlet\" | awk \'NR==1{print $1}\'")
    if not virtlet_container_id:
        (virtlet_container_id, virtlet_err) = runCmd("docker ps | grep registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet | awk \'NR==1{print $1}\'")
    if virtctl_err:
        print('warning: %s\n' % (virtctl_err))
    if virtlet_err:
        print('warning: %s\n' % (virtlet_err))
    if print_result:
        if not virtctl_container_id:    
            print('service \'virtctl\' is not running')
        else:
            print('service \'virtctl(%s)\' is running in container \'%s\'' % (virtctl_running_version, str(virtctl_container_id)))
        if not virtlet_container_id:
            print('service \'virtlet\' is not running')
        else:
            print('service \'virtlet(%s)\' is running in container \'%s\'' % (virtlet_running_version, str(virtlet_container_id)))
        (kubesds_rpc_status, _) =  runCmd('kubesds-rpc status')
        print('service \'kubesds-rpc\' %s' % kubesds_rpc_status)
    if virtctl_err or virtlet_err:
        sys.exit(1)
    return (virtctl_container_id, virtctl_running_version, virtlet_container_id, virtlet_running_version)

def update_online(version='latest'):
    print('updating online')
    print('pulling from official repository...\n')
    time.sleep(3)
    (_, virtctl_err) = runCmd("docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:%s" % version)
    (_, virtlet_err) = runCmd("docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:%s" % version)
    if virtctl_err:
        print('warning: %s\n' % (virtctl_err))
    if virtlet_err:
        print('warning: %s\n' % (virtlet_err))
    if virtctl_err or virtlet_err:
        sys.exit(1)
    stop(ignore_warning=True)
    time.sleep(1)
    start(ignore_warning=True, update_stuff=True, version=version)
    restart_kubesds_rpc(ignore_warning=True)

def update_offline(pack, ignore_warning=True):
    print('updating from package \'%s\'' % pack)
    virtctl_err = None
    virtlet_err = None
    (virtctl_container_id, virtctl_running_version, virtlet_container_id, virtlet_running_version) = status(ignore_warning=ignore_warning)
    if not virtctl_container_id:
        print('error: service \'virtctl\' is not running')
    if not virtlet_container_id:
        print('error: service \'virtlet\' is not running\n') 
    if virtctl_err or virtlet_err:
        sys.exit(1)
    print('\033[3;30;47m*step1: checking package file\033[0m')
    time.sleep(2)
    is_ready = os.path.isfile(pack)
    if not is_ready:
        print('error: wrong pack file')
        print('error: please check the path %s - not exists\n' % pack)
        sys.exit(1)
    print('    package file is ready, continue...\n')
    print('\033[3;30;47m*step2: unpacking .tar.gz file to /tmp dir\033[0m')
    time.sleep(2)
    (_, step2_err) = runCmd('tar -zxvf %s -C %s' % (pack, '/tmp'))
    if step2_err:
        print('error: %s' % step2_err)
        print('error: unpack failed, aborting...\n')
        sys.exit(1)
    print('    unpack done, continue...\n')
    print('\033[3;30;47m*step3: update virtctl & virtlet in docker\033[0m')
    time.sleep(2)
    (_, virtctl_err) = runCmd('docker cp /tmp/kubevmm-service-pack/virtctl/* %s:/home/virtctl/bin' % virtctl_container_id)
    (_, virtlet_err) = runCmd('docker cp /tmp/kubevmm-service-pack/virtlet/* %s:/home/virtlet/bin' % virtlet_container_id)
    if virtctl_err:
        print('warning: %s\n' % (virtctl_err))
    if virtlet_err:
        print('warning: %s\n' % (virtlet_err))
    if virtctl_err or virtlet_err:
        sys.exit(1)
    print('    update complete.\n')

def version(service=False, ignore_warning=False):
    if service:
        (virtctl_running_version, virtlet_running_version) = check_version(ignore_warning=ignore_warning)
        print('virtctl(%s) & virtlet(%s)' % (virtctl_running_version if virtctl_running_version else 'UNKNOWN', virtlet_running_version if virtlet_running_version else 'UNKNOWN'))
    else:
        print(VERSION)
    
def view_bar(num, total):
    r = '\r[%s%s]' % ("#"*num, " "*(100-num))
    sys.stdout.write(r)
    sys.stdout.write(str(num)+'%')
    sys.stdout.flush()

def main():
    usage_msg = 'Usage: %s <service|--version|--help>\n\n' % sys.argv[0]
    usage_service = 'Usage: %s service <start|stop|restart|status|update|--version|--help>\n\n' % sys.argv[0]
    help_subcommands = 'All support sub commands: \n' + \
                        '    service                           service management\n' + \
                        '    --version                         show kubevmm version\n' + \
                        '    --help                            print help\n\n'
    help_service = 'All support options in \'service\': \n' + \
                '    service  start                           start kubevmm services\n' + \
                '    service  stop                            stop kubevmm services\n' + \
                '    service  restart                         restart kubevmm services\n' + \
                '    service  status                          show kubevmm services\n' + \
                '    service  update                          update kubevmm services\n' + \
                '    service  --version                       show services version\n' + \
                '    service  --help                          print help\n\n'
    help_msg = help_subcommands + help_service
    help_update = 'Name:\n' + \
                '    %s service update [--online <version>|--offline <package>|--help]\n' % sys.argv[0] + \
                'Options:\n' + \
                '    --online <version>   update to an online version\n' + \
                '    --offline <package>  absolute path of package file\n\n'
    if len(sys.argv) < 2:
        print(usage_msg)
        sys.exit(1)
        
    if sys.argv[1] == '--help':
        print(help_msg)
    elif sys.argv[1] == '--version':
        version()
    elif sys.argv[1] == 'service':
        if len(sys.argv) < 3:
            print('error: invalid options!\n')
            print(usage_service)
            sys.exit(1)
        params = []
        for i in range(3, len(sys.argv)):
            params.append(sys.argv[i])
            i = i+i
        if sys.argv[2] == 'start':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(usage_service)
                sys.exit(1)            
            start()
        elif sys.argv[2] == 'stop':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(usage_service)
                sys.exit(1)   
            stop()
        elif sys.argv[2] == 'restart':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(usage_service)
                sys.exit(1)   
            restart()
        elif sys.argv[2] == 'status':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(usage_service)
                sys.exit(1)   
            status(True)
        elif sys.argv[2] == 'update':
            if params[0] == '--help':
                if len(params) != 1:
                    print('error: invalid arguments!\n')
                    print(help_update)
                    sys.exit(1)
                print(help_update)
            elif params[0] == '--online':
                if len(params) > 2:
                    print('error: invalid arguments!\n')
                    print(help_update)
                    sys.exit(1)
                elif len(params) == 2:
                    ver = params[1]
                    update_online(ver)
                else:
                    print('error: invalid arguments!\n')
                    print(help_update)
                    sys.exit(1)
            elif params[0] == '--offline':
                if len(params) > 2:
                    print('error: invalid arguments!\n')
                    print(help_update)
                    sys.exit(1)
                elif len(params) == 2:
                    pack = params[1]
                    update_offline(pack)
                else:
                    print('error: invalid arguments!\n')
                    print(help_update)
                    sys.exit(1)
            else:
                print('error: invalid arguments!\n')
                print(help_update)
                sys.exit(1)
        elif sys.argv[2] == '--version':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(usage_service)
                sys.exit(1) 
            version(service=True)
        elif sys.argv[2] == '--help':
            if len(params) != 0:
                print('error: invalid arguments!\n')
                print(usage_service)
                sys.exit(1) 
            print(help_service)
        else:
            print('error: invalid arguments!\n')
            print(usage_service)            
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
