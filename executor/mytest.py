'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

https://pypi.org/project/json2xml/
https://github.com/kubernetes/kubernetes/issues/51046
'''

'''
Import python libs
'''
import os
import sys
import subprocess
import ConfigParser
import socket
import string
import traceback
import pprint
import time
from threading import Thread
from json import loads
from json import dumps
from StringIO import StringIO as _StringIO
from xml.etree.ElementTree import fromstring

'''
Import third party libs
'''
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.client import V1DeleteOptions
from kubernetes.client.models.v1_namespace_status import V1NamespaceStatus
from xmltodict import unparse
from xmljson import badgerfish as bf
from libvirt import libvirtError

'''
Import local libs
'''
# sys.path.append('%s/utils' % (os.path.dirname(os.path.realpath(__file__))))
from utils.libvirt_util import undefine_with_snapshot, destroy, undefine, create, setmem, setvcpus, is_vm_active, is_vm_exists, is_volume_exists, is_snapshot_exists
from utils import logger
from utils.uit_utils import is_block_dev_exists
from utils.utils import ExecuteException, addExceptionMessage

LOG = '/var/log/virtctl.log'

logger = logger.set_logger(os.path.basename(__file__), LOG)


cmd1 = './scripts/mybackup.sh test1'
# cmd2 = 'virsh dumpxml skywind11 > /root/backup.xml'

# PATH = '/root/mybackup'

'''
Run back-end command in subprocess.
'''
def runCmd(cmd):
    std_err = None
    if not cmd:
        #         logger.debug('No CMD to execute.')
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for index,line in enumerate(std_out):
                if not str.strip(line):
                    continue
                if index == len(std_out) - 1:
                    msg = msg + str.strip(line) + '. '
                else:
                    msg = msg + str.strip(line) + ', '
            logger.debug(str.strip(msg))
        if std_err:
            msg = ''
            for index,line in enumerate(std_err):
                if not str.strip(line):
                    continue
                if index == len(std_err) - 1:
                    msg = msg + str.strip(line) + '. ' + '***More details in %s***' % LOG
                else:
                    msg = msg + str.strip(line) + ', '
            logger.error(str.strip(msg))
            raise ExecuteException('VirtctlError', str.strip(msg))
        #         return (str.strip(std_out[0]) if std_out else '', str.strip(std_err[0]) if std_err else '')
        return
    finally:
        p.stdout.close()
        p.stderr.close()

if __name__ == '__main__':
    runCmd(cmd1)