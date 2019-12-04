FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubeext-base:v1.5.0-arm8

RUN mkdir -p /home/kubevmm/bin

RUN mkdir -p /etc/kubevmm

ADD *.py /home/kubevmm/bin/

ADD *.cfg /home/kubevmm/bin/

ADD *.sh /home/kubevmm/bin/

ADD utils /home/kubevmm/bin/utils

ADD yamls /home/kubevmm/bin/yamls

ADD config /home/kubevmm/bin/

ADD VERSION /home/kubevmm/bin

RUN rm -fr /tmp/*

WORKDIR /home/kubevmm/bin

RUN bash virtctl.sh
