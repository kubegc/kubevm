'''
Copyright (2019, ) Institute of Software, Chinese Academy of 

@author: wuheng@otcaix.iscas.ac.cn
@author: wuyuewen@otcaix.iscas.ac.cn
'''

from kubernetes import config, client
from kubernetes.client import V1DeleteOptions
from json import loads
import sys
import os
import json
import subprocess
import ConfigParser
import traceback

from kubernetes.client.rest import ApiException

from utils.libvirt_util import vm_state, is_vm_exists, is_vm_active, get_boot_disk_path, get_xml, undefine_with_snapshot, undefine, define_xml_str
from utils.utils import addPowerStatusMessage, RotatingOperation, ExecuteException, string_switch
from utils import logger

class parser(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

cfg = "%s/default.cfg" % os.path.dirname(os.path.realpath(__file__))
config_raw = parser()
config_raw.read(cfg)

VM_PLURAL = config_raw.get('VirtualMachine', 'plural')
VMI_PLURAL = config_raw.get('VirtualMachineImage', 'plural')
VERSION = config_raw.get('VirtualMachine', 'version')
GROUP = config_raw.get('VirtualMachine', 'group')
DEFAULT_TEMPLATE_DIR = config_raw.get('DefaultTemplateDir', 'default')

LOG = '/var/log/virtctl.log'
logger = logger.set_logger(os.path.basename(__file__), LOG)


'''
A atomic operation: Convert vm to image.
'''
def convert_vm_to_image(name):
    # cmd = os.path.split(os.path.realpath(__file__))[0] +'/scripts/convert-vm-to-image.sh ' + name
    
    '''
    A list to record what we already done.
    '''
    done_operations = []
    doing = ''
    
    class step_1_dumpxml_to_path(RotatingOperation):
        
        def __init__(self, vm, tag):
            self.tag = tag
            self.vm = vm
            self.path = '%s/%s.xml' % (DEFAULT_TEMPLATE_DIR, vm)
    
        def option(self):
            vm_xml = get_xml(self.vm)
            with open(self.path, 'w') as fw:
                fw.write(vm_xml)
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                if os.path.exists(self.path):
                    os.remove(self.path)
            return 
        
    class step_2_copy_template_to_path(RotatingOperation):
        
        def __init__(self, vm, tag, file_type='qcow2', full_copy=True):
            self.tag = tag
            self.vm = vm
            self.file_type = file_type
            self.full_copy = full_copy
            self.source_path = get_boot_disk_path(vm)
            self.dest_path = '%s/%s.%s' % (DEFAULT_TEMPLATE_DIR, vm, file_type)
            self.store_source_path = '%s/%s.path' % (DEFAULT_TEMPLATE_DIR, vm)
            self.xml_path = '%s/%s.xml' % (DEFAULT_TEMPLATE_DIR, vm)
    
        def option(self):
            '''
            Copy template's boot disk to destination dir.
            '''
            if self.full_copy:
                copy_template_cmd = 'cp %s %s' % (self.source_path, self.dest_path)
            runCmd(copy_template_cmd)
            '''
            Store source path of template's boot disk to .path file.
            '''
            with open(self.store_source_path, 'w') as fw:
                fw.write(self.source_path)
            '''
            Replate template's boot disk to dest path in .xml file.
            '''
            string_switch(self.xml_path, self.source_path, self.dest_path, 'g')
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                for path in [self.dest_path, self.store_source_path]:
                    if os.path.exists(path):
                        os.remove(path)
            return 

    class step_3_undefine_vm(RotatingOperation):
        
        def __init__(self, vm, tag, force=True):
            self.tag = tag
            self.vm = vm
            self.force = force
            self.tmp_path = '/tmp/%s.xml' % (vm)
    
        def option(self):
            vm_xml = get_xml(self.vm)
            with open(self.tmp_path, 'w') as fw:
                fw.write(vm_xml)
            try:
                if self.force:
                    undefine_with_snapshot(self.vm)
                else:
                    undefine(self.vm)
            except:
                if is_vm_exists(self.vm):
                    raise Exception('VM %s undefine failed!' % self.vm)
                logger.warning('Oops! ', exc_info=1)
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                with open(self.tmp_path, 'r') as fr:
                    vm_xml = fr.read()
                define_xml_str(vm_xml)
            return 
        
    class final_step_delete_source_file(RotatingOperation):
        
        def __init__(self, vm, tag):
            self.tag = tag
            self.vm = vm
            self.source_path = get_boot_disk_path(vm)
    
        def option(self):
            '''
            Remove source path of template's boot disk
            '''
            if os.path.exists(self.source_path):
                os.remove(self.source_path)
            done_operations.append(self.tag)
            return 
    
        def rotating_option(self):
            if self.tag in done_operations:
                logger.debug('In final step, rotating noting.')
            return 

        
    jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    step1 = step_1_dumpxml_to_path(name, 'Step1: dumpxml')
    step2 = step_2_copy_template_to_path(name, 'Step2: copy template')
    step3 = step_3_undefine_vm(name, 'Step3: undefine vm')
    step_final = final_step_delete_source_file(name, 'Final step: remove source file')
    try:
        #cmd = 'bash %s/scripts/convert-vm-to-image.sh %s' %(PATH, name)
        '''
        #Preparations
        '''
        doing = 'Preparations'
        if not is_vm_exists(name):
            raise Exception('VM not exists!')
        if is_vm_active(name):
            raise Exception('Cannot covert running vm to image.')
        if not os.path.exists(DEFAULT_TEMPLATE_DIR):
            os.makedirs(DEFAULT_TEMPLATE_DIR, 0711)
        '''
        #Step 1: dump VM .xml file to template's path
        '''
        doing = step1.tag
        step1.option()
        '''
        #Step 2: copy template to template's path
        '''       
        doing = step2.tag
        step2.option()
        '''
        #Step 3: undefine vm
        '''       
        doing = step3.tag
        step3.option()
        '''
        #Step 4: synchronize information to Kubernetes
        '''   
        doing = 'Synchronize to Kubernetes'       
        jsonDict = jsonStr.copy()
        jsonDict['kind'] = 'VirtualMachineImage'
        jsonDict['metadata']['kind'] = 'VirtualMachineImage'
        del jsonDict['metadata']['resourceVersion']
        del jsonDict['spec']['lifecycle']
        try:
            client.CustomObjectsApi().create_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, body=jsonDict)
            client.CustomObjectsApi().delete_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name, body=V1DeleteOptions())
        except ApiException:
            logger.warning('Oops! ', exc_info=1)
        '''
        #Final step: delete source file
        '''       
        doing = step_final.tag
        step_final.option()
    except:
        error_reason = 'VmmError'
        error_message = '%s failed!' % doing
        logger.error(error_reason + ' ' + error_message)
        logger.error('Oops! ', exc_info=1)
        report_failure(name, jsonStr, error_reason, error_message, GROUP, VERSION, VM_PLURAL)
        step1.rotating_option()
        step2.rotating_option()
        step3.rotating_option()
        step_final.rotating_option()

