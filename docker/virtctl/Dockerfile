FROM registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-base:latest

RUN mkdir -p /home/kubevmm/bin

RUN mkdir -p /etc/kubevmm

ADD *.py /home/kubevmm/bin/

ADD *.cfg /home/kubevmm/bin/

ADD *.sh /home/kubevmm/bin/

ADD utils /home/kubevmm/bin/utils

ADD yamls /home/kubevmm/bin/yamls

ADD config /home/kubevmm/bin/

ADD kubeovn-adm /home/kubevmm/bin/

ADD kubevirt-ctl /home/kubevmm/bin/

ADD device-passthrough /home/kubevmm/bin/

ADD kubevmm-adm /home/kubevmm/bin/

ADD virt-monitor /home/kubevmm/bin/

# ADD libvirt-event-handler /home/kubevmm/bin/

ADD vmm /home/kubevmm/bin/

ADD kubesds-adm /home/kubevmm/bin/

ADD kubesds-rpc-service /home/kubevmm/bin/

ADD VERSION /home/kubevmm/bin/

RUN rm -fr /tmp/*

WORKDIR /home/kubevmm/bin

RUN bash virtctl.sh
