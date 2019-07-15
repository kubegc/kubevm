'''
Copyright (2019, ) Institute of Software, Chinese Academy of Sciences

@author: wuyuewen@otcaix.iscas.ac.cn
@author: wuheng@otcaix.iscas.ac.cn
'''
    
'''
Import python libs
'''
import os, sys, subprocess

'''
Import local libs
'''
from utils import logger

libvirt_event_handler = '%s/libvirt_event_handler.py' %(os.path.dirname(os.path.realpath(__file__)))
host_cycler = '%s/host_cycler.py' %(os.path.dirname(os.path.realpath(__file__)))
os_event_handler = '%s/os_event_handler.py' %(os.path.dirname(os.path.realpath(__file__)))

'''
Run back-end command in subprocess.
'''
def runCmd(cmd):
    std_err = None
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        return str.strip(std_out[0]) if std_out else []
    finally:
        p.stdout.close()
        p.stderr.close()
 
if __name__ == '__main__':
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)
    cmd1 = 'python %s %s' %(libvirt_event_handler, sys.argv[1])
    cmd2 = 'python %s %s' %(host_cycler, sys.argv[1])
    cmd3 = 'python %s %s' %(os_event_handler, sys.argv[1])
    print(runCmd(cmd1))
    print(runCmd(cmd2))
    print(runCmd(cmd3))
