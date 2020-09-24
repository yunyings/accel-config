%global	project_name	idxd-config

Name:		accel-config
Version:	2.8
Release:	1%{?dist}
Summary:	Configure accelerator subsystem devices
License:	GPLv2
URL:		https://github.com/intel/%{project_name}
Source0:	%{URL}/archive/%{name}-v%{version}.tar.gz

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:	autoconf
BuildRequires:	asciidoc
BuildRequires:	xmlto
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libkmod)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	systemd

# accel-config is for configuring Intel DSA (Data-Streaming
# Accelerator) subsystem in the Linux kernel. It supports x86 only.
ExclusiveArch:	%{ix86} x86_64

%description
Utility library for configuring the accelerator subsystem.

%package -n %{name}-devel
Summary:	Development files for libaccfg
License:	LGPLv2
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n %{name}-libs
Summary:	Configuration library for accelerator subsystem devices
License:	LGPLv2

%description -n %{name}-libs
Libraries for %{name}.

%package -n %{name}-test
Summary:	Unit tests for %{name}.
License:	GPLv2

%description -n %{name}-test
Unit tests for %{name}

%prep
%autosetup -n %{project_name}-%{name}-v%{version}

%build
echo %{version} > version
./autogen.sh
%configure --disable-static --disable-silent-rules --enable-test
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%files
%license Documentation/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{_sysconfdir}/%{name}/%{name}.conf.sample

%files -n %{name}-libs
%doc README.md
%license Documentation/COPYING licenses/BSD-MIT licenses/CC0
%{_libdir}/lib%{name}.so.*

%files -n %{name}-devel
%license Documentation/COPYING
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%files -n %{name}-test
%license Documentation/COPYING
%{_datadir}/%{name}/test/*

%changelog
* Thu Sep 24 2020 Yunying Sun <yunying.sun@intel.com> - 2.8-1
- Initial Packaging
