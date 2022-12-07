'''
Copyright (2021, ) Institute of Software, Chinese Academy of Sciences
    @author: wuyuewen@otcaix.iscas.ac.cn
    @author: wuheng@otcaix.iscas.ac.cn
    
    @since:  2019/09/26  
'''

'''KubeVMM configurations'''
KUBEVMM_CONFIG_FILE_PATH           = "/etc/kubevmm/config"
KUBEVMM_CONFIG_FILE_IN_DOCKER_PATH = "/home/kubevmm/bin/config"
KUBEVMM_VIRTCTL_SEVICE_NAME        = "Virtctl"
KUBEVMM_VIRTLET_SEVICE_NAME        = "Virtlet"
KUBEVMM_VIRTCTL_LOG                = "/var/log/virtctl.log"
KUBEVMM_VIRTLET_LOG                = "/var/log/virtlet.log"
KUBEVMM_LOG_FILE_RESERVED          = 10
KUBEVMM_LOG_FILE_SIZE_BYTES        = 10000000
KUBEVMM_VIRTCTL_SERVICE_LOCK       = "/var/run/virtctl_daemon.pid"
KUBEVMM_VIRTLET_SERVICE_LOCK       = "/var/run/virtlet_daemon.pid"
KUBEVMM_VIRTCTL_DOCKER_LOCK        = "/var/run/virtctl_in_docker.pid"
KUBEVMM_VIRTLET_DOCKER_LOCK        = "/var/run/virtlet_in_docker.pid"

KUBEVMM_EVENT_LIFECYCLE_DOING      = "Doing"
KUBEVMM_EVENT_LIFECYCLE_DONE       = "Done"

KUBEVMM_EVENT_TYPE_ERROR           = "Error"
KUBEVMM_EVENT_TYPE_NORMAL          = "Normal"

KUBEVMM_VM_DEVICES_DIR             = "/var/lib/libvirt/devices"
KUBEVMM_LIBVIRT_VM_XML_DIR         = "/etc/libvirt/qemu"
KUBEVMM_NOVNC_TOKEN                = "/root/noVNC/websockify/token/token.conf"
KUBEVMM_RESOURCE_FILE_PATH         = "/etc/kubevmm/resource"
KUBEVMM_SHARE_FS_MOUNT_POINT       = "/var/lib/libvirt/cstor"
KUBEVMM_VDISK_FS_MOUNT_POINT       = "/mnt/usb"
KUBEVMM_LOCAL_FS_MOUNT_POINT       = "/mnt/localfs"
KUBEVMM_BLOCK_FS_MOUNT_POINT       = "/var/lib/libvirt/cstor"
KUBEVMM_OVN_FILE                   = "/etc/ovn.conf"
KUBEVMM_DEFAULT_JSON_BACKUP_DIR    = "/etc/kubevmm/backup"
KUBEVMM_DEFAULT_VMDI_DIR           = "/var/lib/libvirt/vmdi"

'''Kubernetes configurations'''
KUBERNETES_TOKEN_FILE              = "/root/.kube/config"
KUBERNETES_WATCHER_TIME_OUT        = "31536000"
KUBERNETES_GROUP                   = "doslab.io"
KUBERNETES_API_VERSION             = "v1"
KUBERNETES_PLURAL_VM               = "virtualmachines"
KUBERNETES_KIND_VM                 = "VirtualMachine"
KUBERNETES_PLURAL_VMD              = "virtualmachinedisks"
KUBERNETES_KIND_VMD                = "VirtualMachineDisk"
KUBERNETES_PLURAL_VMDI             = "virtualmachinediskimages"
KUBERNETES_KIND_VMDI               = "VirtualMachineDiskImage"
KUBERNETES_PLURAL_VMDSN            = "virtualmachinedisksnapshots"
KUBERNETES_KIND_VMDSN              = "VirtualMachineDiskSnapshot"
KUBERNETES_PLURAL_VMP              = "virtualmachinepools"
KUBERNETES_KIND_VMP                = "VirtualMachinePool"
KUBERNETES_PLURAL_VMN              = "virtualmachinenetworks"
KUBERNETES_KIND_VMN                = "VirtualMachineNetwork"
KUBERNETES_KIND_VMSN               = "VirtualMachineSnapshot"
KUBERNETES_KIND_VMDEV              = 'VirtualMahcineBlockDevUit'
KUBERNETES_KIND_VMI                = 'VirtualMachineImage'

