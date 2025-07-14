%define		mod_name	auth_mysql
%define		apxs		/usr/sbin/apxs1
Summary:	This is the MySQL authentication module for Apache
Summary(cs.UTF-8):	Základní autentizace pro WWW server Apache pomocí MySQL
Summary(da.UTF-8):	Autenticering for webtjeneren Apache fra en MySQL-database
Summary(de.UTF-8):	Authentifizierung für den Apache Web-Server, der eine MySQL-Datenbank verwendet
Summary(es.UTF-8):	Autenticación vía MySQL para Apache
Summary(fr.UTF-8):	Authentification de base pour le serveur Web Apache utilisant une base de données MySQL
Summary(it.UTF-8):	Autenticazione di base per il server Web Apache mediante un database MySQL
Summary(ja.UTF-8):	MySQL データベースを使った Apache Web サーバーへの基本認証
Summary(nb.UTF-8):	Autentisering for webtjeneren Apache fra en MySQL-database
Summary(pl.UTF-8):	Moduł uwierzytelnienia MySQL dla Apache
Summary(pt_BR.UTF-8):	Autenticação via MySQL para o Apache
Summary(sv.UTF-8):	Grundläggande autenticering för webbservern Apache med en MySQL-databas
Name:		apache1-mod_%{mod_name}
Version:	2.20
Release:	1.4
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.diegonet.com/support/mod_auth_mysql-%{version}.tar.gz
# Source0-md5:	3e88c23aabf2089fc753b2631a938f53
Patch0:		%{name}-mysql-API.patch
URL:		http://www.diegonet.com/support/mod_auth_mysql.shtml
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1(EAPI)
Requires:	apache1-mod_auth
Obsoletes:	apache-mod_auth_mysql <= 2.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using MySQL RDBMS.

%description -l cs.UTF-8
Balíček mod_auth_mysql slouží pro omezení přístupu k dokumentům, které
poskytuje WWW server Apache. Jména a hesla jsou uložena v databázi
MySQL.

%description -l de.UTF-8
mod_auth_mysql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschränken, indem es die Daten in
einer MySQL-Datenbank prüft.

%description -l es.UTF-8
mod_auth_mysql puede usarse para limitar el acceso a documentos
servidos por un servidor web verificando datos en una base de datos
MySQL.

%description -l fr.UTF-8
mod_auth_mysql peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant les données dans une base de
données MySQL.

%description -l it.UTF-8
mod_auth_mysql può essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i dati in un database MySQL.

%description -l ja.UTF-8
mod_auth_mysql は、MySQL データベースのデータをチェックすること
によって、Web サーバーが提供するドキュメントへのアクセスを制限すること
ができます。

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP z użyciem bazy danych MySQL.

%description -l pt_BR.UTF-8
Com o mod_auth_mysql você pode fazer autenticação no Apache usando o
MySQL.

%description -l sv.UTF-8
mod_auth_mysql kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera data i en
MySQL-databas.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch -P0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-apxs=%{apxs} \
	--with-mysql=%{_prefix}

ln -sf config.h auth_mysql_config.h
%{apxs} -c -I %{_includedir}/mysql mod_%{mod_name}.c -o mod_%{mod_name}.so -lmysqlclient

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc README* USAGE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
