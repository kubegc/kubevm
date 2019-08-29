FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest

RUN mkdir -p /home/kubevmm/bin

RUN mkdir -p /etc/kubevmm

ADD *.py /home/kubevmm/bin/

ADD *.cfg /home/kubevmm/bin/

ADD *.sh /home/kubevmm/bin/

ADD utils /home/kubevmm/bin/utils

ADD config /home/kubevmm/bin/

Add kubeovn-adm /home/kubevmm/bin/

Add kubevmm-adm /home/kubevmm/bin/

Add vmm /home/kubevmm/bin/

Add VERSION /home/kubevmm/bin

RUN rm -fr /tmp/*

WORKDIR /home/kubevmm/bin

RUN bash virtctl.sh
