FROM centos:7

RUN yum install epel-release -y

RUN yum install virt-manager python2-devel python2-pip libvirt-devel gcc gcc-c++ glib-devel glibc-devel libvirt virt-install -y

RUN pip install --upgrade pip

RUN pip install --ignore-installed kubernetes libvirt-python xmljson xmltodict watchdog pyyaml pyinstaller

RUN yum clean all

RUN rm -fr /tmp/*