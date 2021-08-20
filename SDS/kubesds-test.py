import argparse

from operation import *

from utils import logger
from utils.exception import ConditionException

LOG = "/var/log/kubesds3.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

SUPPORT_STORAGE_TYPE = ["localfs", "nfs", "glusterfs"]


# os.putenv('LANG', 'en_US.UTF-8')

def execute(f_name, params):
    moudle = __import__('operation')
    func = getattr(moudle, f_name)
    try:
        check(f_name, params)
        func(params)
    except ExecuteException as e:
        logger.debug(f_name)
        logger.debug(params)
        logger.debug(traceback.format_exc())
        error_print(400, "error occur while %s. %s" % (f_name, e.message))
    except Exception:
        logger.debug(f_name)
        logger.debug(params)
        logger.debug(traceback.format_exc())
        error_print(300, "error occur while %s. traceback: %s" % (f_name, traceback.format_exc()))


def check(f_name, args):
    check_storage_type(args)
    check_pool(f_name, args)


def check_storage_type(args):
    if hasattr(args, 'type') and args.type not in SUPPORT_STORAGE_TYPE:
        error_print(100, "unsupported value type: %s" % args.type)


# check pool type, if pool type not match, stop delete pool
def check_pool_type(args):
    try:
        if not hasattr(args, 'type'):
            return
        if not hasattr(args, 'pool'):
            return
        if args is None:
            return
        pool_info = get_pool_info_from_k8s(args.pool)
        if pool_info is None:
            error_print(202, "check_pool_type, cannot get pool info from k8s.")
        if pool_info['pooltype'] == args.type:
            return
        else:
            error_print(221, "check_pool_type, pool type is not match. given is %s, actual is %s" % (
                args.type, pool_info['pooltype']))
    except ExecuteException:
        logger.debug(traceback.format_exc())
        error_print(202, "check_pool_type, cannot get pool info from k8s.")


def check_pool(f_name, args):
    try:
        if f_name == 'cloneDisk':
            return
        if not hasattr(args, 'type'):
            return
        if not hasattr(args, 'pool'):
            return
        if f_name == 'createPool':
            if is_pool_exists(args.uuid):
                raise ConditionException(201, "virsh pool %s has exist" % args.uuid)
        else:
            if f_name == 'deletePool':
                # if pool is not create successful, delete it from k8s.
                helper = K8sHelper("VirtualMachinePool")
                pool_info = helper.get_data(args.pool, "pool")
                if pool_info is None:
                    helper.delete(args.pool)
                    success_print("delete pool %s successful." % args.pool, {})

            check_pool_type(args)
            pool_info = get_pool_info_from_k8s(args.pool)
            pool = pool_info['poolname']
            if not is_pool_exists(pool):
                raise ConditionException(203, "virsh pool %s not exist" % pool)
    except ExecuteException as e1:
        logger.debug(traceback.format_exc())
        error_print(202, "check_pool, cannot get pool info. %s" % e1.message)
    except ConditionException as e2:
        logger.debug(traceback.format_exc())
        error_print(e2.code, e2.msg)


def is_virsh_disk_exist(pool, diskname):
    pool_info = get_pool_info(pool)
    if os.path.isdir('%s/%s' % (pool_info['path'], diskname)):
        return True
    return False


def check_virsh_disk_exist(pool, diskname):
    pool_info = get_pool_info(pool)
    if os.path.isdir('%s/%s' % (pool_info['path'], diskname)):
        error_print(207, "virsh disk %s is in pool %s" % (diskname, pool))


def check_virsh_disk_not_exist(pool, diskname):
    pool_info = get_pool_info(pool)
    if not os.path.isdir('%s/%s' % (pool_info['path'], diskname)):
        error_print(209, "virsh disk %s is not in pool %s" % (diskname, pool))


def check_virsh_disk_snapshot_exist(pool, diskname, snapshot):
    pool_info = get_pool_info(pool)
    if os.path.exists('%s/%s/snapshots/%s' % (pool_info['path'], diskname, snapshot)):
        error_print(209, "virsh disk snapshot %s is in volume %s" % (snapshot, diskname))


def check_virsh_disk_snapshot_not_exist(pool, diskname, snapshot):
    pool_info = get_pool_info(pool)
    if not os.path.exists('%s/%s/snapshots/%s' % (pool_info['path'], diskname, snapshot)):
        error_print(209, "virsh disk snapshot %s is not in volume %s" % (snapshot, diskname))


def check_virsh_disk_size(pool, vol, size):
    if get_volume_size(pool, vol) >= int(size):
        error_print(213, "new disk size must larger than the old size.")


def createPoolParser(args):
    if args.content is None:
        error_print(100, "less arg, content must be set")
    if args.content not in ["vmd", "vmdi", "iso"]:
        error_print(100, "less arg, content just can be vmd, vmdi, iso")

    execute('createPool', args)


def deletePoolParser(args):
    execute('deletePool', args)


def startPoolParser(args):
    execute('startPool', args)


def autoStartPoolParser(args):
    execute('autoStartPool', args)


def stopPoolParser(args):
    execute('stopPool', args)


def showPoolParser(args):
    execute('showPool', args)


def createDiskParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    pool = pool_info['poolname']
    if args.format is None:
        error_print(100, "less arg, format must be set")
    check_virsh_disk_exist(pool, args.vol)

    check_pool_active(pool_info)
    execute('createDisk', args)


def deleteDiskParser(args):
    try:
        helper = K8sHelper("VirtualMachineDisk")
        disk_info = helper.get_data(args.vol, "volume")
        if disk_info is None:
            helper.delete(args.vol)
            success_print("delete disk %s successful." % args.vol, {})
    except ExecuteException as e:
        error_print(400, e.message)
    pool_info = get_pool_info_from_k8s(args.pool)
    pool = pool_info['poolname']
    check_pool_active(pool_info)
    check_virsh_disk_not_exist(pool, args.vol)
    execute('deleteDisk', args)


def resizeDiskParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    pool = pool_info['poolname']
    check_pool_active(pool_info)
    check_virsh_disk_not_exist(pool, args.vol)
    check_virsh_disk_size(pool, args.vol, args.capacity)

    execute('resizeDisk', args)


def cloneDiskParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    # pool = pool_info['poolname']
    try:
        disk_info = get_vol_info_from_k8s(args.newname)
        error_print(500, "vol %s has exist in k8s." % args.newname)
    except ExecuteException:
        pass

    check_pool_active(pool_info)
    # check_virsh_disk_not_exist(pool, args.vol)
    # check_virsh_disk_exist(pool, args.newname)

    execute('cloneDisk', args)


def registerDiskToK8sParser(args):
    execute('registerDiskToK8s', args)


def rebaseDiskSnapshotParser(args):
    execute('rebaseDiskSnapshot', args)


def showDiskParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)
    pool = pool_info['poolname']
    check_virsh_disk_not_exist(pool, args.vol)

    execute('showDisk', args)


def prepareDiskParser(args):
    execute('prepareDisk', args)


def releaseDiskParser(args):
    execute('releaseDisk', args)


def showDiskSnapshotParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)

    pool = pool_info['poolname']
    check_virsh_disk_snapshot_not_exist(pool, args.vol, args.name)

    execute('showDiskSnapshot', args)


def createExternalSnapshotParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)

    pool = pool_info['poolname']
    if args.format is None:
        error_print(100, "less arg, format must be set")
    check_virsh_disk_snapshot_exist(pool, args.vol, args.name)

    disk_dir = '%s/%s' % (get_pool_info(pool)['path'], args.vol)
    config_path = '%s/config.json' % disk_dir
    with open(config_path, "r") as f:
        config = load(f)
    if not os.path.isfile(config['current']):
        error_print(100, "can not find vol current %s." % config['current'])
    if os.path.isfile('%s/snapshots/%s' % (disk_dir, args.name)):
        error_print(100, "snapshot file has exist")

    execute('createExternalSnapshot', args)


def revertExternalSnapshotParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)

    pool = pool_info['poolname']
    if args.format is None:
        error_print(100, "less arg, format must be set")

    check_virsh_disk_snapshot_not_exist(pool, args.vol, args.name)

    disk_dir = '%s/%s' % (get_pool_info(pool)['path'], args.vol)
    config_path = '%s/config.json' % disk_dir
    with open(config_path, "r") as f:
        config = load(f)

    if not os.path.isfile(config['current']):
        error_print(100, "can not find current file")
    execute('revertExternalSnapshot', args)


def deleteExternalSnapshotParser(args):
    try:
        helper = K8sHelper("VirtualMachineDiskSnapshot")
        ss_info = helper.get_data(args.name, "volume")
        if ss_info is None:
            helper.delete(args.name)
            success_print("delete snapshot %s successful." % args.name, {})
    except ExecuteException as e:
        error_print(400, e.message)
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)

    pool = pool_info['poolname']
    check_virsh_disk_snapshot_not_exist(pool, args.vol, args.name)

    disk_dir = '%s/%s' % (get_pool_info(pool)['path'], args.vol)
    ss_path = '%s/snapshots/%s' % (disk_dir, args.name)
    if not os.path.isfile(ss_path):
        error_print(100, "snapshot file not exist")

    execute('deleteExternalSnapshot', args)


def updateDiskCurrentParser(args):
    for current in args.current:
        if not os.path.isfile(current):
            error_print(100, "disk current path %s not exists!" % current)

    execute('updateDiskCurrent', args)


def customizeParser(args):
    execute('customize', args)


def createDiskFromImageParser(args):
    pool_info = get_pool_info_from_k8s(args.targetPool)
    check_pool_active(pool_info)

    pool = pool_info['poolname']
    check_pool_active(pool_info)

    execute('createDiskFromImage', args)


def migrateParser(args):
    if not re.match('^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$', args.ip):
        error_print(100, "ip is not right")
    execute('migrate', args)


def migrateDiskParser(args):
    execute('migrateDisk', args)


def migrateVMDiskParser(args):
    execute('migrateVMDisk', args)


def changeDiskPoolParser(args):
    execute('changeDiskPool', args)


def modifyVMParser(args):
    execute('modifyVM', args)


def exportVMParser(args):
    try:
        execute('exportVM', args)
        vm_heler = K8sHelper('VirtualMachine')
        vm_heler.delete_lifecycle(args.domain)
    except Exception as e:
        raise e


def backupVMParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)
    try:
        execute('backupVM', args)
        vm_heler = K8sHelper('VirtualMachine')
        vm_heler.delete_lifecycle(args.domain)
    except Exception as e:
        raise e


def restoreVMParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)
    if args.target:
        pool_info = get_pool_info_from_k8s(args.target)
        check_pool_active(pool_info)
    execute('restoreVM', args)


def backupDiskParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)
    execute('backupDisk', args)


def restoreDiskParser(args):
    pool_info = get_pool_info_from_k8s(args.pool)
    check_pool_active(pool_info)
    if args.target:
        pool_info = get_pool_info_from_k8s(args.target)
        check_pool_active(pool_info)
    execute('restoreDisk', args)


def showDiskPoolParser(args):
    execute('showDiskPool', args)


def deleteVMBackupParser(args):
    execute('deleteVMBackup', args)


def deleteVMDiskBackupParser(args):
    execute('deleteVMDiskBackup', args)


def deleteRemoteBackupParser(args):
    execute('deleteRemoteBackup', args)


def pullRemoteBackupParser(args):
    execute('pullRemoteBackup', args)


def pushBackupParser(args):
    # if args.vol:
    #     execute('pushVMDiskBackup', args)
    # else:
    #     execute('pushVMBackup', args)
    execute('pushVMBackup', args)


def createCloudInitUserDataImageParser(args):
    execute('createCloudInitUserDataImage', args)


def deleteCloudInitUserDataImageParser(args):
    execute('deleteCloudInitUserDataImage', args)


def updateOSParser(args):
    execute('updateOS', args)


def cleanBackupParser(args):
    execute('cleanBackup', args)


def cleanRemoteBackupParser(args):
    execute('cleanRemoteBackup', args)


def scanBackupParser(args):
    execute('scanBackup', args)


def deleteRemoteBackupServerParser(args):
    execute('deleteRemoteBackupServer', args)


