#!/usr/bin/env bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER

##############################init###############################################
if [ ! -n "$1" ] ;then
    echo "error: please input a release version number!"
    echo "Usage $0 <version number>"
    exit 1
else
    if [[ "$1" =~ ^[A-Za-z0-9.]*$ ]] ;then
        echo "Building a new release version $1"
    else
        echo "error: wrong syntax in release version number, support chars=[A-Za-z0-9.]"
        exit 1
    fi
fi

VERSION=$1

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
docker build base -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest
docker build virtlet -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:${VERSION}
docker build virtctl -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:${VERSION}

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
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:${VERSION}
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:${VERSION}

###############################patch version to SPECS/kubevmm.spec######################################################
echo "#######################################################"
echo "Patch release version number to SPECS/kubevmm.spec"
cd ..
sed "4s/.*/%define         _verstr      ${VERSION}/" SPECS/kubevmm.spec > SPECS/kubevmm.spec.new
mv SPECS/kubevmm.spec.new SPECS/kubevmm.spec
if [ $? -ne 0 ]; then
    echo "Failed to patch version number to SPECS/kubevmm.spec!"
    exit 1
else
    echo "Success patch version number to SPECS/kubevmm.spec."
fi
echo "Push new SPECS/kubevmm.spec to Github."
git add -A SPECS/kubevmm.spec
git commit -a -m "new release version ${VERSION}"
git push
if [ $? -ne 0 ]; then
    echo "Failed to push SPECS/kubevmm.spec to Github!"
    exit 1
else
    echo "Success push SPECS/kubevmm.spec to Github."
fi
