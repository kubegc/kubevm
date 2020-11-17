'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
 
import os, sys, ConfigParser, traceback, time, socket
from threading import Thread
from multiprocessing import Process

'''
Import third party libs
'''
from kubernetes import config

'''
Import local libs
'''
from utils.utils import singleton, runCmd
from utils import logger
from libvirt_event_handler import main as libvirt_event_handler
from libvirt_event_handler_for_4_0 import main as libvirt_event_handler_4_0

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
HOSTNAME = socket.gethostname()
logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

@singleton('/var/run/libvirt_watcher_in_docker.pid')
def main():
    logger.debug("---------------------------------------------------------------------------------")
    logger.debug("--------------------Welcome to Libvirt Watcher Daemon.---------------------------")
    logger.debug("------Copyright (2019, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn, wuheng@otcaix.iscas.ac.cn----------")
    logger.debug("------------------------------liuhe18@otcaix.iscas.ac.cn-------------------------")
    logger.debug("---------------------------------------------------------------------------------")
    
    if os.path.exists(TOKEN):
        config.load_kube_config(config_file=TOKEN)
        try:
            thread_1 = Process(target=get_libvirt_event_handler())
            thread_1.daemon = True
            thread_1.name = 'libvirt_event_handler'
            thread_1.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                return
            thread_1.join()
        except:
            config.load_kube_config(config_file=TOKEN)
            logger.error('Oops! ', exc_info=1)
            
def is_kubernetes_master():
    if runCmd('kubectl get node %s | grep master' % HOSTNAME):
        return True
    else:
        return False
    
def get_libvirt_event_handler():
    retv = runCmd('virsh --version')
    if retv.strip().startswith("4.0"):
        return libvirt_event_handler_4_0
    else:
        return libvirt_event_handler
            
if __name__ == '__main__':
    main()