# --------------------------- cmd line parser ---------------------------------------
parser = argparse.ArgumentParser(prog="kubesds-adm", description="All storage adaptation tools")

subparsers = parser.add_subparsers(help="sub-command help")

# -------------------- add createPool cmd ----------------------------------
parser_create_pool = subparsers.add_parser("createPool", help="createPool help")
parser_create_pool.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                help="storage pool type to use")

parser_create_pool.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="storage pool name to delete")

# localfs, nfs and glusterfs only, target will transfer to path in nfs and glusterfs
parser_create_pool.add_argument("--url", required=True, metavar="[URL]", type=str,
                                help="storage pool create location")

# set autostart
parser_create_pool.add_argument("--autostart", metavar="[AUTOSTART]", type=bool, nargs='?', const=True,
                                help="if autostart, pool will set autostart yes after create pool")

# set content
parser_create_pool.add_argument("--content", metavar="[CONTENT]", type=str,
                                help="pool content")

# nfs only
parser_create_pool.add_argument("--opt", metavar="[OPT]", type=str,
                                help="nfs require or nfs mount options")

# nfs and glusterfs only
parser_create_pool.add_argument("--uuid", metavar="[UUID]", type=str,
                                help="nfs or glusterfs poolname ")

# set default func
parser_create_pool.set_defaults(func=createPoolParser)

# -------------------- add deletePool cmd ----------------------------------
parser_delete_pool = subparsers.add_parser("deletePool", help="deletePool help")
parser_delete_pool.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                help="storage pool type to use")

parser_delete_pool.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="storage pool name to delete")
# set default func
parser_delete_pool.set_defaults(func=deletePoolParser)

# -------------------- add startPool cmd ----------------------------------
parser_start_pool = subparsers.add_parser("startPool", help="startPool help")
parser_start_pool.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                               help="storage pool type to use")

parser_start_pool.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                               help="storage pool name to delete")
# set default func
parser_start_pool.set_defaults(func=startPoolParser)

# -------------------- add autoStartPool cmd ----------------------------------
parser_autostart_pool = subparsers.add_parser("autoStartPool", help="autoStartPool help")
parser_autostart_pool.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                   help="storage pool type to use")

parser_autostart_pool.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                   help="storage pool name to autostart")
parser_autostart_pool.add_argument("--disable", metavar="[DISABLE]", type=bool, nargs='?', const=True,
                                   help="disable autostart")

# set default func
parser_autostart_pool.set_defaults(func=autoStartPoolParser)

# -------------------- add stopPool cmd ----------------------------------
parser_stop_pool = subparsers.add_parser("stopPool", help="stopPool help")
parser_stop_pool.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                              help="storage pool type to use")

parser_stop_pool.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                              help="storage pool name to stop")
# set default func
parser_stop_pool.set_defaults(func=stopPoolParser)

# -------------------- add showPool cmd ----------------------------------
parser_show_pool = subparsers.add_parser("showPool", help="showPool help")
parser_show_pool.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                              help="storage pool type to use")

parser_show_pool.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                              help="storage pool name to show")
# set default func
parser_show_pool.set_defaults(func=showPoolParser)

# -------------------- add createDisk cmd ----------------------------------
parser_create_disk = subparsers.add_parser("createDisk", help="createDisk help")
parser_create_disk.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                help="disk type to use")
parser_create_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="storage pool to use")

parser_create_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                help="volume name to use")

# will transfer to --size when type in nfs or glusterfs
parser_create_disk.add_argument("--capacity", required=True, metavar="[CAPACITY]", type=str,
                                help="capacity is the size of the volume to be created, as a scaled integer (see NOTES above), defaulting to bytes")
parser_create_disk.add_argument("--format", metavar="[raw|bochs|qcow|qcow2|vmdk|qed]", type=str,
                                help="format is used in file based storage pools to specify the volume file format to use; raw, bochs, qcow, qcow2, vmdk, qed.")

# set default func
parser_create_disk.set_defaults(func=createDiskParser)

# -------------------- add deleteDisk cmd ----------------------------------
parser_delete_disk = subparsers.add_parser("deleteDisk", help="deleteDisk help")
parser_delete_disk.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                help="storage pool type to use")
parser_delete_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="storage pool to use")
parser_delete_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                help="volume name to use")
# set default func
parser_delete_disk.set_defaults(func=deleteDiskParser)

# -------------------- add resizeDisk cmd ----------------------------------
parser_resize_disk = subparsers.add_parser("resizeDisk", help="resizeDisk help")
parser_resize_disk.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                help="storage pool type to use")
parser_resize_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="storage pool to use")
parser_resize_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                help="volume name to use")
parser_resize_disk.add_argument("--capacity", required=True, metavar="[CAPACITY]", type=str,
                                help="new volume capacity to use")
parser_resize_disk.add_argument("--vmname", metavar="[VMNAME]", type=str,
                                help="new volume capacity to use")
# set default func
parser_resize_disk.set_defaults(func=resizeDiskParser)

# -------------------- add cloneDisk cmd ----------------------------------
parser_clone_disk = subparsers.add_parser("cloneDisk", help="cloneDisk help")
parser_clone_disk.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                               help="storage pool type to use")
parser_clone_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                               help="storage pool to use")
parser_clone_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                               help="volume name to use")
parser_clone_disk.add_argument("--newname", required=True, metavar="[NEWNAME]", type=str,
                               help="new volume name to use")
parser_clone_disk.add_argument("--format", required=True, metavar="[FORMAT]", type=str,
                               help="format to use")
# set default func
parser_clone_disk.set_defaults(func=cloneDiskParser)

# -------------------- add registerDiskToK8s cmd ----------------------------------
parser_register_disk = subparsers.add_parser("registerDiskToK8s", help="register disk to k8s help")
parser_register_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                  help="storage pool to use")
parser_register_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                  help="volume name to use")
# set default func
parser_register_disk.set_defaults(func=registerDiskToK8sParser)

