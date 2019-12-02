%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      v1.4.10
%endif
 
Name:           kubevmm
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        KubeVMM is a Kubernetes-based virtual machine management platform.
 
Group:          cloudplus/ISCAS
License:        MPLv2.0
URL:            https://github.com/kubesys
Source0:        kubevmm-adm
Source1:        vmm
Source2:        VERSION
Source3:        config
Source4:        kubeovn-adm
Source5:        yamls
Source6:        kubesds-adm
Source7:        kubesds-rpc
Source8:        ovn-ovsdb.service
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
 
%description
"KubeVMM is a Kubernetes-based virtual machine management platform."

%setup -c -n kubevmm
 
%install
mkdir -p %{buildroot}/%{_usr}/bin
mkdir -p %{buildroot}/%{_usr}/lib/systemd/system
install %{SOURCE0} %{buildroot}/%{_usr}/bin/kubevmm-adm
install %{SOURCE1} %{buildroot}/%{_usr}/bin/vmm
install %{SOURCE4} %{buildroot}/%{_usr}/bin/kubeovn-adm
install %{SOURCE6} %{buildroot}/%{_usr}/bin/kubesds-adm
install %{SOURCE7} %{buildroot}/%{_usr}/bin/kubesds-rpc
install %{SOURCE8} %{buildroot}/%{_usr}/lib/systemd/system/ovn-ovsdb.service
mkdir -p %{buildroot}/etc/kubevmm
echo %{version} > %{SOURCE2}
install %{SOURCE2} %{buildroot}/etc/kubevmm
install %{SOURCE3} %{buildroot}/etc/kubevmm
rm -rf %{buildroot}/etc/kubevmm/yamls
mkdir -p %{buildroot}/etc/kubevmm/yamls
install %{SOURCE5}/*.yaml %{buildroot}/etc/kubevmm/yamls

%clean
rm -rf %{buildroot}

%files 
%defattr(755, -, -)
/%{_usr}/bin/kubevmm-adm
/%{_usr}/bin/vmm
/%{_usr}/bin/kubeovn-adm
/%{_usr}/bin/kubesds-adm
/%{_usr}/bin/kubesds-rpc
%defattr(644, -, -)
/etc/kubevmm/VERSION
/etc/kubevmm/config
/%{_usr}/lib/systemd/system/ovn-ovsdb.service
%defattr(755, -, -)
/etc/kubevmm/yamls
