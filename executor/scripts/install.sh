#!/usr/bin/env bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER

echo "reading VERSION file...."
if [ ! -f "VERSION" ]; then
    echo "can't find VERSION file."
    exit 1
fi

VERSION=$(cat VERSION)


HOSTNAME=$(hostname)

# step 1 install packages
yum install epel-release -y
yum install virt-manager python2-devel python2-pip libvirt-devel gcc gcc-c++ glib-devel glibc-devel libvirt virt-install -y
pip install --upgrade pip
pip install setuptools
pip install --ignore-installed kubernetes libvirt-python xmljson xmltodict watchdog pyyaml pyinstaller
yum clean all


# step 2 move vmm to /usr/bin
chmod +X vmm
cp -f vmm /usr/bin

# step 3 pull image and start
#docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v${VERSION}
docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v${VERSION}
docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v${VERSION}

docker run -itd -h ${HOSTNAME} --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube -v /tmp:/tmp registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v${VERSION} bash virtctl.sh

docker run -itd -h ${HOSTNAME} --net=host -v /opt:/opt -v /var/log:/var/log -v /var/lib/libvirt:/var/lib/libvirt -v /var/run:/var/run -v /usr/bin:/usr/bin -v /usr/share:/usr/share -v /root/.kube:/root/.kube registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v${VERSION} bash virtlet.sh

docker ps | grep kubevirt

