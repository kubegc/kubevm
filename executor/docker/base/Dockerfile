FROM centos:7.6.1810

RUN yum install epel-release -y

RUN yum install centos-release-openstack-rocky.noarch -y

RUN yum install libguestfs-tools-c virt-manager python2-devel python2-pip libvirt-devel gcc gcc-c++ glib-devel glibc-devel libvirt virt-install qemu-kvm -y

RUN yum install glusterfs-client-xlators glusterfs-cli lusterfs-extra-xlators glusterfs-fuse iscsiadm -y

RUN yum install openvswitch-ovn* openvswitch python-openvswitch openvswitch-test openvswitch-devel openvswitch-ipsec -y

RUN pip install --upgrade pip

RUN pip install --ignore-installed prometheus_client kubernetes libvirt-python==5.9.0 xmljson xmltodict watchdog pyyaml pyinstaller grpcio grpcio-tools protobuf psutil

RUN yum clean all

RUN rm -fr /tmp/*