# -------------------- add rebaseDiskSnapshot cmd ----------------------------------
parser_rebase_snapshot = subparsers.add_parser("rebaseDiskSnapshot", help="rebase disk snapshot help")
parser_rebase_snapshot.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                    help="storage pool to use")
parser_rebase_snapshot.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                    help="volume name to use")
# set default func
parser_rebase_snapshot.set_defaults(func=rebaseDiskSnapshotParser)

# -------------------- add prepareDisk cmd ----------------------------------
parser_prepare_disk = subparsers.add_parser("prepareDisk", help="prepareDisk help")
parser_prepare_disk.add_argument("--domain", metavar="[DOMAIN]", type=str,
                                 help="storage pool to use")
parser_prepare_disk.add_argument("--vol", metavar="[VOL]", type=str,
                                 help="volume name to use")
parser_prepare_disk.add_argument("--path", metavar="[PATH]", type=str,
                                 help="volume uni to use")
# set default func
parser_prepare_disk.set_defaults(func=prepareDiskParser)

# -------------------- add releaseDisk cmd ----------------------------------
parser_release_disk = subparsers.add_parser("releaseDisk", help="releaseDisk help")
parser_release_disk.add_argument("--domain", metavar="[DOMAIN]", type=str,
                                 help="domain to use")
parser_release_disk.add_argument("--vol", metavar="[VOL]", type=str,
                                 help="volume name to use")
parser_release_disk.add_argument("--path", metavar="[PATH]", type=str,
                                 help="volume path to use")
# set default func
parser_release_disk.set_defaults(func=releaseDiskParser)

# -------------------- add showDisk cmd ----------------------------------
parser_show_disk = subparsers.add_parser("showDisk", help="showDisk help")
parser_show_disk.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                              help="storage pool type to use")
parser_show_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                              help="storage pool to use")
parser_show_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                              help="volume name to use")
# set default func
parser_show_disk.set_defaults(func=showDiskParser)

# -------------------- add showDiskSnapshot cmd ----------------------------------
parser_show_disk_snapshot = subparsers.add_parser("showDiskSnapshot", help="showDiskSnapshot help")
parser_show_disk_snapshot.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                       help="storage pool type to use")
parser_show_disk_snapshot.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                       help="storage pool to use")
parser_show_disk_snapshot.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                       help="volume name to use")
parser_show_disk_snapshot.add_argument("--name", required=True, metavar="[NAME]", type=str,
                                       help="volume snapshot name")
# set default func
parser_show_disk_snapshot.set_defaults(func=showDiskSnapshotParser)

# -------------------- add createExternalSnapshot cmd ----------------------------------
parser_create_ess = subparsers.add_parser("createExternalSnapshot", help="createExternalSnapshot help")
parser_create_ess.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                               help="storage pool type to use")
parser_create_ess.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                               help="storage pool to use")
parser_create_ess.add_argument("--name", required=True, metavar="[NAME]", type=str,
                               help="volume snapshot name to use")
parser_create_ess.add_argument("--format", required=True, metavar="[FORMAT]", type=str,
                               help="disk format to use")
parser_create_ess.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                               help="disk current file to use")
parser_create_ess.add_argument("--domain", metavar="[domain]", type=str,
                               help="domain")
# set default func
parser_create_ess.set_defaults(func=createExternalSnapshotParser)

# -------------------- add revertExternalSnapshot cmd ----------------------------------
parser_revert_ess = subparsers.add_parser("revertExternalSnapshot", help="revertExternalSnapshot help")
parser_revert_ess.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                               help="storage pool type to use")
parser_revert_ess.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                               help="storage pool to use")
parser_revert_ess.add_argument("--name", required=True, metavar="[NAME]", type=str,
                               help="volume snapshot name to use")
parser_revert_ess.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                               help="disk current file to use")
parser_revert_ess.add_argument("--format", required=True, metavar="[FORMAT]", type=str,
                               help="disk format to use")
parser_revert_ess.add_argument("--domain", metavar="[domain]", type=str,
                               help="domain")
# set default func
parser_revert_ess.set_defaults(func=revertExternalSnapshotParser)

# -------------------- add deleteExternalSnapshot cmd ----------------------------------
parser_delete_ess = subparsers.add_parser("deleteExternalSnapshot", help="deleteExternalSnapshot help")
parser_delete_ess.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                               help="storage pool type to use")
parser_delete_ess.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                               help="storage pool to use")
parser_delete_ess.add_argument("--name", required=True, metavar="[NAME]", type=str,
                               help="volume snapshot name to use")
parser_delete_ess.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                               help="disk current file to use")
parser_delete_ess.add_argument("--domain", metavar="[domain]", type=str,
                               help="domain")
# set default func
parser_delete_ess.set_defaults(func=deleteExternalSnapshotParser)

# -------------------- add updateDiskCurrent cmd ----------------------------------
parser_upodate_current = subparsers.add_parser("updateDiskCurrent", help="updateDiskCurrent help")
parser_upodate_current.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                    help="storage pool type to use")
parser_upodate_current.add_argument("--current", required=True, metavar="[CURRENT]", type=str, nargs='*',
                                    help="disk current file to use")
# set default func
parser_upodate_current.set_defaults(func=updateDiskCurrentParser)

# -------------------- add customize cmd ----------------------------------
parser_customize = subparsers.add_parser("customize", help="customize help")
parser_customize.add_argument("--add", required=True, metavar="[ADD]", type=str,
                              help="storage pool type to use")
parser_customize.add_argument("--user", required=False, metavar="[USER]", type=str,
                              help="disk current file to use")
parser_customize.add_argument("--password", required=False, metavar="[PASSWORD]", type=str,
                              help="disk current file to use")
parser_customize.add_argument("--ssh_inject", required=False, metavar="[SSH_INJECT]", type=str,
                              help="disk ssh-inject")
# set default func
parser_customize.set_defaults(func=customizeParser)

# -------------------- add createDiskFromImage cmd ----------------------------------
parser_create_disk_from_image = subparsers.add_parser("createDiskFromImage", help="createDiskFromImage help")
parser_create_disk_from_image.add_argument("--type", required=True, metavar="[localfs|nfs|glusterfs]", type=str,
                                           help="storage pool type to use")
parser_create_disk_from_image.add_argument("--name", required=True, metavar="[name]", type=str,
                                           help="new disk name to use")
