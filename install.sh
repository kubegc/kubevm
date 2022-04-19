#!/usr/bin/env bash

yum install epel-release -y

yum install centos-release-openstack-rocky.noarch -y

yum install python3 python3-devel python3-pip libcurl-devel -y

yum install cloud-utils usbutils libguestfs-tools-c virt-manager python2-devel python2-pip libvirt-devel gcc gcc-c++ glib-devel glibc-devel libvirt virt-install qemu-kvm -y

yum install glusterfs-client-xlators glusterfs-cli lusterfs-extra-xlators glusterfs-fuse iscsiadm -y

yum install openvswitch-ovn* openvswitch python-openvswitch openvswitch-test openvswitch-devel openvswitch-ipsec -y

pip3 install --upgrade pip

pip3 install --ignore-installed threadpool prometheus_client kubernetes libvirt-python==5.9.0 xmljson xmltodict watchdog pyyaml grpcio grpcio-tools protobuf psutil

SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd ${SHELL_FOLDER}

kubectl apply -f ./yamls/*.yaml