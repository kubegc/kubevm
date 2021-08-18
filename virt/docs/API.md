# 研发背景
       
       本项目拟扩展Kubernetes支持虚拟机生命周期管理，本文介绍API详细列表，Java SDK示例，以及Kubernetes验证方法。
			 
1. Java SDK： https://github.com/kubesys/kubeclient
2. JSON examples: https://github.com/kubesys/kubevirt/tree/master/examples
	
# 已知问题
			
1.  暂时不支持细粒度网络管理
3.  VirtualMachine的Domain对象是只读的，对虚拟机的修改：（1）标签修改：可修改VirtualMachine的Metadata；（2）对虚拟机在线操作可根据VirtualMachine的Lifecycle对象
4.  所有请求返回值都是VirtualMachine的Spec中Domain对象，见本文返回值。
5.  可以执行virsh命令获取更多帮助
6.  JSON中的noneName，请根据VM当前部署的物理机信息进行修改

# API列表



## API: createAndStartVMFromISO

**Desc**:create and start a Virtual Machine

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| name | String | Yes | Name of the guest instance | 
| memory | String | Yes | Configure guest memory allocation | 
| vcpus | String | No | Number of vcpus to configure for your guest | 
| cpu | String | No | CPU model and features | 
| metadata | String | No | Configure guest metadata | 
| cdrom | String | No | CD-ROM installation media | 
| location | String | No | Installation source | 
| pxe | String | No | Boot from the network using the PXE protocol | 
| livecd | String | No | Treat the CD-ROM media as a Live CD | 
| extra_args | String | No | Additional arguments to pass to the install kernel booted | 
| initrd_inject | String | No | Add given file to root of initrd | 
| os_variant | String | No | The OS variant being installed guests | 
| boot | String | No | Configure guest boot settings | 
| idmap | String | No | Enable user namespace for LXC container | 
| disk | String | No | Specify storage with various options | 
| network | String | No | Configure a guest network interface | 
| graphics | String | No | Configure guest display settings | 
| controller | String | No | Configure a guest controller device | 
| input | String | No | Configure a guest input device | 
| serial | String | No | Configure a guest serial device | 
| parallel | String | No | Configure a guest parallel device | 
| channel | String | No | Configure a guest communication channel | 
| console | String | No | Configure a text console connection between the guest and host | 
| hostdev | String | No | Configure a text console connection between the gues | 
| filesystem | String | No | Pass host directory to the guest | 
| sound | String | No | Configure guest sound device emulation | 
| watchdog | String | No | Configure a guest watchdog device | 
| smartcard | String | No | Configure a guest smartcard device | 
| redirdev | String | No | Configure a guest redirection device | 
| memballoon | String | No | Configure a guest memballoon device | 
| tpm | String | No | Configure a guest TPM device | 
| rng | String | No | Configure a guest RNG device | 
| panic | String | No | Configure a guest panic device | 
| memdev | String | No | Configure a guest memory device | 
| security | String | No | Set domain security driver configuration | 
| cputune | String | No | Tune CPU parameters for the domain process | 
| numatune | String | No | Tune NUMA policy for the domain process | 
| memtune | String | No | Tune memory policy for the domain process | 
| blkiotune | String | No | Tune blkio policy for the domain process | 
| memorybacking | String | No | Set memory backing policy for the domain process | 
| features | String | No | Set domain xml | 
| clock | String | No | Set domain clock | 
| pm | String | No | Configure VM power management features | 
| events | String | No | Configure VM lifecycle management policy | 
| resource | String | No | Configure VM resource partitioning | 
| sysinfo | String | No | Configure SMBIOS System Information | 
| qemu_commandline | String | No | Pass arguments directly to the qemu emulator | 
| hvm | String | No | This guest should be a fully virtualized guest | 
| paravirt | String | No | This guest should be a paravirtualized guest | 
| container | String | No | This guest should be a container guest | 
| virt_type | String | No | Hypervisor name to use | 
| arch | String | No | The CPU architecture to simulate | 
| machine | String | No | The machine type to emulate | 
| autostart | String | No | Have domain autostart on host boot up | 
| noreboot | String | No | Don't boot guest after completing install | 
| dry_run | String | No | Run through install process, but do not create devices or define the guest | 
| check | String | No | Enable or disable validation checks. | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = new VirtualMachine();
vm.setApiVersion("cloudplus.io/v1alpha3");
vm.setKind("VirtualMachine");
ObjectMeta metadata = new ObjectMeta();
metadata.setName("VM");
vm.setMetadata(metadata );
VirtualMachineSpec spec = new VirtualMachineSpec();
Lifecycle lifecycle = new Lifecycle();
createAndStartVMFromISO createAndStartVM = new createAndStartVMFromISO();
{
	createAndStartVM.setName("string");
	createAndStartVM.setMemory("string");
	createAndStartVM.setVcpus("string");
	createAndStartVM.setCpu("string");
	createAndStartVM.setMetadata("string");
	createAndStartVM.setCdrom("string");
	createAndStartVM.setLocation("string");
	createAndStartVM.setPxe("string");
	createAndStartVM.setLivecd("string");
	createAndStartVM.setExtra_args("string");
	createAndStartVM.setInitrd_inject("string");
	createAndStartVM.setOs_variant("string");
	createAndStartVM.setBoot("string");
	createAndStartVM.setIdmap("string");
	createAndStartVM.setDisk("string");
	createAndStartVM.setNetwork("string");
	createAndStartVM.setGraphics("string");
	createAndStartVM.setController("string");
	createAndStartVM.setInput("string");
	createAndStartVM.setSerial("string");
	createAndStartVM.setParallel("string");
	createAndStartVM.setChannel("string");
	createAndStartVM.setConsole("string");
	createAndStartVM.setHostdev("string");
	createAndStartVM.setFilesystem("string");
	createAndStartVM.setSound("string");
	createAndStartVM.setWatchdog("string");
	createAndStartVM.setSmartcard("string");
	createAndStartVM.setRedirdev("string");
	createAndStartVM.setMemballoon("string");
	createAndStartVM.setTpm("string");
	createAndStartVM.setRng("string");
	createAndStartVM.setPanic("string");
	createAndStartVM.setMemdev("string");
	createAndStartVM.setSecurity("string");
	createAndStartVM.setCputune("string");
	createAndStartVM.setNumatune("string");
	createAndStartVM.setMemtune("string");
	createAndStartVM.setBlkiotune("string");
	createAndStartVM.setMemorybacking("string");
	createAndStartVM.setFeatures("string");
	createAndStartVM.setClock("string");
	createAndStartVM.setPm("string");
	createAndStartVM.setEvents("string");
	createAndStartVM.setResource("string");
	createAndStartVM.setSysinfo("string");
	createAndStartVM.setQemu_commandline("string");
	createAndStartVM.setHvm("string");
	createAndStartVM.setParavirt("string");
	createAndStartVM.setContainer("string");
	createAndStartVM.setVirt_type("string");
	createAndStartVM.setArch("string");
	createAndStartVM.setMachine("string");
	createAndStartVM.setAutostart("string");
	createAndStartVM.setNoreboot("string");
	createAndStartVM.setDry_run("string");
	createAndStartVM.setCheck("string");
}
lifecycle.setCreateAndStartVM(createAndStartVM)
spec.setLifecycle(lifecycle );
vm.setSpec(spec );
vmi.create(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "image": "CentOS7.iso",
        "lifecycle": {
            "createAndStartVM": {
                "arch": "String",
                "autostart": "String",
                "blkiotune": "String",
                "boot": "String",
                "cdrom": "String",
                "channel": "String",
                "check": "String",
                "clock": "String",
                "console": "String",
                "container": "String",
                "controller": "String",
                "cpu": "String",
                "cputune": "String",
                "disk": "String",
                "dry_run": "String",
                "events": "String",
                "extra_args": "String",
                "features": "String",
                "filesystem": "String",
                "graphics": "String",
                "hostdev": "String",
                "hvm": "String",
                "idmap": "String",
                "import": "String",
                "initrd_inject": "String",
                "input": "String",
                "livecd": "String",
                "location": "String",
                "machine": "String",
                "memballoon": "String",
                "memdev": "String",
                "memory": "String",
                "memorybacking": "String",
                "memtune": "String",
                "metadata": "String",
                "name": "String",
                "network": "String",
                "noreboot": "String",
                "numatune": "String",
                "os_variant": "String",
                "panic": "String",
                "parallel": "String",
                "paravirt": "String",
                "pm": "String",
                "pxe": "String",
                "qemu_commandline": "String",
                "redirdev": "String",
                "resource": "String",
                "rng": "String",
                "security": "String",
                "serial": "String",
                "smartcard": "String",
                "sound": "String",
                "sysinfo": "String",
                "tpm": "String",
                "transient": "String",
                "vcpus": "String",
                "virt_type": "String",
                "watchdog": "String"
            }
        }
    }
}
```


## API: createVM

**Desc**:create a domain from an XML file

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| file | String | Yes | file containing an XML domain description | 
| console | Boolean | No | attach to console after creation | 
| paused | Boolean | No | leave the guest paused after creation | 
| autodestroy | Boolean | No | automatically destroy the guest when virsh disconnects | 
| pass-fds | String | No | pass file descriptors N,M,... to the guest | 
| validate | Boolean | No | validate the XML against the schema | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
CreateVM createVM = new CreateVM();
{
	createVM.setFile("string");
	createVM.setConsole(true);
	createVM.setPaused(true);
	createVM.setAutodestroy(true);
	createVM.setPass-fds("string");
	createVM.setValidate(true);
}
lifecycle.setCreateVM(createVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "createVM": {
                "autodestroy": true,
                "console": true,
                "file": "String",
                "pass-fds": "String",
                "paused": true,
                "validate": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: startVM

**Desc**:start a (previously defined) inactive domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | name of the inactive domain | 
| console | Boolean | No | attach to console after creation | 
| paused | Boolean | No | leave the guest paused after creation | 
| autodestroy | Boolean | No | automatically destroy the guest when virsh disconnects | 
| bypass-cache | Boolean | No | avoid file system cache when loading | 
| force-boot | Boolean | No | force fresh boot by discarding any managed save | 
| pass-fds | String | No | pass file descriptors N,M,... to the guest | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
StartVM startVM = new StartVM();
{
	startVM.setDomain("string");
	startVM.setConsole(true);
	startVM.setPaused(true);
	startVM.setAutodestroy(true);
	startVM.setBypass-cache(true);
	startVM.setForce-boot(true);
	startVM.setPass-fds("string");
}
lifecycle.setStartVM(startVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "startVM": {
                "autodestroy": true,
                "bypass-cache": true,
                "console": true,
                "domain": "String",
                "force-boot": true,
                "pass-fds": "String",
                "paused": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: stopVM

**Desc**:gracefully shutdown a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| mode | String | No | shutdown mode: acpi|agent|initctl|signal|paravirt | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
StopVM stopVM = new StopVM();
{
	stopVM.setDomain("string");
	stopVM.setMode("string");
}
lifecycle.setStopVM(stopVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "stopVM": {
                "domain": "String",
                "mode": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: stopVMForce

**Desc**:destroy (stop) a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| graceful | Boolean | No | terminate gracefully | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
StopVMForce stopVMForce = new StopVMForce();
{
	stopVMForce.setDomain("string");
	stopVMForce.setGraceful(true);
}
lifecycle.setStopVMForce(stopVMForce)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "stopVMForce": {
                "domain": "String",
                "graceful": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: deleteVM

**Desc**:undefine a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| managed-save | Boolean | No | remove domain managed state file | 
| storage | String | No | remove associated storage volumes (comma separated list of targets or source paths) (see domblklist) | 
| remove-all-storage | Boolean | No | remove all associated storage volumes (use with caution) | 
| delete-snapshots | Boolean | No | delete snapshots associated with volume(s), requires --remove-all-storage (must be supported by storage driver) | 
| wipe-storage | Boolean | No | wipe data on the removed volumes | 
| snapshots-metadata | Boolean | No | remove all domain snapshot metadata, if inactive | 
| nvram | Boolean | No | remove nvram file, if inactive | 
| keep-nvram | Boolean | No | keep nvram file, if inactive | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
DeleteVM deleteVM = new DeleteVM();
{
	deleteVM.setDomain("string");
	deleteVM.setManaged-save(true);
	deleteVM.setStorage("string");
	deleteVM.setRemove-all-storage(true);
	deleteVM.setDelete-snapshots(true);
	deleteVM.setWipe-storage(true);
	deleteVM.setSnapshots-metadata(true);
	deleteVM.setNvram(true);
	deleteVM.setKeep-nvram(true);
}
lifecycle.setDeleteVM(deleteVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "deleteVM": {
                "delete-snapshots": true,
                "domain": "String",
                "keep-nvram": true,
                "managed-save": true,
                "nvram": true,
                "remove-all-storage": true,
                "snapshots-metadata": true,
                "storage": "String",
                "wipe-storage": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: rebootVM

**Desc**:reboot a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| mode | String | No | shutdown mode: acpi|agent|initctl|signal|paravirt | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
RebootVM rebootVM = new RebootVM();
{
	rebootVM.setDomain("string");
	rebootVM.setMode("string");
}
lifecycle.setRebootVM(rebootVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "rebootVM": {
                "domain": "String",
                "mode": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: resetVM

**Desc**:reset a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
ResetVM resetVM = new ResetVM();
{
	resetVM.setDomain("string");
}
lifecycle.setResetVM(resetVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "resetVM": {
                "domain": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: resumeVM

**Desc**:resume a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
ResumeVM resumeVM = new ResumeVM();
{
	resumeVM.setDomain("string");
}
lifecycle.setResumeVM(resumeVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "resumeVM": {
                "domain": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: suspendVM

**Desc**:suspend a domain

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
SuspendVM suspendVM = new SuspendVM();
{
	suspendVM.setDomain("string");
}
lifecycle.setSuspendVM(suspendVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "suspendVM": {
                "domain": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: saveVM

**Desc**:save a domain state to a file

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| file | String | Yes | where to save the data | 
| bypass-cache | Boolean | No | avoid file system cache when saving | 
| xml | String | No | filename containing updated XML for the target | 
| running | Boolean | No | set domain to be running on restore | 
| paused | Boolean | No | set domain to be paused on restore | 
| verbose | Boolean | No | display the progress of save | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
SaveVM saveVM = new SaveVM();
{
	saveVM.setDomain("string");
	saveVM.setFile("string");
	saveVM.setBypass-cache(true);
	saveVM.setXml("string");
	saveVM.setRunning(true);
	saveVM.setPaused(true);
	saveVM.setVerbose(true);
}
lifecycle.setSaveVM(saveVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "saveVM": {
                "bypass-cache": true,
                "domain": "String",
                "file": "String",
                "paused": true,
                "running": true,
                "verbose": true,
                "xml": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: restoreVM

**Desc**:restore a domain from a saved state in a file

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| file | String | Yes | the state to restore | 
| bypass-cache | Boolean | No | avoid file system cache when restoring | 
| xml | String | No | filename containing updated XML for the target | 
| running | Boolean | No | restore domain into running state | 
| paused | Boolean | No | restore domain into paused state | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
RestoreVM restoreVM = new RestoreVM();
{
	restoreVM.setFile("string");
	restoreVM.setBypass-cache(true);
	restoreVM.setXml("string");
	restoreVM.setRunning(true);
	restoreVM.setPaused(true);
}
lifecycle.setRestoreVM(restoreVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "restoreVM": {
                "bypass-cache": true,
                "file": "String",
                "paused": true,
                "running": true,
                "xml": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: migrateVM

**Desc**:migrate domain to another host

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| desturi | String | Yes | connection URI of the destination host as seen from the client(normal migration) or source(p2p migration) | 
| live | Boolean | No | live migration | 
| offline | Boolean | No | offline migration | 
| p2p | Boolean | No | peer-2-peer migration | 
| direct | Boolean | No | direct migration | 
| tunnelled | Boolean | No | tunnelled migration | 
| persistent | Boolean | No | persist VM on destination | 
| undefinesource | Boolean | No | undefine VM on source | 
| suspend | Boolean | No | do not restart the domain on the destination host | 
| copy-storage-all | Boolean | No | migration with non-shared storage with full disk copy | 
| copy-storage-inc | Boolean | No | migration with non-shared storage with incremental copy (same base image shared between source and destination) | 
| change-protection | Boolean | No | prevent any configuration changes to domain until migration ends | 
| unsafe | Boolean | No | force migration even if it may be unsafe | 
| verbose | Boolean | No | display the progress of migration | 
| compressed | Boolean | No | compress repeated pages during live migration | 
| auto-converge | Boolean | No | force convergence during live migration | 
| rdma-pin-all | Boolean | No | pin all memory before starting RDMA live migration | 
| abort-on-error | Boolean | No | abort on soft errors during migration | 
| postcopy | Boolean | No | enable post-copy migration; switch to it using migrate-postcopy command | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
MigrateVM migrateVM = new MigrateVM();
{
	migrateVM.setDomain("string");
	migrateVM.setDesturi("string");
	migrateVM.setLive(true);
	migrateVM.setOffline(true);
	migrateVM.setP2p(true);
	migrateVM.setDirect(true);
	migrateVM.setTunnelled(true);
	migrateVM.setPersistent(true);
	migrateVM.setUndefinesource(true);
	migrateVM.setSuspend(true);
	migrateVM.setCopy-storage-all(true);
	migrateVM.setCopy-storage-inc(true);
	migrateVM.setChange-protection(true);
	migrateVM.setUnsafe(true);
	migrateVM.setVerbose(true);
	migrateVM.setCompressed(true);
	migrateVM.setAuto-converge(true);
	migrateVM.setRdma-pin-all(true);
	migrateVM.setAbort-on-error(true);
	migrateVM.setPostcopy(true);
}
lifecycle.setMigrateVM(migrateVM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "migrateVM": {
                "abort-on-error": true,
                "auto-converge": true,
                "change-protection": true,
                "compressed": true,
                "copy-storage-all": true,
                "copy-storage-inc": true,
                "desturi": "String",
                "direct": true,
                "domain": "String",
                "live": true,
                "offline": true,
                "p2p": true,
                "persistent": true,
                "postcopy": true,
                "rdma-pin-all": true,
                "suspend": true,
                "tunnelled": true,
                "undefinesource": true,
                "unsafe": true,
                "verbose": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: plugDevice

**Desc**:attach device from an XML file

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| file | String | Yes | XML file | 
| persistent | Boolean | No | make live change persistent | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
PlugDevice plugDevice = new PlugDevice();
{
	plugDevice.setDomain("string");
	plugDevice.setFile("string");
	plugDevice.setPersistent(true);
	plugDevice.setConfig(true);
	plugDevice.setLive(true);
	plugDevice.setCurrent(true);
}
lifecycle.setPlugDevice(plugDevice)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "plugDevice": {
                "config": true,
                "current": true,
                "domain": "String",
                "file": "String",
                "live": true,
                "persistent": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: unplugDevice

**Desc**:detach device from an XML file

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| file | String | Yes | XML file | 
| persistent | Boolean | No | make live change persistent | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
UnplugDevice unplugDevice = new UnplugDevice();
{
	unplugDevice.setDomain("string");
	unplugDevice.setFile("string");
	unplugDevice.setPersistent(true);
	unplugDevice.setConfig(true);
	unplugDevice.setLive(true);
	unplugDevice.setCurrent(true);
}
lifecycle.setUnplugDevice(unplugDevice)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "unplugDevice": {
                "config": true,
                "current": true,
                "domain": "String",
                "file": "String",
                "live": true,
                "persistent": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: plugDisk

**Desc**:attach disk device

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| source | String | Yes | source of disk device | 
| target | String | Yes | target of disk device | 
| targetbus | String | No | target bus of disk device | 
| driver | String | No | driver of disk device | 
| subdriver | String | No | subdriver of disk device | 
| iothread | String | No | IOThread to be used by supported device | 
| cache | String | No | cache mode of disk device | 
| io | String | No | io policy of disk device | 
| type | String | No | target device type | 
| mode | String | No | mode of device reading and writing | 
| sourcetype | String | No | type of source (block|file) | 
| serial | String | No | serial of disk device | 
| wwn | String | No | wwn of disk device | 
| rawio | Boolean | No | needs rawio capability | 
| address | String | No | address of disk device | 
| multifunction | Boolean | No | use multifunction pci under specified address | 
| print-xml | Boolean | No | print XML document rather than attach the disk | 
| persistent | Boolean | No | make live change persistent | 
| config | Boolean | No | affect next boot | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
PlugDisk plugDisk = new PlugDisk();
{
	plugDisk.setDomain("string");
	plugDisk.setSource("string");
	plugDisk.setTarget("string");
	plugDisk.setTargetbus("string");
	plugDisk.setDriver("string");
	plugDisk.setSubdriver("string");
	plugDisk.setIothread("string");
	plugDisk.setCache("string");
	plugDisk.setIo("string");
	plugDisk.setType("string");
	plugDisk.setMode("string");
	plugDisk.setSourcetype("string");
	plugDisk.setSerial("string");
	plugDisk.setWwn("string");
	plugDisk.setRawio(true);
	plugDisk.setAddress("string");
	plugDisk.setMultifunction(true);
	plugDisk.setPrint-xml(true);
	plugDisk.setPersistent(true);
	plugDisk.setConfig(true);
}
lifecycle.setPlugDisk(plugDisk)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "plugDisk": {
                "address": "String",
                "cache": "String",
                "config": true,
                "domain": "String",
                "driver": "String",
                "io": "String",
                "iothread": "String",
                "mode": "String",
                "multifunction": true,
                "persistent": true,
                "print-xml": true,
                "rawio": true,
                "serial": "String",
                "source": "String",
                "sourcetype": "String",
                "subdriver": "String",
                "target": "String",
                "targetbus": "String",
                "type": "String",
                "wwn": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: unplugDisk

**Desc**:detach disk device

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| target | String | Yes | target of disk device | 
| persistent | Boolean | No | make live change persistent | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 
| print-xml | Boolean | No | print XML document rather than detach the disk | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
UnplugDisk unplugDisk = new UnplugDisk();
{
	unplugDisk.setDomain("string");
	unplugDisk.setTarget("string");
	unplugDisk.setPersistent(true);
	unplugDisk.setConfig(true);
	unplugDisk.setLive(true);
	unplugDisk.setCurrent(true);
	unplugDisk.setPrint-xml(true);
}
lifecycle.setUnplugDisk(unplugDisk)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "unplugDisk": {
                "config": true,
                "current": true,
                "domain": "String",
                "live": true,
                "persistent": true,
                "print-xml": true,
                "target": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: plugNIC

**Desc**:attach network interface

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| type | String | Yes | network interface type | 
| source | String | Yes | source of network interface | 
| target | String | No | target network name | 
| mac | String | No | MAC address | 
| script | String | No | script used to bridge network interface | 
| model | String | No | model type | 
| inbound | String | No | control domain's incoming traffics | 
| outbound | String | No | control domain's outgoing traffics | 
| persistent | Boolean | No | make live change persistent | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 
| print-xml | Boolean | No | print XML document rather than attach the interface | 
| managed | Boolean | No | libvirt will automatically detach/attach the device from/to host | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
PlugNIC plugNIC = new PlugNIC();
{
	plugNIC.setDomain("string");
	plugNIC.setType("string");
	plugNIC.setSource("string");
	plugNIC.setTarget("string");
	plugNIC.setMac("string");
	plugNIC.setScript("string");
	plugNIC.setModel("string");
	plugNIC.setInbound("string");
	plugNIC.setOutbound("string");
	plugNIC.setPersistent(true);
	plugNIC.setConfig(true);
	plugNIC.setLive(true);
	plugNIC.setCurrent(true);
	plugNIC.setPrint-xml(true);
	plugNIC.setManaged(true);
}
lifecycle.setPlugNIC(plugNIC)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "plugNIC": {
                "config": true,
                "current": true,
                "domain": "String",
                "inbound": "String",
                "live": true,
                "mac": "String",
                "managed": true,
                "model": "String",
                "outbound": "String",
                "persistent": true,
                "print-xml": true,
                "script": "String",
                "source": "String",
                "target": "String",
                "type": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: unplugNIC

**Desc**:detach network interface

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| type | String | Yes | network interface type | 
| mac | String | No | MAC address | 
| persistent | Boolean | No | make live change persistent | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
UnplugNIC unplugNIC = new UnplugNIC();
{
	unplugNIC.setDomain("string");
	unplugNIC.setType("string");
	unplugNIC.setMac("string");
	unplugNIC.setPersistent(true);
	unplugNIC.setConfig(true);
	unplugNIC.setLive(true);
	unplugNIC.setCurrent(true);
}
lifecycle.setUnplugNIC(unplugNIC)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "unplugNIC": {
                "config": true,
                "current": true,
                "domain": "String",
                "live": true,
                "mac": "String",
                "persistent": true,
                "type": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: createSnapshot

**Desc**:Create a snapshot from a set of args

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| name | String | No | name of snapshot | 
| description | String | No | description of snapshot | 
| print-xml | Boolean | No | print XML document rather than create | 
| no-metadata | Boolean | No | take snapshot but create no metadata | 
| halt | Boolean | No | halt domain after snapshot is created | 
| disk-only | Boolean | No | capture disk state but not vm state | 
| reuse-external | Boolean | No | reuse any existing external files | 
| quiesce | Boolean | No | quiesce guest's file systems | 
| atomic | Boolean | No | require atomic operation | 
| live | Boolean | No | take a live snapshot | 
| memspec | String | No | memory attributes: file=name,snapshot=type | 
| diskspec | String | No | disk attributes: disk,snapshot=type,driver=type,file=name | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
CreateSnapshot createSnapshot = new CreateSnapshot();
{
	createSnapshot.setDomain("string");
	createSnapshot.setName("string");
	createSnapshot.setDescription("string");
	createSnapshot.setPrint-xml(true);
	createSnapshot.setNo-metadata(true);
	createSnapshot.setHalt(true);
	createSnapshot.setDisk-only(true);
	createSnapshot.setReuse-external(true);
	createSnapshot.setQuiesce(true);
	createSnapshot.setAtomic(true);
	createSnapshot.setLive(true);
	createSnapshot.setMemspec("string");
	createSnapshot.setDiskspec("string");
}
lifecycle.setCreateSnapshot(createSnapshot)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "createSnapshot": {
                "atomic": true,
                "description": "String",
                "disk-only": true,
                "diskspec": "String",
                "domain": "String",
                "halt": true,
                "live": true,
                "memspec": "String",
                "name": "String",
                "no-metadata": true,
                "print-xml": true,
                "quiesce": true,
                "reuse-external": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: deleteSnapshot

**Desc**:Delete a domain snapshot

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| snapshotname | String | No | snapshot name | 
| current | Boolean | No | delete current snapshot | 
| children | Boolean | No | delete snapshot and all children | 
| children-only | Boolean | No | delete children but not snapshot | 
| metadata | Boolean | No | delete only libvirt metadata, leaving snapshot contents behind | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
DeleteSnapshot deleteSnapshot = new DeleteSnapshot();
{
	deleteSnapshot.setDomain("string");
	deleteSnapshot.setSnapshotname("string");
	deleteSnapshot.setCurrent(true);
	deleteSnapshot.setChildren(true);
	deleteSnapshot.setChildren-only(true);
	deleteSnapshot.setMetadata(true);
}
lifecycle.setDeleteSnapshot(deleteSnapshot)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "deleteSnapshot": {
                "children": true,
                "children-only": true,
                "current": true,
                "domain": "String",
                "metadata": true,
                "snapshotname": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: createDisk

**Desc**:create a volume from a set of args

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| pool | String | Yes | pool name | 
| name | String | Yes | name of the volume | 
| capacity | String | Yes | size of the vol, as scaled integer (default bytes) | 
| allocation | String | No | initial allocation size, as scaled integer (default bytes) | 
| format | String | No | file format type raw,bochs,qcow,qcow2,qed,vmdk | 
| backing-vol | String | No | the backing volume if taking a snapshot | 
| backing-vol-format | String | No | format of backing volume if taking a snapshot | 
| prealloc-metadata | Boolean | No | preallocate metadata (for qcow2 instead of full allocation) | 
| print-xml | Boolean | No | print XML document, but don't define/create | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
CreateDisk createDisk = new CreateDisk();
{
	createDisk.setPool("string");
	createDisk.setName("string");
	createDisk.setCapacity("string");
	createDisk.setAllocation("string");
	createDisk.setFormat("string");
	createDisk.setBacking-vol("string");
	createDisk.setBacking-vol-format("string");
	createDisk.setPrealloc-metadata(true);
	createDisk.setPrint-xml(true);
}
lifecycle.setCreateDisk(createDisk)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "createDisk": {
                "allocation": "String",
                "backing-vol": "String",
                "backing-vol-format": "String",
                "capacity": "String",
                "format": "String",
                "name": "String",
                "pool": "String",
                "prealloc-metadata": true,
                "print-xml": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: resizeDisk

**Desc**:resize a vol

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| vol | String | Yes | vol name, key or path | 
| capacity | String | Yes | new capacity for the vol, as scaled integer (default bytes) | 
| pool | String | No | pool name or uuid | 
| allocate | Boolean | No | allocate the new capacity, rather than leaving it sparse | 
| delta | Boolean | No | use capacity as a delta to current size, rather than the new size | 
| shrink | Boolean | No | allow the resize to shrink the volume | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
ResizeDisk resizeDisk = new ResizeDisk();
{
	resizeDisk.setVol("string");
	resizeDisk.setCapacity("string");
	resizeDisk.setPool("string");
	resizeDisk.setAllocate(true);
	resizeDisk.setDelta(true);
	resizeDisk.setShrink(true);
}
lifecycle.setResizeDisk(resizeDisk)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "resizeDisk": {
                "allocate": true,
                "capacity": "String",
                "delta": true,
                "pool": "String",
                "shrink": true,
                "vol": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: cloneDisk

**Desc**:clone a volume.

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| vol | String | Yes | vol name, key or path | 
| newname | String | Yes | clone name | 
| pool | String | No | pool name or uuid | 
| prealloc-metadata | Boolean | No | preallocate metadata (for qcow2 instead of full allocation) | 
| reflink | Boolean | No | use btrfs COW lightweight copy | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
CloneDisk cloneDisk = new CloneDisk();
{
	cloneDisk.setVol("string");
	cloneDisk.setNewname("string");
	cloneDisk.setPool("string");
	cloneDisk.setPrealloc-metadata(true);
	cloneDisk.setReflink(true);
}
lifecycle.setCloneDisk(cloneDisk)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "cloneDisk": {
                "newname": "String",
                "pool": "String",
                "prealloc-metadata": true,
                "reflink": true,
                "vol": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: deleteDisk

**Desc**:delete a vol

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| vol | String | Yes | vol name, key or path | 
| pool | String | No | pool name or uuid | 
| delete-snapshots | Boolean | No | delete snapshots associated with volume (must be supported by storage driver) | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
DeleteDisk deleteDisk = new DeleteDisk();
{
	deleteDisk.setVol("string");
	deleteDisk.setPool("string");
	deleteDisk.setDelete-snapshots(true);
}
lifecycle.setDeleteDisk(deleteDisk)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "deleteDisk": {
                "delete-snapshots": true,
                "pool": "String",
                "vol": "String"
            }
        },
        "nodeName": "node22"
    }
}
```


