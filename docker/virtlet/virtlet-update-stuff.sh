#!/usr/bin/env bash
##############################################################
##
##      Copyright (2021, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuyuewen@otcaix.iscas.ac.cn
##
################################################################

echo "Now starting virtlet service..."
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd ${SHELL_FOLDER}
cd ./virtlet
python3 virtlet_in_docker.py