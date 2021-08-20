'''
Run back-end command in subprocess.
'''
import atexit
import fcntl
import hashlib
import operator
import os
import re
import random
import signal
import socket
import string
import subprocess
import sys
import time
import traceback
import uuid
from functools import wraps
from json import loads, dumps, load, dump
from sys import exit
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import grpc
import xmltodict
import yaml
from kubernetes import client
from kubernetes.client.rest import ApiException

from .k8s import K8sHelper, addPowerStatusMessage, updateJsonRemoveLifecycle, get_hostname_in_lower_case, get_node_name, \
    replaceData
from .arraylist import vmArray
from .ftp import FtpHelper

try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET

import cmdcall_pb2
import cmdcall_pb2_grpc
from . import logger
from .exception import ExecuteException
from netutils import get_docker0_IP

DEFARULT_MOUNT_DIR = '/var/lib/libvirt/cstor'

LOG = '/var/log/kubesds3.log'

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '19999'


def runCmdWithResult(cmd):
    if not cmd:
        return
    logger.debug(cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for index, line in enumerate(std_out):
                line = line.decode("utf-8")
                if not str.strip(line):
                    continue
                msg = msg + str.strip(line)
            msg = str.strip(msg)
            logger.debug(msg)
            try:
                result = loads(msg)
                if isinstance(result, dict) and 'result' in list(result.keys()):
                    if result['result']['code'] != 0:
                        if std_err:
                            error_msg = ''
                            for index, line in enumerate(std_err):
                                line = line.decode("utf-8")
                                if not str.strip(line):
                                    continue
                                error_msg = error_msg + str.strip(line)
                            error_msg = str.strip(error_msg).replace('"', "'")
                            result['result']['msg'] = '%s. error output: %s' % (
                                result['result']['msg'], error_msg)
                return result
            except Exception:
                logger.debug(cmd)
                logger.debug(traceback.format_exc())
                error_msg = ''
                for index, line in enumerate(std_err):
                    line = line.decode("utf-8")
                    if not str.strip(line):
                        continue
                    error_msg = error_msg + str.strip(line)
                error_msg = str.strip(error_msg)
                raise ExecuteException('RunCmdError',
                                       'can not parse output to json----%s. %s' % (msg, error_msg))
        if std_err:
            msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                msg = msg + line + ', '
            logger.debug(cmd)
            logger.debug(msg)
            logger.debug(traceback.format_exc())
            if msg.strip() != '':
                raise ExecuteException('RunCmdError', msg)
    finally:
        p.stdout.close()
        p.stderr.close()


def remoteRunCmdWithResult(ip, cmd):
    if not cmd:
        return
    logger.debug(cmd)

    cmd = 'ssh root@%s "%s"' % (ip, cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for index, line in enumerate(std_out):
                line = line.decode("utf-8")
                if not str.strip(line):
                    continue
                msg = msg + str.strip(line)
            msg = str.strip(msg)
            logger.debug(msg)
            try:
                result = loads(msg)
                if isinstance(result, dict) and 'result' in list(result.keys()):
                    if result['result']['code'] != 0:
                        if std_err:
                            error_msg = ''
                            for index, line in enumerate(std_err):
                                line = line.decode("utf-8")
                                if not str.strip(line):
                                    continue
                                error_msg = error_msg + str.strip(line)
                            error_msg = str.strip(error_msg).replace('"', "'")
                            result['result']['msg'] = '%s. error output: %s' % (
                                result['result']['msg'], error_msg)
                return result
            except Exception:
                logger.debug(cmd)
                logger.debug(traceback.format_exc())
                error_msg = ''
                for index, line in enumerate(std_err):
                    line = line.decode("utf-8")
                    if not str.strip(line):
                        continue
                    error_msg = error_msg + str.strip(line)
                error_msg = str.strip(error_msg)
                raise ExecuteException('RunCmdError',
                                       'can not parse output to json----%s. %s' % (msg, error_msg))
        if std_err:
            msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                msg = msg + line + ', '
            logger.debug(cmd)
            logger.debug(msg)
            logger.debug(traceback.format_exc())
            if msg.strip() != '':
                raise ExecuteException('RunCmdError', msg)
    finally:
        p.stdout.close()
        p.stderr.close()


def remoteRunCmdWithOutput(ip, cmd):
    if not cmd:
        return
    logger.debug(cmd)

    cmd = 'ssh root@%s "%s"' % (ip, cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for line in std_out:
                line = line.decode("utf-8")
                msg = msg + line
            return msg
        if std_err:
            msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                if not str.strip(line):
                    continue
                if index == len(std_err) - 1:
                    msg = msg + str.strip(line) + '. ' + '***More details in %s***' % LOG
                else:
                    msg = msg + str.strip(line) + ', '
            logger.debug(cmd)
            logger.debug(msg)
            logger.debug(traceback.format_exc())
            if msg.strip() != '':
                raise ExecuteException('RunCmdError', msg)
    finally:
        p.stdout.close()
        p.stderr.close()


def runCmdAndTransferXmlToJson(cmd):
    xml_str = runCmdAndGetOutput(cmd)
    dic = xmltodict.parse(xml_str, encoding='utf-8')
    dic = dumps(dic)
    dic = dic.replace('@', '').replace('#', '')
    return loads(dic)


def runCmdAndSplitKvToJson(cmd):
    logger.debug(cmd)
    if not cmd:
        #         logger.debug('No CMD to execute.')
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            result = {}
            for index, line in enumerate(std_out):
                line = line.decode("utf-8")
                if not str.strip(line):
                    continue
                line = str.strip(line)
                kv = line.replace(':', '').split()
                if len(kv) == 2:
                    result[kv[0].lower()] = kv[1]
            return result
        if std_err:
            error_msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                if not str.strip(line):
                    continue
                else:
                    error_msg = error_msg + str.strip(line)
            error_msg = str.strip(error_msg)
            logger.debug(error_msg)
            if error_msg.strip() != '':
                raise ExecuteException('RunCmdError', error_msg)
    finally:
        p.stdout.close()
        p.stderr.close()


def runCmdAndGetOutput(cmd):
    if not cmd:
        return
    logger.debug(cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for line in std_out:
                line = line.decode("utf-8")
                msg = msg + line
            return msg
        if std_err:
            msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                if not str.strip(line):
                    continue
                if index == len(std_err) - 1:
                    msg = msg + str.strip(line) + '. ' + '***More details in %s***' % LOG
                else:
                    msg = msg + str.strip(line) + ', '
            logger.debug(cmd)
            logger.debug(msg)
            logger.debug(traceback.format_exc())
            if msg.strip() != '':
                raise ExecuteException('RunCmdError', msg)
    except Exception:
        logger.debug(traceback.format_exc())
    finally:
        p.stdout.close()
        p.stderr.close()


def remoteRunCmd(ip, cmd):
    logger.debug(cmd)
    if not cmd:
        logger.debug('No CMD to execute.')
        return
    cmd = 'ssh root@%s "%s"' % (ip, cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            logger.debug(std_out)
        if std_err:
            msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                msg = msg + line
            if msg.strip() != '':
                raise ExecuteException('RunCmdError', msg)
        return
    finally:
        p.stdout.close()
        p.stderr.close()


'''
Run back-end command in subprocess.
'''


def runCmd(cmd):
    logger.debug(cmd)
    if not cmd:
        #         logger.debug('No CMD to execute.')
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
        p.wait()
        logger.debug('p.returncode: %d' % p.returncode)
        if std_err:
            msg = ''
            for index, line in enumerate(std_err):
                line = line.decode("utf-8")
                msg = msg + line
            logger.debug(msg)
            if msg.strip() != '' and p.returncode != 0:
                raise ExecuteException('RunCmdError', msg)
        return
    finally:
        p.stdout.close()
        p.stderr.close()


def runCmdRaiseException(cmd, head='VirtctlError', use_read=False):
    logger.debug(cmd)
    std_err = None
    if not cmd:
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        if use_read:
            std_out = p.stdout.read()
            std_err = p.stderr.read()
        else:
            std_out = p.stdout.readlines()
            std_err = p.stderr.readlines()
        if std_err:
            logger.debug(std_err)
            raise ExecuteException(head, std_err)
        return std_out
    finally:
        p.stdout.close()
        p.stderr.close()


def rpcCall(cmd):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        response = client.Call(cmdcall_pb2.CallRequest(cmd=cmd))
        logger.debug(response.json)
        jsondict = loads(str(response.json))
    except grpc.RpcError as e:
        logger.debug(traceback.format_exc())
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        logger.debug(e.details())
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        logger.debug(status_code.name)
        # should print `(3, 'invalid argument')`
        logger.debug(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
        raise ExecuteException('RunCmdError', "Cmd: %s failed!" % cmd)
    except Exception:
        logger.debug(traceback.format_exc())
        raise ExecuteException('RunCmdError', "Cmd: %s failed!" % cmd)

    if jsondict['result']['code'] != 0:
        raise ExecuteException('RunCmdError', jsondict['result']['msg'])
    return jsondict


def rpcCallWithResult(cmd):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        # ideally, you should have try catch block here too
        response = client.CallWithResult(cmdcall_pb2.CallRequest(cmd=cmd))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        result = loads(str(response.json))
        return result
    except grpc.RpcError as e:
        logger.debug(traceback.format_exc())
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        logger.debug(e.details())
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        logger.debug(status_code.name)
        # should print `(3, 'invalid argument')`
        logger.debug(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
        raise ExecuteException('RunCmdError', "Cmd: %s failed!" % cmd)
    except Exception:
        logger.debug(traceback.format_exc())
        raise ExecuteException('RunCmdError', 'can not parse rpc response to json.')


def rpcCallAndTransferXmlToJson(cmd):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        # ideally, you should have try catch block here too
        response = client.CallAndTransferXmlToJson(cmdcall_pb2.CallRequest(cmd=cmd))
        result = loads(str(response.json))
        return result
    except grpc.RpcError as e:
        logger.debug(traceback.format_exc())
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        logger.debug(e.details())
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        logger.debug(status_code.name)
        # should print `(3, 'invalid argument')`
        logger.debug(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
        raise ExecuteException('RunCmdError', "Cmd: %s failed!" % cmd)
    except Exception:
        logger.debug(traceback.format_exc())
        raise ExecuteException('RunCmdError', 'can not parse rpc response to json.')


def rpcCallAndTransferKvToJson(cmd):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        # ideally, you should have try catch block here too
        response = client.CallAndSplitKVToJson(cmdcall_pb2.CallRequest(cmd=cmd))
        result = loads(str(response.json))
        return result
    except grpc.RpcError as e:
        logger.debug(traceback.format_exc())
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        logger.debug(e.details())
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        logger.debug(status_code.name)
        # should print `(3, 'invalid argument')`
        logger.debug(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
        raise ExecuteException('RunCmdError', "Cmd: %s failed!" % cmd)
    except Exception:
        logger.debug(traceback.format_exc())
        raise ExecuteException('RunCmdError', 'can not parse rpc response to json.')


def rpcCallAndGetOutput(cmd):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        # ideally, you should have try catch block here too
        response = client.CallAndGetOutput(cmdcall_pb2.CallRequest(cmd=cmd))
        result = loads(str(response.json))
        if result['result']['code'] != 0:
            raise ExecuteException('rpc call %s error' % cmd, result['result']['msg'])
        return result['result']['msg']
    except grpc.RpcError as e:
        logger.debug(traceback.format_exc())
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        logger.debug(e.details())
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        logger.debug(status_code.name)
        # should print `(3, 'invalid argument')`
        logger.debug(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
        raise ExecuteException('RunCmdError', "Cmd: %s failed!" % cmd)
    except Exception:
        logger.debug(traceback.format_exc())
        raise ExecuteException('RunCmdError', 'can not parse rpc response to json.')


def randomUUID():
    u = [random.randint(0, 255) for ignore in range(0, 16)]
    u[6] = (u[6] & 0x0F) | (4 << 4)
    u[8] = (u[8] & 0x3F) | (2 << 6)
    return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2,
                     "%02x" * 6]) % tuple(u)


def randomUUIDFromName(name):
    name = str(name)
    namespace = uuid.NAMESPACE_URL

    return str(uuid.uuid5(namespace, name))


def is_pool_started(pool):
    poolInfo = runCmdAndSplitKvToJson('virsh pool-info %s' % pool)
    if poolInfo['state'] == 'running':
        return True
    return False


def is_pool_exists(pool):
    poolInfo = runCmdAndSplitKvToJson('virsh pool-info %s' % pool)
    if poolInfo and pool == poolInfo['name']:
        return True
    return False


def is_pool_defined(pool):
    poolInfo = runCmdAndSplitKvToJson('virsh pool-info %s' % pool)
    if poolInfo['persistent'] == 'yes':
        return True
    return False


def is_vm_active(domain):
    output = runCmdAndGetOutput('virsh list')
    lines = output.splitlines()
    for line in lines:
        if domain in line.split():
            return True
    return False


def is_vm_exist(domain):
    output = runCmdAndGetOutput('virsh list --all')
    lines = output.splitlines()
    for line in lines:
        if domain in line.split():
            return True
    return False


def get_all_domain():
    output = runCmdAndGetOutput('virsh list --all')
    lines = output.splitlines()
    domains = []
    if len(lines) <= 2:
        return domains
    for i in range(2, len(lines)):
        if len(lines[i].split()) < 3:
            continue
        domains.append(lines[i].split()[1])
    return domains


def get_volume_size(pool, vol):
    disk_config = get_disk_config(pool, vol)
    disk_info = get_disk_info(disk_config['current'])
    return int(disk_info['virtual_size'])


# def get_disks_spec(domain):
#     if domain is None:
#         raise ExecuteException('RunCmdError', 'domin is not set. Can not get domain disk spec.')
#     output = runCmdAndGetOutput('virsh domblklist %s' % domain)
#     lines = output.splitlines()
#     spec = {}
#     for i in range(2, len(lines)):
#         kv = lines[i].split()
#         if len(kv) == 2:
#             spec[kv[1]] = kv[0]
#     return spec


def get_disks_spec(domain):
    if not domain:
        raise ExecuteException('', 'missing parameter: no vm name(%s).' % domain)
    runCmd('virsh dumpxml %s > /tmp/%s.xml' % (domain, domain))
    xmlfile = '/tmp/%s.xml' % domain
    if xmlfile is None:
        raise ExecuteException('RunCmdError', 'domin xml file is not set. Can not get domain disk spec.')

    tree = ET.parse(xmlfile)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    spec = {}
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element is not None:
                    target_element = disk.find("target")
                    spec[source_element.get("file")] = target_element.get('dev')
    runCmd('rm -f %s' % xmlfile)
    return spec


def get_disks_spec_by_xml(xmlfile):
    if xmlfile is None:
        raise ExecuteException('RunCmdError', 'domin xml file is not set. Can not get domain disk spec.')

    tree = ET.parse(xmlfile)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    spec = {}
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element is not None:
                    target_element = disk.find("target")
                    spec[source_element.get("file")] = target_element.get('dev')
    return spec


def get_os_disk(domain):
    if not domain:
        raise ExecuteException('', 'missing parameter: no vm name(%s).' % domain)
    uuid = randomUUID()
    runCmd('virsh dumpxml %s > /tmp/%s.xml' % (domain, uuid))
    xmlfile = '/tmp/%s.xml' % uuid
    if xmlfile is None:
        raise ExecuteException('RunCmdError', 'domin xml file is not set. Can not get domain disk spec.')

    tree = ET.parse(xmlfile)
    os_disk = {}
    root = tree.getroot()
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element is not None:
                    target_element = disk.find("target")
                    runCmd('rm -f %s' % xmlfile)
                    return target_element.get('dev'), source_element.get("file")
    raise ExecuteException('RunCmdError', 'cannot indify vm os disk.')


def get_os_disk_by_xml(xmlfile):
    if xmlfile is None:
        raise ExecuteException('RunCmdError', 'domin xml file is not set. Can not get domain disk spec.')

    tree = ET.parse(xmlfile)
    os_disk = {}
    root = tree.getroot()
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element is not None:
                    target_element = disk.find("target")
                    return target_element.get('dev'), source_element.get("file")
    raise ExecuteException('RunCmdError', 'cannot indify vm os disk.')


class CDaemon:
    '''
    a generic daemon class.
    usage: subclass the CDaemon class and override the run() method
    stderr:
    verbose:
    save_path:
    '''

    def __init__(self, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0o22,
                 verbose=1):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = save_path
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        if self.stderr:
            se = open(self.stderr, 'a+', 0)
        else:
            se = so

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        def sig_handler(signum, frame):
            self.daemon_alive = False

        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)

        if self.verbose >= 1:
            print('daemon process started ...')

        atexit.register(self.del_pid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write('%s\n' % pid)

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def del_pid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self, *args, **kwargs):
        if self.verbose >= 1:
            print('ready to starting ......')
        # check for a pid file to see if the daemon already runs
        pid = self.get_pid()
        if pid:
            msg = 'pid file %s already exists, is it already running?\n'
            sys.stderr.write(msg % self.pidfile)
            sys.exit(1)
        # start the daemon
        self.daemonize()
        self.run(*args, **kwargs)

    def stop(self):
        if self.verbose >= 1:
            print('stopping ...')
        pid = self.get_pid()
        if not pid:
            msg = 'pid file [%s] does not exist. Not running?\n' % self.pidfile
            sys.stderr.write(msg)
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            return
        # try to kill the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)
            if self.verbose >= 1:
                print('Stopped!')

    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)

    def is_running(self):
        pid = self.get_pid()
        # print(pid)
        return pid and os.path.exists('/proc/%d' % pid)

    def run(self, *args, **kwargs):
        'NOTE: override the method in subclass'
        print('base class run()')


def singleton(pid_filename):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            pid = str(os.getpid())
            pidfile = open(pid_filename, 'a+')
            try:
                fcntl.flock(pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                return
            pidfile.seek(0)
            pidfile.truncate()
            pidfile.write(pid)
            pidfile.flush()
            pidfile.seek(0)

            ret = f(*args, **kwargs)

            try:
                pidfile.close()
            except IOError as err:
                if err.errno != 9:
                    return
            os.remove(pid_filename)
            return ret

        return decorated

    return decorator


def get_IP():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def get_pool_info(pool_):
    if not pool_:
        raise ExecuteException('', 'missing parameter: no pool name.')
    result = runCmdAndSplitKvToJson('virsh pool-info %s' % pool_)
    # result['allocation'] = int(1024*1024*1024*float(result['allocation']))
    # result['available'] = int(1024 * 1024 * 1024 * float(result['available']))
    # result['code'] = 0
    # result['capacity'] = int(1024 * 1024 * 1024 * float(result['capacity']))
    if 'allocation' in result.keys():
        del result['allocation']
    if 'available' in result.keys():
        del result['available']

    xml_dict = runCmdAndTransferXmlToJson('virsh pool-dumpxml %s' % pool_)
    result['capacity'] = int(xml_dict['pool']['capacity']['text'])
    result['available'] = int(xml_dict['pool']['capacity']['text'])
    result['path'] = xml_dict['pool']['target']['path']
    return result


def modify_disk_info_in_k8s(poolname, vol):
    helper = K8sHelper("VirtualMachineDisk")
    helper.update(vol, "volume", get_disk_info_to_k8s(poolname, vol))


def modify_snapshot_info_in_k8s(poolname, vol, name):
    helper = K8sHelper("VirtualMachineDiskSnapshot")
    helper.update(name, "volume", get_snapshot_info_to_k8s(poolname, vol, name))


def get_pool_info_from_k8s(pool):
    if not pool:
        raise ExecuteException('', 'missing parameter: no pool name.')
    poolHelper = K8sHelper('VirtualMachinePool')
    pool_info = poolHelper.get_data(pool, 'pool')
    if pool_info == None:
        raise ExecuteException('', 'can not get pool info %s from k8s' % pool)
    return pool_info


def get_image_info_from_k8s(image):
    if not image:
        raise ExecuteException('', 'missing parameter: no image name.')
    image_helper = K8sHelper('VirtualMachineDiskImage')
    return image_helper.get_data(image, 'volume')


def get_vol_info_from_k8s(vol):
    if not vol:
        raise ExecuteException('', 'missing parameter: no disk name.')
    helper = K8sHelper('VirtualMachineDisk')
    vol_info = helper.get_data(vol, 'volume')
    if vol_info == None:
        raise ExecuteException('', 'can not get disk info %s from k8s' % vol)
    return vol_info


def try_get_diskmn_by_path(disk_path):
    if disk_path.find('snapshots') >= 0:
        disk_mn = os.path.basename(os.path.dirname(os.path.dirname(disk_path)))
    else:
        try:
            vol_info = get_vol_info_from_k8s(os.path.basename(disk_path))
            disk_mn = os.path.basename(disk_path)
        except:
            disk_mn = os.path.basename(os.path.dirname(disk_path))
    vol_info = get_vol_info_from_k8s(disk_mn)
    return disk_mn


def get_snapshot_info_from_k8s(snapshot):
    if not snapshot:
        raise ExecuteException('', 'missing parameter: no disk name.')
    helper = K8sHelper('VirtualMachineDiskSnapshot')
    ss_info = helper.get_data(snapshot, 'volume')
    if ss_info == None:
        raise ExecuteException('', 'can not get snapshot info %s from k8s' % snapshot)
    return ss_info


def get_disk_config(pool, vol):
    if not pool or not vol:
        raise ExecuteException('', 'missing parameter: no pool or disk name.')
    poolInfo = get_pool_info(pool)
    pool_path = poolInfo['path']
    if not os.path.isdir(pool_path):
        raise ExecuteException('', "can not get pool %s path." % pool)
    config_path = '%s/%s/config.json' % (pool_path, vol)
    with open(config_path, "r") as f:
        config = load(f)
        return config


def get_disk_config_by_path(config_path):
    if not config_path:
        raise ExecuteException('', 'cannot find "config.json" in disk dir.')
    with open(config_path, "r") as f:
        config = load(f)
        return config


def get_disk_snapshots(ss_path):
    ss_chain = get_sn_chain(ss_path)
    snapshots = []
    for disk_info in ss_chain:
        if disk_info['filename'] != ss_path:
            snapshots.append(disk_info['filename'])
    return snapshots


def get_disk_info(ss_path):
    try:
        result = runCmdWithResult('qemu-img info -U --output json %s' % ss_path)
    except:
        try:
            result = runCmdWithResult('qemu-img info --output json %s' % ss_path)
        except:
            logger.debug(traceback.format_exc())
            error_print(400, "can't get snapshot info in qemu-img.")
            exit(1)
    json_str = dumps(result)
    return loads(json_str.replace('-', '_'))


def change_vol_current(vol, current):
    vol_info = get_vol_info_from_k8s(vol)
    pool_info = get_pool_info_from_k8s(vol_info['pool'])
    check_pool_active(pool_info)

    config_path = '%s/%s/config.json' % (pool_info['path'], vol)
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = load(f)
        config['current'] = current
    else:
        config['name'] = vol
        config['pool'] = vol_info['pool']
        config['poolname'] = vol_info['poolname']
        config['dir'] = '%s/%s' % (pool_info['path'], vol)
        config['current'] = current
    with open(config_path, 'w') as f:
        dump(config, f)
    helper = K8sHelper("VirtualMachineDisk")
    helper.update(vol, 'volume', get_disk_info_to_k8s(pool_info['poolname'], vol))


def get_pool_info_to_k8s(type, pool, url, poolname, content):
    result = get_pool_info(poolname)
    result['content'] = content
    result["pooltype"] = type
    result["pool"] = pool
    result["free"] = result['available']
    result["poolname"] = poolname
    result["uuid"] = poolname
    result["url"] = url
    if is_pool_started(poolname):
        result["state"] = "active"
    else:
        result["state"] = "inactive"
    return result


def write_config(vol, dir, current, pool, poolname):
    config = {}
    config['name'] = vol
    config['dir'] = dir
    config['current'] = current
    config['pool'] = pool
    config['poolname'] = poolname

    with open('%s/config.json' % dir, "w") as f:
        logger.debug(config)
        dump(config, f)


def get_disk_info_to_k8s(poolname, vol):
    config_path = '%s/%s/config.json' % (get_pool_info(poolname)['path'], vol)
    if not os.path.exists(config_path):
        return get_vol_info_from_k8s(vol)
    with open(config_path, "r") as f:
        config = load(f)
    result = get_disk_info(config['current'])
    result['disk'] = vol
    result["pool"] = config['pool']
    result["poolname"] = poolname
    result["uni"] = config['current']
    result["current"] = config['current']
    return result


def get_remote_node_all_nic_ip(remote):
    ips = []
    try:
        output = remoteRunCmdWithOutput(remote, 'ip address | grep inet')
        for line in output.splitlines():
            if len(line.split()) > 1:
                ip = line.split()[1].split('/')[0]
                ips.append(ip)
    except:
        logger.debug(traceback.format_exc())
    return ips


def get_snapshot_info_to_k8s(poolname, vol, name):
    config_path = '%s/%s/config.json' % (get_pool_info(poolname)['path'], vol)
    if not os.path.exists(config_path):
        return get_snapshot_info_from_k8s(name)
    with open(config_path, "r") as f:
        config = load(f)
    ss_path = '%s/snapshots/%s' % (config['dir'], name)
    result = get_disk_info(ss_path)
    result['disk'] = vol
    result["pool"] = config['pool']
    result["poolname"] = poolname
    result["uni"] = config['current']
    result['snapshot'] = name
    return result


def get_sn_chain(ss_path):
    try:
        result = runCmdWithResult('qemu-img info -U --backing-chain --output json %s' % ss_path)
    except:
        try:
            result = runCmdWithResult('qemu-img info --backing-chain --output json %s' % ss_path)
        except:
            logger.debug(traceback.format_exc())
            error_print(400, "can't get snapshot info in qemu-img.")
            exit(1)
    return result


def get_sn_chain_path(ss_path):
    paths = set()
    chain = get_sn_chain(ss_path)
    for info in chain:
        if 'backing-filename' in list(info.keys()):
            paths.add(info['backing-filename'])
    return list(paths)


def get_all_snapshot_to_delete(ss_path, current):
    delete_sn = []
    chain = get_sn_chain(current)
    for info in chain:
        if 'backing-filename' in list(info.keys()) and info['backing-filename'] == ss_path:
            delete_sn.append(info['filename'])
            delete_sn.extend(get_all_snapshot_to_delete(info['filename'], current))
            break
    return delete_sn


class DiskImageHelper(object):
    @staticmethod
    def get_backing_file(file, raise_it=False):
        """ Gets backing file for disk image """
        get_backing_file_cmd = "qemu-img info %s" % file
        try:
            out = runCmdRaiseException(get_backing_file_cmd, use_read=True)
        except Exception as e:
            if raise_it:
                raise e
            get_backing_file_cmd = "qemu-img info -U %s" % file
            out = runCmdRaiseException(get_backing_file_cmd, use_read=True)
        lines = out.decode('utf-8').split('\n')
        for line in lines:
            if re.search("backing file:", line):
                return str(line.strip().split()[2])
        return None

    @staticmethod
    def get_backing_files_tree(file):
        """ Gets all backing files (snapshot tree) for disk image """
        backing_files = []
        backing_file = DiskImageHelper.get_backing_file(file)
        while backing_file is not None:
            backing_files.append(backing_file)
            backing_file = DiskImageHelper.get_backing_file(backing_file)
        return backing_files

    @staticmethod
    def set_backing_file(backing_file, file):
        """ Sets backing file for disk image """
        set_backing_file_cmd = "qemu-img rebase -u -b %s %s" % (backing_file, file)
        runCmdRaiseException(set_backing_file_cmd)


def check_disk_in_use(disk_path):
    try:
        result = runCmdWithResult('qemu-img info --output json %s' % disk_path)
    except:
        return True
    return False


def delete_vm_disk_in_xml(xmlfile, disk_file):
    tree = ET.parse(xmlfile)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element.get("file") == disk_file:
                    caption.remove(disk)
                    tree.write(xmlfile)
                    return True
    return False


def delete_vm_cdrom_file_in_xml(xmlfile):
    tree = ET.parse(xmlfile)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'cdrom' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element is not None:
                    disk.remove(source_element)
                    tree.write(xmlfile)
                    return True
    return False


def modofy_vm_disk_file(xmlfile, source, target):
    tree = ET.parse(xmlfile)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element.get("file") == source:
                    source_element.set("file", target)
                    tree.write(xmlfile)
                    return True
    return False


def attach_vm_disk(vm, disk):
    time = 4
    for t in range(time):
        try:
            disk_specs = get_disks_spec(vm)
            if not os.path.exists(disk):
                raise ExecuteException('', 'disk file %s not exist.' % disk)
            if disk in list(disk_specs.keys()):
                raise ExecuteException('', 'disk file %s has attached in vm %s.' % (disk, vm))
            tag = None
            letter_list = list(string.ascii_lowercase)
            for i in letter_list:
                if ('vd' + i) not in list(disk_specs.values()):
                    tag = 'vd' + i
                    break
            disk_info = get_disk_info(disk)
            if is_vm_active(vm):
                runCmd('virsh attach-disk --domain %s --cache none --live --config %s --target %s --subdriver %s' % (
                    vm, disk, tag, disk_info['format']))
            else:
                runCmd('virsh attach-disk --domain %s --cache none --config %s --target %s --subdriver %s' % (
                    vm, disk, tag, disk_info['format']))
            return
        except Exception:
            logger.debug(traceback.format_exc())
            pass
    raise ExecuteException('RunCmdError', 'can not attach disk %s to vm %s' % (disk, vm))


def modofy_vm_disks(vm, source_to_target):
    if not vm or not source_to_target:
        raise ExecuteException('', 'missing parameter: no vm name(%s) or source_to_target.' % vm)
    runCmd('virsh dumpxml %s > /tmp/%s.xml' % (vm, vm))
    tree = ET.parse('/tmp/%s.xml' % vm)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element.get("file") in list(source_to_target.keys()):
                    source_element.set("file", source_to_target[source_element.get("file")])
        tree.write('/tmp/%s.xml' % vm)
        runCmd('virsh define /tmp/%s.xml' % vm)
        runCmd('rm /tmp/%s.xml' % vm)
        return True
    return False


def define_and_restore_vm_disks(xmlfile, newname, source_to_target):
    logger.debug(xmlfile)
    logger.debug(source_to_target)
    if not xmlfile or not source_to_target:
        raise ExecuteException('', 'missing parameter: no vm xml file %s or source_to_target.' % xmlfile)
    uuid = randomUUID().replace('-', '')
    vm_file = '/tmp/%s.xml' % uuid
    runCmd('cp %s %s' % (xmlfile, vm_file))
    tree = ET.parse(vm_file)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    nameList = root.findall("name")
    for name in nameList:
        name.text = newname
    uuidList = root.findall("uuid")
    for uuid in uuidList:
        uuid.text = randomUUID()

    captionList = root.findall("devices")

    for caption in captionList:
        interfaces = caption.findall("interface")
        for interface in interfaces:
            caption.remove(interface)
        disks = caption.findall("disk")
        disk_need_to_delete = []
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element.get("file") in list(source_to_target.keys()):
                    source_element.set("file", source_to_target[source_element.get("file")])
                else:
                    disk_need_to_delete.append(disk)
        for disk in disk_need_to_delete:
            caption.remove(disk)
    tree.write(vm_file)
    runCmd('virsh define %s' % vm_file)
    runCmd('rm %s' % vm_file)

    try:
        helper = K8sHelper('VirtualMachine')
        vm_xml = get_vm_xml(newname)
        vm_json = toKubeJson(xmlToJson(vm_xml))
        vm_json = updateDomain(loads(vm_json))
        helper.create(newname, 'domain', vm_json)
    except:
        pass


def try_fix_disk_metadata(path):
    if os.path.basename(os.path.dirname(path)) == 'snapshots':
        disk = os.path.basename(os.path.dirname(os.path.dirname(path)))
        disk_dir = os.path.dirname(os.path.dirname(path))
    else:
        disk = os.path.basename(os.path.dirname(path))
        disk_dir = os.path.dirname(path)

    vol_info = get_vol_info_from_k8s(disk)
    pool_info = get_pool_info_from_k8s(vol_info['pool'])
    try:
        config_file = '%s/config.json' % disk_dir
        logger.debug("config_file: %s" % config_file)
        if not os.path.exists(config_file):
            RETRY_TIMES = 4
            for i in range(RETRY_TIMES):
                try:
                    pool_active(pool_info['pool'])
                    break
                except ExecuteException as e:
                    if i < RETRY_TIMES - 1:
                        pass
                    else:
                        error_print(101, "pool %s can not be active" % pool_info['pool'])

        config = get_disk_config_by_path(config_file)

        domains = get_all_domain()
        for domain in domains:
            try:
                disk_specs = get_disks_spec(domain)
                for disk_path in list(disk_specs.keys()):
                    if os.path.basename(os.path.dirname(disk_path)) == disk or os.path.basename(
                            os.path.dirname(os.path.dirname(disk_path))) == disk:
                        if config['current'] != disk_path or vol_info['current'] != disk_path:
                            logger.debug('try_fix_disk_metadata')
                            logger.debug('domain %s current: %s' % (domain, disk_path))
                            write_config(disk, disk_dir, disk_path, config['pool'], config['poolname'])
                            modifyDiskAndSs(config['pool'], disk)
                        return disk_path
            except:
                pass
        # not attach to vm, just try to fix disk
        # lists = []
        # for df in os.listdir(disk_dir):
        #     if df == 'config.json':
        #         continue
        #     lists.append('%s/%s' % (disk_dir, df))
        # ss_dir = '%s/snapshots' % disk_dir
        # if os.path.exists(ss_dir):
        #     for df in os.listdir(ss_dir):
        #         if df == 'config.json':
        #             continue
        #         lists.append('%s/%s' % (ss_dir, df))
        # lists.sort(key=lambda x: os.path.getmtime(x))
        # file_new = lists[-1]
        # disk_info = get_disk_info(file_new)
        # if config['current'] != file_new or vol_info['current'] != file_new:
        #     logger.debug('try_fix_disk_metadata')
        #     logger.debug('current: %s' % file_new)
        #     write_config(disk, disk_dir, file_new, config['pool'], config['poolname'])
        #     modify_disk_info_in_k8s(config['poolname'], disk)
        # return file_new
    except:
        logger.debug(traceback.format_exc())

    return None


def change_vm_os_disk_file(vm, source, target):
    if not vm or not source or not target:
        raise ExecuteException('', 'missing parameter: no vm name(%s) or source path(%s) or target path(%s).' % (
            vm, source, target))
    runCmd('virsh dumpxml %s > /tmp/%s.xml' % (vm, vm))
    tree = ET.parse('/tmp/%s.xml' % vm)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                if source_element.get("file") == source:
                    source_element.set("file", target)
                    tree.write('/tmp/%s.xml' % vm)
                    runCmd('virsh define /tmp/%s.xml' % vm)
                    return True
    return False


def is_shared_storage(path):
    if not path:
        raise ExecuteException('', 'missing parameter: no path.')
    cmd = 'df %s | awk \'{print $1}\' | sed -n "2, 1p"' % path
    fs = runCmdAndGetOutput(cmd)
    if fs:
        fs = fs.strip()
        if re.match('^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}:.*$', fs):
            return True
    return False


def get_vm_disks_from_xml(xmlfile):
    tree = ET.parse(xmlfile)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    all_disks = []
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                disk_file = source_element.get("file")
                if not is_shared_storage(disk_file):
                    all_disks.append(disk_file)

    return all_disks


def is_vm_disk_not_shared_storage(vm):
    if not vm:
        raise ExecuteException('', 'missing parameter: no vm name.')
    runCmd('virsh dumpxml %s > /tmp/%s.xml' % (vm, vm))
    tree = ET.parse('/tmp/%s.xml' % vm)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("source")
                disk_file = source_element.get("file")
                if not is_shared_storage(disk_file):
                    return False

    return True


def is_vm_disk_driver_cache_none(vm):
    if not vm:
        raise ExecuteException('', 'missing parameter: no vm name.')
    runCmd('virsh dumpxml %s > /tmp/%s.xml' % (vm, vm))
    tree = ET.parse('/tmp/%s.xml' % vm)

    root = tree.getroot()
    # for child in root:
    #     print(child.tag, "----", child.attrib)
    captionList = root.findall("devices")
    for caption in captionList:
        disks = caption.findall("disk")
        for disk in disks:
            if 'disk' == disk.attrib['device']:
                source_element = disk.find("driver")
                if "cache" in list(source_element.keys()) and source_element.get("cache") == "none":
                    continue
                else:
                    return False
    return True


def remote_start_pool(ip, pool):
    pool_info = get_pool_info_from_k8s(pool)
    remoteRunCmd(ip, 'kubesds-adm startPool --type %s --pool %s' % (pool_info['pooltype'], pool))


def auto_mount(pool):
    pool_info = get_pool_info_from_k8s(pool)

    proto = pool_info['pooltype']
    # opt = pool_info['url']
    opt = ''

    MOUNT_PATH = os.path.dirname(pool_info['path'])
    if not os.path.exists(MOUNT_PATH):
        os.makedirs(MOUNT_PATH)

    if pool_info['pooltype'] == 'nfs' and 'url' in pool_info.keys():
        url = pool_info['url']
        output = runCmdAndGetOutput('df %s' % MOUNT_PATH)
        for line in output.splitlines():
            if line.find(url) >= 0:
                return

        runCmd(
            'timeout --preserve-status --foreground 5 mount -t %s -o %s %s %s >/dev/null' % (
            proto, opt, url, MOUNT_PATH))


def mount_storage(pooltype, opt, url, path):
    if pooltype == 'nfs':
        runCmd(
            'timeout --preserve-status --foreground 5 mount -t %s -o %s %s %s >/dev/null' % (pooltype, opt, url, path))


def umount_storage(pool):
    pool_info = get_pool_info_from_k8s(pool)

    proto = pool_info['pooltype']
    path = pool_info['path']
    MOUNT_PATH = os.path.dirname(pool_info['path'])
    if proto == 'nfs' and 'url' in pool_info.keys():
        url = pool_info['url']
        output = runCmdAndGetOutput('df %s' % MOUNT_PATH)
        for line in output.splitlines():
            if line.find(url) >= 0:
                runCmd('timeout --preserve-status --foreground 5 umount -f %s >/dev/null' % MOUNT_PATH)




def pool_active(pool):
    auto_mount(pool)


def get_pool_all_disk(poolname):
    output = None
    for i in range(30):
        try:
            output = rpcCallAndGetOutput(
                'kubectl get vmd -o=jsonpath="{range .items[?(@.spec.volume.poolname==\\"%s\\")]}{.metadata.name}{\\"\\t\\"}{.metadata.labels.host}{\\"\\n\\"}{end}"' % poolname)
            break
        except Exception:
            logger.debug(traceback.format_exc())
    disks = []
    if output:
        for line in output.splitlines():
            disk = {}
            if len(line.split()) < 2:
                continue
            disk['disk'] = line.split()[0]
            disk['host'] = line.split()[1]
            disks.append(disk)
    return disks


def get_pool_all_ss(poolname):
    output = None
    for i in range(30):
        try:
            output = rpcCallAndGetOutput(
                'kubectl get vmdsn -o=jsonpath="{range .items[?(@.spec.volume.poolname==\\"%s\\")]}{.metadata.name}{\\"\\t\\"}{.metadata.labels.host}{\\"\\n\\"}{end}"' % poolname)
            break
        except Exception:
            logger.debug(traceback.format_exc())
    disks = []
    if output:
        for line in output.splitlines():
            disk = {}
            if len(line.split()) < 2:
                continue
            disk['ss'] = line.split()[0]
            disk['host'] = line.split()[1]
            disks.append(disk)
    return disks


def get_pools_by_node(node_name):
    output = None
    for i in range(30):
        try:
            output = rpcCallAndGetOutput(
                'kubectl get vmp -o=jsonpath="{range .items[?(.metadata.labels.host==\\"%s\\")]}{.metadata.name}{\\"\\t\\"}{.spec.pool.poolname}{\\"\\t\\"}{.metadata.labels.host}{\\"\\n\\"}{end}"' % node_name)
            break
        except Exception:
            logger.debug(traceback.format_exc())

    pools = []
    if output:
        for line in output.splitlines():
            pool = {}
            if len(line.split()) < 3:
                continue
            pool['pool'] = line.split()[0]
            pool['poolname'] = line.split()[1]
            pools.append(pool)
    return pools


def get_pools_by_path(path):
    output = None
    for i in range(30):
        try:
            output = rpcCallAndGetOutput(
                'kubectl get vmp -o=jsonpath="{range .items[?(@.spec.pool.path==\\"%s\\")]}{.metadata.name}{\\"\\t\\"}{.metadata.labels.host}{\\"\\t\\"}{.spec.pool.path}{\\"\\n\\"}{end}"' % path)
            break
        except Exception:
            logger.debug(traceback.format_exc())
    pools = []
    if output:
        for line in output.splitlines():
            pool = {}
            if len(line.split()) < 3:
                continue
            pool['pool'] = line.split()[0]
            pool['host'] = line.split()[1]
            pools.append(pool)
    return pools


def get_pools_by_poolname(poolname):
    output = None
    for i in range(30):
        try:
            output = rpcCallAndGetOutput(
                'kubectl get vmp -o=jsonpath="{range .items[?(@.spec.pool.poolname==\\"%s\\")]}{.metadata.name}{\\"\\t\\"}{.metadata.labels.host}{\\"\\t\\"}{.spec.pool.path}{\\"\\n\\"}{end}"' % poolname)
            break
        except Exception:
            logger.debug(traceback.format_exc())
    pools = []
    if output:
        for line in output.splitlines():
            pool = {}
            if len(line.split()) < 3:
                continue
            pool['pool'] = line.split()[0]
            pool['host'] = line.split()[1]
            pools.append(pool)
    return pools


def get_all_node_ip():
    all_node_ip = []
    try:
        jsondict = client.CoreV1Api().list_node().to_dict()
        nodes = jsondict['items']
        for node in nodes:
            try:
                node_ip = {}
                node_ip['ip'] = node['metadata']['annotations']['THISIP']
                node_ip['nodeName'] = node['metadata']['name']
                all_node_ip.append(node_ip)
            except:
                logger.debug(traceback.format_exc())
    except ApiException as e:
        logger.debug("Exception when calling CoreV1Api->list_node: %s\n" % e)
    except Exception as e:
        logger.debug("Exception when calling get_all_node_ip: %s\n" % e)

    return all_node_ip


def get_spec(jsondict):
    spec = jsondict.get('spec')
    if not spec:
        raw_object = jsondict.get('raw_object')
        if raw_object:
            spec = raw_object.get('spec')
    return spec


# get disk and snapshot jsondict and change to targetPool
# def get_migrate_disk_jsondict(disk, targetPool):
#     jsondicts = []
#     # two case: 1. pool has same path 2. pool has different path
#     pool_helper = K8sHelper('VirtualMachinePool')
#     pool_metadata = pool_helper.get(targetPool)['metadata']
#     pool_info = pool_helper.get_data(targetPool, 'pool')
#
#     # get disk jsondict
#     disk_helper = K8sHelper('VirtualMachineDisk')
#     disk_info = disk_helper.get_data(disk, 'volume')
#     disk_jsondict = disk_helper.get(disk)
#     if disk_info['poolname'] == pool_info['poolname']:  # same poolname
#         if disk_jsondict:
#             disk_jsondict['metadata']['labels']['host'] = pool_metadata['labels']['host']
#             spec = get_spec(disk_jsondict)
#             if spec:
#                 nodeName = spec.get('nodeName')
#                 if nodeName:
#                     spec['nodeName'] = pool_metadata['labels']['host']
#                 disk_info['pool'] = targetPool
#                 disk_info["poolname"] = pool_info['poolname']
#                 spec['volume'] = disk_info
#                 jsondicts.append(disk_jsondict)
#         ss_helper = K8sHelper('VirtualMachineDiskSnapshot')
#         ss_dir = '%s/%s/snapshots' % (pool_info['path'], disk)
#         for ss in os.listdir(ss_dir):
#             try:
#                 ss_jsondict = ss_helper.get(ss)
#                 if ss_jsondict:
#                     ss_jsondict['metadata']['labels']['host'] = pool_metadata['labels']['host']
#                     spec = get_spec(ss_jsondict)
#                     if spec:
#                         nodeName = spec.get('nodeName')
#                         if nodeName:
#                             spec['nodeName'] = pool_metadata['labels']['host']
#                         disk_info['pool'] = targetPool
#                         disk_info["poolname"] = pool_info['poolname']
#                         spec['volume'] = disk_info
#                         jsondicts.append(ss_jsondict)
#             except ExecuteException:
#                 pass
#
#     else:  #different poolname
#         pass
#
#
#     return jsondicts

def get_disk_jsondict(pool, disk):
    jsondicts = []
    pool_helper = K8sHelper('VirtualMachinePool')
    pool_jsondict = pool_helper.get(pool)
    pool_node_name = pool_jsondict['metadata']['labels']['host']
    pool_info = get_pool_info_from_k8s(pool)
    check_pool_active(pool_info)

    # get disk jsondict
    disk_helper = K8sHelper('VirtualMachineDisk')
    # if pool_info['pooltype'] not in ['localfs', 'nfs', 'glusterfs', "vdiskfs"]:
    #     raise ExecuteException("RunCmdError", "not support pool type %s" % pool_info['pooltype'])

    if disk_helper.exist(disk):  # migrate disk or migrate vm
        disk_jsondict = disk_helper.get(disk)
        # update disk jsondict
        disk_jsondict['metadata']['labels']['host'] = pool_node_name

        spec = get_spec(disk_jsondict)
        logger.debug(disk_jsondict)
        if spec:
            nodeName = spec.get('nodeName')
            if nodeName:
                spec['nodeName'] = pool_node_name
            # disk_dir = '%s/%s' % (pool_info['path'], disk)
            # config = get_disk_config(pool, disk)
            # write_config(disk, disk_dir, config['current'], pool, config['poolname'])
            disk_info = get_disk_info_to_k8s(pool_info['poolname'], disk)
            spec['volume'] = disk_info
            logger.debug(disk_jsondict)
            jsondicts.append(disk_jsondict)
        # update snapshot jsondict
        ss_helper = K8sHelper('VirtualMachineDiskSnapshot')
        ss_dir = '%s/%s/snapshots' % (pool_info['path'], disk)
        if os.path.exists(ss_dir):
            for ss in os.listdir(ss_dir):
                try:
                    ss_jsondict = ss_helper.get(ss)

                    if ss_jsondict and ss_helper.get_data(ss, 'volume')['disk'] == disk:
                        ss_jsondict['metadata']['labels']['host'] = pool_node_name
                        spec = get_spec(ss_jsondict)
                        if spec:
                            nodeName = spec.get('nodeName')
                            if nodeName:
                                spec['nodeName'] = pool_node_name
                            ss_info = get_snapshot_info_to_k8s(pool_info['poolname'], disk, ss)
                            spec['volume'] = ss_info
                            jsondicts.append(ss_jsondict)
                except ExecuteException:
                    pass

    else:  # clone disk
        disk_info = get_disk_info_to_k8s(pool_info['poolname'], disk)
        disk_jsondict = disk_helper.get_create_jsondict(disk, 'volume', disk_info)
        jsondicts.append(disk_jsondict)

        # ss_helper = K8sHelper('VirtualMachineDiskSnapshot')
        # ss_dir = '%s/%s/snapshots' % (pool_info['path'], disk)
        # for ss in os.listdir(ss_dir):
        #     try:
        #         ss_info = get_snapshot_info_to_k8s(pool_info['poolname'], disk, ss)
        #         ss_jsondict = ss_helper.get_create_jsondict(ss)
        #
        #         jsondicts.append(ss_jsondict)
        #     except ExecuteException:
        #         pass

    return jsondicts


def modifyDiskAndSs(pool, disk):
    # get disk node label in ip
    node_name = get_hostname_in_lower_case()
    # node_name = get_node_name_by_node_ip(params.ip)
    logger.debug("node_name: %s" % node_name)

    pool_info = get_pool_info_from_k8s(pool)
    pools = get_pools_by_path(pool_info['path'])
    logger.debug("pools: %s" % dumps(pools))
    logger.debug("node_name: %s" % node_name)
    # change disk node label in k8s.
    targetPool = None
    for pool in pools:
        if pool['host'] == node_name:
            targetPool = pool['pool']
    if targetPool:
        all_jsondicts = get_disk_jsondict(targetPool, disk)
        apply_all_jsondict(all_jsondicts)


def rebase_snapshot_with_config(pool, vol):
    pool_info = get_pool_info_from_k8s(pool)
    check_pool_active(pool_info)
    old_disk_info = get_vol_info_from_k8s(vol)
    old_pool_info = get_pool_info_from_k8s(old_disk_info['pool'])
    check_pool_active(old_pool_info)

    old_disk_dir = '%s/%s' % (old_pool_info['path'], vol)
    disk_dir = '%s/%s' % (pool_info['path'], vol)

    # change config
    old_config = get_disk_config(pool_info['poolname'], vol)
    current = old_config['current'].replace(old_pool_info['path'], pool_info['path'])
    write_config(vol, disk_dir, current, pool, pool_info['poolname'])

    # change backing file
    logger.debug('disk_dir: %s' % disk_dir)
    for ss in os.listdir(disk_dir):
        if ss == 'snapshots' or ss == 'config.json':
            continue
        ss_info = None
        ss_full_path = '%s/%s' % (disk_dir, ss)
        try:
            ss_info = get_disk_info(ss_full_path)
        except ExecuteException:
            pass
        if ss_info:
            if 'backing_filename' in list(ss_info.keys()):
                old_backing_file = ss_info['backing_filename']
                new_backing_file = old_backing_file.replace(old_disk_dir, disk_dir)
                logger.debug('old backing file %s, new backing file %s' % (old_backing_file, new_backing_file))
                if os.path.exists(new_backing_file):
                    runCmd('qemu-img rebase -b %s %s' % (new_backing_file, ss_full_path))
    ss_dir = '%s/snapshots' % disk_dir
    logger.debug('ss_dir: %s' % ss_dir)
    if os.path.exists(ss_dir):
        for ss in os.listdir(ss_dir):
            ss_info = None
            ss_full_path = '%s/%s' % (ss_dir, ss)
            try:
                ss_info = get_disk_info(ss_full_path)
            except ExecuteException:
                pass
            if ss_info:
                if 'backing_filename' in list(ss_info.keys()):
                    old_backing_file = ss_info['backing_filename']
                    new_backing_file = old_backing_file.replace(old_disk_dir, disk_dir)
                    logger.debug('old backing file %s, new backing file %s' % (old_backing_file, new_backing_file))
                    if os.path.exists(new_backing_file):
                        runCmd('qemu-img rebase -u -b %s %s' % (new_backing_file, ss_full_path))
    jsondicts = get_disk_jsondict(pool, vol)

    apply_all_jsondict(jsondicts)


def apply_all_jsondict(jsondicts):
    if len(jsondicts) == 0:
        return
    logger.debug(jsondicts)
    filename = randomUUID()
    logger.debug(filename)
    for i in range(30):
        with open('/tmp/%s.yaml' % filename, 'w') as f:
            for i in range(len(jsondicts)):
                current_jsondict = replaceData(jsondicts[i])
                result = yaml.safe_dump(current_jsondict)
                f.write(result)
                if i != len(jsondicts) - 1:
                    f.write('---\n')
        try:
            logger.debug("jsondicts: /tmp/%s.yaml" % filename)
            runCmd('kubectl apply -f /tmp/%s.yaml' % filename)
            # try:
            #     runCmd('rm -f /tmp/%s.yaml' % filename)
            # except ExecuteException:
            #     pass
            return
        except ExecuteException as e:
            logger.debug(e.message)
            if e.message.find('Warning') >= 0 or e.message.find(
                    'failed to open a connection to the hypervisor software') >= 0:
                pass
    raise ExecuteException('RunCmdError', 'can not apply jsondict %s on k8s.' % dumps(jsondicts))


def create_all_jsondict(jsondicts):
    if len(jsondicts) == 0:
        return
    filename = randomUUID()
    logger.debug(filename)
    with open('/tmp/%s.yaml' % filename, 'w') as f:
        for i in range(len(jsondicts)):
            result = yaml.safe_dump(jsondicts[i])
            f.write(result)
            if i != len(jsondicts) - 1:
                f.write('---\n')
    for i in range(30):
        try:
            runCmd('kubectl create -f /tmp/%s.yaml' % filename)
            # if result['result'] != 0:
            #     raise ExecuteException('RunCmdError', result['result']['msg'])
            try:
                runCmd('rm -f /tmp/%s.yaml' % filename)
            except ExecuteException:
                pass
            return
        except ExecuteException as e:
            logger.debug(e.message)
            if e.message.find('Warning') >= 0 or e.message.find(
                    'failed to open a connection to the hypervisor software') >= 0:
                pass
    raise ExecuteException('RunCmdError', 'can not apply jsondict %s on k8s.' % dumps(jsondicts))


def get_node_ip_by_node_name(nodeName):
    all_node_ip = get_all_node_ip()
    if all_node_ip:
        for ip in all_node_ip:
            if ip['nodeName'] == nodeName:
                return ip['ip']
    return None


def get_node_name_by_node_ip(ip):
    all_node_ip = get_all_node_ip()
    nic_ips = get_remote_node_all_nic_ip(ip)
    if all_node_ip:
        for node in all_node_ip:
            if node['ip'] in nic_ips and node['nodeName'].find("vm.") >= 0:
                return node['nodeName']
    return None


def get_vm_xml(domain):
    return runCmdAndGetOutput('virsh dumpxml %s' % domain)


def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)


def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
        'interface', '_interface').replace('transient', '_transient').replace(
        'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk',
                                                                                      'suspend_to_disk')


def _addListToSpecificField(data):
    if isinstance(data, list):
        return data
    else:
        return [data]


'''
Cautions! Do not modify this function because it uses reflections!
'''


def _userDefinedOperationInList(field, jsondict, alist):
    jsondict = jsondict[field]
    tmp = jsondict
    do_it = False
    for index, value in enumerate(alist):
        if index == 0:
            if value != field:
                break
            continue
        tmp = tmp.get(value)
        if not tmp:
            do_it = False
            break
        do_it = True
    if do_it:
        tmp2 = None
        for index, value in enumerate(alist):
            if index == 0:
                tmp2 = 'jsondict'
            else:
                tmp2 = '{}[\'{}\']'.format(tmp2, value)
        exec(('{} = {}').format(tmp2, _addListToSpecificField(tmp)))
    return


def updateDomain(jsondict):
    for line in vmArray:
        alist = line.split('-')
        _userDefinedOperationInList('domain', jsondict, alist)
    return jsondict


def modifyVMOnNode(domain):
    helper = K8sHelper('VirtualMachine')
    try:
        jsonDict = helper.get(domain)
        vm_xml = get_vm_xml(domain)
        vm_json = toKubeJson(xmlToJson(vm_xml))
        vm_json = updateDomain(loads(vm_json))
        vm_json = updateJsonRemoveLifecycle(jsonDict, vm_json)
        jsonDict = addPowerStatusMessage(vm_json, 'Running', 'The VM is running.')
        helper.updateAll(domain, jsonDict)
    except:
        pass


# def checkVMDiskFileChanged():
#     p = subprocess.Popen('virt-diff ', shell=True, stdout=subprocess.PIPE)
#     try:
#         while True:
#             output = p.stdout.readline()
#             if output == '' and p.poll() is not None:
#                 break
#             if output:
#                 # print output.strip()
#                 p.terminate()
#     except Exception:
#         traceback.print_exc()
#     finally:
#         p.stdout.close()

def checksum(path, block_size=8192):
    with open(path, "rb") as f:
        file_hash = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            file_hash.update(data)
        return file_hash.hexdigest()


def get_disk_backup_current(domain, pool, disk):
    pool_info = get_pool_info_from_k8s(pool)
    disk_backup_dir = '%s/vmbackup/%s/diskbackup/%s' % (pool_info['path'], domain, disk)
    history_file_path = '%s/history.json' % disk_backup_dir
    if not os.path.exists(history_file_path):
        raise ExecuteException('', 'can not find disk %s current full backup version in %s' % (
            disk, history_file_path))
    with open(history_file_path, 'r') as f:
        history = load(f)
        if 'current' not in list(history.keys()):
            raise ExecuteException('', 'disk %s backup version not exist current full backup version. plz check %s' % (
                disk, history_file_path))
        if history['current'] in list(history.keys()):
            return history['current']
        else:
            disk_versions = get_disk_backup_full_version(domain, pool, disk)
            if len(disk_versions) == 0:
                raise ExecuteException('',
                                       'disk %s backup version not exist full backup version. plz check %s' % (
                                           disk, history_file_path))
            time = 0.0
            newestV = None
            for fv in disk_versions:
                for v in list(history[fv].keys()):
                    if history[fv][v]['time'] > time:
                        time = history[fv][v]['time']
                        newestV = fv
            if newestV is None:
                raise ExecuteException('',
                                       'disk %s backup version not exist full backup version. plz check %s' % (
                                           disk, history_file_path))
            else:
                return newestV


def is_disk_backup_exist(domain, pool, disk, version):
    pool_info = get_pool_info_from_k8s(pool)
    disk_backup_dir = '%s/vmbackup/%s/diskbackup/%s' % (pool_info['path'], domain, disk)
    history_file = '%s/history.json' % disk_backup_dir
    if not os.path.exists(history_file):
        return False
    with open(history_file, 'r') as f:
        history = load(f)
        for full_version in list(history.keys()):
            if full_version == 'current':
                continue
            if version in list(history[full_version].keys()):
                return True
    return False


def is_vm_backup_exist(domain, pool, version):
    pool_info = get_pool_info_from_k8s(pool)
    backup_dir = '%s/vmbackup/%s' % (pool_info['path'], domain)
    history_file_path = '%s/history.json' % backup_dir
    if not os.path.exists(history_file_path):
        return False
    with open(history_file_path, 'r') as f:
        history = load(f)
        if version in list(history.keys()):
            return True
    return False


def is_remote_vm_backup_exist(domain, version, remote, port, username, password):
    target_dir = '/vmbackup/%s' % domain
    ftp = FtpHelper(remote, port, username, password)
    history_file = '%s/history.json' % target_dir
    if ftp.is_exist_dir(target_dir) and ftp.is_exist_file(history_file):
        history = ftp.get_json_file_data(history_file)
        if history and version in list(history.keys()):
            return True
    return False


def get_full_version(domain, pool, disk, version):
    pool_info = get_pool_info_from_k8s(pool)
    disk_backup_dir = '%s/vmbackup/%s/diskbackup/%s' % (pool_info['path'], domain, disk)
    history_file = '%s/history.json' % disk_backup_dir
    if not os.path.exists(history_file):
        raise ExecuteException('', 'not exist history file %s' % history_file)
    with open(history_file, 'r') as f:
        history = load(f)
        logger.debug(dumps(history))
        for full_version in list(history.keys()):
            if full_version == 'current':
                continue
            if version in list(history[full_version].keys()):
                return full_version
    raise ExecuteException('', 'not exist disk %s full backup version in history file %s.' % (disk, history_file))


def get_full_version_by_history(disk, version, history):
    for full_version in list(history.keys()):
        if full_version == 'current':
            continue
        if version in list(history[full_version].keys()):
            return full_version
    raise ExecuteException('', 'not exist disk %s backup version %s in history %s.' % (disk, version, dumps(history)))


def get_disk_backup_version(domain, pool, disk):
    pool_info = get_pool_info_from_k8s(pool)
    disk_backup_dir = '%s/vmbackup/%s/diskbackup/%s' % (pool_info['path'], domain, disk)

    vm_history_file = '%s/vmbackup/%s/history.json' % (pool_info['path'], domain)
    vm_disk_full_versions = set()
    if os.path.exists(vm_history_file):
        with open(vm_history_file, 'r') as f:
            vm_history = load(f)
            for v in list(vm_history.keys()):
                record = vm_history[v]
                if disk in list(record.keys()):
                    vm_disk_full_versions.add(record[disk]['full'])

    history_file = '%s/history.json' % disk_backup_dir
    disk_versions = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = load(f)
            logger.debug(dumps(history))
            for full_version in list(history.keys()):
                if full_version == 'current':
                    continue
                if full_version in vm_disk_full_versions:
                    continue
                for v in list(history[full_version].keys()):
                    disk_versions.append(v)
    return disk_versions


def get_disk_backup_full_version(domain, pool, disk):
    pool_info = get_pool_info_from_k8s(pool)
    disk_backup_dir = '%s/vmbackup/%s/diskbackup/%s' % (pool_info['path'], domain, disk)

    vm_history_file = '%s/vmbackup/%s/history.json' % (pool_info['path'], domain)
    vm_disk_full_versions = set()
    if os.path.exists(vm_history_file):
        with open(vm_history_file, 'r') as f:
            vm_history = load(f)
            for v in list(vm_history.keys()):
                record = vm_history[v]
                if disk in list(record.keys()):
                    vm_disk_full_versions.add(record[disk]['full'])

    history_file = '%s/history.json' % disk_backup_dir
    if not os.path.exists(history_file):
        raise ExecuteException('', 'not exist history file %s' % history_file)

    disk_versions = []
    with open(history_file, 'r') as f:
        history = load(f)
        logger.debug(dumps(history))
        for full_version in list(history.keys()):
            if full_version == 'current':
                continue
            if full_version in vm_disk_full_versions:
                continue
            disk_versions.append(full_version)
    return disk_versions


def get_remote_disk_backup_version(domain, disk, remote, port, username, password):
    vm_history_file = '/vmbackup/%s/history.json' % domain
    ftp = FtpHelper(remote, port, username, password)
    vm_history = ftp.get_json_file_data(vm_history_file)
    vm_disk_full_versions = set()
    if vm_history:
        for v in list(vm_history.keys()):
            record = vm_history[v]
            if disk in list(record.keys()):
                vm_disk_full_versions.add(record[disk]['full'])
    disk_versions = []
    disk_backup_dir = '/vmbackup/%s/diskbackup/%s' % (domain, disk)
    history_file = '%s/history.json' % disk_backup_dir
    history = ftp.get_json_file_data(history_file)
    if history:
        logger.debug(dumps(history))
        for full_version in list(history.keys()):
            if full_version == 'current':
                continue
            if full_version in vm_disk_full_versions:
                continue
            for v in list(history[full_version].keys()):
                disk_versions.append(v)
    return disk_versions


def is_remote_disk_backup_exist(domain, disk, version, remote, port, username, password):
    target_dir = '/vmbackup/%s/diskbackup/%s' % (domain, disk)
    ftp = FtpHelper(remote, port, username, password)
    if ftp.is_exist_dir(target_dir) and ftp.is_exist_file('%s/history.json' % target_dir):
        history = ftp.get_json_file_data('%s/history.json' % target_dir)
        if disk not in list(history.keys()):
            return False
        for full_version in list(history.keys()):
            if full_version == 'current':
                continue
            if version in list(history[full_version].keys()):
                return True
    return False


def backup_snapshots_chain(current, backup_path):
    if not os.path.exists(current):
        raise ExecuteException('', 'not exist disk dir need to backup: %s' % current)
    result = {}
    result['current'] = get_disk_info(current)['full_backing_filename']
    backup_files = set()
    image_file = None
    chains = []
    checksums = {}

    # only backup the current chain
    old_current = result['current']
    backup_files.add(old_current)
    # back up disk image
    disk_info = get_disk_info(old_current)
    while 'full_backing_filename' in list(disk_info.keys()):
        backup_files.add(disk_info['full_backing_filename'])
        disk_info = get_disk_info(disk_info['full_backing_filename'])

    # record snapshot chain
    disk_backup_dir = '%s/diskbackup' % backup_path
    backed_disk_file = []
    try:
        for bf in backup_files:
            disk_checksum = backup_file(bf, disk_backup_dir, backed_disk_file)
            checksums[bf] = disk_checksum
    except Exception as e:
        try:
            for df in backed_disk_file:
                runCmd('rm -f %s' % df)
        except:
            pass
        raise e
    for bf in backup_files:
        disk_info = get_disk_info(bf)
        record = {}
        record['path'] = bf
        record['checksum'] = checksums[bf]
        if 'full_backing_filename' in list(disk_info.keys()):
            record['parent'] = disk_info['full_backing_filename']
        else:
            record['parent'] = ''
        chains.append(record)
    result['chains'] = chains
    return result, backed_disk_file


def backup_file(file, target_dir, backed_disk_file):
    # print file
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    file_checksum = checksum(file)
    logger.debug('%s checksum: %s' % (file, file_checksum))
    history_file = '%s/checksum.json' % target_dir
    backupRecord = None
    history = {}
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = load(f)
            if file_checksum in list(history.keys()):
                backupRecord = history[file_checksum]

    if not backupRecord:
        # backup file
        target = '%s/%s' % (target_dir, os.path.basename(file))
        if os.path.exists(target):
            uuid = randomUUID().replace('-', '')
            target = '%s/%s' % (target_dir, uuid)
        backed_disk_file.append(target)
        runCmd('cp -f %s %s' % (file, target))

        # dump hisory
        history[file_checksum] = os.path.basename(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(history_file, 'w') as f:
            dump(history, f)
    return file_checksum


def restore_snapshots_chain(disk_back_dir, record, target_dir):
    vm_backup_path = os.path.dirname(disk_back_dir)
    backup_path = os.path.dirname(vm_backup_path)
    # disk_back_dir = '%s/diskbackup' % vm_backup_path

    checksum_file = '%s/checksum.json' % disk_back_dir
    with open(checksum_file, 'r') as f:
        checksums = load(f)

    old_to_new = {}
    cp_disks = []
    chains = record['chains']
    try:
        # cp all file and make a chain
        # logger.debug(dumps(record))

        disk_checksums = {}
        for d in os.listdir(target_dir):
            if d == 'config.json' or d == 'snapshots':
                continue
            f = '%s/%s' % (target_dir, d)
            c = checksum('%s/%s' % (target_dir, d))
            disk_checksums[c] = f
        snapshot_dir = '%s/snapshots' % target_dir
        if os.path.exists(snapshot_dir):
            for d in os.listdir(snapshot_dir):
                f = '%s/%s' % (snapshot_dir, d)
                c = checksum('%s/%s' % (snapshot_dir, d))
                disk_checksums[c] = f
        for chain in chains:
            # print chain['path']
            if chain['checksum'] not in list(checksums.keys()):
                raise ExecuteException('', 'can not find disk file backup checksum.')

            if chain['checksum'] in list(disk_checksums.keys()):
                old_to_new[chain['path']] = disk_checksums[chain['checksum']]
                logger.debug('do not need cp %s ' % disk_checksums[chain['checksum']])
                continue

            backup_file = '%s/%s' % (disk_back_dir, checksums[chain['checksum']])
            if not os.path.exists(backup_file):
                raise ExecuteException('', 'can not find disk backup file %s.' % backup_file)
            if chain['parent']:
                new_disk_file = '%s/%s' % (target_dir, os.path.basename(chain['path']))
                if chain['path'].find(target_dir) < 0:
                    uuid = randomUUID().replace('-', '')
                    new_disk_file = '%s/%s' % (target_dir, uuid)
                old_to_new[chain['path']] = new_disk_file
                runCmd('cp -f %s %s' % (backup_file, new_disk_file))
                cp_disks.append(new_disk_file)
            else:
                # base image
                # if image exist, not cp
                di_helper = K8sHelper('VirtualMachineDiskImage')
                image = os.path.basename(chain['path'])
                if di_helper.exist(image):
                    volume = di_helper.get_data(image, 'volume')
                    logger.debug('volume')
                    logger.debug(volume)
                    if volume and isinstance(volume, dict) and os.path.exists(volume['current']) and checksum(
                            volume['current']) == chain['checksum']:
                        old_to_new[chain['path']] = volume['current']
                        continue
                logger.debug('base image: start cp')
                if chain['path'].find('snapshots') >= 0:
                    base_file = '%s/snapshots/%s' % (target_dir, os.path.basename(chain['path']))
                else:
                    base_file = '%s/%s' % (target_dir, os.path.basename(chain['path']))
                new_disk_file = '%s/%s' % (target_dir, os.path.basename(chain['path']))
                if not os.path.exists(base_file):
                    old_to_new[chain['path']] = new_disk_file
                    runCmd('cp -f %s %s' % (backup_file, new_disk_file))
                    cp_disks.append(new_disk_file)
                else:
                    base_image_checksum = checksum(base_file)
                    if base_image_checksum == chain['checksum']:
                        old_to_new[chain['path']] = base_file
                    else:
                        old_to_new[chain['path']] = new_disk_file
                        runCmd('cp -f %s %s' % (backup_file, new_disk_file))
                        cp_disks.append(new_disk_file)
        for df in list(old_to_new.values()):
            runCmd('chmod 666 %s' % df)
    except ExecuteException as e:
        for file in cp_disks:
            runCmd('rm -f %s' % file)
        raise e

    logger.debug('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    logger.debug(dumps(disk_checksums))
    logger.debug(dumps(chains))

    # reconnect snapshot chain
    for chain in chains:
        # print dumps(chain)
        if chain['parent']:
            # parent = '%s/%s' % (disk_dir, os.path.basename(chain['parent']))
            # print 'qemu-img rebase -f qcow2 -b %s %s' % (old_to_new[chain['parent']], old_to_new[chain['path']])
            runCmd('qemu-img rebase -f qcow2 -u -b %s %s' % (old_to_new[chain['parent']], old_to_new[chain['path']]))

    # if this disk has no snapshots, try to delete other file
    ss_dir = '%s/snapshots' % target_dir
    exist_ss = False
    if os.path.exists(ss_dir):
        for ss in os.listdir(ss_dir):
            try:
                ss_info = get_snapshot_info_from_k8s(ss)
                exist_ss = True
            except:
                pass
    file_to_delete = []
    if not exist_ss:
        if os.path.exists(ss_dir):
            for ss in os.listdir(ss_dir):
                ss_file = '%s/%s' % (ss_dir, ss)
                if os.path.isfile(ss_file) and ss_file not in list(old_to_new.values()):
                    file_to_delete.append(ss_file)
        if os.path.exists(target_dir):
            for ss in os.listdir(target_dir):
                if ss == 'config.json':
                    continue
                ss_file = '%s/%s' % (target_dir, ss)
                if os.path.isfile(ss_file) and ss_file not in list(old_to_new.values()):
                    file_to_delete.append(ss_file)

    # if backup_disk['current'].find('snapshots') >= 0:
    #     disk_current = '%s/snapshots/%s' % (disk_dir, os.path.basename(backup_disk['current']))
    # else:
    #     disk_current = '%s/%s' % (disk_dir, os.path.basename(backup_disk['current']))
    disk_current = record['current']
    return old_to_new[disk_current], file_to_delete


def check_pool_active(info):
    pool_helper = K8sHelper('VirtualMachinePool')
    this_node_name = get_hostname_in_lower_case()
    pool_node_name = get_node_name(pool_helper.get(info['pool']))
    if this_node_name != pool_node_name:
        if info['state'] == 'inactive':
            error_print(220, 'pool %s is not active, please run "startPool" first' % info['pool'])
        else:
            return

    if this_node_name == pool_node_name and info['state'] == 'active':
        try:
            auto_mount(info['pool'])
            if not is_pool_started(info['poolname']):
                runCmd('virsh pool-start %s' % info['poolname'])
        except ExecuteException as e:
            error_print(221, e.message)

    result = get_pool_info_to_k8s(info['pooltype'], info['pool'], info['url'], info['poolname'], info['content'])
    # update pool
    if operator.eq(info, result) != 0:
        k8s = K8sHelper('VirtualMachinePool')
        try:
            k8s.update(info['pool'], 'pool', result)
        except:
            pass

    if result['state'] != 'active':
        error_print(221, 'pool %s is not active, please run "startPool" first' % info['pool'])


def change_k8s_pool_state(pool, state):
    helper = K8sHelper("VirtualMachinePool")
    pool_info = helper.get_data(pool, "pool")
    pool_info['state'] = state
    helper.update(pool, 'pool', pool_info)


def success_print(msg, data):
    print(dumps({"result": {"code": 0, "msg": msg}, "data": data}))
    # exit(0)


def error_print(code, msg, data=None):
    if data is None:
        print(dumps({"result": {"code": code, "msg": msg}, "data": {}}))
        # exit(1)
    else:
        print(dumps({"result": {"code": code, "msg": msg}, "data": data}))
        # exit(1)


if __name__ == '__main__':
    print(get_pool_info('07098ca5fd174fccafee76b0d7fccde4'))
    print(runCmdAndTransferXmlToJson('virsh pool-dumpxml 07098ca5fd174fccafee76b0d7fccde4'))
    # print is_pool_started("170dd9accdd174caced76b0db2230")
    # print get_all_node_ip()
    # check_pool_active(get_pool_info_from_k8s('migratenodepool22'))
    # print is_vm_exist('dsadada')
    # pool_helper = K8sHelper('VirtualMachinePool')
    # # pool_info = get_pool_info_to_k8s('nfs', 'migratepoolnodepool22', '170dd9accdd174caced76b0db2223', 'vmd')
    # # pool_helper.update('migratepoolnodepool22', 'pool', pool_info)
    # pool_helper.delete_lifecycle('migratepoolnodepool22')
    # print get_os_disk("cloudinitbackup")

    # print get_pools_by_node('vm.node25')
    # print get_pool_info_from_k8s('7daed7737ea0480eb078567febda62ea')
    # jsondicts = get_migrate_disk_jsondict('vm006migratedisk1', 'migratepoolnode35')
    # apply_all_jsondict(jsondicts)
# print get_snapshot_info_from_k8s('disktestd313.2')
# print get_pool_info(' node22-poolnfs')
# print is_vm_disk_not_shared_storage('vm006')

# print change_vm_os_disk_file('vm010', '/uit/pooluittest/diskuittest/snapshots/diskuittest.2', '/uit/pooluittest/diskuittest/snapshots/diskuittest.1')
# print get_all_snapshot_to_delete('/var/lib/libvirt/pooltest/disktest/disktest', '/var/lib/libvirt/pooltest/disktest/ss3')

# print os.path.basename('/var/lib/libvirt/pooltest/disktest/disktest')

# print get_disk_snapshots('/var/lib/libvirt/pooltest/disktest/ss1')

# print get_pool_info('test1')

# print get_sn_chain_path('/var/lib/libvirt/pooltest/disktest/0e8e48d9-b6ab-4477-999d-0e57b521a51b')
