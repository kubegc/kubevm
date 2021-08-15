'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''

from utils import runCmd

def get_block_dev_json(block):
    cmd = '/usr/bin/qucli %s' % block
    return runCmd(cmd)

def is_block_dev_exists(block):
    cmd = 'lvdisplay %s' % block
    return runCmd(cmd)