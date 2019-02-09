Name:       mce-plugin-libhybris-nondroid
Summary:    Libhybris plugin for Mode Control Entity (libhybris-free variant)
Version:    1.12.3
Release:    1
Group:      System/System Control
License:    LGPLv2.1
URL:        https://github.com/nemomobile/mce-plugin-libhybris
Source0:    %{name}-%{version}.tar.bz2

Requires:         mce >= 1.12.10
Requires:         systemd
Requires(pre):    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Provides:         mce-plugin-libhybris

BuildRequires:  pkgconfig(glib-2.0) >= 2.18.0
BuildRequires:  systemd

%description
This package contains a mce plugin that allows mce to control sysfs-exposed
LEDs. If you use a libhybris-powered HW adaptation, use mce-plugin-libhybris
instead.
This package, despite its name, doesn't actually require libhybris.

%prep
%setup -q -n %{name}-%{version}

%build
make ENABLE_HYBRIS_SUPPORT=n %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# rpm automajick needs +x bits on all elf files after install
chmod 755 %{buildroot}%{_libdir}/mce/modules/hybris.so

%pre
if [ "$1" = "2" ]; then
  # upgrade
  systemctl stop mce.service || :
fi

%post
# upgrade or install
systemctl restart mce.service || :

%preun
if [ "$1" = "0" ]; then
  # uninstall
  systemctl stop mce.service || :
fi

%postun
if [ "$1" = "0" ]; then
  # uninstall
  systemctl start mce.service || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING
# do not include the bogus +x bit for packaged DSOs
%attr(644,-,-) %{_libdir}/mce/modules/hybris.so
