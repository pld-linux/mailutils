# TODO:
# - look at files in main package (more split?)
# - guile and python packages? (note: lmtpd, mda, putmail, mu-mh/inc link with libmu_scm/libmu_py libraries)
# - scripts for daemons
# - dbm switches? (GDBM BDB NDBM TC KC)
#
# Conditional build:
%bcond_without	emacs		# Emacs support for mailutils
%bcond_without	gssapi		# GSSAPI authentication (gss/heimdal/krb5)
%bcond_with	gss		# GSS for GSSAPI
%bcond_without	heimdal		# Heimdal for GSSAPI
%bcond_with	krb5		# MIT Kerberos for GSSAPI
%bcond_without	ldap		# LDAP support
%bcond_with	radius		# RADIUS support [requires gnu-radius, which is not ready for guile 2.x]
%bcond_without	sasl		# without SASL (using GNU SASL)
# language support
%bcond_without	cxx		# C++ wrapper
%bcond_without	guile		# Guile support
%bcond_without	python		# Python support
# SQL:
%bcond_without	mysql		# MySQL module
%bcond_without	pgsql		# PostgreSQL module
%bcond_without	odbc		# ODBC module (any variant)
%bcond_with	iodbc		# ODBC module using libiodbc
%bcond_without	unixodbc	# ODBC module using unixODBC
#
%if %{with iodbc}
%undefine	with_unixodbc
%endif
%if %{without odbc}
%undefine	with_iodbc
%undefine	with_unixodbc
%endif
%if %{with gss} || %{with krb5}
%undefine	with_heimdal
%endif
%if %{without gssapi}
%undefine	with_gss
%undefine	with_heimdal
%undefine	with_krb5
%endif
Summary:	GNU mail utilities
Summary(pl.UTF-8):	Narzędzia pocztowe z projektu GNU
Name:		mailutils
Version:	3.15
Release:	4
License:	GPL v3+
Group:		Applications/Mail
Source0:	https://ftp.gnu.org/gnu/mailutils/%{name}-%{version}.tar.xz
# Source0-md5:	82ede2c796541814ea0a10ff13b40a0a
Patch0:		%{name}-info.patch
Patch1:		%{name}-tinfo.patch
Patch2:		link.patch
Patch3:		%{name}-includes.patch
Patch4:		%{name}-examples.patch
Patch5:		%{name}-extern.patch
Patch6:		%{name}-cpp.patch
Patch8:		%{name}-normalize.patch
URL:		http://www.gnu.org/software/mailutils/mailutils.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.15
BuildRequires:	bison
%{?with_emacs:BuildRequires:	emacs}
BuildRequires:	flex
BuildRequires:	fribidi-devel
BuildRequires:	gettext-tools >= 0.19
%{?with_radius:BuildRequires:	gnu-radius-devel >= 1.6}
BuildRequires:	gnutls-devel >= 1.2.5
%{?with_sasl:BuildRequires:	gsasl-devel >= 0.2.3}
%{?with_gss:BuildRequires:	gss-devel >= 0.0.9}
%{?with_guile:BuildRequires:	guile-devel >= 5:2.2.0}
%{?with_heimdal:BuildRequires:	heimdal-devel}
%{?with_krb5:BuildRequires:	krb5-devel}
%{?with_iodbc:BuildRequires:	libiodbc-devel}
BuildRequires:	libltdl-devel >= 2:2.4.6
%if %{with cxx}
BuildRequires:	libstdc++-devel
%endif
BuildRequires:	libwrap-devel
BuildRequires:	libtool >= 2:2.4.6
BuildRequires:	libunistring-devel
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	ncurses-devel
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	pam-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
%{?with_unixodbc:BuildRequires:	unixODBC-devel}
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	mailutils-doc < 0.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# mailutils variant of traditional PREFIX/bin/mh dir (FHS disallows */bin subdir other than plain "mh")
%define		mh_bindir	%{_libexecdir}/mu-mh

%description
GNU mail utilities.

%description -l pl.UTF-8
Narzędzia pocztowe z projektu GNU.

