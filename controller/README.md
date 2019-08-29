## Prerequisite

You are on the master with installed kubernetes

## Step 1: pack

```
mvn clean install
```

## Step 2: build

```
cp target/kubevirt-controller-1.0.0-SNAPSHOT-jar-with-dependencies.jar docker/
cp /etc/kubernetes/admin.conf docker/
docker build docker/ -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-controller-manager:v1.0.0
```

## Versions

- 1.0.0 (20190829)
  - Support VirtualMachine
  - Support VirtualMachineDisk
  - Support VirtualMachinePool
  - Support VirtualMachineImage
  - Support VirtualMachineSnapshot
  - Support VirtualMachineNetwork
