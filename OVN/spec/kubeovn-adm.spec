# Copyright (2018, ) Institute of Software, Chinese Academy of Sciences
# Author wuheng@iscas.ac.cn
# Date   2018-11-29

Name: kubeovn-adm
Version: v1.0.0
Release: cloudplus.1909%{?dist}
Source: %{name}-%{version}.tar.gz
Summary: auto generated
Requires: libmlx5
Requires: openvswitch-ovn-host
Requires: openvswitch-ovn-common
Requires: openvswitch-ovn-central
Requires: openvswitch-ipsec
Requires: openvswitch-ovn-vtep
Requires: openvswitch
Packager: wuheng@otcaix.iscas.ac.cn
License: ASL 2.0

%description
kubeovn-adm-v1.0.0

%prep
%setup -n %{name}-%{version}

%install
mkdir -p %{buildroot}/
cp -r /root/rpmbuild/BUILD/%{name}-%{version}/* %{buildroot}/

%files
/

