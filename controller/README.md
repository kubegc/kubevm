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

## RoadMap

- 1.0.0 (20190701)
  - Support VirtualMachine
  - Support VirtualMachineDisk
  - Support VirtualMachineSnapshot
- 1.1.0 (20190729)
  - Support VirtualMachineDiskImage
  - Support VirtualMachineImage
- 1.2.0 (20190829)
  - Support VirtualMachinePool
  - Support VirtualMachineNetwork
- 1.3.0 (20190925)
  - Reengineering and now it is a framework
- 1.4.0 (20191007, final)
  - support HA 
