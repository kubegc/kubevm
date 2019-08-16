#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import sys
import os
import json

uusvolcli = '/usr/lib/uraid/scripts/vols/vol.sh'
LOCAL_FS = 'localfs'
NFS = 'nfs'
GLUSTERFS = 'glusterfs'
UUS = 'uus'

CSTOR_DIR = '/etc/sysconfig/cstor'
CSTOR_POOL = '/etc/sysconfig/cstor/pool'

    
def main(*argv):
    parser = argparse.ArgumentParser(prog=argv[0])

    sub_parser = parser.add_subparsers(title='subcommands' ,description='subcommands help use subcommands -h', help='')
    ###########################
    devlist_parser = sub_parser.add_parser('dev-list',help='list storage phy-pool')
    devlist_parser.add_argument('--type', required=True, help='localfs/nfs/glusterfs/uus')
    devlist_parser.add_argument('--url', required=True, help='localfs:available or all \n nfs:ip/sharename \nglusterfs:ip/volname \nuus:ip:port/poolname')
    devlist_parser.set_defaults(func=dev_list)
    
    pooladd_local_parser = sub_parser.add_parser('pooladd-localfs',help='add local storage pool')
    pooladd_local_parser.add_argument('--poolname', required=True, help='poolname')
    pooladd_local_parser.add_argument('--url', required=True, help='url from dev-list')
    pooladd_local_parser.set_defaults(func=pooladd_local)
    
    pooladd_nfs_parser = sub_parser.add_parser('pooladd-nfs',help='add nfs storage pool')
    pooladd_nfs_parser.add_argument('--poolname', required=True, help='poolname')
    pooladd_nfs_parser.add_argument('--url', required=True, help='url from dev-list')
    pooladd_nfs_parser.add_argument('--path', required=True, help='mount path')
    pooladd_nfs_parser.add_argument('--opt', required=False, help='mount option')
    pooladd_nfs_parser.set_defaults(func=pooladd_nfs)
    
    pooladd_glusterfs_parser = sub_parser.add_parser('pooladd-glusterfs',help='add glusterfs storage pool')
    pooladd_glusterfs_parser.add_argument('--poolname', required=True, help='poolname')
    pooladd_glusterfs_parser.add_argument('--url', required=True, help='url from dev-list')
    pooladd_glusterfs_parser.add_argument('--path', required=True, help='mount path')
    pooladd_glusterfs_parser.add_argument('--opt', required=False, help='mount option')
    pooladd_glusterfs_parser.set_defaults(func=pooladd_glusterfs)
    
    pooladd_uus_parser = sub_parser.add_parser('pooladd-uus',help='add uus storage pool')
    pooladd_uus_parser.add_argument('--poolname', required=True, help='poolname')
    pooladd_uus_parser.add_argument('--url', required=True, help='url from dev-list')
    pooladd_uus_parser.add_argument('--user', required=True, help='username')
    pooladd_uus_parser.add_argument('--pwd', required=True, help='password')
    pooladd_uus_parser.set_defaults(func=pooladd_uus)
    
    poollist_parser = sub_parser.add_parser('pool-list',help='list storage pool')
    poollist_parser.set_defaults(func=pool_list)
    
    poolshow_parser = sub_parser.add_parser('pool-show',help='show storage pool')
    poolshow_parser.add_argument('--poolname', required=True, help='poolname')
    poolshow_parser.set_defaults(func=pool_show)
    
    poolremove_parser = sub_parser.add_parser('pool-remove',help='remove storage pool')
    poolremove_parser.add_argument('--poolname', required=True, help='poolname')
    poolremove_parser.set_defaults(func=pool_remove)
    
    ##########################
    
    ##############create##################
    create_parser = sub_parser.add_parser('vdisk-create',help='create volume')
    create_parser.add_argument('--poolname', required=True, help='storage pool')
    create_parser.add_argument('--name', required=True, help='volume name')
    create_parser.add_argument('--size', required=True, help='volume size GB')
    #create_parser.add_argument('--type', required=False, help='default qcow2, raw, block')
    create_parser.set_defaults(func=create_volume)
    
    ##############remove##################
    remove_parser = sub_parser.add_parser('vdisk-remove', help='remove volume')
    remove_parser.add_argument('--poolname', required=True, help='storage pool')
    remove_parser.add_argument('--name', required=True, help='volume name') 
    remove_parser.set_defaults(func=remove_volume)
    
    ################show###################
    show_parser = sub_parser.add_parser('vdisk-show', help='show volume info')
    show_parser.add_argument('--poolname', required=True, help='storage pool')
    show_parser.add_argument('--name', required=True, help='volume name')   
    show_parser.set_defaults(func=show_volume)
    
    ################expand###################
    expand_parser = sub_parser.add_parser('vdisk-expand',help='expand volume to new size GB')
    expand_parser.add_argument('--poolname', required=True, help='storage pool')
    expand_parser.add_argument('--name', required=True, help='volume name')
    expand_parser.add_argument('--size', required=True, help='volume new size GB')
    
    expand_parser.set_defaults(func=expand_volume)
    
    ################add snapshot###################
    add_ss_parser = sub_parser.add_parser('vdisk-add-ss',help='create volume snapshot')
    add_ss_parser.add_argument('--poolname', required=True, help='storage pool')
    add_ss_parser.add_argument('--name', required=True, help='volume name')
    add_ss_parser.add_argument('--sname', required=True, help='snapshot name')  
    add_ss_parser.set_defaults(func=add_volume_snapshot)
    
    ################show snapshot###################
    show_ss_parser = sub_parser.add_parser('vdisk-show-ss',help='create volume snapshot')
    show_ss_parser.add_argument('--poolname', required=True, help='storage pool')
    show_ss_parser.add_argument('--name', required=True, help='volume name')
    show_ss_parser.add_argument('--sname', required=True, help='snapshot name')  
    show_ss_parser.set_defaults(func=show_volume_snapshot)
    
    ################recover snapshot###################
    recover_ss_parser = sub_parser.add_parser('vdisk-rr-ss',help='recover volume snapshot')
    recover_ss_parser.add_argument('--poolname', required=True, help='storage pool')
    recover_ss_parser.add_argument('--name', required=True, help='volume name')
    recover_ss_parser.add_argument('--sname', required=True, help='snapshot name')  
    recover_ss_parser.set_defaults(func=recover_volume_snapshot)
    
    ################remvoe snapshot###################
    rm_ss_parser = sub_parser.add_parser('vdisk-rm-ss',help='remove volume snapshot')
    rm_ss_parser.add_argument('--poolname', required=True, help='storage pool')
    rm_ss_parser.add_argument('--name', required=True, help='volume name')
    rm_ss_parser.add_argument('--sname', required=True, help='snapshot name')   
    rm_ss_parser.set_defaults(func=remove_volume_snapshot)
    
    ################clone##################
    clone_parser = sub_parser.add_parser('vdisk-clone',help='remove volume snapshot')
    clone_parser.add_argument('--poolname', required=True, help='storage pool')
    clone_parser.add_argument('--name', required=True, help='volume name')
    clone_parser.add_argument('--clonename', required=True, help='clone name')
    clone_parser.set_defaults(func=clone_volume)    
   
    
    ##############prepare vol##############
    prep_vol_parser = sub_parser.add_parser('vdisk-prepare',help='connect volume')
    prep_vol_parser.add_argument('--poolname', required=True, help='storage pool')
    prep_vol_parser.add_argument('--name', required=True, help='volume name')
    prep_vol_parser.add_argument('--sname', required=False, help='snapshot name')
    prep_vol_parser.set_defaults(func=prepare_volume)
    
    ##############attach vol##############
    #attach_vol_parser = sub_parser.add_parser('vdisk-attach',help='attach volume')
    #attach_vol_parser.add_argument('--poolname', required=True, help='storage pool')
    #attach_vol_parser.add_argument('--name', required=True, help='volume name')
    #attach_vol_parser.add_argument('--sname', required=False, help='snapshot name')
    #attach_vol_parser.add_argument('--vm', required=True, help='vm name')
    #attach_vol_parser.add_argument('--dev', required=False, help='dev name in vm')
    #attach_vol_parser.set_defaults(func=attach_volume)
    
    ##############detach vol##############
    #detach_vol_parser = sub_parser.add_parser('vdisk-detach',help='detach volume')
    #detach_vol_parser.add_argument('--poolname', required=True, help='storage pool')
    #detach_vol_parser.add_argument('--name', required=True, help='volume name')
    #detach_vol_parser.add_argument('--sname', required=False, help='snapshot name')
    #detach_vol_parser.add_argument('--vm', required=False, help='vm name')
    #detach_vol_parser.add_argument('--dev', required=False, help='dev name in vm')
    #detach_vol_parser.set_defaults(func=detach_volume)
    
    ##############release vol##############
    release_vol_parser = sub_parser.add_parser('vdisk-release',help='connect volume')
    release_vol_parser.add_argument('--poolname', required=True, help='storage pool')
    release_vol_parser.add_argument('--name', required=True, help='volume name')
    release_vol_parser.add_argument('--sname', required=False, help='snapshot name')
    release_vol_parser.set_defaults(func=release_volume)
    ##########################################################

    args = parser.parse_args()
    args.func(args)


