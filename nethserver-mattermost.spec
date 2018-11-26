%define mattermost_release 5.5.0

# HACK: avoid "No build ID note found" error
%undefine _missing_build_ids_terminate_build
# Disable debug package
%define debug_package %{nil}

Summary: NethServer Mattermost configuration
Name: nethserver-mattermost
Version: 1.1.2
Release: 1%{?dist}
License: Proprietary
Source: %{name}-%{version}.tar.gz
Source1: https://releases.mattermost.com/%{mattermost_release}/mattermost-%{mattermost_release}-linux-amd64.tar.gz
Source2: %{name}.tar.gz
BuildArch: x86_64
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Requires: nethserver-httpd, nethserver-postgresql94

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
%{genfilelist} %{buildroot} \
  --dir /var/lib/nethserver/mattermost/backup 'attr(0755,postgres,postgres)' \
  --dir /var/lib/nethserver/mattermost/data 'attr(0755,mattermost,mattermost)'  | grep -v /opt/mattermost/ >  %{name}-%{version}-filelist


cat %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir /opt/mattermost %attr(0755,mattermost,mattermost)
%attr(-,mattermost,mattermost) /opt/mattermost/*
%config /opt/mattermost/config/config.json
%doc COPYING
%dir %{_nseventsdir}/%{name}-update


%changelog
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

