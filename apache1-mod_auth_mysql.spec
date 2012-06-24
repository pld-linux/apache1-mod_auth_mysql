# TODO
# - doesn't build
%define		mod_name	auth_mysql
%define		apxs		/usr/sbin/apxs1
Summary:	This is the MySQL authentication module for Apache
Summary(cs):	Z�kladn� autentizace pro WWW server Apache pomoc� MySQL
Summary(da):	Autenticering for webtjeneren Apache fra en MySQL-database
Summary(de):	Authentifizierung f�r den Apache Web-Server, der eine MySQL-Datenbank verwendet
Summary(es):	Autenticaci�n v�a MySQL para Apache
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant une base de donn�es MySQL
Summary(it):	Autenticazione di base per il server Web Apache mediante un database MySQL
Summary(ja):	MySQL �ǡ����١�����Ȥä� Apache Web �����С��ؤδ���ǧ��
Summary(nb):	Autentisering for webtjeneren Apache fra en MySQL-database
Summary(pl):	Modu� uwierzytelnienia MySQL dla Apache
Summary(pt_BR):	Autentica��o via MySQL para o Apache
Summary(sv):	Grundl�ggande autenticering f�r webbservern Apache med en MySQL-databas
Name:		apache1-mod_%{mod_name}
Version:	2.20
Release:	1.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.diegonet.com/support/mod_auth_mysql-%{version}.tar.gz
# Source0-md5:	3e88c23aabf2089fc753b2631a938f53
URL:		http://www.diegonet.com/support/mod_auth_mysql.shtml
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	%{apxs}
Requires:	apache1 >= 1.3.33-2
Requires:	apache1-mod_auth
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using MySQL RDBMS.

%description -l cs
Bal��ek mod_auth_mysql slou�� pro omezen� p��stupu k dokument�m, kter�
poskytuje WWW server Apache. Jm�na a hesla jsou ulo�ena v datab�zi
MySQL.

%description -l de
mod_auth_mysql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschr�nken, indem es die Daten in
einer MySQL-Datenbank pr�ft.

%description -l es
mod_auth_mysql puede usarse para limitar el acceso a documentos
servidos por un servidor web verificando datos en una base de datos
MySQL.

%description -l fr
mod_auth_mysql peut �tre utilis� pour limiter l'acc�s � des documents
servis par un serveur Web en v�rifiant les donn�es dans une base de
donn�es MySQL.

%description -l it
mod_auth_mysql pu� essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i dati in un database MySQL.

%description -l ja
mod_auth_mysql �ϡ�MySQL �ǡ����١����Υǡ���������å����뤳��
�ˤ�äơ�Web �����С����󶡤���ɥ�����ȤؤΥ������������¤��뤳��
���Ǥ��ޤ���

%description -l pl
To jest modu� uwierzytelnienia dla Apache pozwalaj�cy na
uwierzytelnianie klient�w HTTP z u�yciem bazy danych MySQL.

%description -l pt_BR
Com o mod_auth_mysql voc� pode fazer autentica��o no Apache usando o
MySQL.

%description -l sv
mod_auth_mysql kan anv�ndas f�r att begr�nsa �tkomsten till dokument
servade av en webbserver genom att kontrollera data i en
MySQL-databas.

%prep
%setup -q -n mod_%{mod_name}-%{version}

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
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README* USAGE
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