def json_load_file(path, filename):
    fullname = '%s/%s' % (path, filename)
    if not path_exist(CSTOR_POOL):
        mkdir_p(CSTOR_POOL)
    if not path_exist(fullname):
        cmd = 'echo -n "{}"> %s' % fullname
        execcmd_str(cmd)
        
    load_dict = {}
    with open(fullname, 'r') as f:
        load_dict = json.load(f)
    return load_dict    

def json_dump_file(path, filename, new_dict):
    fullname = '%s/%s' % (path, filename)
    if not path_exist(CSTOR_POOL):
        mkdir_p(CSTOR_POOL)
        
    with open(fullname, "w") as f:
        json.dump(new_dict,f)
    return 0
    
def path_exist(p):
    return os.path.exists(p)

def mkdir_p(path):
    err = 1
    try:
        os.makedirs(path)
        err = 0
    except OSError as e:
        if e.errno == 17:
            err = 0
    return err  
    
def execcmd_str(cmd):
    process = os.popen(cmd) # return file
    restr = process.read()
    process.close()
    return restr
    
def exec_system(cmd):
    err = os.system(cmd)
    if not err:
        err = 0
    else:
        err = err >> 8
    return err

def execcmd_json(cmd):
    process = os.popen(cmd) # return file
    restr = process.read()
    process.close()
    result = {}
    result['msg'] = 'no output'
    result['code'] = 200
    rj = {}
    rj['result'] = result
    rj['data'] = {}
    if restr:
        rj = json.loads(restr)
    return rj   
    
def get_resultjson(errcode, errmsg, objtag):
     rj = """ {"result":{"code":%d, "msg":"%s"}, "data":{}, "obj":"%s"} """ % (errcode, errmsg, objtag)
     
     return rj
     
