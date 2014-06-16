Name:           harvest-monitor
Version:        0.2.0
Release:        1
Summary:        Harvest Network Traffic Monitor

License:        GPLv2+
URL:            https://github.com/tchx84/harvest-monitor
Source0:        %{name}-%{version}.tar.gz

Requires:       python >= 2.7, olpc-powerd >= 110

BuildArch:      noarch

%description
Network traffic monitoring tool based iptables counters, to be used for the Harvest project

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt/harvest-monitor/
cp -r daemon.py harvest misc $RPM_BUILD_ROOT/opt/harvest-monitor/

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/
cp etc/harvest-monitor.service $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/opt/harvest-monitor/daemon.py
/opt/harvest-monitor/misc/rules.sh
/opt/harvest-monitor/harvest/__init__.py
/opt/harvest-monitor/harvest/log.py
/opt/harvest-monitor/harvest/monitor.py
%{_sysconfdir}/systemd/system/harvest-monitor.service

%changelog
* Thu Jun 12 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- initial version
