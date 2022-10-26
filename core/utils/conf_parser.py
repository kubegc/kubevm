#coding=UTF-8
'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences

    @author: wuyuewen@otcaix.iscas.ac.cn
    @author: wuheng@otcaix.iscas.ac.cn
    
    @since:  2019/09/29

'''
import os
import re

try:
    from utils import constants
except:
    import constants

# 匹配、解析constant中命令
class UserDefinedParser:
    '''功能类：配置文件解析器'''
    
    def __init__(self):  
        '''读取指定目录下的配置文件.
        
        指定文件访问顺序 KUBEVMM_CONFIG_FILE_PATH, KUBEVMM_CONFIG_FILE_IN_DOCKER_PATH
        
        '''
        self.cfg = constants.KUBEVMM_CONFIG_FILE_PATH
        if not os.path.exists(self.cfg):
            self.cfg = constants.KUBEVMM_CONFIG_FILE_IN_DOCKER_PATH
        
    def get_all_support_cmds(self):
        ''' 获取所有支持的CMDs
        Returns:
            list: 所有支持的命令
        '''
        cmds = []
        for k in constants.__dict__.keys():
            # 以cmd结尾的是命令 如CREATE_VM_CMD
            if k.endswith('CMD'):
                cmd_key = k.replace('_CMD','').replace('_', '').lower()
                cmds.append(cmd_key)
        return cmds
    
    def getCmds(self, the_cmd_key):
        ''' 获取命令的配置项
        Returns:
            string: '策略,关键字,执行命令,查询命令'
        '''
        retv = ''
        the_cmd_key = the_cmd_key.lower()
        for k,v in constants.__dict__.items():
            if k.endswith('CMD'):
                cmd_key = k.replace('_CMD','').replace('_', '').lower()
                # 遍历constant中的cmd，和传入的the_cmd_key匹配
                if cmd_key == the_cmd_key:
                    v_parser = ['' if i.strip() in ['none', 'None', 'null'] else i.strip() for i in v.split(',')]
                    for i, v_val in enumerate(v_parser):
                        if i == len(v_parser) - 1:
                            retv = retv + v_val
                        else:
                            retv = retv + v_val + ','
        return retv
    
if __name__ == '__main__':
    import pprint
    p = UserDefinedParser()
    pprint.pprint(p.getCmds('deleteVM'))