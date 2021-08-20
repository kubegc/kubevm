import os
import traceback
from json import loads

import grpc

from netutils import get_docker0_IP
from utils import logger

import cmdcall_pb2
import cmdcall_pb2_grpc
from utils.exception import ExecuteException

LOG = "/var/log/cmdrpc-cli.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '19999'

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

rpcCallWithResult('ls .')