def get_resultjson_errcode(jsonobj):
    err = -1
    if isinstance(jsonobj, dict) and jsonobj.has_key('result'):
        resultobj = jsonobj['result']
        err = resultobj['code']
    return err      
     
def print_resultjson(errcode, errmsg, objtag):
     rj = """ {"result":{"code":%d, "msg":"%s"}, "data":{}, "obj":"%s"} """ % (errcode, errmsg, objtag)
     print rj
     return errcode
    
def print_datajson(errcode, errmsg, objtag, obj_dict):
    jsonobj = json.dumps(obj_dict)
    rj = """ {"result":{"code":%d, "msg":"%s"}, "data":%s, "obj":"%s"} """ % (errcode, errmsg, jsonobj, objtag)
    print rj
    return errcode

def create_file_vdisk(filepath, size, ftype):
    #qemu-img create -f qcow2 /root/vm/uus.qcow2 40G
    if path_exist(filepath):
        return 1
    cmd_str = 'qemu-img create -f %s %s %sG >/dev/null' % (ftype, filepath, size)
    return exec_system(cmd_str)

def rm_file_empty_dir(path):
    err = 1
    if os.path.isfile(path):
        try:
           os.remove(path)
           err = 0
        except OSError as e:
            if e.errno == 2:
                err = 0    
    elif os.path.isdir(path):   
        #try:
        #    shutil.rmtree(path)
        #    err = 0
        #except OSError as e:
        #    if e.errno == 2:
        #        err = 0
        try :
            os.rmdir(path)
            err = 0
        except OSError as e:
            if e.errno == 2:
                err = 0     
    else:
        if not os.path.exists(path):
            err = 0
                
    return err
    
############################################    
def localfs_mount(all):
    cmd = 'mount|grep /dev/sd'
    lines = execcmd_str(cmd)
    mountlist = []
    for line in lines.split('\n'):
        if line :
            line = line.split()
            dev = line[0]
            item = line[2]
            if item != '/' and item != '/boot':
                if not all:
                   cmd = 'ls %s/.cstor-tag* >/dev/null' % (item)
                   if exec_system(cmd):
                        add_item = 'localfs://%s:%s' % (dev, item)
                        add_dict = {'url':add_item, 'tag': dev}
                        add_dict.update(get_mount_used(item))
                        mountlist.append(add_dict)
                else:
                    add_item = 'localfs://%s:%s' % (dev, item)
                    add_dict = {'url':add_item, 'tag': dev}
                    add_dict.update(get_mount_used(item))
                    mountlist.append(add_dict)
            
    return mountlist

def uus_parse_url(url):
    #uname:pwd@ip:port
    conf = url.split('@')
    ip = conf[1]
    user = conf[0].split(':')
    uname = user[0]
    pwd = user[1]
    return (uname, pwd, ip)
    
def uus_dev_pool(url):
    '''
    /etc/sysconfig/cstor/uus.conf
    {
        "uus-iscsi-independent":{"n":4,"m":2,"k":0,"strip":32,"prealloc":1,"tag":"uus-iscsi-fast"},
        "uus-iscsi":{"n":4,"m":2,"k":0,"strip":32,"prealloc":1,"tag":"uus-iscsi"},
        "uus-dev-independent":{"n":4,"m":2,"k":0,"strip":32,"prealloc":1,"tag":"uus-dev-fast"},
        "uus-dev":{"n":4,"m":2,"k":0,"strip":32,"prealloc":1,"tag":"uus-dev"}
    }
    '''
    #oldurl ip:port/poolname
    #neturl user:pwd@ip:port
    import base64
    
    ret = []    
    
    uname, pwd, ip = uus_parse_url(url)
    upwd = base64.b64encode(pwd)
    
    cmd = 'curl http://%s/uraidapi/pool/list?tmptoken=%s@@%s 2>/dev/null' % (ip, uname, upwd)
    jsonobj = execcmd_json(cmd)
    
    uus_conf = json_load_file(CSTOR_DIR, 'uus.conf')
    
    if jsonobj and uus_conf:
        err = get_resultjson_errcode(jsonobj)
        if not err:
            data_arr = jsonobj['data']
            for poolobj in data_arr:
                poolname = poolobj['pool_name']
                cap_total = poolobj['cap_total'] * 1000
                cap_free = poolobj['cap_free'] * 1000
                cap_used = cap_total - cap_free             
       
                for key,val in uus_conf.items():
                    item = {}
                    item['url'] = '%s://%s:%s@%s/%s/%d/%d/%d/%d/%d' % (key, uname, pwd, ip, poolname, val['n'], val['m'], val['k'], val['strip'], val['prealloc'])
                    item['total'] = cap_total
                    item['free'] = cap_free
                    item['used'] = cap_used
                    item['tag'] = '%s@%s' % (val['tag'], poolname) 
                    ret.append(item)    
    return ret
    
def get_mount_used(dir):
    cmd = 'df  %s|grep -v Filesystem' % dir
    strused = execcmd_str(cmd)
    used = {}
    if strused:
        ua = strused.split()
        used['total'] = long(ua[1]) >> 20
        used['used'] = long(ua[2]) >> 20
        used['free'] = long(ua[3]) >> 20
        used['status'] = 'active'
    else:
        used['total'] = 0
        used['used'] = 0
        used['free'] = 0
        used['status'] = 'inactive'
    return used

