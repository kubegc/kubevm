FROM hrishikesh/systemd-in-docker

RUN yum install epel-release -y

RUN yum install centos-release-openstack-rocky.noarch -y

RUN yum install python3 python3-devel python3-pip libcurl-devel -y

RUN yum install cloud-utils usbutils libguestfs-tools-c virt-manager python2-devel python2-pip libvirt-devel gcc gcc-c++ glib-devel glibc-devel libvirt virt-install qemu-kvm -y

RUN yum install openssh-server openssh-clients arpwatch glusterfs-client-xlators glusterfs-cli lusterfs-extra-xlators glusterfs-fuse iscsiadm -y

RUN yum install openvswitch-ovn* openvswitch python-openvswitch openvswitch-test openvswitch-devel openvswitch-ipsec -y

RUN pip2 install --upgrade "pip < 21.0.0"

RUN pip2 install --ignore-installed threadpool setuptools==38.4.0 cachetools prometheus_client kubernetes==11.0.0 libvirt-python==5.9.0 xmljson xmltodict watchdog==0.10.7 pyyaml grpcio==1.28.1 grpcio-tools==1.28.1 protobuf psutil

RUN pip3 install --upgrade pip

RUN pip3 install --ignore-installed threadpool prometheus_client kubernetes libvirt-python==5.9.0 xmljson xmltodict watchdog pyyaml grpcio grpcio-tools protobuf psutil

# RUN export PYCURL_SSL_LIBRARY=openssl

# RUN easy_install pycurl

RUN yum clean all

RUN rm -fr /tmp/*

RUN systemctl enable libvirtd; systemctl enable virtlockd 

RUN echo "root:root" |chpasswd
RUN systemctl enable sshd
RUN sed -i 's|[#]*PermitRootLogin no|PermitRootLogin yes|g' /etc/ssh/sshd_config
RUN sed -i 's|[#]*PasswordAuthentication no|PasswordAuthentication yes|g' /etc/ssh/sshd_config
RUN sed -i 's|[#]*ChallengeResponseAuthentication no|ChallengeResponseAuthentication yes|g' /etc/ssh/sshd_config
RUN sed -i 's|UsePAM no|UsePAM yes|g' /etc/ssh/sshd_config

RUN echo "listen_tls = 0" >> /etc/libvirt/libvirtd.conf; \
echo 'listen_tcp = 1' >> /etc/libvirt/libvirtd.conf; \
echo 'tls_port = "16514"' >> /etc/libvirt/libvirtd.conf; \ 
echo 'tcp_port = "16509"' >> /etc/libvirt/libvirtd.conf; \
echo 'auth_tcp = "none"' >> /etc/libvirt/libvirtd.conf

RUN echo 'vnc_listen = "0.0.0.0"' >> /etc/libvirt/qemu.conf

RUN echo 'LIBVIRTD_ARGS="--listen"' >> /etc/sysconfig/libvirtd

ADD customlibvirtpost.service /usr/lib/systemd/system/customlibvirtpost.service
ADD customlibvirtpost.sh /customlibvirtpost.sh
RUN chmod a+x /customlibvirtpost.sh
Add network.xml /network.xml
RUN systemctl enable customlibvirtpost

EXPOSE 22
EXPOSE 16509
EXPOSE 5900

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]