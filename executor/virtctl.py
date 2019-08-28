'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
 
import os, sys, ConfigParser, traceback

'''
Import third party libs
'''
from kubernetes import config

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
import invoker
from utils.utils import CDaemon, singleton
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
logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtctl.log')

class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=022, verbose=1):
        CDaemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name
 
    @singleton('/var/run/virtctl_daemon.pid')
    def run(self, output_fn, **kwargs):
        config.load_kube_config(config_file=TOKEN)
        try:
            invoker.main()
        except:
            logger.error('Oops! ', exc_info=1)
            
def daemonize():
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print help_msg
        sys.exit(1)
    p_name = 'virtctl'
    pid_fn = '/var/run/virtctl_daemon.pid'
    log_fn = '/var/log/virtctl.log'
    err_fn = '/var/log/virtctl.log'
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