def get_tmpmount_used(proto, url):
    tmppath = '/tmp/cstor/%d' % os.getpid() 
    mkdir_p(tmppath)
    cmd = 'mount -t %s %s %s >/dev/null' % (proto, url, tmppath)
    err = exec_system(cmd)
    
    used = {}
    
    if err:
        used['total'] = 0
        used['used'] = 0
        used['free'] = 0 
    else:
        used = get_mount_used(tmppath)
        cmd = 'umount %s' % tmppath
        exec_system(cmd)
        rm_file_empty_dir(tmppath)
        del use['status']
    return used
    
def dev_list(args):
    #localfs/nfs/glusterfs/uus
    args_dict = vars(args)
    t = args_dict['type']
    url = args_dict['url']
    
    retarray = []
    
    if t == LOCAL_FS: 
        showall = 0
        if url == 'all':
            showall = 1     
        retarray = localfs_mount(showall)
    elif t == NFS:      
        used = get_tmpmount_used(NFS, url) 
        used['url'] = 'nfs://%s' % url
        used['tag'] = url
        retarray.append(used)
    elif t == GLUSTERFS:
        used = get_tmpmount_used(GLUSTERFS, url) 
        used['url'] = 'glusterfs://%s' % url
        used['tag'] = url
        retarray.append(used)
    elif t == UUS:
        retarray = uus_dev_pool(url)
    else:
        pass
    
    #print retarray
    return print_datajson(0, 'success', 'dev-list', retarray)

def check_pool(pool_desc):
    proto = pool_desc['proto']
    if proto != NFS and proto != GLUSTERFS:
        return 0
        
    path = pool_desc['mountpath']
    url = pool_desc['url']
    
    cmd = 'mount |grep "%s on " >/dev/null' % url
    
    if exec_system(cmd):
        mkdir_p(path)
        cmd = 'mount -t %s %s %s >/dev/null' % (proto, url, path)
        err = exec_system(cmd)
        if err:
            return print_resultjson(100, 'failed', 'check mount')
        
    return 0
    
def pool_add(poolname, data):
    filename = '%s/%s' % (CSTOR_POOL, poolname)
    if path_exist(filename):
        return print_resultjson(1, 'pool exist', poolname)
    
    data['poolname'] = poolname 
    if data['disktype'] == 'file':
        err = check_pool(data)
        if err:
            return
            
        cmd = 'touch %s/.cstor-tag.%s >/dev/null' % (data['mountpath'], poolname)
        exec_system(cmd)
        pooldatadir = '%s/%s' % (data['mountpath'], poolname)
        mkdir_p(pooldatadir)
        
    json_dump_file(CSTOR_POOL, poolname, data)
    
    pooljson = pool_get_json(poolname)
    return print_datajson(0, 'success', 'poolshow', pooljson)
    
def pooladd_local(args):
    args_dict = vars(args)
    poolname = args_dict['poolname']
    url = args_dict['url']
    
    data = {}
    url = url[10:].split(':')
    data['url'] = url[0]
    data['proto'] = LOCAL_FS
    data['disktype'] = 'file'
    data['mountpath'] = url[1]
    
    return pool_add(poolname, data)
    
def pooladd_nfs(args):
    args_dict = vars(args)
    poolname = args_dict['poolname']
    url = args_dict['url']
    mountpath = args_dict['path']
    mountopt = args_dict['opt']
    
    data = {}
    data['url'] = url[6:]
    data['proto'] = NFS
    data['opt'] = mountopt
    data['disktype'] = 'file'
    data['mountpath'] = mountpath
    
    return pool_add(poolname, data) 
    
def pooladd_glusterfs(args):
    args_dict = vars(args)
    poolname = args_dict['poolname']
    url = args_dict['url']
    mountpath = args_dict['path']
    mountopt = args_dict['opt']
    
    data = {}
    data['url'] = url[12:]
    data['proto'] = GLUSTERFS
    data['opt'] = mountopt
    data['disktype'] = 'file'
    data['mountpath'] = mountpath
    
    return pool_add(poolname, data) 

def pooladd_uus(args):
    args_dict = vars(args)
    poolname = args_dict['poolname']
    url = args_dict['url']
    user = args_dict['user']
    pwd = args_dict['pwd']
    
    #url uus-iscsi://test:123456@172.18.70.214:7000/test/4/2/0/32/1
    
    pos = url.find('://')
    blocktype = url[0:pos].split('-')
    other = url[pos+3:].split('/')
    
    auth = other[0].split('@')
    authuser = auth[0].split(':')
    
    data = {}
    data['url'] = url
    data['proto'] = UUS
    data['disktype'] = 'uus_%s' % (blocktype[1])
    data['prealloc'] = other[6]
    
    if len(blocktype) == 3:
        data['blocktype'] == 'lvm'
    else:
        data['blocktype'] == 'raw'
        
    data['user'] = authuser[0]
    data['pwd'] = authuser[1]
    data['ip'] = auth[1]
    data['poolname'] = other[1]
    data['nmk_strip'] = '%s %s %s %s' % (other[2], other[3], other[4], other[5])
    
    return pool_add(poolname, data) 

def pool_get_json(poolname):
    pooljson = json_load_file(CSTOR_POOL, poolname)
    if pooljson:
        poolused = {}
        if pooljson['disktype'] == 'file':
            poolused = get_mount_used(pooljson['mountpath'])
            pooljson.update(poolused)         
    else:
        pooljson = {}
    return pooljson     
    
