FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest

RUN mkdir -p /home/virtctl/bin

ADD *.py /home/virtctl/bin/

ADD *.cfg /home/virtctl/bin/

ADD virtctl.sh /home/virtctl/bin/

ADD utils /home/virtctl/bin/utils

RUN rm -fr /tmp/*

WORKDIR /home/virtctl/bin

RUN bash virtctl.sh
