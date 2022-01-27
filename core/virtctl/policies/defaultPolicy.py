# -*- coding: utf-8 -*-
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

    @author: wuyuewen@otcaix.iscas.ac.cn
    @author: wuheng@otcaix.iscas.ac.cn
    
    @since:  2019/09/28  

'''

import os
import time

from utils import constants
from utils import logger
from utils.misc import runCmdWithResult
from utils.exception import BadRequest, Forbidden, NotFound, InternalServerError

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
    if cmd:
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
    for i in range(1,60):
        try:
            logger.debug("Executing command %s, a %d try." % (cmd, i))
            return runCmdWithResult(cmd)
        except Exception as e:
            if cmd.find('virsh start') != -1 and i == 59:
                raise BadRequest(repr(e))
            elif cmd.find('virsh start') == -1 and i ==3:
                raise BadRequest(repr(e))
            elif cmd.find('virt-install') != -1:
                if e.message and e.message.find('already in use') != -1:
                    logger.warning('***VM has already existed and can no longer be created.')
                    return
                elif i ==3:
                    raise BadRequest(repr(e))
                else:
                    time.sleep(3)
                    continue
            elif cmd.find('kubeovn-adm unbind-swport') != -1:
                if e.message and e.message.find('already in use') != -1:
                    logger.warning('***Switch port already deleted.')
                    return
                elif i ==3:
                    raise BadRequest(repr(e))
                else:
                    time.sleep(3)
                    continue
            else:
#             if i < 4:
                if cmd.find('virsh start') != -1 and e \
                and e.message.find('Domain is already active') != -1:
                    return
                time.sleep(3)
#             else:
#                 time.sleep(i)
                continue

if __name__ == '__main__':
    print()
