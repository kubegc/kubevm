'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn

https://pypi.org/project/json2xml/
https://github.com/kubernetes/kubernetes/issues/51046
'''

from utils import runCmd

def get_block_dev_json(block):
    cmd = '/usr/bin/qucli %s' % block
    return runCmd(cmd)

def is_block_dev_exists(block):
    cmd = 'lvdisplay %s' % block
    return runCmd(cmd)