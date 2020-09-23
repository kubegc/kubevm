%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      v1.9.9.rc7
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
Source7:        kubesds-rpc-service
Source8:        ovn-ovsdb.service
Source9:        yum.repos.d
Source10:       kubevirt-ctl
Source11:       device-passthrough
Source12:       kubesds.service
Source13:       virt-monitor
Source14:       virt-monitor-ctl
Source15:       kubevmm-monitor.service
Source16:       kubesds-ctl.sh
Source17:       monitor
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
install %{SOURCE7} %{buildroot}/%{_usr}/bin/kubesds-rpc-service
install %{SOURCE10} %{buildroot}/%{_usr}/bin/kubevirt-ctl
install %{SOURCE11} %{buildroot}/%{_usr}/bin/device-passthrough
install %{SOURCE16} %{buildroot}/%{_usr}/bin/kubesds-ctl.sh
install %{SOURCE13} %{buildroot}/%{_usr}/bin/virt-monitor
install %{SOURCE14} %{buildroot}/%{_usr}/bin/virt-monitor-ctl
install %{SOURCE8} %{buildroot}/%{_usr}/lib/systemd/system/ovn-ovsdb.service
install %{SOURCE12} %{buildroot}/%{_usr}/lib/systemd/system/kubesds.service
install %{SOURCE15} %{buildroot}/%{_usr}/lib/systemd/system/kubevmm-monitor.service
mkdir -p %{buildroot}/etc/kubevmm
echo %{version} > %{SOURCE2}
install %{SOURCE2} %{buildroot}/etc/kubevmm
install %{SOURCE3} %{buildroot}/etc/kubevmm
rm -rf %{buildroot}/etc/kubevmm/yamls
mkdir -p %{buildroot}/etc/kubevmm/yamls/cloudplus
install %{SOURCE5}/cloudplus/* %{buildroot}/etc/kubevmm/yamls/cloudplus
rm -rf %{buildroot}/etc/kubevmm/monitor
mkdir -p %{buildroot}/etc/kubevmm/monitor
install %{SOURCE17}/* %{buildroot}/etc/kubevmm/monitor
mkdir -p %{buildroot}/etc/yum.repos.d
install %{SOURCE9}/*.repo %{buildroot}/etc/yum.repos.d

%clean
rm -rf %{buildroot}

%files 
%defattr(755, -, -)
/%{_usr}/bin/kubevmm-adm
/%{_usr}/bin/vmm
/%{_usr}/bin/kubeovn-adm
/%{_usr}/bin/kubesds-adm
/%{_usr}/bin/kubesds-rpc-service
/%{_usr}/bin/kubevirt-ctl
/%{_usr}/bin/device-passthrough
/%{_usr}/bin/kubesds-ctl.sh
/%{_usr}/bin/virt-monitor
/%{_usr}/bin/virt-monitor-ctl
%defattr(644, -, -)
/etc/kubevmm/VERSION
/etc/kubevmm/config
/%{_usr}/lib/systemd/system/ovn-ovsdb.service
/%{_usr}/lib/systemd/system/kubevmm-monitor.service
/%{_usr}/lib/systemd/system/kubesds.service
%defattr(644, -, -, 755)
/etc/kubevmm/yamls/cloudplus
/etc/yum.repos.d
/etc/kubevmm/monitor
