#!/usr/bin/env bash
##############################################################
##
##      Copyright (2019, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuheng@otcaix.iscas.ac.cn
##
################################################################

echo "Now starting libvirt watcher service..."
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd ${SHELL_FOLDER}
cd ./libvirtwatcher
python3 libvirt_watcher_in_docker.py