'''Virtual Machine supported commands'''
CREATE_AND_START_VM_FROM_ISO_CMD   = "default,name,none,virshplus create_and_start_vm_from_iso,virshplus dumpxml"
CREATE_VM_CMD                      = "default,domain,none,virsh create,virshplus dumpxml"
START_VM_CMD                       = "default,domain,none,virsh start,virshplus dumpxml"
STOP_VM_CMD                        = "default,domain,none,virsh shutdown,virshplus dumpxml"
STOP_VM_FORCE_CMD                  = "default,domain,none,virsh destroy,virshplus dumpxml"
DELETE_VM_CMD                      = "default,domain,none,virshplus delete_vm,none"
REBOOT_VM_CMD                      = "default,domain,none,virsh reboot,virshplus dumpxml"
RESET_VM_CMD                       = "default,domain,none,virsh reset,virshplus dumpxml"
RESUME_VM_CMD                      = "default,domain,none,virsh resume,virshplus dumpxml"
SUSPEND_VM_CMD                     = "default,domain,none,virsh suspend,virshplus dumpxml"
SAVE_VM_CMD                        = "default,domain,none,virsh save,virshplus dumpxml"
RESTORE_VM_CMD                     = "default,domain,none,virsh restore,virshplus dumpxml"
MIGRATE_VM_CMD                     = "rpc,domain,none,kubesds-adm migrate,virshplus dumpxml"
MANAGE_ISO_CMD                     = "default,domain,none,virsh change-media,virshplus dumpxml"
UPDATE_OS_CMD                      = "default,domain,none,virshplus update-os,virshplus dumpxml"
PLUG_DEVICE_CMD                    = "default,domain,none,virsh attach-device,virshplus dumpxml"
UNPLUG_DEVICE_CMD                  = "default,domain,none,virsh detach-device,virshplus dumpxml"
PLUG_DISK_CMD                      = "default,domain,none,virshplus plug_disk,virshplus dumpxml"
UNPLUG_DISK_CMD                    = "default,domain,none,virshplus unplug_disk,virshplus dumpxml"
PLUG_NIC_CMD                       = "default,domain,none,virshplus plug_nic,virshplus dumpxml"
UNPLUG_NIC_CMD                     = "default,domain,none,virshplus unplug_nic,virshplus dumpxml"
CHANGE_NUMBER_OF_CPU_CMD           = "default,domain,none,virsh setvcpus,virshplus dumpxml"
RESIZE_RAM_CMD                     = "default,domain,none,virsh setmem,virshplus dumpxml"
RESIZE_MAX_RAM_CMD                 = "default,domain,none,virsh setmaxmem,virshplus dumpxml"
RESIZE_VM_CMD                      = "default,domain,none,virsh blockresize,virshplus dumpxml"
TUNE_DISK_QOS_CMD                  = "default,domain,none,virsh blkdeviotune,virshplus dumpxml"
TUNE_NIC_QOS_CMD                   = "default,domain,none,virsh domiftune,virshplus dumpxml"
SET_BOOT_ORDER_CMD                 = "default,domain,none,virshplus set_boot_order,virshplus dumpxml"
SET_VNC_PASSWORD_CMD               = "default,domain,none,virshplus set_vnc_password,virshplus dumpxml"
UNSET_VNC_PASSWORD_CMD             = "default,domain,none,virshplus unset_vnc_password,virshplus dumpxml"
SET_GUEST_PASSWORD_CMD             = "default,domain,none,virshplus set_guest_password,virshplus dumpxml"

'''Virtual Machine Disk supported commands'''
# CREATE_DISK_INTERNAL_SNAPSHOT_CMD  = "default,name,none,virshplus create_disk_snapshot,virshplus dumpxml"
# DELETE_DISK_INTERNAL_SNAPSHOT_CMD  = "default,name,none,virshplus delete_disk_snapshot,virshplus dumpxml"
# REVERT_DISK_INTERNAL_SNAPSHOT_CMD  = "default,name,none,virshplus revert_disk_internal_snapshot,virshplus dumpxml"
CREATE_DISK_INTERNAL_SNAPSHOT_CMD  = "default,name,none,sdsctl create-internal-snapshot,none"
DELETE_DISK_INTERNAL_SNAPSHOT_CMD  = "default,name,none,sdsctl delete-internal-snapshot,none"
REVERT_DISK_INTERNAL_SNAPSHOT_CMD  = "default,name,none,sdsctl revert-internal-snapshot,none"

CREATE_DISK_FROM_DISK_IMAGE_CMD    = "default,name,none,sdsctl create-disk-from-image,none"
CREATE_DISK_CMD                    = "default,vol,none,sdsctl create-disk,none"
RESIZE_DISK_CMD                    = "default,vol,none,sdsctl resize-disk,none"
CLONE_DISK_CMD                     = "default,vol,none,sdsctl clone-disk,none"
DELETE_DISK_CMD                    = "default,vol,none,sdsctl delete-disk,none"

CREATE_DISK_EXTERNAL_SNAPSHOT_CMD  = "default,name,none,sdsctl create-external-snapshot,none"
REVERT_DISK_EXTERNAL_SNAPSHOT_CMD  = "default,name,none,sdsctl revert-external-snapshot,none"
DELETE_DISK_EXTERNAL_SNAPSHOT_CMD  = "default,name,none,sdsctl delete-external-snapshot,none"

