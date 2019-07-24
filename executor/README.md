
# Prepare environment

1. Shutdown **SELinux** and reboot.
2. Execute following commands:
```
yum install virt-install libvirt 
systemctl stop firewalld
systemctl disable firewalld
systemctl start libvirtd
systemctl enable libvirtd
```

# How to run.
## Pull docker images.
```
docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v1.14.1
docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v1.14.1
```
## Start virtctl.

```
docker run -itd -h <hostname> --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v1.14.1 bash virtctl.sh
```

## Start virtlet.

```
docker run -itd -h <hostname> --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v1.14.1 bash virtlet.sh
```

## Verify services.
```
docker ps | grep kubevirt
```