parser_create_disk_from_image.add_argument("--targetPool", required=True, metavar="[targetPool]", type=str,
                                           help="storage pool to use")
parser_create_disk_from_image.add_argument("--source", required=True, metavar="[source]", type=str,
                                           help="disk source to use")
parser_create_disk_from_image.add_argument("--full_copy", metavar="[full_copy]", type=bool, nargs='?', const=True,
                                           help="if full_copy, new disk will be created by snapshot")
# set default func
parser_create_disk_from_image.set_defaults(func=createDiskFromImageParser)

# -------------------- add migrate cmd ----------------------------------
parser_migrate = subparsers.add_parser("migrate", help="migrate help")
parser_migrate.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                            help="vm domain to migrate")
parser_migrate.add_argument("--ip", required=True, metavar="[IP]", type=str,
                            help="storage pool type to use")
parser_migrate.add_argument("--offline", metavar="[OFFLINE]", type=bool, nargs='?', const=True,
                            help="support migrate offline")
# set default func
parser_migrate.set_defaults(func=migrateParser)

# -------------------- add migrateDisk cmd ----------------------------------
parser_migrate_disk = subparsers.add_parser("migrateDisk", help="migrate disk help")
parser_migrate_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                 help="vol to migrate")
parser_migrate_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                 help="target storage pool to use")
# set default func
parser_migrate_disk.set_defaults(func=migrateDiskParser)

# -------------------- add migrateVMDisk cmd ----------------------------------
parser_migrate_vm_disk = subparsers.add_parser("migrateVMDisk", help="migrateVMDisk help")
parser_migrate_vm_disk.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                    help="vm domain to migrate")
parser_migrate_vm_disk.add_argument("--ip", required=True, metavar="[IP]", type=str,
                                    help="storage pool type to use")
parser_migrate_vm_disk.add_argument("--migratedisks", required=True, metavar="[MIGRATEDISKS]", type=str,
                                    help="vol opt to migrate")
# parser_migrate_vm_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
#                             help="target storage pool to use")
# set default func
parser_migrate_vm_disk.set_defaults(func=migrateVMDiskParser)

# -------------------- add restoreDisk cmd ----------------------------------
parser_change_disk_pool = subparsers.add_parser("changeDiskPool", help="changeDiskPool help")
parser_change_disk_pool.add_argument("--xml", required=True, metavar="[XML]", type=str,
                                     help="vm disk to backup")
# set default func
parser_change_disk_pool.set_defaults(func=changeDiskPoolParser)

# -------------------- add migrateVMDisk cmd ----------------------------------
parser_modify_vm = subparsers.add_parser("modifyVM", help="modifyVM help")
parser_modify_vm.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                              help="vm domain to migrate")
# parser_migrate_vm_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
#                             help="target storage pool to use")
# set default func
parser_modify_vm.set_defaults(func=modifyVMParser)

# -------------------- add exportVM cmd ----------------------------------
parser_export_vm = subparsers.add_parser("exportVM", help="exportVM help")
parser_export_vm.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                              help="vm domain to export")
parser_export_vm.add_argument("--path", required=True, metavar="[PATH]", type=str,
                              help="vm disk file to export")
# set default func
parser_export_vm.set_defaults(func=exportVMParser)

# -------------------- add backupVM cmd ----------------------------------
parser_backup_vm = subparsers.add_parser("backupVM", help="backupVM help")
parser_backup_vm.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                              help="vm domain to export")
parser_backup_vm.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                              help="vm domain backup pool, must shared type, like nfs")
parser_backup_vm.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                              help="backup version id")
parser_backup_vm.add_argument("--all", required=False, metavar="[ALL]", type=bool, nargs='?', const=True,
                              help="all vm disk")
parser_backup_vm.add_argument("--full", required=False, metavar="[FULL]", type=bool, nargs='?', const=True,
                              help="full backup")
parser_backup_vm.add_argument("--remote", required=False, metavar="[REMOTE]", type=str,
                              help="remote server host.")
parser_backup_vm.add_argument("--port", required=False, metavar="[PORT]", type=str,
                              help="remote server port.")
parser_backup_vm.add_argument("--username", required=False, metavar="[REMOTE]", type=str,
                              help="remote server username.")
parser_backup_vm.add_argument("--password", required=False, metavar="[REMOTE]", type=str,
                              help="remote server password.")
# set default func
parser_backup_vm.set_defaults(func=backupVMParser)

# -------------------- add restoreVM cmd ----------------------------------
parser_restore_vm = subparsers.add_parser("restoreVM", help="restoreVM help")
parser_restore_vm.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                               help="vm domain to export")
parser_restore_vm.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                               help="vm domain backup pool, must shared type, like nfs")
parser_restore_vm.add_argument("--all", required=False, metavar="[ALL]", type=bool, nargs='?', const=True,
                               help="all vm disk")
parser_restore_vm.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                               help="backup version id")
parser_restore_vm.add_argument("--newname", required=False, metavar="[NEWNAME]", type=str,
                               help="name when create a new domain")
parser_restore_vm.add_argument("--target", required=False, metavar="[TARGET]", type=str,
                               help="use target pool to create a new domain")
# set default func
parser_restore_vm.set_defaults(func=restoreVMParser)

# -------------------- add backupDisk cmd ----------------------------------
parser_backup_disk = subparsers.add_parser("backupDisk", help="backupDisk help")
parser_backup_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                help="vm disk to backup")
parser_backup_disk.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                help="vm domain to export")
parser_backup_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="vm domain backup pool, must shared type, like nfs")
parser_backup_disk.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                help="backup version id")
parser_backup_disk.add_argument("--full", required=False, metavar="[FULL]", type=bool, nargs='?', const=True,
                                help="full backup")
parser_backup_disk.add_argument("--remote", required=False, metavar="[REMOTE]", type=str,
                                help="remote server host.")
parser_backup_disk.add_argument("--port", required=False, metavar="[PORT]", type=str,
                                help="remote server port.")
parser_backup_disk.add_argument("--username", required=False, metavar="[REMOTE]", type=str,
                                help="remote server username.")
parser_backup_disk.add_argument("--password", required=False, metavar="[REMOTE]", type=str,
                                help="remote server password.")