'''
A atomic operation: Convert image to vm.
'''
def convert_image_to_vm(name):
    jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, name=name)
    try:
#         cmd = '/bin/bash %s/scripts/convert-image-to-vm.sh %s' %(PATH, name)
#         runCmd(cmd)
        jsonDict = jsonStr.copy()
        jsonDict['kind'] = 'VirtualMachine'
        jsonDict['metadata']['kind'] = 'VirtualMachine'
        del jsonDict['metadata']['resourceVersion']
        del jsonDict['spec']['lifecycle']
        client.CustomObjectsApi().create_namespaced_custom_object(
            group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, body=jsonDict)
        client.CustomObjectsApi().delete_namespaced_custom_object(
            group=GROUP, version=VERSION, namespace='default', plural=VMI_PLURAL, name=name, body=V1DeleteOptions())
    except ApiException:
        pass
    logger.debug('convert Image to VM successful.')

# def toImage(name):
#     jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachines', name=name)
#     jsonDict = jsonStr.copy()
#     jsonDict['kind'] = 'VirtualMachineImage'
#     jsonDict['metadata']['kind'] = 'VirtualMachineImage'
#     del jsonDict['metadata']['resourceVersion']
#     del jsonDict['spec']['lifecycle']
#     client.CustomObjectsApi().create_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachineimages', body=jsonDict)
#     client.CustomObjectsApi().delete_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachines', name=name, body=V1DeleteOptions())
#     logger.debug('convert VM to Image successful.')
#     
# def toVM(name):
#     jsonStr = client.CustomObjectsApi().get_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachineimages', name=name)
#     jsonDict = jsonStr.copy()
#     jsonDict['kind'] = 'VirtualMachine'
#     jsonDict['metadata']['kind'] = 'VirtualMachine'
#     del jsonDict['spec']['lifecycle']
#     del jsonDict['metadata']['resourceVersion']
#     client.CustomObjectsApi().create_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachines', body=jsonDict)
#     client.CustomObjectsApi().delete_namespaced_custom_object(
#         group=GROUP, version=VERSION, namespace='default', plural='virtualmachineimages', name=name, body=V1DeleteOptions())
#     logger.debug('convert Image to VM successful.')


