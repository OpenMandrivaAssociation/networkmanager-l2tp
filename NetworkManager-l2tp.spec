%global _disable_ld_no_undefined 1

%global pppd_version %(rpm -q --qf "%{VERSION}" ppp)

%bcond_with strongswan

Summary:	NetworkManager VPN plugin for L2TP and L2TP/IPsec
Name:		networkmanager-l2tp
Version:	1.20.8
Release:	1
License:	GPLv2+
Group:		System Environment/Base
Url:		https://github.com/nm-l2tp/NetworkManager-l2tp
Source0:	https://github.com/nm-l2tp/NetworkManager-l2tp/releases/download/%{version}/NetworkManager-l2tp-%{version}.tar.xz

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	ppp-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libnma)
BuildRequires:  pkgconfig(libnma-gtk4)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(nss)

Requires:	dbus
Requires:	gtk+3
Requires:	gtk4
Requires:	NetworkManager
Requires:	ppp = %{ppp_version}
Requires:	pptp
Requires:	shared-mime-info
Requires:	xl2tpd

%if %with strongswan
Recommends:	strongswan
%endif

%description
This package contains software for integrating L2TP and L2TP over	
IPsec VPN support with 	the NetworkManager and the GNOME desktop.

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md NEWS
%{_datadir}/dbus-1/system.d/nm-l2tp-service.conf
%{_prefix}/lib/NetworkManager/VPN/nm-l2tp-service.name
%{_libexecdir}/nm-l2tp-auth-dialog
%{_libexecdir}/nm-l2tp-service
%{_libdir}/NetworkManager/libnm-vpn-plugin-l2tp.so
%{_libdir}/NetworkManager/libnm-vpn-plugin-l2tp-editor.so
%{_libdir}/NetworkManager/libnm-gtk4-vpn-plugin-l2tp-editor.so
%{_libdir}/pppd/%{pppd_version}/nm-l2tp-pppd-plugin.so
%{_metainfodir}/network-manager-l2tp.metainfo.xml
%ghost %attr(0600 - -) %{_sysconfdir}/ipsec.d/ipsec.nm-l2tp.secrets
%ghost %attr(0600 - -) %{_sysconfdir}/strongswan/ipsec.d/ipsec.nm-l2tp.secrets

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n NetworkManager-l2tp-%{version}

%build
autoreconf -fiv
%configure \
	--enable-more-warnings=yes \
	--enable-lto=yes \
	--runstatedir=/run \
	--with-gnome=yes \
	--with-gtk4 \
%if %with strongswan
	--enable-libreswan-dh2 \
	--with-nm-ipsec-nss-dir=%{_sysconfdir}/ipsec.d \
%else
	--with-nm-ipsec-nss-dir=%{_sharedstatedir}/ipsec/nss \
%endif
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{pppd_version} \
	--with-dist-version=%{version}-%{release} \
	%{nil}
%make_build

%install
%make_install

# remove static
find %{buildroot}%{_libdir} -name \*\.la -delete

mkdir -p %{buildroot}%{_sysconfdir}/ipsec.d
mkdir -p %{buildroot}%{_sysconfdir}/strongswan/ipsec.d

touch %{buildroot}%{_sysconfdir}/ipsec.d/ipsec.nm-l2tp.secrets
touch %{buildroot}%{_sysconfdir}/strongswan/ipsec.d/ipsec.nm-l2tp.secrets

# locales
%find_lang %{name} --all-name
 
%check
make check