# set default func
parser_backup_disk.set_defaults(func=backupDiskParser)

# -------------------- add restoreDisk cmd ----------------------------------
parser_restore_disk = subparsers.add_parser("restoreDisk", help="restoreDisk help")
parser_restore_disk.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                 help="vm disk to backup")
parser_restore_disk.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                 help="vm domain to export")
parser_restore_disk.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                 help="vm domain backup pool, must shared type, like nfs")
parser_restore_disk.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                 help="backup version id")
parser_restore_disk.add_argument("--newname", required=False, metavar="[NEWNAME]", type=str,
                                 help="name when create a new domain")
parser_restore_disk.add_argument("--target", required=False, metavar="[TARGET]", type=str,
                                 help="use target pool to create a new domain")
parser_restore_disk.add_argument("--targetDomain", required=False, metavar="[TARGETDOMAIN]", type=str,
                                 help="target domain to attach disk")
# set default func
parser_restore_disk.set_defaults(func=restoreDiskParser)

# -------------------- add showDiskPool cmd ----------------------------------
parser_show_disk_pool = subparsers.add_parser("showDiskPool", help="showDiskPool help")
parser_show_disk_pool.add_argument("--path", required=True, metavar="[PATH]", type=str,
                                   help="vm disk path")
# set default func
parser_show_disk_pool.set_defaults(func=showDiskPoolParser)

# -------------------- add deleteVMBackup cmd ----------------------------------
parser_delete_vm_backup = subparsers.add_parser("deleteVMBackup", help="restoreVM help")
parser_delete_vm_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                     help="vm domain to export")
parser_delete_vm_backup.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                     help="vm domain backup pool, must shared type, like nfs")
parser_delete_vm_backup.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                     help="backup version id")
# set default func
parser_delete_vm_backup.set_defaults(func=deleteVMBackupParser)

# -------------------- add deleteVMDiskBackup cmd ----------------------------------
parser_delete_vm_disk_backup = subparsers.add_parser("deleteVMDiskBackup", help="restoreVM help")
parser_delete_vm_disk_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                          help="vm domain to export")
parser_delete_vm_disk_backup.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                          help="vm disk to backup")
parser_delete_vm_disk_backup.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                          help="vm domain backup pool, must shared type, like nfs")
parser_delete_vm_disk_backup.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                          help="backup version id")
# set default func
parser_delete_vm_disk_backup.set_defaults(func=deleteVMDiskBackupParser)

# -------------------- add deleteRemoteBackup cmd ----------------------------------
parser_delete_remote_backup = subparsers.add_parser("deleteRemoteBackup", help="restoreVM help")
parser_delete_remote_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                         help="vm domain to export")
parser_delete_remote_backup.add_argument("--vol", required=False, metavar="[VOL]", type=str,
                                         help="vm disk to backup")
parser_delete_remote_backup.add_argument("--pool", required=False, metavar="[POOL]", type=str,
                                         help="vm pool to backup")
parser_delete_remote_backup.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                         help="backup version id")
parser_delete_remote_backup.add_argument("--remote", required=True, metavar="[REMOTE]", type=str,
                                         help="remote server host.")
parser_delete_remote_backup.add_argument("--port", required=True, metavar="[PORT]", type=str,
                                         help="remote server port.")
parser_delete_remote_backup.add_argument("--username", required=True, metavar="[USERNAME]", type=str,
                                         help="remote server username.")
parser_delete_remote_backup.add_argument("--password", required=True, metavar="[PASSWORD]", type=str,
                                         help="remote server password.")
# set default func
parser_delete_remote_backup.set_defaults(func=deleteRemoteBackupParser)

# -------------------- add pullRemoteBackup cmd ----------------------------------
parser_pull_remote_backup = subparsers.add_parser("pullRemoteBackup", help="pullRemoteBackup help")
parser_pull_remote_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                       help="vm domain to export")
parser_pull_remote_backup.add_argument("--vol", required=False, metavar="[VOL]", type=str,
                                       help="vm disk to backup")
parser_pull_remote_backup.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                       help="backup to store")
parser_pull_remote_backup.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                       help="backup version id")
parser_pull_remote_backup.add_argument("--remote", required=True, metavar="[REMOTE]", type=str,
                                       help="remote server host.")
parser_pull_remote_backup.add_argument("--port", required=True, metavar="[PORT]", type=str,
                                       help="remote server port.")
parser_pull_remote_backup.add_argument("--username", required=True, metavar="[USERNAME]", type=str,
                                       help="remote server username.")
parser_pull_remote_backup.add_argument("--password", required=True, metavar="[PASSWORD]", type=str,
                                       help="remote server password.")
# set default func
parser_pull_remote_backup.set_defaults(func=pullRemoteBackupParser)

# -------------------- add pushBackup cmd ----------------------------------
parser_push_backup = subparsers.add_parser("pushBackup", help="pushBackup help")
parser_push_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                help="vm domain to export")
parser_push_backup.add_argument("--vol", required=False, metavar="[VOL]", type=str,
                                help="vm disk to backup")
parser_push_backup.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="backup to store")
parser_push_backup.add_argument("--version", required=True, metavar="[VERSION]", type=str,
                                help="backup version id")
parser_push_backup.add_argument("--remote", required=True, metavar="[REMOTE]", type=str,
                                help="remote server host.")
parser_push_backup.add_argument("--port", required=True, metavar="[PORT]", type=str,
                                help="remote server port.")
parser_push_backup.add_argument("--username", required=True, metavar="[USERNAME]", type=str,
                                help="remote server username.")
parser_push_backup.add_argument("--password", required=True, metavar="[PASSWORD]", type=str,
                                help="remote server password.")
# set default func
parser_push_backup.set_defaults(func=pushBackupParser)

# -------------------- add createCloudInitUserDataImage cmd ----------------------------------
parser_create_cloud_init = subparsers.add_parser("createCloudInitUserDataImage",
                                                 help="createCloudInitUserDataImage help")
parser_create_cloud_init.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                      help="backup to store")
parser_create_cloud_init.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                      help="vol")
parser_create_cloud_init.add_argument("--userData", required=False, metavar="[USERDATA]", type=str,
                                      help="userData")
