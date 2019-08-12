#!/usr/bin/env bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER

##############################init###############################################
echo "Reading VERSION file...."
if [ ! -f "VERSION" ]; then
    echo "can't find VERSION file."
    exit 1
fi

VERSION=$(cat VERSION)

echo "#######################################################"
echo "Pull latest version from Github."
git pull
if [ $? -ne 0 ]; then
    echo "Failed to pull latest version from Github!"
    exit 1
else
    echo "Success pull latest version."
fi

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
echo "#######################################################"
echo "Login docker image repository in aliyun."
echo "Username: bigtree0613@126.com"
docker login --username=bigtree0613@126.com registry.cn-hangzhou.aliyuncs.com
if [ $? -ne 0 ]; then
    echo "Failed to login aliyun repository!"
    exit 1
else
    echo "Success login...Pushing images!"
fi
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

DIR=kubevmm-v${VERSION}
mkdir ${DIR}
cp -rf ../yamls dist/vmm install.sh VERSION ${DIR}

tar -zcvf kubevmm-v${VERSION}.tar.gz ${DIR}

# step 3 delete files
rm -rf dist/ build/ vmm.spec ${DIR}
