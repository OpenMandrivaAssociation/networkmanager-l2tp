%define nm_version          0.9.8.0
%define dbus_version        0.74
%define gtk3_version        3.0
%define shared_mime_version 0.16-3
%define up_ver	0.9

Summary:   NetworkManager VPN plugin for l2tp
Name:      NetworkManager-l2tp
Version:   0.9.6
Release:   1%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       https://launchpad.net/~seriy-pr/+archive/network-manager-l2tp
Source:    %{name}-%{version}.tar.gz

BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: perl-XML-Parser
BuildRequires: perl
BuildRequires: ppp-devel
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libnm-util) >= %{nm_version}
BuildRequires: pkgconfig(libnm-glib) >= %{nm_version}
BuildRequires: pkgconfig(libnm-glib-vpn) >= %{nm_version}
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libpng15)
Requires: dbus
Requires: gtk+3            >= %{gtk3_version}
Requires: dbus             >= %{dbus_version}
Requires: NetworkManager   >= %{nm_version}
Requires: shared-mime-info >= %{shared_mime_version}
Requires: gnome-keyring
Requires: pptp-linux
Requires: ppp-pppoe
Requires: xl2tpd

%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q


%build
./autogen.sh
%configure2_5x \
	--disable-static \
	--disable-dependency-tracking \
	--enable-more-warnings=yes

%make

%install
%makeinstall_std

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%find_lang NetworkManager-l2tp


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%{_libexecdir}/nm-l2tp-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libexecdir}/nm-l2tp-service
%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
#%{_datadir}/applications/nm-pptp.desktop
#%{_datadir}/icons/hicolor/48x48/apps/gnome-mime-application-x-pptp-settings.png
%dir %{_datadir}/gnome-vpn-properties/l2tp
%{_datadir}/gnome-vpn-properties/l2tp/nm-l2tp-dialog.ui

%changelog

* Thu Feb 26 2012 akdengi <akdengi> - 0.9.6-1
- initial version based on NetworkManager-pptp 1:0.9.3.997-3

