# KubeVMM


**KubeVMM** is a Kubernetes-based virtual machine management platform.

**Note:** KubeVMM is a heavy work in progress.

**Authors**
- wuheng@otcaix.iscas.ac.cn
- wuyuewen@otcaix.iscas.ac.cn
- liuhe18@otcaix.iscas.ac.cn

# Introduction

## Virtualization extension for Kubernetes

KubeVMM extends [Kubernetes](https://kubernetes.io/) by adding
additional virtualization resource types through
[Kubernetes's Custom Resource Definitions API](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/).
By using this mechanism, the Kubernetes API can be used to manage these `VM`
resources alongside all other resources Kubernetes provides.

Unlike [kubevirt/kubebirt](https://github.com/kubevirt/kubevirt), we do not
plan to manage VM using the pod model. Instead, we design a new virtctl to
support VM's lifecycle.

## Quick start

```
kubectl apply -f yamls/
```


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

![avatar](docs/images/arch.png)

- **[Analyser](analyser)**: converte libvirt's XML to Kubernetes's YAML, the libvirt's XML is used by [Openstack](https://www.openstack.org/) (Go, Shell, Python). 
- **[Controller](controller)**: extend Kubernetes to support VirtualMachine resource (Java).
- **[Scheduler](https://github.com/kubesys/kubeext-scheduler)**:  extend Kubernetes to schedule VirtualMachine (Go).
- **[Executor(aka Virtctl)](executor)**:  manage VM's lifecycle (Python, Shell).

# Roadmap

# Note:

1: http://39.106.124.113/uit-plus/

- virt-install: unable to clone paused VMs
- kubeadm: unable to provide services after a year
