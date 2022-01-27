#!/usr/bin/env bash
##############################################################
##
##      Copyright (2021, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuyuewen@otcaix.iscas.ac.cn
##
################################################################

#SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
#cd $SHELL_FOLDER
#rm -rf dist/ build/ vmm.spec
#pyinstaller -F vmm.py -p ./
#chmod +x dist/vmm
#cp -f dist/vmm /usr/bin

# update VERSION file
echo "+++ Processing: update conf file"
cp -rf /home/kubevmm/conf/* /etc/kubevmm/
echo "--- Done: update conf file"
# update binaries
echo "+++ Processing: update binaries"
cp -f /home/kubevmm/bin/* /usr/bin/
echo "--- Done: update binaries"
# apply kubevirtResource.yaml
if [ -f "/etc/kubevmm/yamls/kubevirtResource.yaml" ];then
	echo "+++ Processing: apply new kubevirtResource.yaml"
	kubectl apply -f /etc/kubevmm/yamls/kubevirtResource.yaml
	echo "--- Done: apply new kubevirtResource.yaml"
else
	echo "*** Warning: apply new kubevirtResource.yaml failed!"
	echo "*** Warning: file /etc/kubevmm/yamls/kubevirtResource.yaml not exists!"
fi
# run virtctl service
echo "Now starting virtctl service..."
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd ${SHELL_FOLDER}
cd ./virtctl
python3 virtctl_in_docker.py