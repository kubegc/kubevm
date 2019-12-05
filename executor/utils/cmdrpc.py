import os
import traceback
from json import loads

import grpc

from netutils import get_docker0_IP
import logger

import cmdcall_pb2
import cmdcall_pb2_grpc

from utils import ExecuteException

LOG = "/var/log/virtctl.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '19999'

# cmd = 'virsh pool-define-as --type dir  --name pooldir2  --target /var/lib/libvirt/pooldir2'
# with grpc.insecure_channel("{0}:{1}".format(host, port)) as channel:
#     client = cmdcall_pb2_grpc.CmdCallStub(channel=channel)
#     response = client.Call(cmdcall_pb2.CallRequest(cmd=cmd))
#     logger.debug("received: " + response.json)
#     print response.json



def rpcCallWithResult(cmd, raise_it=True):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        # ideally, you should have try catch block here too
        response = client.CallWithResult(cmdcall_pb2.CallRequest(cmd=cmd))
        result = loads(str(response.json))
        logger.debug(result)
        if result is None:
            raise ExecuteException('RunCmdError', 'can not get cmd output.')
        if result['result']['code'] != 0 and raise_it:
            raise ExecuteException('RunCmdError', result['result']['msg'])
        return result['result'], result['data']
    except grpc.RpcError, e:
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
    except Exception, e:
        logger.debug(traceback.format_exc())
        raise ExecuteException('RunCmdError', e.message)

def rpcCall(cmd, raise_it=True):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = cmdcall_pb2_grpc.CmdCallStub(channel)
        response = client.Call(cmdcall_pb2.CallRequest(cmd=cmd))
        result = loads(str(response.json))
        logger.debug(result)
        if result is None:
            raise ExecuteException('RunCmdError', 'can not get cmd output.')
        if result['result']['code'] != 0 and raise_it:
            raise ExecuteException('RunCmdError', result['result']['msg'])
    except grpc.RpcError, e:
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

if __name__ == '__main__':
    rpcCall('python /tmp/pycharm_project_666/vmm.py  delete_vmdi  --sourcePool node22poolnfsvmdi --name disktest11daa.temp2')