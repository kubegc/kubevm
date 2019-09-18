%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      v1.2.6
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
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
 
%description
"KubeVMM is a Kubernetes-based virtual machine management platform."

%setup -c -n kubevmm
 
%install
mkdir -p %{buildroot}/%{_usr}/bin
install %{SOURCE0} %{buildroot}/%{_usr}/bin/kubevmm-adm
install %{SOURCE1} %{buildroot}/%{_usr}/bin/vmm
install %{SOURCE4} %{buildroot}/%{_usr}/bin/kubeovn-adm
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
%defattr(644, -, -)
/etc/kubevmm/VERSION
/etc/kubevmm/config
%defattr(755, -, -)
/etc/kubevmm/yamls
