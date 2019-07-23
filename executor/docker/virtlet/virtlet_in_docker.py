'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
 
import os, sys, ConfigParser, traceback, time
from threading import Thread

'''
Import third party libs
'''
from kubernetes import config

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
from utils import logger
from libvirt_event_handler import main as libvirt_event_handler
from os_event_handler import main as os_event_handler
from host_cycler import main as host_cycler

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 
    
cfg = "%s/default.cfg" % os.path.dirname(os.path.realpath(__file__))
config_raw = parser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtlet.log')

def main():
    logger.debug("---------------------------------------------------------------------------------")
    logger.debug("------------------------Welcome to Virtlet Daemon.-------------------------------")
    logger.debug("------Copyright (2019, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn, wuheng@otcaix.iscas.ac.cn----------")
    logger.debug("------------------------------liuhe18@otcaix.iscas.ac.cn-------------------------")
    logger.debug("---------------------------------------------------------------------------------")
    
    if os.path.exists(TOKEN):
        config.load_kube_config(config_file=TOKEN)
    try:
        thread_1 = Thread(target=libvirt_event_handler)
        thread_1.daemon = True
        thread_1.name = 'libvirt_event_handler'
        thread_1.start()
        thread_2 = Thread(target=os_event_handler)
        thread_2.daemon = True
        thread_2.name = 'os_event_handler'
        thread_2.start()
        thread_3 = Thread(target=host_cycler)
        thread_3.daemon = True
        thread_3.name = 'host_cycler'
        thread_3.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return
        thread_1.join()
        thread_2.join()
        thread_3.join()
    except:
        logger.error('Oops! ', exc_info=1)
            
if __name__ == '__main__':
    main()


