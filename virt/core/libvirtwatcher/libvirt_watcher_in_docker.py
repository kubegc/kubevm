# -*- coding: utf-8 -*-
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''
 
import os, sys, traceback, time, socket
from threading import Thread
from multiprocessing import Process
sys.path.append("..")

'''
Import third party libs
'''
from kubernetes import config

'''
Import local libs
'''
from utils.misc import singleton, runCmd
from utils import logger
from utils import constants
    
# from services import libvirt_event_handler_for_4_0
from services import libvirt_event_handler
# from libvirt_event_handler import virt as libvirt_event_handler
# from libvirt_event_handler_for_4_0 import virt as libvirt_event_handler_4_0

TOKEN = constants.KUBERNETES_TOKEN_FILE
HOSTNAME = socket.gethostname()
logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTLET_LOG)

@singleton('/var/run/libvirt_watcher_in_docker.pid')
def main():
    logger.debug("---------------------------------------------------------------------------------")
    logger.debug("--------------------Welcome to Libvirt Watcher Daemon.---------------------------")
    logger.debug("------Copyright (2021, ) Institute of Software, Chinese Academy of Sciences------")
    logger.debug("---------author: wuyuewen@otcaix.iscas.ac.cn, wuheng@otcaix.iscas.ac.cn----------")
    logger.debug("---------------------------------------------------------------------------------")
    
    if os.path.exists(TOKEN):
        config.load_kube_config(config_file=TOKEN)
        try:
#             thread_1 = Process(target=get_libvirt_event_handler())
#             thread_1.daemon = True
#             thread_1.name = 'libvirt_event_handler'
#             thread_1.start()
#             try:
#                 while True:
#                     time.sleep(1)
#             except KeyboardInterrupt:
#                 return
#             thread_1.join()
            libvirt_event_handler.main()
        except:
            config.load_kube_config(config_file=TOKEN)
            logger.error('Oops! ', exc_info=1)
            
def is_kubernetes_master():
    if runCmd('kubectl get node %s | grep master' % HOSTNAME):
        return True
    else:
        return False
    
# def run_libvirt_event_handler():
#     retv = runCmd('virsh --version')
#     if retv.strip().startswith("4.0"):
#         libvirt_event_handler_for_4_0.main()
#     else:
#         libvirt_event_handler.main()
            
if __name__ == '__main__':
    main()


