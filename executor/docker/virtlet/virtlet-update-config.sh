#!/usr/bin/env bash
##############################################################
##
##      Copyright (2019, ) Institute of Software
##          Chinese Academy of Sciences
##             Author: wuheng@otcaix.iscas.ac.cn
##
################################################################

cp -f /home/kubevmm/bin/config /etc/kubevmm/config-virtlet.new
mv -f /etc/kubevmm/config-virtlet.new /etc/kubevmm/config
python virtlet_in_docker.py