%package libs
Summary:	GNU mail utilities libraries
Summary(pl.UTF-8):	Biblioteka narzędzi pocztowych GNU
License:	LGPL v3+
Group:		Libraries
Obsoletes:	libmailbox < 0.3.1

%description libs
The runtime library libmailbox. This library contains various mailbox
access routines and support for a number of mailbox types, such as
mbox, mh, POP3, and IMAP4. It also support mime message handling, and
sending mail via SMTP and /usr/sbin/sendmail.

%description libs -l pl.UTF-8
Biblioteka libmailbox zawiera różne funkcje dostępu do skrzynek
pocztowych obsługujące wiele typów skrzynek, takich jak mbox, mh, POP3
i IMAP4. Wspiera także obsługę wiadomości MIME i wysyłanie poczty
przez SMP oraz /usr/sbin/sendmail.

%package devel
Summary:	Header files for GNU mail utilities libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek narzędzi pocztowych GNU
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	libmailbox-dev < 0.3.1

%description devel
Header files for GNU mail utilities libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek narzędzi pocztowych GNU.

%package static
Summary:	GNU mail utilities static libraries
Summary(pl.UTF-8):	Statyczne biblioteki narzędzi pocztowych GNU
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNU mail utilities static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki narzędzi pocztowych GNU.

%package -n gnu-mail
Summary:	GNU mail utilities mail(x) replacement
Summary(pl.UTF-8):	Zamiennik mail(x) z narzędzi pocztowych GNU
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description -n gnu-mail
A replacement for /bin/mail(x) conforming to the UNIX98 specification
for mailx.

%description -n gnu-mail -l pl.UTF-8
Zamiennik /bin/mail(x) zgodny ze specyfikacją UNIX98 dla mailx.

%package -n gnu-pop3d
Summary:	GNU mail utilites POP3 daemon
Summary(pl.UTF-8):	Demon POP3 z narzędzi pocztowych GNU
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}
# inetd or standalone

%description -n gnu-pop3d
The GNU POP3 daemon. Uses libmailbox to support different styles of
mailboxes.

%description -n gnu-pop3d -l pl.UTF-8
Demon GNU POP3. Wykorzystuje libmailbox do obsługi różnych rodzajów
skrzynek pocztowych.

%package -n gnu-imap4d
Summary:	GNU mail utilities IMAP4 daemon
Summary(pl.UTF-8):	Demon IMAP4 z narzędzi pocztowych GNU
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}
# inetd or standalone

%description -n gnu-imap4d
The GNU IMAP4 daemon. Uses libmailbox to support different styles of
mailboxes.

%description -n gnu-imap4d -l pl.UTF-8
Demon GNU IMAP4. Wykorzystuje libmailbox do obsługi różnych rodzajów
skrzynek pocztowych.

%package -n emacs-mailutils
Summary:	Emacs support for GNU mailutils
Summary(pl.UTF-8):	Wsparcie dla GNU mailutils w Emacsie
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs

%description -n emacs-mailutils
Emacs support for GNU mailutils.

%description -n emacs-mailutils -l pl.UTF-8
Wsparcie dla GNU mailutils w Emacsie.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1

%{__rm} po/stamp-po

%build
%{__libtoolize}
%{__aclocal} -I m4 -I am -I gint -I doc/imprimatur
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_emacs:EMACS=no} \
	%{!?with_gss:ac_cv_header_gss_h=no} \
	%{!?with_cxx:--disable-cxx} \
	%{!?debug:--disable-debug} \
	--enable-experimental \
	%{!?with_python:--disable-python} \
	%{?with_radius:--enable-radius} \
	--disable-silent-rules \
	--with-dbm=BDB \
	--with-gnutls \
	%{?with_sasl:--with-gsasl} \
	%{?with_gssapi:--with-gssapi} \
	%{!?with_guile:--without-guile} \
	%{!?with_ldap:--without-ldap} \
	--with-mail-spool=/var/mail \
	--with-mh-bindir=%{_libexecdir}/mu-mh \
	%{?with_mysql:--with-mysql} \
	%{?with_odbc:--with-odbc=%{?with_iodbc:iodbc}%{?with_unixodbc:odbc}} \
	%{?with_pgsql:--with-postgres}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/mailutils/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/mailutils/c_api.{la,a}

