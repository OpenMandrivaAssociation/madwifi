# I love OpenSource :-(

%define name madwifi
#define rversion 20050829
#define version 0.%{rversion}
%define version 0.9.3.2
%define rversion 0.9.3.2
%define mdkrelease 1
%define release %mkrel %{mdkrelease}

Summary:	Multiband Atheros Driver for WiFi (MADWIFI) support.
Name:		%{name}
Epoch:  	1
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{rversion}.tar.bz2
Patch0:		madwifi-20050829-x86_64-rules.patch
License:	BSD or GPLv2
Url:		http://sourceforge.net/projects/madwifi
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-buildroot
Prefix:		%{_prefix}
Requires:	drakxtools >= 9.2-8mdk
BuildRequires:	sharutils kernel-source

%description -n %{name}
Multiband Atheros Driver for WiFi (MADWIFI): 
Linux driver for 802.11a/b/g universal NIC cards Cardbus, PCI, or miniPCI
using Atheros chip sets. See also: 
 http://www.mattfoster.clara.co.uk/madwifi-faq.htm, 
 http://madwifiwiki.thewebhost.de/wiki/

%package -n dkms-%{name}
Summary:	Multiband Atheros Driver for WiFi (MADWIFI) dkms driver.
Group:		System/Kernel and hardware
Requires:	dkms, drakxtools >= 9.2-8mdk

%description -n dkms-%{name}
Multiband Atheros Driver for WiFi (MADWIFI): 
Linux driver for 802.11a/b/g universal NIC cards Cardbus, PCI, or miniPCI
using Atheros chip sets. See also: 
 http://www.mattfoster.clara.co.uk/madwifi-faq.htm, 
 http://madwifiwiki.thewebhost.de/wiki/

%prep
%setup -q -n %{name}-%{rversion}
%patch0 -p1 -b .x86_64-rules

%build
%make -C tools

%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/%{name}-%{rversion}

# driver source
mkdir -p $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}
cp -r * $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}
cat > $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}/dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}

DEST_MODULE_LOCATION[0]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[1]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[2]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[3]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[4]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[5]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[6]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[7]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[8]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[9]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[10]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[11]=/kernel/drivers/net/wireless
DEST_MODULE_LOCATION[12]=/kernel/drivers/net/wireless
BUILT_MODULE_NAME[0]=ath_pci
BUILT_MODULE_LOCATION[0]=ath
BUILT_MODULE_NAME[1]=ath_hal
BUILT_MODULE_LOCATION[1]=ath_hal
BUILT_MODULE_NAME[2]=wlan
BUILT_MODULE_LOCATION[2]=net80211
BUILT_MODULE_NAME[3]=wlan_wep
BUILT_MODULE_LOCATION[3]=net80211
BUILT_MODULE_NAME[4]=wlan_tkip
BUILT_MODULE_LOCATION[4]=net80211
BUILT_MODULE_NAME[5]=wlan_ccmp
BUILT_MODULE_LOCATION[5]=net80211
BUILT_MODULE_NAME[6]=wlan_xauth
BUILT_MODULE_LOCATION[6]=net80211
BUILT_MODULE_NAME[7]=wlan_acl
BUILT_MODULE_LOCATION[7]=net80211
BUILT_MODULE_NAME[8]=wlan_scan_ap
BUILT_MODULE_LOCATION[8]=net80211
BUILT_MODULE_NAME[9]=wlan_scan_sta
BUILT_MODULE_LOCATION[9]=net80211
BUILT_MODULE_NAME[10]=ath_rate_amrr
BUILT_MODULE_LOCATION[10]=ath_rate/amrr
BUILT_MODULE_NAME[11]=ath_rate_onoe
BUILT_MODULE_LOCATION[11]=ath_rate/onoe
BUILT_MODULE_NAME[12]=ath_rate_sample
BUILT_MODULE_LOCATION[12]=ath_rate/sample

MAKE[0]="make KERNELPATH=\${kernel_source_dir} TARGET=%{_arch}-elf modules"

AUTOINSTALL=yes
EOF

# utils 
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
%makeinstall -C tools DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} MANDIR=%{_mandir}

%post -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %name -v %version
/usr/sbin/dkms --rpm_safe_upgrade build -m %name -v %version
/usr/sbin/dkms --rpm_safe_upgrade install -m %name -v %version

%preun -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %name -v %version --all

%clean
rm -rf $RPM_BUILD_DIR/%{name}
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYRIGHT README
%{_bindir}/*
%{_mandir}/man*/*

%files -n dkms-%{name}
%defattr(-,root,root)
%doc COPYRIGHT README
%dir %{_usr}/src/%{name}-%{version}
%{_usr}/src/%{name}-%{version}/*
