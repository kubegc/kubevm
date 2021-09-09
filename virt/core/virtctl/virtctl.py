# -*- coding: utf-8 -*-
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
 
import os, sys
sys.path.append("..")

'''
Import third party libs
'''
from kubernetes import config

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
from utils import constants
from utils.misc import CDaemon, singleton
from utils import logger
from services import watcher

logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTCTL_LOG)

class ClientDaemon(CDaemon):
    '''virtctl程序启动器
    '''
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0o22, verbose=1):
        CDaemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name
 
    @singleton(constants.KUBEVMM_VIRTCTL_SERVICE_LOCK)
    def run(self, output_fn, **kwargs):
        '''virtctl程序启动器，运行在宿主机的守护进程里
        '''
        config.load_kube_config(config_file=constants.KUBERNETES_TOKEN_FILE)
        try:
            watcher.main()
        except:
            logger.error('Oops! ', exc_info=1)
            
def daemonize():
    '''守护进程的实现
    '''
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)
    p_name = constants.KUBEVMM_VIRTCTL_SEVICE_NAME
    pid_fn = constants.KUBEVMM_VIRTCTL_SERVICE_LOCK
    log_fn = constants.KUBEVMM_VIRTCTL_LOG
    err_fn = constants.KUBEVMM_VIRTCTL_LOG
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
            print('process [%s] is running ......' % cD.get_pid())
        else:
            print('daemon process [%s] stopped' %cD.name)
    else:
        print('invalid argument!')
        print(help_msg)    
 
 
if __name__ == '__main__':
    daemonize()


