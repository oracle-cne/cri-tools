
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%global _find_debuginfo_dwz_opts %{nil}
%else
%global debug_package   %{nil}
%endif

%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:      cri-tools
Version:   1.35.0
Release:   1%{?dist}
Vendor:    Oracle America
Summary:   CLI tool for Kubelet Container Runtime Interface
Group:     Development/Tools
License:   Apache-2.0

Source0: %{name}-%{version}.tar.bz2
BuildRequires: golang
Provides: %{_sysconfdir}/cri-tools/1.35

%description
cri-tools are a utilities for Kubelet Container Runtime Interface runtimes, such as CRI-O.

%prep
%setup -q

%build
mkdir -p _output/src/github.com/kubernetes-incubator/
ln -s `pwd` _output/src/github.com/kubernetes-incubator/cri-tools
export GOFLAGS="-trimpath=false"
export GO_LDFLAGS="-X main.VERSION=v%{version}"
make binaries

%install
rm -rf %{buildroot}

# Create a version file so this project can be bounded as a dependency
install -dp %{buildroot}%{_sysconfdir}/cri-tools
touch %{buildroot}%{_sysconfdir}/cri-tools/1.35

make install BINDIR=%{buildroot}/usr/bin

%files
%license LICENSE THIRD_PARTY_LICENSES.txt
%defattr(-,root,root,-)
%{_sysconfdir}/cri-tools/1.35
/usr/bin/crictl
/usr/bin/critest

%changelog
* Wed Dec 10 2025 Oracle Cloud Native Environment Authors <noreply@oracle.com> - 1.35.0-1
- Added Oracle Specific Build Files for cri-tools
