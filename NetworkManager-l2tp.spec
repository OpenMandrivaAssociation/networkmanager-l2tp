%define url_ver %(echo %{version}|cut -d. -f1,2)
%define pppver %(rpm -q --qf "%{VERSION}" ppp)
%define pppddir %{_libdir}/pppd/%{pppver}

Summary:	NetworkManager VPN plugin for l2tp
Name:		networkmanager-l2tp
Version:	0.9.8.0
Release:	1
License:	GPLv2+
Group:		System Environment/Base
Url:		https://launchpad.net/~seriy-pr/+archive/network-manager-l2tp
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	ppp-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libnm-util)
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libnm-glib-vpn)
Requires:	dbus
Requires:	gnome-keyring
Requires:	NetworkManager
Requires:	ppp
Requires:	pptp
Requires:	shared-mime-info
Requires:	xl2tpd

%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q

%build
./autogen.sh
%configure \
	--disable-static \
	--enable-more-warnings=yes \
	--with-pppd-plugin-dir=%{pppddir}

%make

%install
%makeinstall_std

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libdir}/NetworkManager/lib*.so*
%{_libexecdir}/nm-l2tp-service
%{_libexecdir}/nm-l2tp-auth-dialog
%{pppddir}/nm-l2tp-pppd-plugin.so
%dir %{_datadir}/gnome-vpn-properties/l2tp
%{_datadir}/gnome-vpn-properties/l2tp/nm-l2tp-dialog.ui

