#!/usr/bin/env bash

##############################init###############################################
git pull
rm -rf patch
mkdir patch

##############################patch image#########################################
VERSION=$1

# step 1 copy file
cp -rf utils arraylist.cfg default.cfg invoker.py virtctl.py docker/virtctl

#step 2 docker build
cd docker
docker build base -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v${VERSION}
docker build virtlet -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:v${VERSION}
docker build virtctl -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v${VERSION}

#step 3 docker push
#docker login --username=bigtree0613@126.com registry.cn-hangzhou.aliyuncs.com --password=
#docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:v${VERSION}

###############################patch vmm######################################################
cd ..
# step 1 install pyinstaller
pip install --ignore-installed pyinstaller

# step 2 make vmm
rm -rf dist/ build/ vmm.spec
pyinstaller -F vmm.py -p ./
chmod +x dist/vmm

cp -f dist/vmm install.sh  patch/

tar -zcvf patch-v${VERSION}.tar.gz patch/

# step 3 delete files
rm -rf dist/ build/ vmm.spec patch/