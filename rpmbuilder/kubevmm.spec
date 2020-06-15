# Copyright (2018, ) Institute of Software, Chinese Academy of Sciences
# Author wuheng@iscas.ac.cn
# Date   2018-11-29

Name: kubevmm
Version: 1.17.5
Release: 2020.iscas%{?dist}
Source: %{name}-%{version}.tar.gz
Summary: auto generated
Packager: _MAINTAINER_
License: ASL 2.0

%description
_NAME_-_VERSION_

%prep
%setup -n %{name}-%{version}

%install
mkdir -p %{buildroot}/
cp -r /root/rpmbuild/BUILD/%{name}-%{version}/* %{buildroot}/

%files
/
