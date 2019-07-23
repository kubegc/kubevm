FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v1.14.1

RUN mkdir -p /home/virtctl/bin

ADD *.py /home/virtctl/bin/

ADD *.cfg /home/virtctl/bin/

ADD virtctl.sh /home/virtctl/bin/

ADD utils /home/virtctl/bin/utils

ADD scripts /home/virtctl/bin/scripts

RUN rm -fr /tmp/*

WORKDIR /home/virtctl/bin

RUN bash virtctl.sh
