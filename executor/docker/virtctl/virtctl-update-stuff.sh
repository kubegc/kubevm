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
# update vmm
cp -f /home/kubevmm/bin/vmm /usr/bin/vmm.new
mv -f /usr/bin/vmm /usr/bin/vmm.old
chmod -x /usr/bin/vmm.old
mv -f /usr/bin/vmm.new /usr/bin/vmm
# run virtctl service
python virtctl_in_docker.py
