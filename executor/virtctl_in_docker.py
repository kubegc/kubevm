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
from utils.utils import singleton
from utils import logger

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
logger = logger.set_logger(os.path.basename(__file__), '/var/log/virtctl.log')

@singleton('/var/run/virtctl_in_docker.pid')
def main():
    if os.path.exists(TOKEN):
        config.load_kube_config(config_file=TOKEN)
        try:
            invoker.main()
        except:
            config.load_kube_config(config_file=TOKEN)
            logger.error('Oops! ', exc_info=1)
            
if __name__ == '__main__':
    main()


