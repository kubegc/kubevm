FROM centos:7.6.1810

RUN yum install epel-release -y

RUN yum install centos-release-openstack-rocky.noarch -y

RUN yum install python3 python3-devel python3-pip libcurl-devel -y

RUN yum install cloud-utils usbutils libguestfs-tools-c virt-manager python2-devel python2-pip libvirt-devel gcc gcc-c++ glib-devel glibc-devel libvirt virt-install qemu-kvm -y

RUN yum install glusterfs-client-xlators glusterfs-cli lusterfs-extra-xlators glusterfs-fuse iscsiadm -y

RUN yum install openvswitch-ovn* openvswitch python-openvswitch openvswitch-test openvswitch-devel openvswitch-ipsec -y

RUN pip2 install --upgrade "pip < 21.0"

RUN pip2 install --ignore-installed threadpool cachetools==3.1.1 setuptools==44.1.1 prometheus_client kubernetes==12.0.1 libvirt-python==5.9.0 xmljson xmltodict watchdog==0.10.7 pyyaml grpcio grpcio-tools protobuf psutil

RUN pip3 install --upgrade pip

RUN pip3 install --ignore-installed threadpool prometheus_client kubernetes libvirt-python==5.9.0 xmljson xmltodict watchdog pyyaml grpcio grpcio-tools protobuf psutil

# RUN export PYCURL_SSL_LIBRARY=openssl

# RUN easy_install pycurl

RUN yum clean all

RUN rm -fr /tmp/*