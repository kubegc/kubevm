# -*- coding: utf-8 -*-
'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

    @author: wuyuewen@otcaix.iscas.ac.cn
    @author: liuhe18@otcaix.iscas.ac.cn
    @author: wuheng@otcaix.iscas.ac.cn
    
    @since:  2019/09/29

'''

import os
import sys
sys.path.append("..")
from importlib import import_module

from utils import constants
from utils import logger
from utils.exception import BadRequest


logger = logger.set_logger(os.path.basename(__file__), constants.KUBEVMM_VIRTCTL_LOG)

class Executor():
    '''执行器，通过subprocess运行命令
    '''
    
    def __init__(self, policy, prepare_cmd, invoke_cmd, query_cmd):
        self.policy = policy
        self.prepare_cmd = prepare_cmd
        self.invoke_cmd = invoke_cmd
        self.query_cmd = query_cmd
    
    def execute(self):
        '''执行invoke和query命令，如果没有query命令，则返回invoke命令的结果
        Returns:
            (str, obj): (code, data)
        '''
        code, data = 1, ''
        try:
            policyObj = import_module('policies.%sPolicy' % (self.policy))
        except ImportError:
            logger.error("Unsupported policy %sPolicy." % (self.policy), exc_info=1) 
            raise BadRequest("Unsupported policy %sPolicy." % self.policy)
        for cmd in [self.prepare_cmd, self.invoke_cmd, self.query_cmd]:
            if cmd:
                code, data = policyObj.runCmd(cmd)
            else:
                continue
        return code, data
    