'''Virtual Machine Disk Image supported commands'''
# CREATE_DISK_IMAGE_FROM_DISK_CMD    = "rpc,name,none,virshplus create_vmdi_from_disk,kubesds-adm showDisk"
# CREATE_DISK_IMAGE_CMD              = "rpc,name,none,virshplus create_vmdi,kubesds-adm showDisk"
# DELETE_DISK_IMAGE_CMD              = "rpc,name,none,virshplus delete_vmdi"
CREATE_DISK_IMAGE_FROM_DISK_CMD    = "default,name,none,sdsctl create-image-from-disk,none"
CREATE_DISK_IMAGE_CMD              = "default,name,none,sdsctl create-disk-image,none"
DELETE_DISK_IMAGE_CMD              = "default,name,none,sdsctl delete-disk-image,none"
# upload & download
UPLOAD_DISK_IMAGE_CMD              = "default,name,none,sdsctl upload-disk-image,none"
DOWNLOAD_DISK_IMAGE_CMD              = "default,name,none,sdsctl download-disk-image,none"

'''Virtual Machine Pool supported commands'''
# CREATE_POOL_CMD                    = "default,pool,none,virshplus create_pool,none"
CREATE_POOL_CMD                    = "default,pool,none,sdsctl create-pool,none"
# DELETE_POOL_CMD                    = "default,pool,none,virshplus delete_pool,none"
DELETE_POOL_CMD                    = "default,pool,none,sdsctl delete-pool,none"
START_POOL_CMD                     = "default,pool,none,sdsctl start-pool,none"
AUTO_START_POOL_CMD                = "default,pool,none,sdsctl auto-start-pool,none"
STOP_POOL_CMD                      = "default,pool,none,sdsctl stop-pool,none"

'''Virtual Machine Network supported commands'''
BIND_PORT_VLAN_CMD                 = "default,name,none,kubeovn-adm bindport-vlan,virshplus dump_l2_network_info"
UNBIND_PORT_VLAN_CMD               = "default,name,none,kubeovn-adm unbindport-vlan,virshplus dump_l2_network_info"
CREATE_SWITCH_CMD                  = "default,name,none,kubeovn-adm create-switch,virshplus dump_l3_network_info"
MODIDY_SWITCH_CMD                  = "default,name,none,kubeovn-adm modify-switch,virshplus dump_l3_network_info"
DELETE_SWITCH_CMD                  = "default,name,none,kubeovn-adm delete-switch,virshplus delete_network"
# DELETE_SWITCH_CMD                  = "default,name,none,kubeovn-adm delete-switch,none"
CREATE_ADDRESS_CMD                 = "default,name,none,kubeovn-adm create-address,virshplus dump_l3_network_info"
MODIFY_ADDRESS_CMD                 = "default,name,none,kubeovn-adm modify-address,virshplus dump_l3_network_info"
DELETE_ADDRESS_CMD                 = "default,name,none,kubeovn-adm delete-address,virshplus delete_network"
BIND_FLOATING_IP_CMD               = "default,domain,none,kubeovn-adm bind-fip,virshplus dump_l3_network_info"
UNBIND_FLOATING_IP_CMD             = "default,domain,none,kubeovn-adm unbind-fip,virshplus dump_l3_network_info"
ADD_ACL_CMD                        = "default,domain,none,kubeovn-adm create-acl,virshplus dump_l3_network_info"
MODIFY_ACL_CMD                     = "default,domain,none,kubeovn-adm modify-acl,virshplus dump_l3_network_info"
DEPRECATED_ACL_CMD                 = "default,domain,none,kubeovn-adm delete-acl,virshplus dump_l3_network_info"
SET_QOS_CMD                        = "default,domain,none,kubeovn-adm create-qos,virshplus dump_l3_network_info"
MODIFY_QOS_CMD                     = "default,domain,none,kubeovn-adm modify-qos,virshplus dump_l3_network_info"
UNSET_QOS_CMD                      = "default,domain,none,kubeovn-adm delete-qos,virshplus dump_l3_network_info"
CREATE_BRIDGE_CMD                  = "default,domain,none,kubeovn-adm create-bridge,virshplus dump_l3_network_info"
DELETE_BRIDGE_CMD                  = "default,domain,none,kubeovn-adm delete-bridge,virshplus delete_network"
SET_BRIDGE_VLAN_CMD                = "default,domain,none,kubeovn-adm setbridge-vlan,virshplus dump_l3_network_info"
DEL_BRIDGE_VLAN_CMD                = "default,domain,none,kubeovn-adm delbridge-vlan,virshplus dump_l3_network_info"
BIND_SW_PORT_CMD                   = "default,switch,none,kubeovn-adm bind-swport,virshplus dump_l3_network_info"
UNBIND_SW_PORT_CMD                 = "default,switch,none,kubeovn-adm unbind-swport,virshplus dump_l3_network_info"
