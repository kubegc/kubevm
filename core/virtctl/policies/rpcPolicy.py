# -*- coding: utf-8 -*-
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

    @author: wuyuewen@otcaix.iscas.ac.cn
    @author: wuheng@otcaix.iscas.ac.cn
    
    @since:  2019/09/28  

'''

import os

from utils import constants
from utils import logger
from utils.cmdrpc import rpcCallWithResult

logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTCTL_LOG)

def toPrepareCmd(cmd, paramJson):
    '''将json转换为prepare cmd
    '''
    return _toCmd(cmd, paramJson)

def toInvokeCmd(cmd, paramJson):
    '''将json转换为invoke cmd
    '''
    return _toCmd(cmd, paramJson)

def toQueryCmd(cmd, paramJson):
    '''将json转换为query cmd
    '''
    return _toCmd(cmd, paramJson)

def _toCmd(cmd, paramJson):
    for key in paramJson:
        value = str(paramJson[key])
        if value == "False":
            continue
        elif value == "True":
            cmd = cmd + " --" + key.replace("_", "-")
        else:
            cmd = cmd + " --" + key.replace("_", "-") + " " + value
    return cmd

def runCmd(cmd):
    return rpcCallWithResult(cmd)

if __name__ == '__main__':
    print()
