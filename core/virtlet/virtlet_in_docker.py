# -*- coding: utf-8 -*-
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
 
import os, sys, time
from threading import Thread
sys.path.append("..")

'''
Import third party libs
'''
from kubernetes import config

'''
Import local libs
'''
from utils.misc import singleton
from utils import constants
from utils import logger
# from services.libvirt_event_handler import main as libvirt_event_handler
from services.os_event_handler import main as os_event_handler
from services.host_reporter import main as host_reporter
# from services.monitor import main as monitor

logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTLET_LOG)

@singleton(constants.KUBEVMM_VIRTLET_DOCKER_LOCK)
def main():
    '''virtlet进程，运行在docker容器里
    '''
    logger.debug("---------------------------------------------------------------------------------")
    logger.debug("------------------------Welcome to Virtlet Daemon.-------------------------------")
    logger.debug("------Copyright (2021, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn, wuheng@otcaix.iscas.ac.cn----------")
    logger.debug("---------------------------------------------------------------------------------")
    
    if os.path.exists(constants.KUBERNETES_TOKEN_FILE):
        config.load_kube_config(config_file=constants.KUBERNETES_TOKEN_FILE)
        try:
#             thread_1 = Thread(target=libvirt_event_handler)
#             thread_1.daemon = True
#             thread_1.name = 'libvirt_event_handler'
#             thread_1.start()
            thread_2 = Thread(target=os_event_handler)
            thread_2.daemon = True
            thread_2.name = 'os_event_handler'
            thread_2.start()
#             if not is_kubernetes_master():
            thread_3 = Thread(target=host_reporter)
            thread_3.daemon = True
            thread_3.name = 'host_reporter'
            thread_3.start()
#             thread_4 = Thread(target=monitor)
#             thread_4.daemon = True
#             thread_4.name = 'monitor'
#             thread_4.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                return
#             thread_1.join()
            thread_2.join()
#             if not is_kubernetes_master():
            thread_3.join()
#             thread_4.join()
        except:
            logger.error('Oops! ', exc_info=1)
            
if __name__ == '__main__':
    main()


