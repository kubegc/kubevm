FROM centos:7

RUN mkdir -p /etc/kubernetes

ADD ./scheduler /usr/local/bin/kubevirt-scheduler
ADD ./admin.conf /etc/kubernetes/

WORKDIR /usr/local/bin/

#RUN ./kubecrd-scheduler --kubeconfig=/etc/kubernetes/admin.conf --scheduler-name=kubecrd-scheduler --port=10253 --secure-port=10261 --leader-elect=true --lock-object-namespace=cloudplus