def updateOS(name, source, target):
    jsonDict = client.CustomObjectsApi().get_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name)
    jsonString = json.dumps(jsonDict)
    if jsonString.find(source) >= 0 and os.path.exists(target):
        runCmd('cp %s %s' %(target, source))
    else:
        raise Exception('Wrong source or target.')
    jsonDict = deleteLifecycleInJson(jsonDict)
    vm_power_state = vm_state(name).get(name)
    body = addPowerStatusMessage(jsonDict, vm_power_state, 'The VM is %s' % vm_power_state)
    client.CustomObjectsApi().replace_namespaced_custom_object(
        group=GROUP, version=VERSION, namespace='default', plural=VM_PLURAL, name=name, body=body)
    
def deleteLifecycleInJson(jsondict):
    if jsondict:
        '''
        Get target VM name from Json.
        '''
        spec = jsondict['spec']
        if spec:
            lifecycle = spec.get('lifecycle')
            if lifecycle:
                del spec['lifecycle']
    return jsondict

def report_failure(name, jsondict, error_reason, error_message, group, version, plural):
    try:
        jsondict = client.CustomObjectsApi().get_namespaced_custom_object(group=group, 
                                                                          version=version, 
                                                                          namespace='default', 
                                                                          plural=plural, 
                                                                          name=name)
        jsondict = deleteLifecycleInJson(jsondict)
        body = addExceptionMessage(jsondict, error_reason, error_message)
        retv = client.CustomObjectsApi().replace_namespaced_custom_object(
            group=group, version=version, namespace='default', plural=plural, name=name, body=body)
        return retv
    except ApiException:
        logger.error('Oops! ', exc_info=1)
        
def addExceptionMessage(jsondict, reason, message):
    if jsondict:
        status = {'conditions':{'state':{'waiting':{'message':message, 'reason':reason}}}}
        spec = jsondict['spec']
        if spec:
            spec['status'] = status
    return jsondict

def main():
    help_msg = 'Usage: python %s <convert_vm_to_image|convert_image_to_vm|update-os|--help>' % sys.argv[0]
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print (help_msg)
        sys.exit(1)
    print sys.argv
    if len(sys.argv)%2 != 0:
        print ("wrong parameter number")
        sys.exit(1)
 
    params = {}
    for i in range(2, len(sys.argv) - 1):
        params[sys.argv[i]] = sys.argv[i+1]
        i = i+2
    
    if sys.argv[1] == 'convert_vm_to_image':
        convert_vm_to_image(params['--name'])
    elif sys.argv[1] == 'convert_image_to_vm':
        convert_image_to_vm(params['--name'])
    elif sys.argv[1] == 'update-os':
        updateOS(params['--domain'], params['--source'], params['--target'])
    else:
        print ('invalid argument!')
        print (help_msg)


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
        if std_out:
#             msg = ''
#             for index,line in enumerate(std_out):
#                 if not str.strip(line):
#                     continue
#                 if index == len(std_out) - 1:
#                     msg = msg + str.strip(line) + '. '
#                 else:
#                     msg = msg + str.strip(line) + ', '
#             logger.debug(str.strip(msg))
            logger.debug(std_out)
        if std_err:
#             msg = ''
#             for index, line in enumerate(std_err):
#                 if not str.strip(line):
#                     continue
#                 if index == len(std_err) - 1:
#                     msg = msg + str.strip(line) + '. ' + '***More details in %s***' % LOG
#                 else:
#                     msg = msg + str.strip(line) + ', '
#             logger.error(msg)
#             raise ExecuteException('VirtctlError', str.strip(msg))
            raise ExecuteException('VmmError', std_err)
#         return (str.strip(std_out[0]) if std_out else '', str.strip(std_err[0]) if std_err else '')
        return
    finally:
        p.stdout.close()
        p.stderr.close()


# def run(cmd):
#     try:
#         result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
#         logger.debug(result)
#         print result
#     except Exception:
#         traceback.format_exc()
#         print(sys.exc_info())
#         raise ExecuteException('vmmError', sys.exc_info()[1])


if __name__ == '__main__':
    config.load_kube_config(config_file="/root/.kube/config")
    main()
    pass
