# Kube-vmm


**Kube-vmm** is a Kubernetes-based virtual machine management platform. Unlike [kubevirt (Pod-based)](https://github.com/kubevirt/kubevirt), we prefer [another way](https://www.mirantis.com/blog/kubevirt-vs-virtlet-comparison-better/) to support libvirt/VM.

**Note:** Kube-vmm is a heavy work in progress to support python3


**Authors**
- wuheng@otcaix.iscas.ac.cn
- wuyuewen@otcaix.iscas.ac.cn


## Limitations

- just focus on compute resource (libvirt), it cannot replace Openstack (network, storage, and so on)
- the size of VirtualMachine's yaml should not be great than 128K
- a machine cannot run both container and VM

## Capacities

- VirtualMachine **(Supported)**
- VirtualMachineDisk **(Supported)**
- VirtualMachineSnapshot **(Supported)**
- VirtualMachineImage **(Supported)**
- VirtualMachineNetwork **(Supported)**
- VirtualMachineStoragePool **(Supported)**

# Architecture



# Roadmap

- 2.0.x: use python3
