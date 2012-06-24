%define		mod_name	auth_mysql
%define 	apxs		/usr/sbin/apxs
Summary:	This is the MySQL authentication module for Apache
Name:		apache-mod_%{mod_name}
Version:	2.20a
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://web.oyvax.com/src/mod_auth_mysql-%{version}.tar.gz
URL:		http://www.diegonet.com/support/mod_auth_mysql.shtml
BuildRequires:	mysql-devel
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
Requires:	apache-mod_auth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using mysql RDBMS.

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
To jest modu� autentykacji dla Apache pozwalaj�cy na autentykacj�
klient�w HTTP z u�yciem bazy danych mysql.

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
%{configure2_13} \
	--with-apxs=%{apxs} \
	--with-mysql=%{_prefix}

%{apxs} -c -I %{_includedir}/mysql mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

gzip -9nf README README-2.20a USAGE

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_pkglibdir}/*