%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/decodemail
%attr(755,root,root) %{_bindir}/dotlock
%attr(755,root,root) %{_bindir}/frm
%attr(755,root,root) %{_bindir}/from
%if %{with guile}
%attr(755,root,root) %{_bindir}/guimb
%endif
%attr(755,root,root) %{_bindir}/mailutils
%attr(755,root,root) %{_bindir}/messages
%attr(755,root,root) %{_bindir}/mimeview
%attr(755,root,root) %{_bindir}/movemail
%attr(755,root,root) %{_bindir}/putmail
%attr(755,root,root) %{_bindir}/readmsg
%attr(755,root,root) %{_bindir}/sieve
%attr(755,root,root) %{_sbindir}/comsatd
%attr(755,root,root) %{_sbindir}/lmtpd
%attr(755,root,root) %{_sbindir}/mda
%dir %{mh_bindir}
%attr(755,root,root) %{mh_bindir}/ali
%attr(755,root,root) %{mh_bindir}/anno
%attr(755,root,root) %{mh_bindir}/burst
%attr(755,root,root) %{mh_bindir}/comp
%attr(755,root,root) %{mh_bindir}/fmtcheck
%attr(755,root,root) %{mh_bindir}/folder
%attr(755,root,root) %{mh_bindir}/folders
%attr(755,root,root) %{mh_bindir}/forw
%attr(755,root,root) %{mh_bindir}/inc
%attr(755,root,root) %{mh_bindir}/install-mh
%attr(755,root,root) %{mh_bindir}/mark
%attr(755,root,root) %{mh_bindir}/mhl
%attr(755,root,root) %{mh_bindir}/mhn
%attr(755,root,root) %{mh_bindir}/mhparam
%attr(755,root,root) %{mh_bindir}/mhpath
%attr(755,root,root) %{mh_bindir}/mhseq
%attr(755,root,root) %{mh_bindir}/msgchk
%attr(755,root,root) %{mh_bindir}/next
%attr(755,root,root) %{mh_bindir}/pick
%attr(755,root,root) %{mh_bindir}/prev
%attr(755,root,root) %{mh_bindir}/prompter
%attr(755,root,root) %{mh_bindir}/refile
%attr(755,root,root) %{mh_bindir}/repl
%attr(755,root,root) %{mh_bindir}/rmf
%attr(755,root,root) %{mh_bindir}/rmm
%attr(755,root,root) %{mh_bindir}/scan
%attr(755,root,root) %{mh_bindir}/send
%attr(755,root,root) %{mh_bindir}/show
%attr(755,root,root) %{mh_bindir}/sortm
%attr(755,root,root) %{mh_bindir}/whatnow
%attr(755,root,root) %{mh_bindir}/whom
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/mailutils
%endif
%attr(755,root,root) %{_libexecdir}/mailutils/mailutils-*
%dir %{_libdir}/mailutils
%attr(755,root,root) %{_libdir}/mailutils/*.so
%{_datadir}/mailutils
%if %{with guile}
%{_datadir}/guile/site/*.*/mailutils
%endif
%if %{with python}
%dir %{py3_sitedir}/mailutils
%attr(755,root,root) %{py3_sitedir}/mailutils/c_api.so
%dir %{py3_sitescriptdir}/mailutils
%{py3_sitescriptdir}/mailutils/*.py
%{py3_sitescriptdir}/mailutils/__pycache__
%endif
%{_infodir}/mailutils.info*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmailutils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmailutils.so.9
%attr(755,root,root) %{_libdir}/libmu_auth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_auth.so.9
%if %{with cxx}
%attr(755,root,root) %{_libdir}/libmu_cpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_cpp.so.9
%endif
%attr(755,root,root) %{_libdir}/libmu_dbm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_dbm.so.9
%attr(755,root,root) %{_libdir}/libmu_dotmail.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_dotmail.so.9
%attr(755,root,root) %{_libdir}/libmu_imap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_imap.so.9
%attr(755,root,root) %{_libdir}/libmu_maildir.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_maildir.so.9
%attr(755,root,root) %{_libdir}/libmu_mailer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_mailer.so.9
%attr(755,root,root) %{_libdir}/libmu_mbox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_mbox.so.9
%attr(755,root,root) %{_libdir}/libmu_mh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_mh.so.9
%attr(755,root,root) %{_libdir}/libmu_pop.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_pop.so.9
%if %{with python}
%attr(755,root,root) %{_libdir}/libmu_py.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_py.so.9
%endif
%if %{with guile}
%attr(755,root,root) %{_libdir}/libmu_scm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_scm.so.9
%endif
%attr(755,root,root) %{_libdir}/libmu_sieve.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_sieve.so.9
%attr(755,root,root) %{_libdir}/libmuaux.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmuaux.so.9
%if %{with guile}
%attr(755,root,root) %{_libdir}/libguile-mailutils-v-%{version}.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mailutils-config
%attr(755,root,root) %{_libdir}/libmailutils.so
%attr(755,root,root) %{_libdir}/libmu_auth.so
%attr(755,root,root) %{_libdir}/libmu_dbm.so
%attr(755,root,root) %{_libdir}/libmu_dotmail.so
%attr(755,root,root) %{_libdir}/libmu_imap.so
%attr(755,root,root) %{_libdir}/libmu_maildir.so
%attr(755,root,root) %{_libdir}/libmu_mailer.so
%attr(755,root,root) %{_libdir}/libmu_mbox.so
%attr(755,root,root) %{_libdir}/libmu_mh.so
%attr(755,root,root) %{_libdir}/libmu_pop.so
%if %{with python}
%attr(755,root,root) %{_libdir}/libmu_py.so
%endif
%if %{with guile}
%attr(755,root,root) %{_libdir}/libmu_scm.so
%endif
%attr(755,root,root) %{_libdir}/libmu_sieve.so
%attr(755,root,root) %{_libdir}/libmuaux.so
%{_libdir}/libmailutils.la
%{_libdir}/libmu_auth.la
%{_libdir}/libmu_dbm.la
%{_libdir}/libmu_dotmail.la
%{_libdir}/libmu_imap.la
%{_libdir}/libmu_maildir.la
%{_libdir}/libmu_mailer.la
%{_libdir}/libmu_mbox.la
%{_libdir}/libmu_mh.la
%{_libdir}/libmu_pop.la
%if %{with python}
%{_libdir}/libmu_py.la
%endif
%if %{with guile}
%{_libdir}/libmu_scm.la
%endif
%{_libdir}/libmu_sieve.la
%{_libdir}/libmuaux.la
%if %{with cxx}
%attr(755,root,root) %{_libdir}/libmu_cpp.so
%{_libdir}/libmu_cpp.la
%endif
%{_includedir}/mailutils
%{_aclocaldir}/mailutils.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libmailutils.a
%{_libdir}/libmu_auth.a
%if %{with cxx}
%{_libdir}/libmu_cpp.a
%endif
%{_libdir}/libmu_dbm.a
%{_libdir}/libmu_dotmail.a
%{_libdir}/libmu_imap.a
%{_libdir}/libmu_maildir.a
%{_libdir}/libmu_mailer.a
%{_libdir}/libmu_mbox.a
%{_libdir}/libmu_mh.a
%{_libdir}/libmu_pop.a
%if %{with python}
%{_libdir}/libmu_py.a
%endif
%if %{with guile}
%{_libdir}/libmu_scm.a
%endif
%{_libdir}/libmu_sieve.a
%{_libdir}/libmuaux.a

%files -n gnu-mail
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mail
%{_mandir}/man1/mail.1*

%files -n gnu-pop3d
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/popauth
%attr(755,root,root) %{_sbindir}/pop3d
%{_mandir}/man1/pop3d.1*
%{_mandir}/man1/popauth.1*

%files -n gnu-imap4d
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/imap4d
%{_mandir}/man1/imap4d.1*

%if %{with emacs}
%files -n emacs-mailutils
%defattr(644,root,root,755)
%{_emacs_lispdir}/mailutils-mh.el*
%endif
