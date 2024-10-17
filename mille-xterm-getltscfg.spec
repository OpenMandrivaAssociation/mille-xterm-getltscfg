%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define svn 2137

Summary:	Tool to parse LTSP configuration
Name:		mille-xterm-getltscfg
Version:	1.0
Release:	%mkrel 0.%{svn}.4
License:	GPL
Group:		System/Libraries
URL:		https://www.ltsp.org
Source0:	http://www.ltsp.org/tarballs/%{name}-%{version}.tar.bz2
BuildRequires:	bison
BuildRequires:	uClibc-popt-devel
BuildRequires:	uClibc-flex
BuildRequires:	uClibc-devel
BuildRequires:	uClibc-static-devel
BuildRequires:	flex
BuildRoot:	%{_tmppath}/%{name}-root

%description
This program is used in LTSP to read the lts.cfg config file.

%prep

%setup -q

# uClibc hack
perl -pi -e "s|^LEX.*|LEX=%{_bindir}/flex|g" src/Makefile
perl -pi -e "s|^LIBS.*|LIBS=%{_prefix}/%{_target_cpu}-linux-uclibc/usr/lib/libfl.a %{_prefix}/%{_target_cpu}-linux-uclibc/usr/lib/libpopt.a|g" src/Makefile
perl -pi -e "s|^CCFLAGS=.*|CCFLAGS=-Os -Wl,-Bstatic|g" src/Makefile
perl -pi -e "s|^LDFLAGS=.*|LDFLAGS=-s -static|g" src/Makefile

%build

cd src
uclibc make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}/bin

install -m0755 src/getltscfg %{buildroot}/bin/getltscfg.real
install -m0755 src/getltscfg.script %{buildroot}/bin/getltscfg
install -m0644 src/lts.conf %{buildroot}%{_sysconfdir}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING AUTHORS Changelog
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/lts.conf
%attr(0755,root,root) /bin/getltscfg
%attr(0755,root,root) /bin/getltscfg.real