## API: changeNumberOfCPU

**Desc**:change number of virtual CPUs

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| count | Integer | Yes | number of virtual CPUs | 
| maximum | Boolean | No | set maximum limit on next boot | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 
| guest | Boolean | No | modify cpu state in the guest | 
| hotpluggable | Boolean | No | make added vcpus hot(un)pluggable | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
ChangeNumberOfCPU changeNumberOfCPU = new ChangeNumberOfCPU();
{
	changeNumberOfCPU.setDomain("string");
	changeNumberOfCPU.setCount(1);
	changeNumberOfCPU.setMaximum(true);
	changeNumberOfCPU.setConfig(true);
	changeNumberOfCPU.setLive(true);
	changeNumberOfCPU.setCurrent(true);
	changeNumberOfCPU.setGuest(true);
	changeNumberOfCPU.setHotpluggable(true);
}
lifecycle.setChangeNumberOfCPU(changeNumberOfCPU)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "changeNumberOfCPU": {
                "config": true,
                "count": 1,
                "current": true,
                "domain": "String",
                "guest": true,
                "hotpluggable": true,
                "live": true,
                "maximum": true
            }
        },
        "nodeName": "node22"
    }
}
```


## API: resizeRAM

**Desc**:change memory allocation

**Parameters**:

| name |  type  | optional | description|
| ----- | ------ | ------ | ------ |
| domain | String | Yes | domain name, id or uuid | 
| size | Integer | Yes | new memory size, as scaled integer (default KiB) | 
| config | Boolean | No | affect next boot | 
| live | Boolean | No | affect running domain | 
| current | Boolean | No | affect current domain | 

**Sample**:

```
ExtendedKubernetesClient client =
	ExtendedKubernetesClient.defaultConfig("config");
