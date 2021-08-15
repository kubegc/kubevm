'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

'''

import ConfigParser
import socket
from kubernetes import client, config, watch, stream

cfg = "./default.cfg"
config_raw = ConfigParser.RawConfigParser()
config_raw.read(cfg)

TOKEN = config_raw.get('Kubernetes', 'token_file')
PLURAL = config_raw.get('VirtualMachine', 'plural')
VERSION = config_raw.get('VirtualMachine', 'version')
GROUP = config_raw.get('VirtualMachine', 'group')

LABEL = 'host=%s' % (socket.gethostname())
# CMD = 'http://127.0.0.1:9090/apis/[GROUP]/[VERSION]/[PLURAL]?labelSelector=host%3Dlocalhost.localdomain2&watch=true'

if __name__ == '__main__':
    config.load_kube_config(config_file=TOKEN)
#     crd = client.ApiextensionsV1beta1Api().read_custom_resource_definition(NAME)
#     client.CustomObjectsApi().list_cluster_custom_object_with_http_info(group=GROUP, version=VERSION, plural=PLURAL, labelSelector='host=a', watch=True);
    print('hello')
    w = watch.Watch()
    kwargs = {}
    kwargs['label_selector'] = LABEL
    kwargs['watch'] = True
    for vm in w.stream(client.CustomObjectsApi().list_cluster_custom_object,
                                group=GROUP, version=VERSION, plural=PLURAL, **kwargs):
        print(vm)
    pass