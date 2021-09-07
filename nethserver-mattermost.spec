%define mattermost_release 5.38.2

# HACK: avoid "No build ID note found" error
%undefine _missing_build_ids_terminate_build
# Disable debug package
%define debug_package %{nil}

Summary: NethServer Mattermost configuration
Name: nethserver-mattermost
Version: 1.6.12
Release: 1%{?dist}
License: Proprietary
Source: %{name}-%{version}.tar.gz
Source1: https://releases.mattermost.com/%{mattermost_release}/mattermost-%{mattermost_release}-linux-amd64.tar.gz
Source2: %{name}.tar.gz
BuildArch: x86_64
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Requires: nethserver-httpd, nethserver-postgresql12

%description
NethServer Mattermost files and configuration.

%pre
if ! getent passwd mattermost >/dev/null; then
   # Add the "mattermost" user
   useradd -r -U -s /sbin/nologin -d /var/lib/nethserver/mattermost -c "Mattermost user" mattermost
fi


%prep
%setup


%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
mkdir -p %{buildroot}/opt
tar xvf %{SOURCE1} -C %{buildroot}/opt
mkdir -p %{buildroot}/var/lib/nethserver/mattermost/{backup,data}

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE2} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%{genfilelist} %{buildroot} \
  --file /etc/sudoers.d/50_nsapi_nethserver_mattermost 'attr(0440,root,root)' \
  --dir /var/lib/nethserver/mattermost/backup 'attr(0755,postgres,postgres)' \
  --dir /var/lib/nethserver/mattermost/data 'attr(0755,mattermost,mattermost)'  | grep -v /opt/mattermost/ >  %{name}-%{version}-filelist


cat %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir /opt/mattermost %attr(0755,mattermost,mattermost)
%attr(-,mattermost,mattermost) /opt/mattermost/*
%config(noreplace) /opt/mattermost/config/config.json
%doc COPYING
%dir %{_nseventsdir}/%{name}-update


%changelog
* Tue Sep 07 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.12-1
- Mattermost 5.38.2 - NethServer/dev#6565

* Wed Jul 21 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.11-1
- Mattermost 5.37.0 - NethServer/dev#6545

* Tue Jun 22 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.10-1
- Mattermost 5.36.1 - NethServer/dev#6532

* Mon Jun 21 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.9-1
- Mattermost 5.36.0 - NethServer/dev#6525

* Mon Jun 14 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.8-1
- Mattermost 5.35.3 - NethServer/dev#6524

* Mon May 17 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.7-1
- Mattermost 5.35.0 - NethServer/dev#6512

* Mon Apr 19 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.6-1
- Mattermost: push notification server overwritten by update - Bug NethServer/dev#6489
- Mattermost 5.34.1 - NethServer/dev#6484

* Thu Mar 25 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.5-1
- Mattermost 5.33.0 - NethServer/dev#6459

* Mon Feb 22 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.4-1
- Mattermost 5.32.1 - NethServer/dev#6430

* Thu Feb 11 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.3-1
- Mattermost 5.31.1 - NethServer/dev#6421

* Mon Feb 01 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.2-1
- Mattermost corrupted configuration file - Bug NethServer/dev#6407

* Wed Jan 20 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.1-1
- Mattermost 5.31.0 - NethServer/dev#6395

* Tue Dec 22 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.0-1
- Mattermost 5.30.1 - NethServer/dev#6372

* Tue Nov 17 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.5-1
- Mattermost 5.29.0 - NethServer/dev#6331

* Wed Oct 21 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.4-1
- Correct counting of Mattermost users - NethServer/dev#6312

* Tue Oct 20 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.3-1
- Mattermost 5.28.1 - NethServer/dev#6311

* Tue Sep 29 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.2-1
- Mattermost DB encoding error with LATIN1 - Bug NethServer/dev#6286

* Mon Sep 21 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.1-1
- Mattermost wrong SMTP configiration - Bug NethServer/dev#6273
- Mattermost 5.27.0 - NethServer/dev#6272

* Wed Sep 16 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- Mattermost 5.26.2 - NethServer/dev#6263

* Wed Sep 02 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.11-1
- Mattermost 5.25.4 - NethServer/dev#6251

* Mon Jul 27 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.10-1
- Mattermost 5.25.1 - NethServer/dev#6240

* Thu Jul 16 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.9-1
- Mattermost 5.25.0 - NethServer/dev#6227

* Wed Jul 01 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.8-1
- Mattermost 5.24.2 - NethServer/dev#6214
- Human readable numbers in Cockpit dashboards - NethServer/dev#6206

* Thu Jun 04 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.7-1
- Mattermost: Database and data disk usage in dashboard - NethServer/dev#6191
- Mattermost 5.23.1 - NethServer/dev#6189
- Remove TLS 1.0 and TLS 1.1 - NethServer/dev#6170

* Fri May 15 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.6-1
- Mattermost 5.23.0 - NethServer/dev#6167

* Mon Apr 20 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.5-1
- Mattermost 5.22.0 - NethServer/dev#6129

* Wed Mar 25 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.4-1
- Mattermost 5.21.0 - NethServer/dev#6094
- Cockpit: change package Dashboard page title - NethServer/dev#6004

* Mon Dec 09 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.3-1
- Inventory: add new application facts - NethServer/dev#5979

* Mon Dec 02 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.2-1
- Mattermost 5.17.1 - NethServer/dev#5968

* Wed Oct 09 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.1-1
- Mattermost bulk user creation script fails - Bug NethServer/dev#5851
- Mattermost 5.15 - NethServer/dev#5857

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805
- systemd unit: catch stdout to avoid useless logs (#22)

* Tue Sep 03 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.2-1
- Cockpit. List correct application version - NethServer/dev#5819
- Mattermost 5.14 - NethServer/dev#5820

* Mon Aug 26 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.1-1
- Cockpit. fix various bugs - Bug Nethserver/dev#5810

* Wed Jul 10 2019 Davide Principi <davide.principi@nethesis.it> - 1.3.0-1
- Mattermost 5.12 - NethServer/dev#5785

* Tue Mar 26 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.3-1
- Mattermost: update to 5.9.0 - NethServer/dev#5734

* Fri Feb 15 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.2-1
- Mattermost: update to 5.7.1 - NethServer/dev#5711

* Tue Feb 12 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.1-1
- Mattermost: update to 5.7.0 - NethServer/dev#5702

* Mon Dec 03 2018 Davide Principi <davide.principi@nethesis.it> - 1.2.0-1
- Mattermost: update to 5.5.0 - NethServer/dev#5659

* Tue Sep 25 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.2-1
- Mattermost: update to release 5.3.1 - NethServer/dev#5587

* Thu Jun 14 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.1-1
- Mattermost: upgrade to 4.10.1 - NethServer/dev#5526
- Improve SSL configuration - NethServer/dev#5509

* Thu Apr 26 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.0-1
- Mattermost blocks Let's Encrypt certificate requests - Bug NethServer/dev#5466
- Remove "Import users" button from UI

* Mon Apr 09 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- Mattermost - NethServer/dev#5448

