%define	_hordeapp mimp
#
%include	/usr/lib/rpm/macros.php
Summary:	MIMP - a stripped down version of IMP for use on mobile phones/PDAs
Summary(pl.UTF-8):	MIMP - uproszczona wersja IMP-a do używania na telefonach przenośnych i PDA
Name:		horde-%{_hordeapp}
Version:	1.1.1
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/mimp/%{_hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	4c70f8cffe9f0d997dd079186a71c0bc
Source1:	%{_hordeapp}.conf
Patch0:		%{_hordeapp}-prefs.patch
URL:		http://www.horde.org/mimp/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.15.1
Requires:	horde >= 3.0
Requires:	webapps
Obsoletes:	%{_hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(Horde.*)' 'pear(Text/Flowed.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
MIMP is a project to create a version of IMP suitable for mobile
devices such as WAP phones or PDAs. Basic functionality is now all
implemented, including mailbox viewing and paging, viewing messages,
deleting, replying, forwarding, and composing new messages.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with MIMP) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
MIMP to projekt mający na celu stworzenie wersji IMP-a odpowiedniej
dla urządzeń przenośnych, takich jak telefony WAP czy PDA. Podstawowa
funkcjonalność jest teraz zaimplementowana w całości, włącznie z
oglądaniem skrzynek pocztowych i stronicowaniem, oglądaniem
wiadomości, usuwaniem, odpowiadaniem, przekazywaniem i tworzeniem
nowych wiadomości.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
Genral Public License. Więcej informacji (włącznie z pomocą dla
MIMP-a) można znaleźć na stronie <http://www.horde.org/>.

%prep
%setup -q -n %{_hordeapp}-h3-%{version}
%patch0 -p1

for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- horde-%{_hordeapp} < 0.1-0.20051116.0.3, %{_hordeapp}
for i in conf.php filter.txt header.txt menu.php mime_drivers.php motd.php prefs.php servers.php trailer.txt; do
	if [ -f /etc/horde.org/%{_hordeapp}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/%{_hordeapp}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

if [ -L /etc/apache/conf.d/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register apache %{_webapp}
	rm -f /etc/apache/conf.d/99_horde-%{_hordeapp}.conf
	%service -q apache reload
fi
if [ -L /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	rm -f /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc README docs/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
