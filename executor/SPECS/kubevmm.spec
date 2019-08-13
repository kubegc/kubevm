%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      v0.8.0
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
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
 
%description
"kubevmm-adm is a command for service managent in KubeVMM platform."

%setup -c -n kubevmm
 
%install
mkdir -p %{buildroot}/%{_usr}/bin
install %{SOURCE0} %{buildroot}/%{_usr}/bin/kubevmm-adm
install %{SOURCE1} %{buildroot}/%{_usr}/bin/vmm

%clean
rm -rf %{buildroot}

%files 
%defattr(755, -, -)
/%{_usr}/bin/kubevmm-adm
/%{_usr}/bin/vmm
