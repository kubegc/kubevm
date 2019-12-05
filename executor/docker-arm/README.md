## Prerequisite

You are on the master with installed kubernetes


## Step 1: build

```
docker build base -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v1.14.1
docker build virtlet -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v1.14.1
docker build virtctl -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v1.14.1
```
