FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubernetes-kvm-base:latest

RUN mkdir -p /home/kubevmm/core

RUN mkdir -p /etc/kubevmm

ADD *.sh /home/kubevmm/core/

ADD virtlet /home/kubevmm/core/virtlet

ADD utils /home/kubevmm/core/utils

ADD *.cfg /home/kubevmm/core/utils

RUN rm -fr /tmp/*

WORKDIR /home/kubevmm/core

RUN systemctl start libvirtd

RUN bash virtlet.sh