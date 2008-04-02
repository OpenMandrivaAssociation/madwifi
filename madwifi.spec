# I love OpenSource :-(

%define name madwifi
%define version 0.9.3.3
%define snaprev r3114
%define snapdate 20080104
%define mdkrelease 5
%if %{snapdate}
%define distname madwifi-ng-%{snaprev}-%{snapdate}
%define release %mkrel %{mdkrelease}.%{snaprev}
%else
%define distname %{name}-%{version}
%define release %mkrel %{mdkrelease}
%endif

Summary:	Multiband Atheros Driver for WiFi (MADWIFI) support
Name:		%{name}
Epoch:  	1
Version:	%{version}
Release:	%{release}
Source0:	%{distname}.tar.gz
Source1:	eee-wlan
Source2:	eee-wlan-off
Source3:	eee-wlan-on
Patch0: 	madwifi-20050829-x86_64-rules.patch
# from http://madwifi.org/attachment/ticket/1679/
# (with first hunk removed)
Patch1:		madwifi-ng-0933.ar2425.20071130.i386.patch
License:	BSD or GPLv2
Url:		http://sourceforge.net/projects/madwifi
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	sharutils kernel-source

%description -n %{name}
Multiband Atheros Driver for WiFi (MADWIFI): 
Linux driver for 802.11a/b/g universal NIC cards Cardbus, PCI, or miniPCI
using Atheros chip sets. See also: 
 http://www.mattfoster.clara.co.uk/madwifi-faq.htm, 
 http://madwifiwiki.thewebhost.de/wiki/

%package -n dkms-%{name}
Summary:	Multiband Atheros Driver for WiFi (MADWIFI) dkms driver
Group:		System/Kernel and hardware
Requires:	dkms

%description -n dkms-%{name}
Multiband Atheros Driver for WiFi (MADWIFI): 
Linux driver for 802.11a/b/g universal NIC cards Cardbus, PCI, or miniPCI
using Atheros chip sets. See also: 
 http://www.mattfoster.clara.co.uk/madwifi-faq.htm, 
 http://madwifiwiki.thewebhost.de/wiki/

%prep
%setup -q -n %{distname}
%patch0 -p1 -b .x86_64-rules
%ifarch %{ix86}
# (blino) applied on i386 only since it breaks ABI and only i386 HAL has been updated
%patch1 -p0 -b .ar2425
%endif

%build
%make -C tools

%install
rm -rf $RPM_BUILD_ROOT

# driver source
mkdir -p $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}-%{release}
cp -r * $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}-%{release}
cat > $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}

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

# reload ath_pci after suspend
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pm/config.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/pm/config.d/%name <<EOF
SUSPEND_MODULES="\$SUSPEND_MODULES ath_pci"
EOF
# reload ath_pci on EEE after switching wlan
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/{events,actions}
cp %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions
cp %SOURCE2 %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events

%post -n dkms-%{name}
/usr/sbin/dkms --rpm_safe_upgrade add -m %name -v %version-%release
/usr/sbin/dkms --rpm_safe_upgrade build -m %name -v %version-%release
/usr/sbin/dkms --rpm_safe_upgrade install -m %name -v %version-%release --force
exit 0

%preun -n dkms-%{name}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %name -v %version-%release --all
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYRIGHT README
%{_bindir}/*
%{_mandir}/man*/*
%{_sysconfdir}/pm/config.d/%name
%{_sysconfdir}/acpi/*/eee-*

%files -n dkms-%{name}
%defattr(-,root,root)
%doc COPYRIGHT README
%dir %{_usr}/src/%{name}-%{version}-%{release}
%{_usr}/src/%{name}-%{version}-%{release}/*
