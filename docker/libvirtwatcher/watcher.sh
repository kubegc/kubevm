#!/usr/bin/env bash
##############################################################
##
##      Copyright (2021, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuyuewen@otcaix.iscas.ac.cn
##
################################################################

echo "Now starting libvirt watcher service..."
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd ${SHELL_FOLDER}
cd ./libvirtwatcher
python3 libvirt_watcher_in_docker.py