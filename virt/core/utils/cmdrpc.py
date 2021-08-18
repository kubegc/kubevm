import os
import traceback
import time
from json import loads

import grpc

try:
    from utils.netutils import get_docker0_IP
    from utils import logger
    from utils.exception import BadRequest
    from utils import constants
    from utils import cmdcall_pb2
    from utils import cmdcall_pb2_grpc
except:
    from netutils import get_docker0_IP
    import logger
    from exception import BadRequest
    import constants
    import cmdcall_pb2
    import cmdcall_pb2_grpc


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
    for i in range(1,4):
        logger.debug("Executing command %s, a %d try." % (cmd, i))
        try:
            host = get_docker0_IP()
            channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
            client = cmdcall_pb2_grpc.CmdCallStub(channel)
            # ideally, you should have try catch block here too
            response = client.CallWithResult(cmdcall_pb2.CallRequest(cmd=cmd))
            result = loads(str(response.json))
            # logger.debug(result)
            if result is None:
                raise BadRequest('RunCmdError: %s' % 'can not get cmd output.')
            if result['result']['code'] != 0 and raise_it:
                raise BadRequest('RunCmdError: %s' % result['result']['msg'])
            return result['result'], result['data']
        except grpc.RpcError as e:
            logger.debug(repr(e))
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
            if i == 3:
                raise BadRequest('RpcError: %s' % status_code.name)
            time.sleep(3)
            logger.debug(cmd)
            continue
#             raise ExecuteException('RpcError', status_code.name)
        except Exception as e:
            logger.debug(repr(e))
            if i == 3:
                raise BadRequest('RunCmdError: %s' % e.message)
            time.sleep(3)
            continue
#             raise ExecuteException('RunCmdError', e.message)

def rpcCall(cmd, raise_it=True):
    for i in range(1,4):
        logger.debug("Executing command %s, a %d try." % (cmd, i))
        try:
            host = get_docker0_IP()
            channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
            client = cmdcall_pb2_grpc.CmdCallStub(channel)
            response = client.Call(cmdcall_pb2.CallRequest(cmd=cmd))
            result = loads(str(response.json))
            logger.debug(result)
            if result is None:
                raise BadRequest('RunCmdError: %s' % 'can not get cmd output.')
            if result['result']['code'] != 0 and raise_it:
                raise BadRequest('RunCmdError: %s' % result['result']['msg'])
            return
        except grpc.RpcError as e:
            logger.debug(repr(e))
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
            if i == 3:
                raise BadRequest('RpcError: %s' % status_code.name)
            time.sleep(3)
            continue
        except Exception as e:
            logger.debug(repr(e))
            if i == 3:
                raise BadRequest('RunCmdError: %s' % e.message)
            time.sleep(3)
            continue

if __name__ == '__main__':
#     rpcCall('python /tmp/pycharm_project_666/vmm.py  delete_vmdi  --sourcePool node22poolnfsvmdi --name disktest11daa.temp2')
    rpcCall('kubesds-adm prepareDisk --path /var/lib/libvirt/cstor/076fe6aa813842d3ba141f172e3f8eb6/076fe6aa813842d3ba141f172e3f8eb6/4a2b67b44f4c4fca87e7a811e9fd545c.iso')