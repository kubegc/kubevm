#!/usr/bin/env bash
##############################################################
##
##      Copyright (2021, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuyuewen@otcaix.iscas.ac.cn
##
################################################################

echo "Now starting virt monitor service..."
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd ${SHELL_FOLDER}
cd ./virtmonitor
python3 virt_monitor_in_docker.py