VirtualMachineImpl vmi = client.virtualMachines();
VirtualMachine vm = vmi.get("VM");
VirtualMachineSpec spec = vm.getSpec();
Lifecycle lifecycle = new Lifecycle();
ResizeRAM resizeRAM = new ResizeRAM();
{
	resizeRAM.setDomain("string");
	resizeRAM.setSize(1);
	resizeRAM.setConfig(true);
	resizeRAM.setLive(true);
	resizeRAM.setCurrent(true);
}
lifecycle.setResizeRAM(resizeRAM)
spec.setLifecycle(lifecycle );
vmi.update(vm );
```

**JSON**:

```
{
    "apiVersion": "cloudplus.io/v1alpha3",
    "kind": "VirtualMachine",
    "metadata": {
        "name": "VM"
    },
    "spec": {
        "domain": {
            "name": {
                "text": "CentOS"
            }
        },
        "image": "CentOS7.iso",
        "lifecycle": {
            "resizeRAM": {
                "config": true,
                "current": true,
                "domain": "String",
                "live": true,
                "size": 1
            }
        },
        "nodeName": "node22"
    }
}
```

# 返回值

以下是可能支持的所有返回值，实际返回值只是其中一部分，该对象是只读的
client.VirtualMachine().getSpec().getDomain()

如果你觉得返回值过于复杂，可以设计你需要的样式，我们会提供自动转换器进行适配。

```
{
    "domain": {
        "_id": "string",
        "_type": "string",
        "blkiotune": {
            "device": [
                {
                    "path": {
                        "text": "string"
                    },
                    "read_bytes_sec": {
                        "text": "string"
                    },
                    "read_iops_sec": {
                        "text": "string"
                    },
                    "weight": {
                        "text": "string"
                    },
                    "write_bytes_sec": {
                        "text": "string"
                    },
                    "write_iops_sec": {
                        "text": "string"
                    }
                },
                {
                    "path": {
                        "text": "string"
                    },
                    "read_bytes_sec": {
                        "text": "string"
                    },
                    "read_iops_sec": {
                        "text": "string"
                    },
                    "weight": {
                        "text": "string"
                    },
                    "write_bytes_sec": {
                        "text": "string"
                    },
                    "write_iops_sec": {
                        "text": "string"
                    }
                }
            ],
            "weight": {
                "text": "string"
            }
        },
        "bootloader": {
            "text": "string"
        },
        "bootloader_args": {
            "text": "string"
        },
        "clock": {
            "_adjustment": "string",
            "_basis": "string",
            "_offset": "string",
            "_timezone": "string",
            "timer": [
                {
                    "_frequency": "string",
                    "_mode": "string",
                    "_name": "string",
                    "_present": "string",
                    "_tickpolicy": "string",
                    "_track": "string",
                    "catchup": {
                        "_limit": "string",
                        "_slew": "string",
                        "_threshold": "string"
                    }
                },
                {
                    "_frequency": "string",
                    "_mode": "string",
                    "_name": "string",
                    "_present": "string",
                    "_tickpolicy": "string",
                    "_track": "string",
                    "catchup": {
                        "_limit": "string",
                        "_slew": "string",
                        "_threshold": "string"
                    }
                }
            ]
        },
        "cpu": {
            "_check": "string",
            "_match": "string",
            "_mode": "string",
            "cache": {
                "_level": "string",
                "_mode": "string"
            },
            "feature": [
                {
                    "_name": "string",
                    "_policy": "string"
                },
                {
                    "_name": "string",
                    "_policy": "string"
                }
            ],
            "model": {
                "text": "string",
                "_fallback": "string",
                "_vendor_id": "string"
            },
            "numa": {
                "cell": [
                    {
                        "_cpus": "string",
                        "_discard": "string",
                        "_id": "string",
                        "_memAccess": "string",
                        "_memory": "string",
                        "_unit": "string",
                        "distances": {
                            "sibling": [
                                {
                                    "_id": "string",
                                    "_value": "string"
                                },
                                {
                                    "_id": "string",
                                    "_value": "string"
                                }
                            ]
                        }
                    },
                    {
                        "_cpus": "string",
                        "_discard": "string",
                        "_id": "string",
                        "_memAccess": "string",
                        "_memory": "string",
                        "_unit": "string",
                        "distances": {
                            "sibling": [
                                {
                                    "_id": "string",
                                    "_value": "string"
                                },
                                {
                                    "_id": "string",
                                    "_value": "string"
                                }
                            ]
                        }
                    }
                ]
            },
            "topology": {
                "_cores": "string",
                "_sockets": "string",
                "_threads": "string"
            },
            "vendor": {
                "text": "string"
            }
        },
        "cputune": {
            "cachetune": [
                {
                    "_vcpus": "string",
                    "cache": [
                        {
                            "_id": "string",
                            "_level": "string",
                            "_size": "string",
                            "_type": "string",
                            "_unit": "string"
                        },
                        {
                            "_id": "string",
                            "_level": "string",
                            "_size": "string",
                            "_type": "string",
                            "_unit": "string"
                        }
                    ],
                    "monitor": [
                        {
                            "_level": "string",
                            "_vcpus": "string"
                        },
                        {
                            "_level": "string",
                            "_vcpus": "string"
                        }
                    ]
                },
                {
                    "_vcpus": "string",
                    "cache": [
                        {
                            "_id": "string",
                            "_level": "string",
                            "_size": "string",
                            "_type": "string",
                            "_unit": "string"
                        },
                        {
                            "_id": "string",
                            "_level": "string",
                            "_size": "string",
                            "_type": "string",
                            "_unit": "string"
                        }
                    ],
                    "monitor": [
                        {
                            "_level": "string",
                            "_vcpus": "string"
                        },
                        {
                            "_level": "string",
                            "_vcpus": "string"
                        }
                    ]
                }
            ],
            "emulator_period": {
                "text": "string"
            },
            "emulator_quota": {
                "text": "string"
            },
            "emulatorpin": {
                "_cpuset": "string"
            },
            "global_period": {
                "text": "string"
            },
            "global_quota": {
                "text": "string"
            },
            "iothread_period": {
                "text": "string"
            },
            "iothread_quota": {
                "text": "string"
            },
            "iothreadpin": [
                {
                    "_cpuset": "string",
                    "_iothread": "string"
                },
                {
                    "_cpuset": "string",
                    "_iothread": "string"
                }
            ],
            "iothreadsched": [
                {
                    "_iothreads": "string",
                    "_priority": "string",
                    "_scheduler": "string"
                },
                {
                    "_iothreads": "string",
                    "_priority": "string",
                    "_scheduler": "string"
                }
            ],
            "memorytune": [
                {
                    "_vcpus": "string",
                    "node": [
                        {
                            "_bandwidth": "string",
                            "_id": "string"
                        },
                        {
                            "_bandwidth": "string",
                            "_id": "string"
                        }
                    ]
                },
                {
                    "_vcpus": "string",
                    "node": [
                        {
                            "_bandwidth": "string",
                            "_id": "string"
                        },
                        {
                            "_bandwidth": "string",
                            "_id": "string"
                        }
                    ]
                }
            ],
            "period": {
                "text": "string"
            },
            "quota": {
                "text": "string"
            },
            "shares": {
                "text": "string"
            },
            "vcpupin": [
                {
                    "_cpuset": "string",
                    "_vcpu": "string"
                },
                {
                    "_cpuset": "string",
                    "_vcpu": "string"
                }
            ],
            "vcpusched": [
                {
                    "_priority": "string",
                    "_scheduler": "string",
                    "_vcpus": "string"
                },
                {
                    "_priority": "string",
                    "_scheduler": "string",
                    "_vcpus": "string"
                }
            ]
        },
        "currentMemory": {
            "text": "string",
            "_unit": "string"
        },
        "description": {
            "text": "string"
        },
        "devices": {
            "channel": [
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {}
                },
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {}
                }
            ],
            "console": [
                {
                    "_tty": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {
                        "_port": "string",
                        "_type": "string"
                    }
                },
                {
                    "_tty": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {
                        "_port": "string",
                        "_type": "string"
                    }
                }
            ],
            "controller": [
                {
                    "_index": "string",
                    "_model": "string",
                    "_type": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_cmd_per_lun": "string",
                        "_ioeventfd": "string",
                        "_iommu": "string",
                        "_iothread": "string",
                        "_max_sectors": "string",
                        "_queues": "string"
                    }
                },
                {
                    "_index": "string",
                    "_model": "string",
                    "_type": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_cmd_per_lun": "string",
                        "_ioeventfd": "string",
                        "_iommu": "string",
                        "_iothread": "string",
                        "_max_sectors": "string",
                        "_queues": "string"
                    }
                }
            ],
            "disk": [
                {
                    "_device": "string",
                    "_model": "string",
                    "_rawio": "string",
                    "_sgio": "string",
                    "_snapshot": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "auth": {
                        "_username": "string",
                        "secret": {
                            "_type": "string",
                            "_usage": "string",
                            "_uuid": "string"
                        }
                    },
                    "backingStore": {
                        "_index": "string",
                        "format": {
                            "_type": "string"
                        },
                        "source": {
                            "_index": "string",
                            "_startupPolicy": "string",
                            "encryption": {
                                "_format": "string",
                                "secret": {
                                    "_type": "string",
                                    "_usage": "string",
                                    "_uuid": "string"
                                }
                            },
                            "reservations": {
                                "_enabled": "string",
                                "_managed": "string",
                                "source": {}
                            }
                        }
                    },
                    "blockio": {
                        "_logical_block_size": "string",
                        "_physical_block_size": "string"
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_cache": "string",
                        "_copy_on_read": "string",
                        "_detect_zeroes": "string",
                        "_discard": "string",
                        "_error_policy": "string",
                        "_event_idx": "string",
                        "_io": "string",
                        "_ioeventfd": "string",
                        "_iommu": "string",
                        "_iothread": "string",
                        "_name": "string",
                        "_queues": "string",
                        "_rerror_policy": "string",
                        "_type": "string"
                    },
                    "encryption": {
                        "_format": "string",
                        "secret": {
                            "_type": "string",
                            "_usage": "string",
                            "_uuid": "string"
                        }
                    },
                    "geometry": {
                        "_cyls": "string",
                        "_heads": "string",
                        "_secs": "string",
                        "_trans": "string"
                    },
                    "iotune": {
                        "group_name": {
                            "text": "string"
                        },
                        "read_bytes_sec": {
                            "text": "string"
                        },
                        "read_bytes_sec_max": {
                            "text": "string"
                        },
                        "read_bytes_sec_max_length": {
                            "text": "string"
                        },
                        "read_iops_sec": {
                            "text": "string"
                        },
                        "read_iops_sec_max": {
                            "text": "string"
                        },
                        "read_iops_sec_max_length": {
                            "text": "string"
                        },
                        "size_iops_sec": {
                            "text": "string"
                        },
                        "total_bytes_sec": {
                            "text": "string"
                        },
                        "total_bytes_sec_max": {
                            "text": "string"
                        },
                        "total_bytes_sec_max_length": {
                            "text": "string"
                        },
                        "total_iops_sec": {
                            "text": "string"
                        },
                        "total_iops_sec_max": {
                            "text": "string"
                        },
                        "total_iops_sec_max_length": {
                            "text": "string"
                        },
                        "write_bytes_sec": {
                            "text": "string"
                        },
                        "write_bytes_sec_max": {
                            "text": "string"
                        },
                        "write_bytes_sec_max_length": {
                            "text": "string"
                        },
                        "write_iops_sec": {
                            "text": "string"
                        },
                        "write_iops_sec_max": {
                            "text": "string"
                        },
                        "write_iops_sec_max_length": {
                            "text": "string"
                        }
                    },
                    "mirror": {
                        "_job": "string",
                        "_ready": "string",
                        "format": {
                            "_type": "string"
                        },
                        "source": {
                            "_index": "string",
                            "_startupPolicy": "string",
                            "encryption": {
                                "_format": "string",
                                "secret": {
                                    "_type": "string",
                                    "_usage": "string",
                                    "_uuid": "string"
                                }
                            },
                            "reservations": {
                                "_enabled": "string",
                                "_managed": "string",
                                "source": {}
                            }
                        }
                    },
                    "product": {
                        "text": "string"
                    },
                    "readonly": {},
                    "serial": {
                        "text": "string"
                    },
                    "shareable": {},
                    "source": {
                        "_index": "string",
                        "_startupPolicy": "string",
                        "encryption": {
                            "_format": "string",
                            "secret": {
                                "_type": "string",
                                "_usage": "string",
                                "_uuid": "string"
                            }
                        },
                        "reservations": {
                            "_enabled": "string",
                            "_managed": "string",
                            "source": {}
                        }
                    },
                    "target": {
                        "_bus": "string",
                        "_dev": "string",
                        "_removable": "string",
                        "_tray": "string"
                    },
                    "_transient": {},
                    "vendor": {
                        "text": "string"
                    },
                    "wwn": {
                        "text": "string"
                    }
                },
                {
                    "_device": "string",
                    "_model": "string",
                    "_rawio": "string",
                    "_sgio": "string",
                    "_snapshot": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "auth": {
                        "_username": "string",
                        "secret": {
                            "_type": "string",
                            "_usage": "string",
                            "_uuid": "string"
                        }
                    },
                    "backingStore": {
                        "_index": "string",
                        "format": {
                            "_type": "string"
                        },
                        "source": {
                            "_index": "string",
                            "_startupPolicy": "string",
                            "encryption": {
                                "_format": "string",
                                "secret": {
                                    "_type": "string",
                                    "_usage": "string",
                                    "_uuid": "string"
                                }
                            },
                            "reservations": {
                                "_enabled": "string",
                                "_managed": "string",
                                "source": {}
                            }
                        }
                    },
                    "blockio": {
                        "_logical_block_size": "string",
                        "_physical_block_size": "string"
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_cache": "string",
                        "_copy_on_read": "string",
                        "_detect_zeroes": "string",
                        "_discard": "string",
                        "_error_policy": "string",
                        "_event_idx": "string",
                        "_io": "string",
                        "_ioeventfd": "string",
                        "_iommu": "string",
                        "_iothread": "string",
                        "_name": "string",
                        "_queues": "string",
                        "_rerror_policy": "string",
                        "_type": "string"
                    },
                    "encryption": {
                        "_format": "string",
                        "secret": {
                            "_type": "string",
                            "_usage": "string",
                            "_uuid": "string"
                        }
                    },
                    "geometry": {
                        "_cyls": "string",
                        "_heads": "string",
                        "_secs": "string",
                        "_trans": "string"
                    },
                    "iotune": {
                        "group_name": {
                            "text": "string"
                        },
                        "read_bytes_sec": {
                            "text": "string"
                        },
                        "read_bytes_sec_max": {
                            "text": "string"
                        },
                        "read_bytes_sec_max_length": {
                            "text": "string"
                        },
                        "read_iops_sec": {
                            "text": "string"
                        },
                        "read_iops_sec_max": {
                            "text": "string"
                        },
                        "read_iops_sec_max_length": {
                            "text": "string"
                        },
                        "size_iops_sec": {
                            "text": "string"
                        },
                        "total_bytes_sec": {
                            "text": "string"
                        },
                        "total_bytes_sec_max": {
                            "text": "string"
                        },
                        "total_bytes_sec_max_length": {
                            "text": "string"
                        },
                        "total_iops_sec": {
                            "text": "string"
                        },
                        "total_iops_sec_max": {
                            "text": "string"
                        },
                        "total_iops_sec_max_length": {
                            "text": "string"
                        },
                        "write_bytes_sec": {
                            "text": "string"
                        },
                        "write_bytes_sec_max": {
                            "text": "string"
                        },
                        "write_bytes_sec_max_length": {
                            "text": "string"
                        },
                        "write_iops_sec": {
                            "text": "string"
                        },
                        "write_iops_sec_max": {
                            "text": "string"
                        },
                        "write_iops_sec_max_length": {
                            "text": "string"
                        }
                    },
                    "mirror": {
                        "_job": "string",
                        "_ready": "string",
                        "format": {
                            "_type": "string"
                        },
                        "source": {
                            "_index": "string",
                            "_startupPolicy": "string",
                            "encryption": {
                                "_format": "string",
                                "secret": {
                                    "_type": "string",
                                    "_usage": "string",
                                    "_uuid": "string"
                                }
                            },
                            "reservations": {
                                "_enabled": "string",
                                "_managed": "string",
                                "source": {}
                            }
                        }
                    },
                    "product": {
                        "text": "string"
                    },
                    "readonly": {},
                    "serial": {
                        "text": "string"
                    },
                    "shareable": {},
                    "source": {
                        "_index": "string",
                        "_startupPolicy": "string",
                        "encryption": {
                            "_format": "string",
                            "secret": {
                                "_type": "string",
                                "_usage": "string",
                                "_uuid": "string"
                            }
                        },
                        "reservations": {
                            "_enabled": "string",
                            "_managed": "string",
                            "source": {}
                        }
                    },
                    "target": {
                        "_bus": "string",
                        "_dev": "string",
                        "_removable": "string",
                        "_tray": "string"
                    },
                    "_transient": {},
                    "vendor": {
                        "text": "string"
                    },
                    "wwn": {
                        "text": "string"
                    }
                }
            ],
            "emulator": {
                "text": "string"
            },
            "filesystem": [
                {
                    "_accessmode": "string",
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_format": "string",
                        "_iommu": "string",
                        "_name": "string",
                        "_type": "string",
                        "_wrpolicy": "string"
                    },
                    "readonly": {},
                    "source": {},
                    "space_hard_limit": {
                        "text": "string",
                        "_unit": "string"
                    },
                    "space_soft_limit": {
                        "text": "string",
                        "_unit": "string"
                    },
                    "target": {
                        "_dir": "string"
                    }
                },
                {
                    "_accessmode": "string",
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_format": "string",
                        "_iommu": "string",
                        "_name": "string",
                        "_type": "string",
                        "_wrpolicy": "string"
                    },
                    "readonly": {},
                    "source": {},
                    "space_hard_limit": {
                        "text": "string",
                        "_unit": "string"
                    },
                    "space_soft_limit": {
                        "text": "string",
                        "_unit": "string"
                    },
                    "target": {
                        "_dir": "string"
                    }
                }
            ],
            "graphics": [
                {},
                {}
            ],
            "hostdev": [
                {
                    "_managed": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "rom": {
                        "_bar": "string",
                        "_enabled": "string",
                        "_file": "string"
                    }
                },
                {
                    "_managed": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "rom": {
                        "_bar": "string",
                        "_enabled": "string",
                        "_file": "string"
                    }
                }
            ],
            "hub": [
                {
                    "_type": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    }
                },
                {
                    "_type": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    }
                }
            ],
            "input": [
                {
                    "_bus": "string",
                    "_model": "string",
                    "_type": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_iommu": "string"
                    },
                    "source": {
                        "_evdev": "string"
                    }
                },
                {
                    "_bus": "string",
                    "_model": "string",
                    "_type": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_iommu": "string"
                    },
                    "source": {
                        "_evdev": "string"
                    }
                }
            ],
            "_interface": [
                {
                    "_managed": "string",
                    "_trustGuestRxFilters": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "backend": {
                        "_tap": "string",
                        "_vhost": "string"
                    },
                    "bandwidth": {
                        "inbound": {
                            "_average": "string",
                            "_burst": "string",
                            "_floor": "string",
                            "_peak": "string"
                        },
                        "outbound": {
                            "_average": "string",
                            "_burst": "string",
                            "_floor": "string",
                            "_peak": "string"
                        }
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "coalesce": {
                        "rx": {
                            "frames": {
                                "_max": "string"
                            }
                        }
                    },
                    "driver": {
                        "_ats": "string",
                        "_event_idx": "string",
                        "_ioeventfd": "string",
                        "_iommu": "string",
                        "_name": "string",
                        "_queues": "string",
                        "_rx_queue_size": "string",
                        "_tx_queue_size": "string",
                        "_txmode": "string",
                        "guest": {
                            "_csum": "string",
                            "_ecn": "string",
                            "_tso4": "string",
                            "_tso6": "string",
                            "_ufo": "string"
                        },
                        "host": {
                            "_csum": "string",
                            "_ecn": "string",
                            "_gso": "string",
                            "_mrg_rxbuf": "string",
                            "_tso4": "string",
                            "_tso6": "string",
                            "_ufo": "string"
                        }
                    },
                    "filterref": {
                        "_filter": "string",
                        "parameter": [
                            {
                                "_name": "string",
                                "_value": "string"
                            },
                            {
                                "_name": "string",
                                "_value": "string"
                            }
                        ]
                    },
                    "guest": {
                        "_actual": "string",
                        "_dev": "string"
                    },
                    "ip": [
                        {
                            "_address": "string",
                            "_family": "string",
                            "_peer": "string",
                            "_prefix": "string"
                        },
                        {
                            "_address": "string",
                            "_family": "string",
                            "_peer": "string",
                            "_prefix": "string"
                        }
                    ],
                    "link": {
                        "_state": "string"
                    },
                    "mac": {
                        "_address": "string"
                    },
                    "model": {
                        "_type": "string"
                    },
                    "mtu": {
                        "_size": "string"
                    },
                    "rom": {
                        "_bar": "string",
                        "_enabled": "string",
                        "_file": "string"
                    },
                    "route": [
                        {
                            "_address": "string",
                            "_family": "string",
                            "_gateway": "string",
                            "_metric": "string",
                            "_netmask": "string",
                            "_prefix": "string"
                        },
                        {
                            "_address": "string",
                            "_family": "string",
                            "_gateway": "string",
                            "_metric": "string",
                            "_netmask": "string",
                            "_prefix": "string"
                        }
                    ],
                    "script": {
                        "_path": "string"
                    },
                    "source": {},
                    "target": {
                        "_dev": "string"
                    },
                    "tune": {
                        "sndbuf": {
                            "text": "string"
                        }
                    },
                    "virtualport": {
                        "parameters": {}
                    },
                    "vlan": {
                        "_trunk": "string",
                        "tag": [
                            {
                                "_id": "string",
                                "_nativeMode": "string"
                            },
                            {
                                "_id": "string",
                                "_nativeMode": "string"
                            }
                        ]
                    }
                },
                {
                    "_managed": "string",
                    "_trustGuestRxFilters": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "backend": {
                        "_tap": "string",
                        "_vhost": "string"
                    },
                    "bandwidth": {
                        "inbound": {
                            "_average": "string",
                            "_burst": "string",
                            "_floor": "string",
                            "_peak": "string"
                        },
                        "outbound": {
                            "_average": "string",
                            "_burst": "string",
                            "_floor": "string",
                            "_peak": "string"
                        }
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "coalesce": {
                        "rx": {
                            "frames": {
                                "_max": "string"
                            }
                        }
                    },
                    "driver": {
                        "_ats": "string",
                        "_event_idx": "string",
                        "_ioeventfd": "string",
                        "_iommu": "string",
                        "_name": "string",
                        "_queues": "string",
                        "_rx_queue_size": "string",
                        "_tx_queue_size": "string",
                        "_txmode": "string",
                        "guest": {
                            "_csum": "string",
                            "_ecn": "string",
                            "_tso4": "string",
                            "_tso6": "string",
                            "_ufo": "string"
                        },
                        "host": {
                            "_csum": "string",
                            "_ecn": "string",
                            "_gso": "string",
                            "_mrg_rxbuf": "string",
                            "_tso4": "string",
                            "_tso6": "string",
                            "_ufo": "string"
                        }
                    },
                    "filterref": {
                        "_filter": "string",
                        "parameter": [
                            {
                                "_name": "string",
                                "_value": "string"
                            },
                            {
                                "_name": "string",
                                "_value": "string"
                            }
                        ]
                    },
                    "guest": {
                        "_actual": "string",
                        "_dev": "string"
                    },
                    "ip": [
                        {
                            "_address": "string",
                            "_family": "string",
                            "_peer": "string",
                            "_prefix": "string"
                        },
                        {
                            "_address": "string",
                            "_family": "string",
                            "_peer": "string",
                            "_prefix": "string"
                        }
                    ],
                    "link": {
                        "_state": "string"
                    },
                    "mac": {
                        "_address": "string"
                    },
                    "model": {
                        "_type": "string"
                    },
                    "mtu": {
                        "_size": "string"
                    },
                    "rom": {
                        "_bar": "string",
                        "_enabled": "string",
                        "_file": "string"
                    },
                    "route": [
                        {
                            "_address": "string",
                            "_family": "string",
                            "_gateway": "string",
                            "_metric": "string",
                            "_netmask": "string",
                            "_prefix": "string"
                        },
                        {
                            "_address": "string",
                            "_family": "string",
                            "_gateway": "string",
                            "_metric": "string",
                            "_netmask": "string",
                            "_prefix": "string"
                        }
                    ],
                    "script": {
                        "_path": "string"
                    },
                    "source": {},
                    "target": {
                        "_dev": "string"
                    },
                    "tune": {
                        "sndbuf": {
                            "text": "string"
                        }
                    },
                    "virtualport": {
                        "parameters": {}
                    },
                    "vlan": {
                        "_trunk": "string",
                        "tag": [
                            {
                                "_id": "string",
                                "_nativeMode": "string"
                            },
                            {
                                "_id": "string",
                                "_nativeMode": "string"
                            }
                        ]
                    }
                }
            ],
            "iommu": {
                "_model": "string",
                "driver": {
                    "_caching_mode": "string",
                    "_eim": "string",
                    "_intremap": "string",
                    "_iotlb": "string"
                }
            },
            "lease": [
                {
                    "key": {
                        "text": "string"
                    },
                    "lockspace": {
                        "text": "string"
                    },
                    "target": {
                        "_offset": "string",
                        "_path": "string"
                    }
                },
                {
                    "key": {
                        "text": "string"
                    },
                    "lockspace": {
                        "text": "string"
                    },
                    "target": {
                        "_offset": "string",
                        "_path": "string"
                    }
                }
            ],
            "memballoon": {
                "_autodeflate": "string",
                "_model": "string",
                "address": {},
                "alias": {
                    "_name": "string"
                },
                "driver": {
                    "_ats": "string",
                    "_iommu": "string"
                },
                "stats": {
                    "_period": "string"
                }
            },
            "memory": [
                {
                    "_access": "string",
                    "_discard": "string",
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "source": {
                        "alignsize": {
                            "text": "string",
                            "_unit": "string"
                        },
                        "nodemask": {
                            "text": "string"
                        },
                        "pagesize": {
                            "text": "string",
                            "_unit": "string"
                        },
                        "path": {
                            "text": "string"
                        },
                        "pmem": {}
                    },
                    "target": {
                        "label": {
                            "size": {
                                "text": "string",
                                "_unit": "string"
                            }
                        },
                        "node": {
                            "text": "string"
                        },
                        "readonly": {},
                        "size": {
                            "text": "string",
                            "_unit": "string"
                        }
                    }
                },
                {
                    "_access": "string",
                    "_discard": "string",
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "source": {
                        "alignsize": {
                            "text": "string",
                            "_unit": "string"
                        },
                        "nodemask": {
                            "text": "string"
                        },
                        "pagesize": {
                            "text": "string",
                            "_unit": "string"
                        },
                        "path": {
                            "text": "string"
                        },
                        "pmem": {}
                    },
                    "target": {
                        "label": {
                            "size": {
                                "text": "string",
                                "_unit": "string"
                            }
                        },
                        "node": {
                            "text": "string"
                        },
                        "readonly": {},
                        "size": {
                            "text": "string",
                            "_unit": "string"
                        }
                    }
                }
            ],
            "nvram": {
                "address": {},
                "alias": {
                    "_name": "string"
                }
            },
            "panic": [
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    }
                },
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    }
                }
            ],
            "parallel": [
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {
                        "_port": "string",
                        "_type": "string"
                    }
                },
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {
                        "_port": "string",
                        "_type": "string"
                    }
                }
            ],
            "redirdev": [
                {
                    "_bus": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {}
                },
                {
                    "_bus": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "boot": {
                        "_loadparm": "string",
                        "_order": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {}
                }
            ],
            "redirfilter": [
                {
                    "usbdev": [
                        {
                            "_allow": "string",
                            "_class": "string",
                            "_product": "string",
                            "_vendor": "string",
                            "_version": "string"
                        },
                        {
                            "_allow": "string",
                            "_class": "string",
                            "_product": "string",
                            "_vendor": "string",
                            "_version": "string"
                        }
                    ]
                },
                {
                    "usbdev": [
                        {
                            "_allow": "string",
                            "_class": "string",
                            "_product": "string",
                            "_vendor": "string",
                            "_version": "string"
                        },
                        {
                            "_allow": "string",
                            "_class": "string",
                            "_product": "string",
                            "_vendor": "string",
                            "_version": "string"
                        }
                    ]
                }
            ],
            "rng": [
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "backend": {},
                    "driver": {
                        "_ats": "string",
                        "_iommu": "string"
                    },
                    "rate": {
                        "_bytes": "string",
                        "_period": "string"
                    }
                },
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "backend": {},
                    "driver": {
                        "_ats": "string",
                        "_iommu": "string"
                    },
                    "rate": {
                        "_bytes": "string",
                        "_period": "string"
                    }
                }
            ],
            "serial": [
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {
                        "_port": "string",
                        "_type": "string",
                        "model": {
                            "_name": "string"
                        }
                    }
                },
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "log": {
                        "_append": "string",
                        "_file": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {},
                    "target": {
                        "_port": "string",
                        "_type": "string",
                        "model": {
                            "_name": "string"
                        }
                    }
                }
            ],
            "shmem": [
                {
                    "_name": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "model": {
                        "_type": "string"
                    },
                    "msi": {
                        "_enabled": "string",
                        "_ioeventfd": "string",
                        "_vectors": "string"
                    },
                    "server": {
                        "_path": "string"
                    },
                    "size": {
                        "text": "string",
                        "_unit": "string"
                    }
                },
                {
                    "_name": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "model": {
                        "_type": "string"
                    },
                    "msi": {
                        "_enabled": "string",
                        "_ioeventfd": "string",
                        "_vectors": "string"
                    },
                    "server": {
                        "_path": "string"
                    },
                    "size": {
                        "text": "string",
                        "_unit": "string"
                    }
                }
            ],
            "smartcard": [
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "certificate": [
                        {
                            "text": "string"
                        },
                        {
                            "text": "string"
                        }
                    ],
                    "database": {
                        "text": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {}
                },
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "certificate": [
                        {
                            "text": "string"
                        },
                        {
                            "text": "string"
                        }
                    ],
                    "database": {
                        "text": "string"
                    },
                    "protocol": {
                        "_type": "string"
                    },
                    "source": {}
                }
            ],
            "sound": [
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "codec": [
                        {
                            "_type": "string"
                        },
                        {
                            "_type": "string"
                        }
                    ]
                },
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "codec": [
                        {
                            "_type": "string"
                        },
                        {
                            "_type": "string"
                        }
                    ]
                }
            ],
            "tpm": [
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "backend": {}
                },
                {
                    "_model": "string",
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "backend": {}
                }
            ],
            "video": [
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_iommu": "string",
                        "_vgaconf": "string"
                    },
                    "model": {
                        "_heads": "string",
                        "_primary": "string",
                        "_ram": "string",
                        "_type": "string",
                        "_vgamem": "string",
                        "_vram": "string",
                        "_vram64": "string",
                        "acceleration": {
                            "_accel2d": "string",
                            "_accel3d": "string"
                        }
                    }
                },
                {
                    "address": {},
                    "alias": {
                        "_name": "string"
                    },
                    "driver": {
                        "_ats": "string",
                        "_iommu": "string",
                        "_vgaconf": "string"
                    },
                    "model": {
                        "_heads": "string",
                        "_primary": "string",
                        "_ram": "string",
                        "_type": "string",
                        "_vgamem": "string",
                        "_vram": "string",
                        "_vram64": "string",
                        "acceleration": {
                            "_accel2d": "string",
                            "_accel3d": "string"
                        }
                    }
                }
            ],
            "vsock": {
                "_model": "string",
                "address": {},
                "alias": {
                    "_name": "string"
                },
                "cid": {
                    "_address": "string",
                    "_auto": "string"
                }
            },
            "watchdog": {
                "_action": "string",
                "_model": "string",
                "address": {},
                "alias": {
                    "_name": "string"
                }
            }
        },
        "features": {
            "acpi": {},
            "apic": {
                "_eoi": "string"
            },
            "capabilities": {
                "_policy": "string",
                "audit_control": {
                    "_state": "string"
                },
                "audit_write": {
                    "_state": "string"
                },
                "block_suspend": {
                    "_state": "string"
                },
                "chown": {
                    "_state": "string"
                },
                "dac_override": {
                    "_state": "string"
                },
                "dac_read_Search": {
                    "_state": "string"
                },
                "fowner": {
                    "_state": "string"
                },
                "fsetid": {
                    "_state": "string"
                },
                "ipc_lock": {
                    "_state": "string"
                },
                "ipc_owner": {
                    "_state": "string"
                },
                "kill": {
                    "_state": "string"
                },
                "lease": {
                    "_state": "string"
                },
                "linux_immutable": {
                    "_state": "string"
                },
                "mac_admin": {
                    "_state": "string"
                },
                "mac_override": {
                    "_state": "string"
                },
                "mknod": {
                    "_state": "string"
                },
                "net_admin": {
                    "_state": "string"
                },
                "net_bind_service": {
                    "_state": "string"
                },
                "net_broadcast": {
                    "_state": "string"
                },
                "net_raw": {
                    "_state": "string"
                },
                "setfcap": {
                    "_state": "string"
                },
                "setgid": {
                    "_state": "string"
                },
                "setpcap": {
                    "_state": "string"
                },
                "setuid": {
                    "_state": "string"
                },
                "sys_admin": {
                    "_state": "string"
                },
                "sys_boot": {
                    "_state": "string"
                },
                "sys_chroot": {
                    "_state": "string"
                },
                "sys_module": {
                    "_state": "string"
                },
                "sys_nice": {
                    "_state": "string"
                },
                "sys_pacct": {
                    "_state": "string"
                },
                "sys_ptrace": {
                    "_state": "string"
                },
                "sys_rawio": {
                    "_state": "string"
                },
                "sys_resource": {
                    "_state": "string"
                },
                "sys_time": {
                    "_state": "string"
                },
                "sys_tty_config": {
                    "_state": "string"
                },
                "syslog": {
                    "_state": "string"
                },
                "wake_alarm": {
                    "_state": "string"
                }
            },
            "gic": {
                "_version": "string"
            },
            "hap": {
                "_state": "string"
            },
            "hpt": {
                "_resizing": "string",
                "maxpagesize": {
                    "text": "string",
                    "_unit": "string"
                }
            },
            "htm": {
                "_state": "string"
            },
            "hyperv": {
                "evmcs": {
                    "_state": "string"
                },
                "frequencies": {
                    "_state": "string"
                },
                "ipi": {
                    "_state": "string"
                },
                "reenlightenment": {
                    "_state": "string"
                },
                "relaxed": {
                    "_state": "string"
                },
                "reset": {
                    "_state": "string"
                },
                "runtime": {
                    "_state": "string"
                },
                "spinlocks": {
                    "_retries": "string"
                },
                "stimer": {
                    "_state": "string"
                },
                "synic": {
                    "_state": "string"
                },
                "tlbflush": {
                    "_state": "string"
                },
                "vapic": {
                    "_state": "string"
                },
                "vendor_id": {
                    "_value": "string"
                },
                "vpindex": {
                    "_state": "string"
                }
            },
            "ioapic": {
                "_driver": "string"
            },
            "kvm": {
                "hidden": {
                    "_state": "string"
                }
            },
            "msrs": {
                "_unknown": "string"
            },
            "nested_hv": {
                "_state": "string"
            },
            "pae": {},
            "pmu": {
                "_state": "string"
            },
            "privnet": {},
            "pvspinlock": {
                "_state": "string"
            },
            "smm": {
                "_state": "string",
                "tseg": {
                    "text": "string",
                    "_unit": "string"
                }
            },
            "viridian": {},
            "vmcoreinfo": {
                "_state": "string"
            },
            "vmport": {
                "_state": "string"
            }
        },
        "genid": {
            "text": "string"
        },
        "idmap": {
            "gid": [
                {
                    "_count": "string",
                    "_start": "string",
                    "_target": "string"
                },
                {
                    "_count": "string",
                    "_start": "string",
                    "_target": "string"
                }
            ],
            "uid": [
                {
                    "_count": "string",
                    "_start": "string",
                    "_target": "string"
                },
                {
                    "_count": "string",
                    "_start": "string",
                    "_target": "string"
                }
            ]
        },
        "iothreadids": {
            "iothread": [
                {
                    "_id": "string"
                },
                {
                    "_id": "string"
                }
            ]
        },
        "iothreads": {
            "text": "string"
        },
        "keywrap": {
            "cipher": [
                {
                    "_name": "string",
                    "_state": "string"
                },
                {
                    "_name": "string",
                    "_state": "string"
                }
            ]
        },
        "launchSecurity": {},
        "maxMemory": {
            "text": "string",
            "_slots": "string",
            "_unit": "string"
        },
        "memory": {
            "text": "string",
            "_dumpCore": "string",
            "_unit": "string"
        },
        "memoryBacking": {
            "access": {
                "_mode": "string"
            },
            "allocation": {
                "_mode": "string"
            },
            "discard": {},
            "hugepages": {
                "page": [
                    {
                        "_nodeset": "string",
                        "_size": "string",
                        "_unit": "string"
                    },
                    {
                        "_nodeset": "string",
                        "_size": "string",
                        "_unit": "string"
                    }
                ]
            },
            "locked": {},
            "nosharepages": {},
            "source": {
                "_type": "string"
            }
        },
        "memtune": {
            "hard_limit": {
                "text": "string",
                "_unit": "string"
            },
            "min_guarantee": {
                "text": "string",
                "_unit": "string"
            },
            "soft_limit": {
                "text": "string",
                "_unit": "string"
            },
            "swap_hard_limit": {
                "text": "string",
                "_unit": "string"
            }
        },
        "metadata": {},
        "name": {
            "text": "string"
        },
        "numatune": {
            "memnode": [
                {
                    "_cellid": "string",
                    "_mode": "string",
                    "_nodeset": "string"
                },
                {
                    "_cellid": "string",
                    "_mode": "string",
                    "_nodeset": "string"
                }
            ],
            "memory": {
                "_mode": "string",
                "_nodeset": "string",
                "_placement": "string"
            }
        },
        "on_crash": {
            "text": "string"
        },
        "on_poweroff": {
            "text": "string"
        },
        "on_reboot": {
            "text": "string"
        },
        "os": {
            "acpi": {
                "table": [
                    {
                        "text": "string",
                        "_type": "string"
                    },
                    {
                        "text": "string",
                        "_type": "string"
                    }
                ]
            },
            "bios": {
                "_rebootTimeout": "string",
                "_useserial": "string"
            },
            "boot": [
                {
                    "_dev": "string"
                },
                {
                    "_dev": "string"
                }
            ],
            "bootmenu": {
                "_enable": "string",
                "_timeout": "string"
            },
            "cmdline": {
                "text": "string"
            },
            "dtb": {
                "text": "string"
            },
            "init": {
                "text": "string"
            },
            "initarg": {
                "text": "string"
            },
            "initdir": {
                "text": "string"
            },
            "initenv": [
                {
                    "text": "string",
                    "_name": "string"
                },
                {
                    "text": "string",
                    "_name": "string"
                }
            ],
            "initgroup": {
                "text": "string"
            },
            "initrd": {
                "text": "string"
            },
            "inituser": {
                "text": "string"
            },
            "kernel": {
                "text": "string"
            },
            "loader": {
                "text": "strin readonly='string' secure='string' type='string'>"
            },
            "nvram": {
                "text": "strin template='string'>"
            },
            "smbios": {
                "_mode": "string"
            },
            "type": {
                "text": "string",
                "_arch": "string",
                "_machine": "string"
            }
        },
        "perf": {
            "event": [
                {
                    "_enabled": "string",
                    "_name": "string"
                },
                {
                    "_enabled": "string",
                    "_name": "string"
                }
            ]
        },
        "pm": {
            "suspend_to_disk": {
                "_enabled": "string"
            },
            "suspend_to_mem": {
                "_enabled": "string"
            }
        },
        "resource": {
            "partition": {
                "text": "string"
            }
        },
        "seclabel": [
            {
                "_model": "string",
                "_relabel": "string",
                "_type": "string",
                "baselabel": {
                    "text": "string"
                },
                "imagelabel": {
                    "text": "string"
                },
                "label": {
                    "text": "string"
                }
            },
            {
                "_model": "string",
                "_relabel": "string",
                "_type": "string",
                "baselabel": {
                    "text": "string"
                },
                "imagelabel": {
                    "text": "string"
                },
                "label": {
                    "text": "string"
                }
            }
        ],
        "sysinfo": {
            "_type": "string",
            "baseBoard": [
                {
                    "entry": [
                        {
                            "text": "string",
                            "_name": "string"
                        },
                        {
                            "text": "string",
                            "_name": "string"
                        }
                    ]
                },
                {
                    "entry": [
                        {
                            "text": "string",
                            "_name": "string"
                        },
                        {
                            "text": "string",
                            "_name": "string"
                        }
                    ]
                }
            ],
            "bios": {
                "entry": [
                    {
                        "text": "string",
                        "_name": "string"
                    },
                    {
                        "text": "string",
                        "_name": "string"
                    }
                ]
            },
            "chassis": {
                "entry": [
                    {
                        "text": "string",
                        "_name": "string"
                    },
                    {
                        "text": "string",
                        "_name": "string"
                    }
                ]
            },
            "memory": [
                {
                    "entry": [
                        {
                            "text": "string",
                            "_name": "string"
                        },
                        {
                            "text": "string",
                            "_name": "string"
                        }
                    ]
                },
                {
                    "entry": [
                        {
                            "text": "string",
                            "_name": "string"
                        },
                        {
                            "text": "string",
                            "_name": "string"
                        }
                    ]
                }
            ],
            "oemStrings": {
                "entry": {
                    "text": "string"
                }
            },
            "processor": [
                {
                    "entry": [
                        {
                            "text": "string",
                            "_name": "string"
                        },
                        {
                            "text": "string",
                            "_name": "string"
                        }
                    ]
                },
                {
                    "entry": [
                        {
                            "text": "string",
                            "_name": "string"
                        },
                        {
                            "text": "string",
                            "_name": "string"
                        }
                    ]
                }
            ],
            "system": {
                "entry": [
                    {
                        "text": "string",
                        "_name": "string"
                    },
                    {
                        "text": "string",
                        "_name": "string"
                    }
                ]
            }
        },
        "title": {
            "text": "string"
        },
        "uuid": {
            "text": "string"
        },
        "vcpu": {
            "text": "string",
            "_cpuset": "string",
            "_current": "string",
            "_placement": "string"
        },
        "vcpus": {
            "vcpu": [
                {
                    "_enabled": "string",
                    "_hotpluggable": "string",
                    "_id": "string",
                    "_order": "string"
                },
                {
                    "_enabled": "string",
                    "_hotpluggable": "string",
                    "_id": "string",
                    "_order": "string"
                }
            ]
        }
    }
}
```

