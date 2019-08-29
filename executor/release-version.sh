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
        echo -e "\033[3;30;47m*** Build a new release version: \033[5;36;47m($1)\033[0m)"
        echo -e "Institute of Software, Chinese Academy of Sciences"
        echo -e "        wuyuewen@otcaix.iscas.ac.cn"
        echo -e "              Copyright (2019)\n"
    else
        echo "error: wrong syntax in release version number, support chars=[A-Za-z0-9.]"
        exit 1
    fi
fi

VERSION=$1

echo -e "\033[3;30;47m*** Pull latest version from Github.\033[0m"
git pull
if [ $? -ne 0 ]; then
    echo "    Failed to pull latest version from Github!"
    exit 1
else
    echo "    Success pull latest version."
fi

##############################patch image#########################################

# step 1 copy file
cp -rf utils config arraylist.cfg invoker.py virtctl.py docker/virtctl
cp -rf utils config arraylist.cfg host_cycler.py libvirt_event_handler.py os_event_handler.py virtlet.py docker/virtlet

#step 2 docker build
cd docker
docker build base -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest
docker build virtlet -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:${VERSION}
docker build virtctl -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:${VERSION}

#step 3 docker push
echo -e "\033[3;30;47m*** Login docker image repository in aliyun.\033[0m"
echo "Username: bigtree0613@126.com"
docker login --username=bigtree0613@126.com registry.cn-hangzhou.aliyuncs.com
if [ $? -ne 0 ]; then
    echo "    Failed to login aliyun repository!"
    exit 1
else
    echo "    Success login...Pushing images!"
fi
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:${VERSION}
docker push registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:${VERSION}

###############################patch version to SPECS/kubevmm.spec######################################################
echo -e "\033[3;30;47m*** Patch release version number to SPECS/kubevmm.spec\033[0m"
cd ..
if [ ! -d "./dist" ]; then
	mkdir ./dist
fi
cp -f config ./dist
cp -f kubeovn-adm ./dist
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
find ${SHELL_FOLDER}/dist -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \;
sed "4s/.*/%define         _verstr      ${VERSION}/" SPECS/kubevmm.spec > SPECS/kubevmm.spec.new
mv SPECS/kubevmm.spec.new SPECS/kubevmm.spec
if [ $? -ne 0 ]; then
    echo "    Failed to patch version number to SPECS/kubevmm.spec!"
    exit 1
else
    echo "    Success patch version number to SPECS/kubevmm.spec."
fi

echo -e "\033[3;30;47m*** Push new SPECS/kubevmm.spec to Github.\033[0m"
git add ./SPECS/kubevmm.spec
git commit -m "new release version ${VERSION}"
git push
if [ $? -ne 0 ]; then
    echo "    Failed to push SPECS/kubevmm.spec to Github!"
    exit 1
else
    echo "    Success push SPECS/kubevmm.spec to Github."
fi