# set default func
parser_create_cloud_init.set_defaults(func=createCloudInitUserDataImageParser)

# -------------------- add createCloudInitUserDataImage cmd ----------------------------------
parser_delete_cloud_init = subparsers.add_parser("deleteCloudInitUserDataImage",
                                                 help="deleteCloudInitUserDataImage help")
parser_delete_cloud_init.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                      help="backup to store")
parser_delete_cloud_init.add_argument("--vol", required=True, metavar="[VOL]", type=str,
                                      help="vol")
# set default func
parser_delete_cloud_init.set_defaults(func=deleteCloudInitUserDataImageParser)

# -------------------- add createCloudInitUserDataImage cmd ----------------------------------
parser_update_os = subparsers.add_parser("updateOS", help="deleteCloudInitUserDataImage help")
parser_update_os.add_argument("--domain", required=True, metavar="[POOL]", type=str,
                              help="backup to store")
parser_update_os.add_argument("--source", required=True, metavar="[POOL]", type=str,
                              help="backup to store")
parser_update_os.add_argument("--target", required=True, metavar="[VOL]", type=str,
                              help="vol")
# set default func
parser_update_os.set_defaults(func=updateOSParser)

# -------------------- add cleanBackup cmd ----------------------------------
parser_clean_backup = subparsers.add_parser("cleanBackup", help="cleanBackup help")
parser_clean_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                 help="vm domain to export")
parser_clean_backup.add_argument("--vol", required=False, metavar="[VOL]", type=str,
                                 help="vm disk to backup")
parser_clean_backup.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                 help="backup to store")
parser_clean_backup.add_argument("--version", required=False, metavar="[VERSION]", type=str,
                                 help="backup version id")
parser_clean_backup.add_argument("--all", required=False, metavar="[ALL]", type=bool, nargs='?', const=True,
                                 help="full clean")
# set default func
parser_clean_backup.set_defaults(func=cleanBackupParser)

# -------------------- add cleanBackup cmd ----------------------------------
parser_clean_remote_backup = subparsers.add_parser("cleanRemoteBackup", help="cleanRemoteBackup help")
parser_clean_remote_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                        help="vm domain to export")
parser_clean_remote_backup.add_argument("--pool", required=False, metavar="[POOL]", type=str,
                                        help="vm pool to backup")
parser_clean_remote_backup.add_argument("--vol", required=False, metavar="[VOL]", type=str,
                                        help="vm disk to backup")
parser_clean_remote_backup.add_argument("--version", required=False, metavar="[VERSION]", type=str,
                                        help="backup version id")
parser_clean_remote_backup.add_argument("--all", required=False, metavar="[ALL]", type=bool, nargs='?', const=True,
                                        help="full clean")
parser_clean_remote_backup.add_argument("--remote", required=True, metavar="[REMOTE]", type=str,
                                        help="remote server host.")
parser_clean_remote_backup.add_argument("--port", required=True, metavar="[PORT]", type=str,
                                        help="remote server port.")
parser_clean_remote_backup.add_argument("--username", required=True, metavar="[USERNAME]", type=str,
                                        help="remote server username.")
parser_clean_remote_backup.add_argument("--password", required=True, metavar="[PASSWORD]", type=str,
                                        help="remote server password.")
# set default func
parser_clean_remote_backup.set_defaults(func=cleanRemoteBackupParser)

# -------------------- add scanBackup cmd ----------------------------------
parser_scan_backup = subparsers.add_parser("scanBackup", help="scanBackup help")
parser_scan_backup.add_argument("--domain", required=True, metavar="[DOMAIN]", type=str,
                                help="vm domain to export")
parser_scan_backup.add_argument("--vol", required=False, metavar="[VOL]", type=str,
                                help="vm disk to backup")
parser_scan_backup.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                help="backup to store")
# set default func
parser_scan_backup.set_defaults(func=scanBackupParser)

# -------------------- add deleteRemoteBackupServer cmd ----------------------------------
parser_delete_remote_backup_server = subparsers.add_parser("deleteRemoteBackupServer",
                                                           help="deleteRemoteBackupServer help")
parser_delete_remote_backup_server.add_argument("--remote", required=True, metavar="[REMOTE]", type=str,
                                                help="remote server host.")
parser_delete_remote_backup_server.add_argument("--port", required=True, metavar="[PORT]", type=str,
                                                help="remote server port.")
parser_delete_remote_backup_server.add_argument("--username", required=True, metavar="[USERNAME]", type=str,
                                                help="remote server username.")
parser_delete_remote_backup_server.add_argument("--password", required=True, metavar="[PASSWORD]", type=str,
                                                help="remote server password.")
parser_delete_remote_backup_server.add_argument("--pool", required=True, metavar="[POOL]", type=str,
                                                help="storage pool to use")
# set default func
parser_delete_remote_backup_server.set_defaults(func=deleteRemoteBackupServerParser)




test_args = []

