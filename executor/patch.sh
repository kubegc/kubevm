#!/usr/bin/env bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER



##############################init###############################################

echo "reading VERSION file...."
if [ ! -f "VERSION" ]; then
    echo "can't find VERSION file."
    exit
fi

VERSION=$(cat VERSION)

git pull
rm -rf patch
mkdir patch

##############################patch image#########################################

# step 1 copy file
cp -rf utils arraylist.cfg default.cfg invoker.py virtctl.py docker/virtctl
cp -rf utils arraylist.cfg default.cfg host_cycler.py libvirt_event_handler.py os_event_handler.py virtlet.py docker/virtlet

#step 2 docker build
cd docker
docker build base -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v${VERSION}
docker build virtlet -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v${VERSION}
docker build virtctl -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v${VERSION}

#step 3 docker push
docker login --username=bigtree0613@126.com registry.cn-hangzhou.aliyuncs.com
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v${VERSION}
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v${VERSION}
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v${VERSION}

###############################patch vmm######################################################
cd ..
# step 1 install pyinstaller
pip install --ignore-installed pyinstaller

# step 2 make vmm
rm -rf dist/ build/ vmm.spec
pyinstaller -F vmm.py -p ./
chmod +x dist/vmm

cp -f dist/vmm install.sh VERSION  patch/

tar -zcvf patch-v${VERSION}.tar.gz patch/

# step 3 delete files
rm -rf dist/ build/ vmm.spec patch/
