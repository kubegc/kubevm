## Prerequisite

You are on the master with installed kubernetes

## Step 1: pack

```
mvn clean install
```

## Step 2: build

```
cp target/kubevirt-controller-1.6.0-SNAPSHOT-jar-with-dependencies.jar docker/
cp /etc/kubernetes/admin.conf docker/
docker build docker/ -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-controller-manager:v1.6.0
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

## Reference

Etcd开启访问控制
进入bin/目录
添加root用户并设置密码
./etcdctl user add root
 

开启认证
./etcdctl auth enable
由于etcd开启访问控制之后，默认会启用两个角色 root 和 guest， root 和 guest 角色都拥有所有权限，当我们未指定身份的时候其实是通过 guest 角色进行操作，所以要收回guest的所有权限
./etcdctl -u root:root role revoke guest --path '/*' --rw
 

jetcd api调用
Client connect = Client.builder().endpoints(EtcdHosts).authority("root:password").build();