dir1 = parser.parse_args(["createPool", "--type", "localfs", "--pool", "pooldir", "--url", "/mnt/localfs/pooldir", "--content", "vmd", "--uuid", "07098ca5fd174fccafee76b0d7fccde4"])
dir2 = parser.parse_args(["createDisk", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--capacity", "1073741824", "--format", "qcow2"])
dir3 = parser.parse_args(["prepareDisk", "--path", "/var/lib/libvirt/cstor/07098ca5fd174fccafee76b0d7fccde4/07098ca5fd174fccafee76b0d7fccde4/diskdir/diskdir"])
dir4 = parser.parse_args(["createExternalSnapshot", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--name", "diskdir.1", "--format", "qcow2"])
dir5 = parser.parse_args(["createExternalSnapshot", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--name", "diskdir.2", "--format", "qcow2"])
dir6 = parser.parse_args(["revertExternalSnapshot", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--name", "diskdir.1", "--format", "qcow2"])
dir7 = parser.parse_args(["createExternalSnapshot", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--name", "diskdir.3", "--format", "qcow2"])
dir8 = parser.parse_args(["deleteExternalSnapshot", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--name", "diskdir.1"])
dir9 = parser.parse_args(["resizeDisk", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--capacity", "2147483648"])
dir10 = parser.parse_args(["cloneDisk", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir", "--newname", "diskdirclone", "--format", "qcow2"])
dir11 = parser.parse_args(["releaseDisk", "--vol", "diskdir"])
dir12 = parser.parse_args(["deleteDisk", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdirclone"])
dir13 = parser.parse_args(["deleteDisk", "--type", "localfs", "--pool", "pooldir", "--vol", "diskdir"])
dir14 = parser.parse_args(["stopPool", "--type", "localfs", "--pool", "pooldir"])
dir15 = parser.parse_args(["deletePool", "--type", "localfs", "--pool", "pooldir"])

nfs1 = parser.parse_args(["createPool", "--type", "nfs", "--pool", "poolnfs", "--url", "133.133.135.30:/home/nfs", "--opt", "nolock", "--content", "vmd", "--uuid", "07098ca5fd174fccafee76b0d7fccde4"])
nfs2 = parser.parse_args(["createDisk", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--capacity", "1073741824", "--format", "qcow2"])
nfs3 = parser.parse_args(["prepareDisk", "--path", "/var/lib/libvirt/cstor/07098ca5fd174fccafee76b0d7fccde4/07098ca5fd174fccafee76b0d7fccde4/disknfs/disknfs"])
nfs4 = parser.parse_args(["createExternalSnapshot", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--name", "disknfs.1", "--format", "qcow2"])
nfs5 = parser.parse_args(["createExternalSnapshot", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--name", "disknfs.2", "--format", "qcow2"])
nfs6 = parser.parse_args(["revertExternalSnapshot", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--name", "disknfs.1", "--format", "qcow2"])
nfs7 = parser.parse_args(["createExternalSnapshot", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--name", "disknfs.3", "--format", "qcow2"])
nfs8 = parser.parse_args(["deleteExternalSnapshot", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--name", "disknfs.1"])
nfs9 = parser.parse_args(["resizeDisk", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--capacity", "2147483648"])
nfs10 = parser.parse_args(["cloneDisk", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs", "--newname", "disknfsclone", "--format", "qcow2"])
nfs11 = parser.parse_args(["deleteDisk", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfsclone"])
nfs12 = parser.parse_args(["releaseDisk", "--vol", "disknfs"])
nfs13 = parser.parse_args(["deleteDisk", "--type", "nfs", "--pool", "poolnfs", "--vol", "disknfs"])
nfs14 = parser.parse_args(["stopPool", "--type", "nfs", "--pool", "poolnfs"])
nfs15 = parser.parse_args(["deletePool", "--type", "nfs", "--pool", "poolnfs"])

gfs1 = parser.parse_args(["createPool", "--type", "glusterfs", "--pool", "poolglusterfs", "--url", "192.168.3.100:nfsvol", "--content", "vmd", "--uuid", "07098ca5fd174fccafee76b0d7fccde4"])
gfs2 = parser.parse_args(["createDisk", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--capacity", "1073741824", "--format", "qcow2"])
gfs3 = parser.parse_args(["prepareDisk", "--path", "/var/lib/libvirt/cstor/abc/07098ca5fd174fccafee76b0d7fccde4/diskglusterfs/diskglusterfs"])
gfs4 = parser.parse_args(["createExternalSnapshot", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--name", "diskglusterfs.1", "--format", "qcow2"])
gfs5 = parser.parse_args(["createExternalSnapshot", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--name", "diskglusterfs.2", "--format", "qcow2"])
gfs6 = parser.parse_args(["revertExternalSnapshot", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--name", "diskglusterfs.1", "--format", "qcow2"])
gfs7 = parser.parse_args(["createExternalSnapshot", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--name", "diskglusterfs.3", "--format", "qcow2"])
gfs8 = parser.parse_args(["deleteExternalSnapshot", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--name", "diskglusterfs.1"])
gfs9 = parser.parse_args(["resizeDisk", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--capacity", "2147483648"])
gfs10 = parser.parse_args(["cloneDisk", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs", "--newname", "diskglusterfsclone", "--format", "qcow2"])
gfs11 = parser.parse_args(["deleteDisk", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfsclone"])
gfs12 = parser.parse_args(["releaseDisk", "--vol", "diskglusterfs"])
gfs13 = parser.parse_args(["deleteDisk", "--type", "glusterfs", "--pool", "poolglusterfs", "--vol", "diskglusterfs"])
gfs14 = parser.parse_args(["stopPool", "--type", "glusterfs", "--pool", "poolglusterfs"])
gfs15 = parser.parse_args(["deletePool", "--type", "glusterfs", "--pool", "poolglusterfs"])

# test_args.append(dir1)
# test_args.append(dir2)
# test_args.append(dir3)
# test_args.append(dir4)
# test_args.append(dir5)
# test_args.append(dir6)
# test_args.append(dir7)
# test_args.append(dir8)
# test_args.append(dir9)
# test_args.append(dir10)
# test_args.append(dir11)
# test_args.append(dir12)
# test_args.append(dir13)
# test_args.append(dir14)
# test_args.append(dir15)


test_args.append(nfs1)
test_args.append(nfs2)
test_args.append(nfs3)
test_args.append(nfs4)
test_args.append(nfs5)
test_args.append(nfs6)
test_args.append(nfs7)
test_args.append(nfs8)
test_args.append(nfs9)
test_args.append(nfs10)
test_args.append(nfs11)
test_args.append(nfs12)
test_args.append(nfs13)
test_args.append(nfs14)
test_args.append(nfs15)

# test_args.append(gfs1)
# test_args.append(gfs2)
# test_args.append(gfs3)
# test_args.append(gfs4)
# test_args.append(gfs5)
# test_args.append(gfs6)
# test_args.append(gfs7)
# test_args.append(gfs8)
# test_args.append(gfs9)
# test_args.append(gfs10)
# test_args.append(gfs11)
# test_args.append(gfs12)
# test_args.append(gfs13)
# test_args.append(gfs14)
# test_args.append(gfs15)


for args in test_args:
    try:
        args.func(args)
    except Exception:
        print(traceback.format_exc())
        logger.debug(traceback.format_exc())
