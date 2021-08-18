## VirtualMachine

rules:

1. '--' to '__', such __size
2. 'interface' to '_interface'

```
{
  "apiVersion": "cloudplus.io/v1alpha3",
  "kind": "VirtualMachine",
  "metadata": {
    "name": "testvmi-nocloud"
  },
  "spec": {
    "domain": {
    },
    "lifecycle": {
      "command": {
      }
    },
    "image": "string",
    "nodeName": "string"
  }
}
```

## Domain

## Lifecycle

```
{
	"lifecycle": {
		"restore": {
			"file": "string"
		},
		"domfsfreeze": {
			"domain": "string"
		},
		"vol_create": {
			"file": "string",
			"pool": "string"
		},
		"net_dumpxml": {
			"network": "string"
		},
		"numatune": {
			"domain": "string"
		},
		"vol_create_as": {
			"capacity": "string",
			"name": "string",
			"pool": "string"
		},
		"domjobabort": {
			"domain": "string"
		},
		"nwfilter_undefine": {
			"nwfilter": "string"
		},
		"dompmsuspend": {
			"domain": "string",
			"target": "string"
		},
		"attach_device": {
			"domain": "string",
			"file": "string"
		},
		"vol_resize": {
			"vol": "string",
			"capacity": "string"
		},
		"net_undefine": {
			"network": "string"
		},
		"pool_autostart": {
			"pool": "string"
		},
		"secret_set_value": {
			"secret": "string",
			"base64": "string"
		},
		"guestvcpus": {
			"domain": "string"
		},
		"vol_upload": {
			"vol": "string",
			"file": "string"
		},
		"domif_getlink": {
			"_interface": "string",
			"domain": "string"
		},
		"setvcpu": {
			"domain": "string",
			"vcpulist": "string"
		},
		"migrate_getmaxdowntime": {
			"domain": "string"
		},
		"autostart": {
			"domain": "string"
		},
		"qemu_attach": {
			"pid": "string"
		},
		"domfsinfo": {
			"domain": "string"
		},
		"save": {
			"domain": "string",
			"file": "string"
		},
		"lxc_enter_namespace": {
			"domain": "string",
			"cmd": "string"
		},
		"blkdeviotune": {
			"device": "string",
			"domain": "string"
		},
		"pool_destroy": {
			"pool": "string"
		},
		"save_image_edit": {
			"file": "string"
		},
		"setmaxmem": {
			"domain": "string",
			"__size": "string"
		},
		"domifstat": {
			"_interface": "string",
			"domain": "string"
		},
		"nwfilter_binding_delete": {
			"binding": "string"
		},
		"secret_define": {
			"file": "string"
		},
		"detach_device_alias": {
			"alias": "string",
			"domain": "string"
		},
		"domuuid": {
			"domain": "string"
		},
		"iothreadadd": {
			"domain": "string",
			"__id": "string"
		},
		"desc": {
			"domain": "string"
		},
		"vcpucount": {
			"domain": "string"
		},
		"domcontrol": {
			"domain": "string"
		},
		"ttyconsole": {
			"domain": "string"
		},
		"edit": {
			"domain": "string"
		},
		"nodedev_dumpxml": {
			"device": "string"
		},
		"dommemstat": {
			"domain": "string"
		},
		"vcpuinfo": {
			"domain": "string"
		},
		"iface_name": {
			"_interface": "string"
		},
		"secret_undefine": {
			"secret": "string"
		},
		"net_name": {
			"network": "string"
		},
		"migrate_compcache": {
			"domain": "string"
		},
		"net_info": {
			"network": "string"
		},
		"metadata": {
			"domain": "string",
			"uri": "string"
		},
		"iface_bridge": {
			"_interface": "string",
			"bridge": "string"
		},
		"snapshot_edit": {
			"domain": "string"
		},
		"domblkstat": {
			"domain": "string"
		},
		"set_lifecycle_action": {
			"action": "string",
			"domain": "string",
			"type": "string"
		},
		"set_user_password": {
			"domain": "string",
			"password": "string",
			"user": "string"
		},
		"dump": {
			"domain": "string",
			"file": "string"
		},
		"nodedev_destroy": {
			"device": "string"
		},
		"managedsave_remove": {
			"domain": "string"
		},
		"iface_start": {
			"_interface": "string"
		},
		"net_update": {
			"xml": "string",
			"section": "string",
			"command": "string",
			"network": "string"
		},
		"detach__interface": {
			"domain": "string",
			"type": "string"
		},
		"snapshot_create_as": {
			"domain": "string"
		},
		"dompmwakeup": {
			"domain": "string"
		},
		"attach_disk": {
			"source": "string",
			"domain": "string",
			"target": "string"
		},
		"iothreadinfo": {
			"domain": "string"
		},
		"snapshot_revert": {
			"domain": "string"
		},
		"pool_edit": {
			"pool": "string"
		},
		"reboot": {
			"domain": "string"
		},
		"pool_undefine": {
			"pool": "string"
		},
		"vcpupin": {
			"domain": "string"
		},
		"migrate_getspeed": {
			"domain": "string"
		},
		"snapshot_create": {
			"domain": "string"
		},
		"change_media": {
			"path": "string",
			"domain": "string"
		},
		"managedsave_edit": {
			"domain": "string"
		},
		"domjobinfo": {
			"domain": "string"
		},
		"resume": {
			"domain": "string"
		},
		"vol_pool": {
			"vol": "string"
		},
		"nodedev_reset": {
			"device": "string"
		},
		"snapshot_current": {
			"domain": "string"
		},
		"pool_delete": {
			"pool": "string"
		},
		"detach_disk": {
			"domain": "string",
			"target": "string"
		},
		"setmem": {
			"domain": "string",
			"__size": "string"
		},
		"blockpull": {
			"path": "string",
			"domain": "string"
		},
		"vol_name": {
			"vol": "string"
		},
		"iface_destroy": {
			"_interface": "string"
		},
		"blockcommit": {
			"path": "string",
			"domain": "string"
		},
		"snapshot_parent": {
			"domain": "string"
		},
		"domfsthaw": {
			"domain": "string"
		},
		"iothreadpin": {
			"domain": "string",
			"__iothread": "string",
			"cpulist": "string"
		},
		"memtune": {
			"domain": "string"
		},
		"net_start": {
			"network": "string"
		},
		"net_define": {
			"file": "string"
		},
		"vol_key": {
			"vol": "string"
		},
		"pool_refresh": {
			"pool": "string"
		},
		"iface_define": {
			"file": "string"
		},
		"pool_create_as": {
			"type": "string",
			"name": "string"
		},
		"suspend": {
			"domain": "string"
		},
		"send_key": {
			"domain": "string",
			"keycode": "string"
		},
		"migrate_postcopy": {
			"domain": "string"
		},
		"vol_download": {
			"vol": "string",
			"file": "string"
		},
		"snapshot_info": {
			"domain": "string"
		},
		"domstate": {
			"domain": "string"
		},
		"shutdown": {
			"domain": "string"
		},
		"migrate_setmaxdowntime": {
			"domain": "string",
			"__downtime": "string"
		},
		"domfstrim": {
			"domain": "string"
		},
		"domxml_to_native": {
			"format": "string"
		},
		"iface_undefine": {
			"_interface": "string"
		},
		"schedinfo": {
			"domain": "string"
		},
		"nwfilter_edit": {
			"nwfilter": "string"
		},
		"net_dhcp_leases": {
			"network": "string"
		},
		"create": {
			"file": "string"
		},
		"save_image_dumpxml": {
			"file": "string"
		},
		"net_edit": {
			"network": "string"
		},
		"start": {
			"domain": "string"
		},
		"domifaddr": {
			"domain": "string"
		},
		"secret_dumpxml": {
			"secret": "string"
		},
		"attach__interface": {
			"source": "string",
			"domain": "string",
			"type": "string"
		},
		"iothreaddel": {
			"domain": "string",
			"__id": "string"
		},
		"qemu_agent_command": {
			"domain": "string",
			"cmd": "string"
		},
		"define": {
			"file": "string"
		},
		"blockcopy": {
			"path": "string",
			"domain": "string"
		},
		"find_storage_pool_sources": {
			"type": "string"
		},
		"domif_setlink": {
			"_interface": "string",
			"domain": "string",
			"state": "string"
		},
		"domtime": {
			"domain": "string"
		},
		"nodedev_reattach": {
			"device": "string"
		},
		"vol_info": {
			"vol": "string"
		},
		"send_process_signal": {
			"domain": "string",
			"pid": "string",
			"signame": "string"
		},
		"iface_dumpxml": {
			"_interface": "string"
		},
		"save_image_define": {
			"xml": "string",
			"file": "string"
		},
		"reset": {
			"domain": "string"
		},
		"vol_path": {
			"vol": "string"
		},
		"net_create": {
			"file": "string"
		},
		"nwfilter_binding_create": {
			"file": "string"
		},
		"iface_mac": {
			"_interface": "string"
		},
		"nwfilter_define": {
			"file": "string"
		},
		"pool_uuid": {
			"pool": "string"
		},
		"domblkinfo": {
			"domain": "string"
		},
		"qemu_monitor_command": {
			"domain": "string",
			"cmd": "string"
		},
		"iface_unbridge": {
			"bridge": "string"
		},
		"domrename": {
			"domain": "string",
			"new_name": "string"
		},
		"secret_get_value": {
			"secret": "string"
		},
		"migrate": {
			"domain": "string",
			"desturi": "string"
		},
		"vol_delete": {
			"vol": "string"
		},
		"nodedev_detach": {
			"device": "string"
		},
		"emulatorpin": {
			"domain": "string"
		},
		"domid": {
			"domain": "string"
		},
		"find_storage_pool_sources_as": {
			"type": "string"
		},
		"detach_device": {
			"domain": "string",
			"file": "string"
		},
		"domiftune": {
			"_interface": "string",
			"domain": "string"
		},
		"snapshot_dumpxml": {
			"snapshotname": "string",
			"domain": "string"
		},
		"nwfilter_dumpxml": {
			"nwfilter": "string"
		},
		"dominfo": {
			"domain": "string"
		},
		"net_destroy": {
			"network": "string"
		},
		"managedsave_dumpxml": {
			"domain": "string"
		},
		"pool_define_as": {
			"type": "string",
			"name": "string"
		},
		"pool_define": {
			"file": "string"
		},
		"pool_info": {
			"pool": "string"
		},
		"net_autostart": {
			"network": "string"
		},
		"destroy": {
			"domain": "string"
		},
		"vol_create_from": {
			"vol": "string",
			"file": "string",
			"pool": "string"
		},
		"migrate_setspeed": {
			"domain": "string",
			"__bandwidth": "string"
		},
		"managedsave": {
			"domain": "string"
		},
		"pool_name": {
			"pool": "string"
		},
		"screenshot": {
			"domain": "string"
		},
		"managedsave_define": {
			"xml": "string",
			"domain": "string"
		},
		"nwfilter_binding_dumpxml": {
			"binding": "string"
		},
		"vol_clone": {
			"vol": "string",
			"newname": "string"
		},
		"undefine": {
			"domain": "string"
		},
		"vol_wipe": {
			"vol": "string"
		},
		"pool_build": {
			"pool": "string"
		},
		"update_device": {
			"domain": "string",
			"file": "string"
		},
		"pool_dumpxml": {
			"pool": "string"
		},
		"domxml_from_native": {
			"config": "string",
			"format": "string"
		},
		"cpu_stats": {
			"domain": "string"
		},
		"blockjob": {
			"path": "string",
			"domain": "string"
		},
		"net_uuid": {
			"network": "string"
		},
		"inject_nmi": {
			"domain": "string"
		},
		"domname": {
			"domain": "string"
		},
		"snapshot_delete": {
			"domain": "string"
		},
		"dumpxml": {
			"domain": "string"
		},
		"pool_start": {
			"pool": "string"
		},
		"blkiotune": {
			"domain": "string"
		},
		"iface_edit": {
			"_interface": "string"
		},
		"blockresize": {
			"path": "string",
			"domain": "string",
			"__size": "string"
		},
		"vol_dumpxml": {
			"vol": "string"
		},
		"nodedev_create": {
			"file": "string"
		},
		"domblkerror": {
			"domain": "string"
		},
		"pool_create": {
			"file": "string"
		},
		"setvcpus": {
			"__count": "string",
			"domain": "string"
		},
		"install": {
			"__name": "string",
			"__memory": "string",
			"__vcpus": "string",
			"__cpu": "string",
			"__metadata": "string",
			"__cdrom": "string",
			"__location": "string",
			"__pxe": "string",
			"__import": "string",
			"__livecd": "string",
			"__extra_args": "string",
			"__initrd_inject": "string",
			"__os_variant": "string",
			"__boot": "string",
			"__idmap": "string",
			"__disk": "string",
			"__network": "string",
			"__graphics": "string",
			"__controller": "string",
			"__input": "string",
			"__serial": "string",
			"__parallel": "string",
			"__channel": "string",
			"__console": "string",
			"__hostdev": "string",
			"__filesystem": "string",
			"__sound": "string",
			"__watchdog": "string",
			"__smartcard": "string",
			"__redirdev": "string",
			"__memballoon": "string",
			"__tpm": "string",
			"__rng": "string",
			"__panic": "string",
			"__memdev": "string",
			"__security": "string",
			"__cputune": "string",
			"__numatune": "string",
			"__memtune": "string",
			"__blkiotune": "string",
			"__memorybacking": "string",
			"__features": "string",
			"__clock": "string",
			"__pm": "string",
			"__events": "string",
			"__resource": "string",
			"__sysinfo": "string",
			"__qemu_commandline": "string",
			"__hvm": "string",
			"__paravirt": "string",
			"__container": "string",
			"__virt_type": "string",
			"__arch": "string",
			"__machine": "string",
			"__autostart": "string",
			"__transient": "string",
			"__noreboot": "string",
			"__dry_run": "string",
			"__check": "string"
		},
		"clone": {
			"__original": "string",
			"__original_xml": "string",
			"__auto_clone": "string",
			"__name": "string",
			"__reflink": "string",
			"__file": "string",
			"__force_copy": "string",
			"__nonsparse": "string",
			"__preserve_data": "string",
			"__nvram": "string",
			"__mac": "string",
			"__replace": "string",
			"__check": "string"
		}
	}
}
```
