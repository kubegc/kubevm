FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:v1.14.1

RUN mkdir -p /home/virtlet/bin

ADD virtlet.py /home/virtlet/bin

ADD virtlet.sh /home/virtlet/bin

ADD utils /home/virtlet/bin/utils

ADD host_cycler.py /home/virtlet/bin

ADD libvirt_event_handler.py /home/virtlet/bin

ADD default.cfg /home/virtlet/bin

RUN rm -fr /tmp/*

WORKDIR /home/virtlet/bin

RUN bash virtlet.sh
