
%define	_snap	2005-09-03
%define	_rel	4

%include	/usr/lib/rpm/macros.php
Summary:	MIMP - a stripped down version of IMP for use on mobile phones/PDAs
Summary(pl):	MIMP - uproszczona wersja IMP-a do u¿ywania na telefonach przeno¶nych i PDA
Name:		mimp
Version:	0.1
Release:	%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.horde.org/pub/snaps/%{_snap}/%{name}-HEAD-%{_snap}.tar.gz
# Source0-md5:	45f846e8cd5e5a798174cdbf204db7f9
Source1:	%{name}.conf
Patch0:		%{name}-prefs.patch
URL:		http://www.horde.org/mimp/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc	CREDITS
%define		_noautoreq		'pear(Horde.*)' 'pear(Text/Flowed.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{name}
%define		_sysconfdir	/etc/horde.org

%description
MIMP is a project to create a version of IMP suitable for mobile
devices such as WAP phones or PDAs. Basic functionality is now all
implemented, including mailbox viewing and paging, viewing messages,
deleting, replying, forwarding, and composing new messages.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with MIMP) please visit <http://www.horde.org/>.

%description -l pl
MIMP to projekt maj±cy na celu stworzenie wersji IMP-a odpowiedniej
dla urz±dzeñ przeno¶nych, takich jak telefony WAP czy PDA. Podstawowa
funkcjonalno¶æ jest teraz w ca³o¶ci zaimplementowana, w³±cznie z
ogl±daniem skrzynek pocztowych i stronicowaniem, ogl±daniem
wiadomo¶ci, usuwaniem, odpowiadaniem, przekazywaniem i tworzeniem
nowych wiadomo¶ci.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
Genral Public License. Wiêcej informacji (w³±cznie z pomoc± dla
MIMP-a) mo¿na znale¼æ na stronie <http://www.horde.org/>.

%prep
%setup -q -c -n %{name}-%{_snap}
mv mimp/* .
%patch0 -p1

rm -f config/.htaccess

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
cp -pR	config/*.xml		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
cp -p config/conf.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR locale/*			$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR themes/*			$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/*.txt
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
