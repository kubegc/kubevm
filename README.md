# KubeVMM


**KubeVMM** is a Kubernetes-based virtual machine management platform.

**Note:** KubeVMM is a heavy work in progress.

**Authors**
- wuheng@otcaix.iscas.ac.cn
- wuyuewen@otcaix.iscas.ac.cn

**Thanks**
- xianghao16@otcaix.iscas.ac.cn
- shizhonghao17@otcaix.iscas.ac.cn
- yangchen18@otcaix.iscas.ac.cn

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

## Guide

- [API introduction](docs/API.md)


## Limitations

- just focus on compute resource (libvirt), it cannot replace Openstack (network, storage, and so on)
- the size of VirtualMachine's yaml should not be great than 128K
- a machine cannot run both container and VM

## Capacities

- VirtualMachine **(Supported)**
- VirtualMachineDisk **(Supported)**
- VirtualMachineSnapshot **(Supported)**
- VirtualMachineImage **(Supported)**
- VirtualMachineNetwork
- VirtualMachineStoragePool

# Architecture

![avatar](docs/images/arch.png)

- **[Analyser](analyser)**: converte libvirt's XML to Kubernetes's YAML, the libvirt's XML is used by [Openstack](https://www.openstack.org/) (Go, Shell, Python). 
- **[Controller](controller)**: extend Kubernetes to support VirtualMachine resource (Java).
- **[Scheduler](scheduler)**:  extend Kubernetes to schedule VirtualMachine (Go).
- **[Executor(aka Virtctl)](executor)**:  manage VM's lifecycle (Python, Shell).

# Roadmap

- **2019.7**: support VirtualMachine, VirtualMachineImage  and VirtualMachineSnapshot
- **2019.8**: support VirtualNetwork, VirtualDisk and VirtualMachineStoragePool
- **2019.9**: support some advanced capacities
