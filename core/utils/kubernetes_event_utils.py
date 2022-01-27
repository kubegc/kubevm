#coding=UTF-8
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''
import os
import time
from kubernetes import client, config
try:
    from utils import logger
    from utils.misc import randomUUID, now_to_datetime, UserDefinedEvent
    from utils import constants
except:
    import logger
    from misc import randomUUID, now_to_datetime, UserDefinedEvent
    import constants

logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTCTL_LOG)
TOKEN = constants.KUBERNETES_TOKEN_FILE

class KubernetesEvent:
    
    def __init__(self, metadata_name, the_cmd_key, k8s_object_kind, event_id):
        self.involved_object_name = metadata_name
        self.involved_object_kind = k8s_object_kind
        self.involved_cmd_key = the_cmd_key
        self.event_metadata_name = randomUUID()
        self.reporter = constants.KUBEVMM_VIRTCTL_SEVICE_NAME
        self.event_id = event_id
        self.time_start = now_to_datetime()

    def create_event(self, status, event_type):
        time_end = now_to_datetime()
        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' \
        % (self.involved_object_kind, self.involved_object_name, self.involved_cmd_key, status, 
           self.reporter, self.event_id, (time_end - self.time_start).total_seconds())
        event = UserDefinedEvent(self.event_metadata_name, self.time_start, time_end, 
                                 self.involved_object_name, self.involved_object_kind, 
                                 message, self.involved_cmd_key, event_type) 
        for i in range(1,10):
            try:
                config.load_kube_config(config_file=TOKEN)
                event.registerKubernetesEvent()
                return
            except Exception as e:
                if i == 9:
                    raise e
                else:
                    time.sleep(3)   
            
    def update_evet(self, status, event_type):
        time_end = now_to_datetime()
        message = 'type:%s, name:%s, operation:%s, status:%s, reporter:%s, eventId:%s, duration:%f' \
        % (self.involved_object_kind, self.involved_object_name, self.involved_cmd_key, status, 
           self.reporter, self.event_id, (time_end - self.time_start).total_seconds())
        event = UserDefinedEvent(self.event_metadata_name, self.time_start, time_end, 
                                 self.involved_object_name, self.involved_object_kind, 
                                 message, self.involved_cmd_key, event_type)    
        for i in range(1,10):
            try:
                config.load_kube_config(config_file=TOKEN)
                event.updateKubernetesEvent()
                return
            except Exception as e:
                if i == 9:
                    raise e
                else:
                    time.sleep(3)