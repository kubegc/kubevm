## Prerequisite

You are on the master with installed kubernetes

## Step 1: pack

```
mvn clean install
```

## Step 2: build

```
cp target/kubevirt-controller-2.0.0-SNAPSHOT-jar-with-dependencies.jar docker/
cp /etc/kubernetes/admin.conf docker/
docker build docker/ -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-controller-manager:v1.14.1
```
