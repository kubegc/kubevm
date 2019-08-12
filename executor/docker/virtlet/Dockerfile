FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest

RUN mkdir -p /home/virtlet/bin

ADD *.py /home/virtlet/bin/

ADD *.cfg /home/virtlet/bin/

ADD virtlet.sh /home/virtlet/bin/

ADD utils /home/virtlet/bin/utils

RUN rm -fr /tmp/*

WORKDIR /home/virtlet/bin

RUN bash virtlet.sh