def pool_list(args):
    pool_exist = []
    poollist = os.listdir(CSTOR_POOL)
    for pool in poollist:       
        pool_exist.append(pool_get_json(pool))
    
    return print_datajson(0, 'success', 'poollist', pool_exist) 

def pool_show(args):
    args_dict = vars(args)
    poolname = args_dict['poolname']  
    pooljson = pool_get_json(poolname)
    return print_datajson(0, 'success', 'poolshow', pooljson)
    
def pool_remove(args):
    args_dict = vars(args)
    poolname = args_dict['poolname']
    pooljson = pool_get_json(poolname)
    
    if pooljson and pooljson.has_key('disktype') and pooljson['disktype'] == 'file':
        err = check_pool(pooljson)
        if err:
            return
        
        pooldatadir = '%s/%s' % (pooljson['mountpath'], poolname)
        if len(os.listdir(pooldatadir)):
            return print_resultjson(1, 'vdisk exist', poolname)
            
        rm_file_empty_dir(pooldatadir)
    
        fullname = '%s/.cstor-tag.%s' % (pooljson['mountpath'], poolname)
        rm_file_empty_dir(fullname)
     
     
    fullname = '%s/%s' % (CSTOR_POOL, poolname)
    rm_file_empty_dir(fullname) 
    
    return print_resultjson(0, 'success', 'poolname')

##############################################  
    
def create_volume(args):
    
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_create_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict)  

def remove_volume(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_remove_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict) 

def show_volume(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_show_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict) 

