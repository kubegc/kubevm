#!/usr/bin/env bash
##############################################################
##
##      Copyright (2019, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuheng@otcaix.iscas.ac.cn
##
################################################################

#SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
#cd $SHELL_FOLDER
#rm -rf dist/ build/ vmm.spec
#pyinstaller -F vmm.py -p ./
#chmod +x dist/vmm
#cp -f dist/vmm /usr/bin

# update config file
cp -f /home/kubevmm/bin/config /etc/kubevmm/config.new
mv -f /etc/kubevmm/config /etc/kubevmm/config.old
mv -f /etc/kubevmm/config.new /etc/kubevmm/config
# update VERSION file
cp -f /home/kubevmm/bin/VERSION /etc/kubevmm/VERSION.new
mv -f /etc/kubevmm/VERSION /etc/kubevmm/VERSION.old
mv -f /etc/kubevmm/VERSION.new /etc/kubevmm/VERSION
# update yamls file
cp -rf /home/kubevmm/bin/yamls /etc/kubevmm/yamls.new
mv -f /etc/kubevmm/yamls /etc/kubevmm/yamls.old
mv -f /etc/kubevmm/yamls.new /etc/kubevmm/yamls
# update kubevmm-adm
cp -f /home/kubevmm/bin/kubevmm-adm /usr/bin/kubevmm-adm.new
mv -f /usr/bin/kubevmm-adm /usr/bin/kubevmm-adm.old
chmod -x /usr/bin/kubevmm-adm.old
mv -f /usr/bin/kubevmm-adm.new /usr/bin/kubevmm-adm
# update kubeovn-adm
cp -f /home/kubevmm/bin/kubeovn-adm /usr/bin/kubeovn-adm.new
mv -f /usr/bin/kubeovn-adm /usr/bin/kubeovn-adm.old
chmod -x /usr/bin/kubeovn-adm.old
mv -f /usr/bin/kubeovn-adm.new /usr/bin/kubeovn-adm
chmod +x /usr/bin/kubeovn-adm
# update vmm
cp -f /home/kubevmm/bin/vmm /usr/bin/vmm.new
mv -f /usr/bin/vmm /usr/bin/vmm.old
chmod -x /usr/bin/vmm.old
mv -f /usr/bin/vmm.new /usr/bin/vmm
# apply kubevirtResource.yaml
if [ -f "/etc/kubevmm/yamls/kubevirtResource.yaml" ];then
	echo "Ready: apply new /etc/kubevmm/yamls/kubevirtResource.yaml"
	kubectl apply -f /etc/kubevmm/yamls/kubevirtResource.yaml
else
	echo "Warning: file /etc/kubevmm/yamls/kubevirtResource.yaml not exists!"
fi
# run virtctl service
python virtctl_in_docker.py