def expand_volume(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
        
    exec_fun = '%s_expand_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict) 

def add_volume_snapshot(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
        
    exec_fun = '%s_add_vol_snapshot' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict) 
     
def recover_volume_snapshot(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_reocver_vol_snapshot' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict)      
    
def remove_volume_snapshot(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_remove_vol_snapshot' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict) 

def show_volume_snapshot(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_show_vol_snapshot' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict)     

def clone_volume(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_clone_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict)  
    
def prepare_volume(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    err = check_pool(pooljson)
    if err:
        return
    
    exec_fun = '%s_prepare_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict) 
    
def release_volume(args):
    args_dict = vars(args)
    pool = args_dict['poolname']
    
    pooljson = pool_get_json(pool)
    
    exec_fun = '%s_release_vol' % pooljson['disktype']
    
    return eval(exec_fun)(pooljson, args_dict)   

############################################

def file_create_vol(pool_desc, disk_desc):
            
    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    size = disk_desc['size']
    
    data = {}
    
    fullname = '%s/%s/%s' % (path, poolname, name)
    err = create_file_vdisk(fullname, size, 'qcow2')
    msg = 'success'
    if err:
        msg = 'failed'
    else:   
        data['name'] = name
        data['poolname'] = poolname
        data['filetype'] = 'qcow2'
        data['size'] = size
        data['path'] = fullname
    
    return print_datajson(err, msg, 'create', data)
    
def file_show_vol(pool_desc, disk_desc):
    '''
    qemu-img  info test.rawa >/dev/null
    qemu-img: Could not open 'test.rawa': Could not open 'test.rawa': No such file or directory

    qemu-img  info abc.qcow2 
    image: abc.qcow2
    file format: qcow2
    virtual size: 10G (10737418240 bytes)
    disk size: 196K
    cluster_size: 65536
    Format specific information:
        compat: 1.1
        lazy refcounts: false

    qemu-img  info test.raw 
    image: test.raw
    file format: qcow2
    virtual size: 10G (10737418240 bytes)
    disk size: 208K
    cluster_size: 65536
    Snapshot list:
    ID        TAG                 VM SIZE                DATE       VM CLOCK
    1         ss1                       0 2019-08-08 11:03:07   00:00:00.000
    Format specific information:
        compat: 1.1
        lazy refcounts: false 
    '''

    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    
    fullname = '%s/%s/%s' % (path, poolname, name)
    cmd = 'qemu-img info %s' % fullname
    retstr = execcmd_str(cmd)
    
    desc = retstr.split('\n')
    
    if len(desc) < 8:
        return print_resultjson(1, 'not exist', name)
    
    data = {}
    data['name'] = name
    data['poolname'] = poolname
    data['filetype'] = desc[1].split(': ')[1]
    data['size'] = int(desc[2].split(': ')[1].split('(')[1].split()[0]) >> 30
    data['path'] = fullname
    
    return print_datajson(0, 'success', 'show', data)
    
def file_remove_vol(pool_desc, disk_desc):
    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    
    fullname = '%s/%s/%s' % (path, poolname, name)
    err = rm_file_empty_dir(fullname)
    msg = 'success'
    if err:
        msg = 'failed'
        
    return print_resultjson(err, msg, 'remove')
    
def file_expand_vol(pool_desc, disk_desc):
    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    size = disk_desc['size']
    
    fullname = '%s/%s/%s' % (path, poolname, name)
    
    cmd = 'qemu-img resize %s %sG >/dev/null' % (fullname, size)
    err = exec_system(cmd)
    msg = 'success'
    if err:
        msg = 'failed'
        
    return print_resultjson(err, msg, 'expand')

def file_snapshot(fullname, sname):
    cmd = 'qemu-img snapshot -l %s|grep "%s "' % (fullname, sname)
    cmdstr = execcmd_str(cmd)
    strarr = cmdstr.split()
    err = 1
    data = {}
    if len(strarr) > 4:
        err = 0
        #data['id'] = strarr[0]
        data['vmsize'] = strarr[2]
        data['date'] = '%s %s' % (strarr[3], strarr[4])
    else:
        #data['id'] = ''
        data['vmsize'] = '0'
        data['date'] = ''
    
    return err, data
    
def file_snapshot_fun(pool_desc, disk_desc, op, tag):
    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    sname = disk_desc['sname']
    
    fullname = '%s/%s/%s' % (path, poolname, name)
    if op == '-c':
        err, data = file_snapshot(fullname, sname)
        if not err:
            err = 2
            msg = 'already exist'
            return print_resultjson(err, msg, tag)
            
    cmd = 'qemu-img snapshot %s %s %s >/dev/null' % (op, sname, fullname)
    err = exec_system(cmd)
    msg = 'success'
    if err:
        msg = 'failed'
        
    data = {}
    if op == '-c':  
        err, ss = file_snapshot(fullname, sname)
        if err:
            msg = 'failed'
        else:
            msg = 'success'
            data['name'] = name
            data['poolname'] = poolname
            data['filetype'] = 'qcow2'
            data['sname'] = sname
            data['path'] = fullname
            data.update(ss)
        
        
    return print_datajson(err, msg, tag, data)   
 
def file_add_vol_snapshot(pool_desc, disk_desc):
    return file_snapshot_fun(pool_desc, disk_desc, '-c', 'add snapshot')

def file_show_vol_snapshot(pool_desc, disk_desc):
    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    sname = disk_desc['sname']
    fullname = '%s/%s/%s' % (path, poolname, name)
    
    data = {}
    err, ss = file_snapshot(fullname, sname)
    if err:
        msg = 'failed'
    else:
        msg = 'success'
        data['name'] = name
        data['poolname'] = poolname
        data['filetype'] = 'qcow2'
        data['sname'] = sname
        data['path'] = fullname
        data.update(ss)
        
    return print_datajson(err, msg, 'show snapshot', data)  
    
def file_reocver_vol_snapshot(pool_desc, disk_desc):
    return file_snapshot_fun(pool_desc, disk_desc, '-a', 'recover snapshot')
    
def file_remove_vol_snapshot(pool_desc, disk_desc):
    return file_snapshot_fun(pool_desc, disk_desc, '-d', 'remove snapshot') 

def file_clone_vol(pool_desc, disk_desc):
    path = pool_desc['mountpath']
    poolname = disk_desc['poolname']
    name = disk_desc['name']
    clonename = disk_desc['clonename']
    
    fullname = '%s/%s/%s' % (path, poolname, name)
    cmd = 'qemu-img info %s' % fullname
    retstr = execcmd_str(cmd)
    
    desc = retstr.split('\n')
    
    if len(desc) < 8:
        return print_resultjson(1, 'not exist', name)
        
    filetype = desc[1].split(': ')[1]
    size = int(desc[2].split(': ')[1].split('(')[1].split()[0]) >> 30
    
    clone_fullname = '%s/%s/%s' % (path, poolname, clonename)
    
    cmd = 'cp %s %s >/dev/null' % (fullname, clone_fullname)
    err = exec_system(cmd)
    if err:
        return print_resultjson(2, 'clone failed', name)
    
    data = {}
    data['name'] = clonename
    data['poolname'] = poolname
    data['filetype'] = filetype
    data['size'] = size
    data['path'] = clone_fullname
    
    return print_datajson(0, 'success', 'clone', data)  
    
def file_prepare_vol(pool_desc, disk_desc):
    return file_show_vol(pool_desc, disk_desc)

def file_release_vol(pool_desc, disk_desc):
    return print_resultjson(0, 'success', 'release') 

########################################### 
def uus_check_snapshot_support(pool_desc, tag):
    if pool_desc['blocktype'] != 'lvm':
        return print_resultjson(101, 'not support', tag)
    return 0
    
def uus_vol_active_nodeid(volname):
    cmd = '%s usb_remove_snapshot_json %s,%s' % (uusvolcli, volname)
    jsonobj = execcmd_json(cmd)
    err = get_resultjson_errcode(jsonobj)
    if err:
        return -1
        
    dataobj = jsonobj['data'][0]
    return dataobj['now_host']

def uus_node_id():
    jsonobj = json_load_file('/etc/uraid/conf/broker', 'broker.json')
    if jsonobj:     
        return int(jsonobj['node_id'], 16)
        
    return -1
    
def uus_dev_create_vol(pool_desc, disk_desc):
    #ucli vol hmd multi-create-uraid xname 1 -1 0 0 undefined xprealloc 0 xsizeG raw 4 1 0 128 xpoolname
    
    app_type = 'hmd'
    name = disk_desc['name']
    size = disk_desc['size']
    poolname = disk_desc['poolname']
    
    nmk_strip = pool_desc['nmk_strip']
    blocktype = pool_desc['blocktype']
    prealloc = pool_desc['prealloc']
    
    cmd = 'env OFMT=JSON ucli vol hmd multi-create-uraid %s 1 -1 0 0 undefined %s 0 %sG %s %s %s' % (name, prealloc, size, blocktype, nmk_strip, poolname)
    
    jsonobj = execcmd_json(cmd)
    
    err = get_resultjson_errcode(jsonobj)
    if err:
        return print_resultjson(err, 'create uus vol failed', 'uus_dev_create_vol')
    else:
        cmd = '%s usb_volume_mark_used_json %s,%s 1>/dev/null 2>&1' % (uusvolcli, name, app_type)
        exec_system(cmd)
        
        fullname = ''
        
        dataobj = jsonobj['data']
        if blocktype == 'lvm':
            fullname = '/dev/%s/%s' % (name, name)          
        else:
            id = dataobj['id']
            fullname = '/dev/md%d' % id
            
        data = {}
        data['name'] = name
        data['poolname'] = poolname
        data['filetype'] = 'block'
        data['size'] = size
        data['path'] = fullname
        
        return print_datajson(err, 'create uus vol success', 'create', data)

def uus_dev_show_vol(pool_desc, disk_desc):
    
    name = disk_desc['name']
    cmd = 'env OFMT=JSON ucli vol show %s' % name
    jsonobj = execcmd_json(cmd)
    err = get_resultjson_errcode(jsonobj)
    if err:
        return print_resultjson(err, 'get uus vol failed', 'uus_dev_show_vol')
    else:
        dataobj = jsonobj['data']
        strsize = dataobj['size'].replace('M', '')
        size = float(strsize) / 1000
        
        data = {}
        data['name'] = name
        data['poolname'] = disk_desc['poolname']
        data['filetype'] = 'block'
        data['size'] = size
        data['path'] = dataobj['path']
        
        return print_datajson(err, 'success', 'show', data)

def uus_dev_remove_vol(pool_desc, disk_desc):
    name = disk_desc['name']
    cmd = 'env OFMT=JSON ucli vol del_hmd %s' % name
    jsonobj = execcmd_json(cmd)
    
    err = get_resultjson_errcode(jsonobj)
    msg = 'success'
    if err:
        msg = 'failed'
        
    return print_resultjson(err, msg, 'remove')
    
def uus_dev_expand_vol(pool_desc, disk_desc):
    err = uus_check_snapshot_support(pool_desc, 'expand')
    if err:
        return err
        
    name = disk_desc['name']
    size = disk_desc['size']
    
    cmd = '%s usb_expand_volume_json %s,%s 2>/dev/null' % (uusvolcli, name, size)
    jsonobj = execcmd_json(cmd)
    
    err = get_resultjson_errcode(jsonobj)
    msg = 'success'
    if err:
        msg = 'failed'
        
    return print_resultjson(err, msg, 'expand')

def uus_dev_add_vol_snapshot(pool_desc, disk_desc):
    err = uus_check_snapshot_support(pool_desc, 'add snapshot')
    if err:
        return err
        
    name = args_dict['name']
    sname = args_dict['sname']
    
    cmd = '%s usb_create_snapshot_json %s,%s' % (uusvolcli, name, sname)    
    jsonobj = execcmd_json(cmd)
    err = get_resultjson_errcode(jsonobj)
    
    if err:
        return print_resultjson(err, 'add snapshot failed', 'sanpshot')
        
    data = {} 
    data['name'] = name
    data['poolname'] = disk_desc['poolname']
    data['filetype'] = 'block'
    data['sname'] = sname   
    
    cmd = '%s usb_get_volume_snapshots_json %s,%s' % (uusvolcli, name, sname)   
    jsonobj = execcmd_json(cmd)
    
    dataobj = jsonobj['data']['lvs']
    
    if len(dataobj) > 0:
        dataobj = dataobj[0]
        dt = dataobj['LV Creation host, time'].split()
        data['path'] = '/dev/%s/%s' % (name, sname)
        size = float(dataobj['size'].replace('M', '')) * float(dataobj['snap_percent'])
        #data['id'] = ''
        data['vmsize'] = ''
        data['date'] = '%s %s' % (dt[1], dt[2])
    else:
        data['path'] = ''
        #data['id'] = ''
        data['vmsize'] = '%fM' % size
        data['date'] = ''
        
    return print_datajson(err, 'success', 'add snapshot', data) 

def uus_dev_show_vol_snapshot(pool_desc, disk_desc):
    err = uus_check_snapshot_support(pool_desc, 'show snapshot')
    if err:
        return err
        
    data = {} 
    data['name'] = disk_desc['name']
    data['poolname'] = disk_desc['poolname']
    data['filetype'] = 'block'
    data['sname'] = disk_desc['sname']  
    
    cmd = '%s usb_get_volume_snapshots_json %s,%s' % (uusvolcli, name, sname)   
    jsonobj = execcmd_json(cmd)
    
    err = get_resultjson_errcode(jsonobj)   
    if not err: 
        dataobj = jsonobj['data']['lvs']        
        if len(dataobj) > 0:
            dataobj = dataobj[0]
            dt = dataobj['LV Creation host, time'].split()
            data['path'] = '/dev/%s/%s' % (name, sname)
            size = float(dataobj['size'].replace('M', '')) * float(dataobj['snap_percent'])
            #data['id'] = ''
            data['vmsize'] = ''
            data['date'] = '%s %s' % (dt[1], dt[2])
        else:
            data['path'] = ''
            #data['id'] = ''
            data['vmsize'] = '%fM' % size
            data['date'] = ''
        
    return print_datajson(err, 'success', 'show snapshot', data)    

def uus_dev_reocver_vol_snapshot(pool_desc, disk_desc):

    err = uus_check_snapshot_support(pool_desc, 'recover snapshot')
    if err:
        return err
        
    cmd = '%s lvm_recover_snap_json %s,%s' % (uusvolcli, disk_desc['name'], disk_desc['sname']) 
    jsonobj = execcmd_json(cmd)
    
    err = get_resultjson_errcode(jsonobj)
    msg = 'success'
    if err:
        msg = 'failed'
    return print_resultjson(err, msg, 'recover')

def uus_dev_remove_vol_snapshot(pool_desc, disk_desc):

    err = uus_check_snapshot_support(pool_desc, 'expand')
    if err:
        return err
    
    cmd = '%s usb_remove_snapshot_json %s,%s' % (uusvolcli, disk_desc['name'], disk_desc['sname']) 
    jsonobj = execcmd_json(cmd)
    
    err = get_resultjson_errcode(jsonobj)
    msg = 'success'
    if err:
        msg = 'failed'
    return print_resultjson(err, msg, 'remove') 

def uus_dev_clone_vol(pool_desc, disk_desc):
    return print_resultjson(101, 'not support', 'clone')
    
def uus_dev_prepare_vol(pool_desc, disk_desc):
    cur_nodeid = uus_node_id()
    if cur_nodeid <= 0:
        return print_resultjson(102, 'uus not configure', 'prepare')
    
    name = disk_desc['name']
    sname = disk_desc['sname']
    poolname = disk_desc['poolname']
    
    if sname:
        err = uus_check_snapshot_support(pool_desc, 'prepare')
        if err:
            return err
    
    active_nodeid = uus_vol_active_nodeid(name)
    
    if active_nodeid < 0:
        return print_resultjson(103, 'unknown vol', 'prepare')
        
    if active_nodeid != cur_nodeid:
        if active_nodeid > 0:
            cmd = 'node = %d ucli vol stop %s >/dev/null' % (active_nodeid, name)
            err = exec_system(cmd)
            if err:
               return print_resultjson(104, 'stop vol failed', 'prepare')
               
        cmd = 'ucli vol run %s >/dev/null' % name
        err = exec_system(cmd)
        if err:
            return print_resultjson(105, 'stop vol failed', 'prepare')
            
    
    if not sname:
        return uus_dev_show_vol(pool_desc, disk_desc)
    else:
        cmd = '%s usb_export_snapshot_json %s,%s >/dev/null' % (uusvolcli, name, sname)
        exec_system(cmd)
        return uus_dev_show_vol_snapshot(pool_desc, disk_desc)
    
def uus_dev_release_vol(pool_desc, disk_desc):
    return print_resultjson(0, 'success', 'release')
###############################################
def uus_make_http_request(pool_desc, cmd, op, param, is_json, nodeid):
    #"http://127.0.0.1:7000/uraidapi/vol/hmd?p1=multi-create-uraid%20xname%201%20-1%200%200%20undefined%20xprealloc%200%20xsizeG%20raw%204%201%200%20128%20xpoolname&outcmd=1&tmptoken=admin@@YWRtaW4="
    import base64
    p1 = ''
    if param:
        p1 = param.replace(' ', '%20')
        
    cmd_url = 'curl http://%s/uraidapi/%s/%s?tmptoken=%s@@%s&p1=%s&node=%s' % (pool_desc['ip'], cmd, op, pool_desc['user'], base64.b64encode(pool_desc['pwd']), p1, nodeid)
    outdata = ''
    if is_json:
        outdata = execcmd_json(cmd_url)
    else:
        outdata = execcmd_str(cmd_url)
        
    return outdata

def uus_calc_nodeid(pool_desc):
    #curl "http://127.0.0.1:7000/uraidapi/vol/uvol_node?tmptoken=admin@@YWRtaW4="
    nodeid = uus_make_http_request(pool_desc, 'uvol_node', '', 0, '0')
    return nodeid
    
def uus_iscsi_export_mode(pool_desc):
    return '3'

def uus_iscsi_create_vol(pool_desc, disk_desc):
    name = disk_desc['name']
    size = disk_desc['size']
    poolname = disk_desc['poolname']
    
    nmk_strip = pool_desc['nmk_strip']
    blocktype = pool_desc['blocktype']
    prealloc = pool_desc['prealloc']
    #create block
    nodeid = uus_calc_nodeid(pool_desc)
    param = 'multi-create-uraid %s 1 -1 0 0 undefined %s 0 %sG %s %s %s' % (name, prealloc, size, blocktype, nmk_strip, poolname)
    jsonobj = uus_make_http_request(pool_desc, 'vol', 'uvol', param, 1, nodeid)
    err = get_resultjson_errcode(jsonobj)
    if err:
        return print_resultjson(err, 'create uus vol failed', 'uus_iscsi_create_vol')
        
    param = "0 0 %s" %  uus_iscsi_export_mode(pool_desc)
    jsonobj = uus_make_http_request(pool_desc, 'uvol', 'add', param, 1, nodeid)

def uus_iscsi_show_vol(pool_desc, disk_desc):
    
    pass

def uus_iscsi_remove_vol(pool_desc, disk_desc):
    pass
    
def uus_iscsi_expand_vol(pool_desc, disk_desc):
    pass

def uus_iscsi_add_vol_snapshot(pool_desc, disk_desc):
    pass

def uus_iscsi_show_vol_snapshot(pool_desc, disk_desc):
    pass

def uus_iscsi_reocver_vol_snapshot(pool_desc, disk_desc):
    pass

def uus_iscsi_remove_vol_snapshot(pool_desc, disk_desc):
    pass  

def uus_iscsi_clone_vol(pool_desc, disk_desc):
    return print_resultjson(101, 'not support', 'clone')    
 
def uus_iscsi_prepare_vol(pool_desc, disk_desc):
    pass
    
def uus_iscsi_release_vol(pool_desc, disk_desc):
    pass
    
if __name__ == '__main__':
    main(*sys.argv)
    
    

