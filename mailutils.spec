# TODO:
# - look at files in main package (more split?)
# - guile and python packages?
# - scripts for daemons
# - some dbm? (berkeley db?)
#
# Conditional build:
%bcond_without	gssapi	# GSSAPI authentication (krb5 or heimdal)
%bcond_without	sasl	# without SASL (using GNU SASL)
%bcond_with	gss	# use GSS instead of heimdal
#
Summary:	GNU mail utilities
Summary(pl.UTF-8):	Narzędzia pocztowe z projektu GNU
Name:		mailutils
Version:	2.2
Release:	1
License:	GPL v3+
Group:		Applications/Mail
Source0:	http://ftp.gnu.org/gnu/mailutils/%{name}-%{version}.tar.lzma
# Source0-md5:	9cd0b3af77df3442665d1a12c329b807
Patch0:		%{name}-info.patch
Patch1:		%{name}-tinfo.patch
Patch2:		link.patch
URL:		http://www.gnu.org/software/mailutils/mailutils.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	fribidi-devel
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	gnu-radius-devel >= 1.6
BuildRequires:	gnutls-devel >= 1.2.5
%{?with_sasl:BuildRequires:	gsasl-devel >= 0.2.3}
BuildRequires:	guile-devel >= 1.8
BuildRequires:	libltdl-devel
BuildRequires:	libwrap-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	unixODBC-devel
BuildRequires:	xz
%if %{with gssapi}
%if %{with gss}
BuildRequires:	gss-devel >= 0.0.9
%else
BuildRequires:	heimdal-devel
%endif
%endif
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	mailutils-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}

%description
GNU mail utilities.

%description -l pl.UTF-8
Narzędzia pocztowe z projektu GNU.

%package libs
Summary:	GNU mail utilities libraries
Summary(pl.UTF-8):	Biblioteka narzędzi pocztowych GNU
License:	LGPL
Group:		Libraries
Obsoletes:	libmailbox

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
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	libmailbox-dev

%description devel
Header files for GNU mail utilities libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek narzędzi pocztowych GNU.

%package static
Summary:	GNU mail utilities static libraries
Summary(pl.UTF-8):	Statyczne biblioteki narzędzi pocztowych GNU
License:	LGPL
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

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%{__rm} po/stamp-po

%build
%{__libtoolize}
%{__aclocal} -I m4 -I am -I gint
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_gss:ac_cv_header_gss_h=no} \
	--disable-silent-rules \
	--with-gnutls \
	%{?with_sasl:--with-gsasl} \
	%{?with_gssapi:--with-gssapi} \
	--with-mh-bindir=%{_libexecdir}/mu-mh \
	--with-mysql \
	--with-odbc=odbc \
	--with-postgres

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/mailutils/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/mailutils/c_api.{la,a}

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
%attr(755,root,root) %{_bindir}/dotlock
%attr(755,root,root) %{_bindir}/frm
%attr(755,root,root) %{_bindir}/from
%attr(755,root,root) %{_bindir}/guimb
%attr(755,root,root) %{_bindir}/messages
%attr(755,root,root) %{_bindir}/mimeview
%attr(755,root,root) %{_bindir}/movemail
%attr(755,root,root) %{_bindir}/readmsg
%attr(755,root,root) %{_bindir}/sieve
%attr(755,root,root) %{_bindir}/sieve.scm
%attr(755,root,root) %{_sbindir}/comsatd
%attr(755,root,root) %{_sbindir}/maidag
# traditional bin/mh dir
%dir %{_libexecdir}/mu-mh
%attr(755,root,root) %{_libexecdir}/mu-mh/ali
%attr(755,root,root) %{_libexecdir}/mu-mh/anno
%attr(755,root,root) %{_libexecdir}/mu-mh/burst
%attr(755,root,root) %{_libexecdir}/mu-mh/comp
%attr(755,root,root) %{_libexecdir}/mu-mh/fmtcheck
%attr(755,root,root) %{_libexecdir}/mu-mh/folder
%attr(755,root,root) %{_libexecdir}/mu-mh/folders
%attr(755,root,root) %{_libexecdir}/mu-mh/forw
%attr(755,root,root) %{_libexecdir}/mu-mh/inc
%attr(755,root,root) %{_libexecdir}/mu-mh/install-mh
%attr(755,root,root) %{_libexecdir}/mu-mh/mark
%attr(755,root,root) %{_libexecdir}/mu-mh/mhl
%attr(755,root,root) %{_libexecdir}/mu-mh/mhn
%attr(755,root,root) %{_libexecdir}/mu-mh/mhparam
%attr(755,root,root) %{_libexecdir}/mu-mh/mhpath
%attr(755,root,root) %{_libexecdir}/mu-mh/pick
%attr(755,root,root) %{_libexecdir}/mu-mh/refile
%attr(755,root,root) %{_libexecdir}/mu-mh/repl
%attr(755,root,root) %{_libexecdir}/mu-mh/rmf
%attr(755,root,root) %{_libexecdir}/mu-mh/rmm
%attr(755,root,root) %{_libexecdir}/mu-mh/scan
%attr(755,root,root) %{_libexecdir}/mu-mh/send
%attr(755,root,root) %{_libexecdir}/mu-mh/sortm
%attr(755,root,root) %{_libexecdir}/mu-mh/whatnow
%attr(755,root,root) %{_libexecdir}/mu-mh/whom
%dir %{_libdir}/mailutils
%attr(755,root,root) %{_libdir}/mailutils/*.so
%{_datadir}/mailutils
%{_datadir}/guile/site/mailutils
%dir %{py_sitedir}/mailutils
%attr(755,root,root) %{py_sitedir}/mailutils/c_api.so
%dir %{py_sitescriptdir}/mailutils
%{py_sitescriptdir}/mailutils/*.py[co]
%{_infodir}/mailutils.info*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmailutils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmailutils.so.2
%attr(755,root,root) %{_libdir}/libmu_auth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_auth.so.2
%attr(755,root,root) %{_libdir}/libmu_cfg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_cfg.so.0
%attr(755,root,root) %{_libdir}/libmu_cpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_cpp.so.2
%attr(755,root,root) %{_libdir}/libmu_imap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_imap.so.2
%attr(755,root,root) %{_libdir}/libmu_maildir.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_maildir.so.2
%attr(755,root,root) %{_libdir}/libmu_mailer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_mailer.so.2
%attr(755,root,root) %{_libdir}/libmu_mbox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_mbox.so.2
%attr(755,root,root) %{_libdir}/libmu_mh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_mh.so.2
%attr(755,root,root) %{_libdir}/libmu_nntp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_nntp.so.2
%attr(755,root,root) %{_libdir}/libmu_pop.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_pop.so.2
%attr(755,root,root) %{_libdir}/libmu_py.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_py.so.2
%attr(755,root,root) %{_libdir}/libmu_scm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_scm.so.2
%attr(755,root,root) %{_libdir}/libmu_sieve.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmu_sieve.so.2
%attr(755,root,root) %{_libdir}/libguile-mailutils-v-2.2.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mailutils-config
%attr(755,root,root) %{_libdir}/libmailutils.so
%attr(755,root,root) %{_libdir}/libmu_auth.so
%attr(755,root,root) %{_libdir}/libmu_cfg.so
%attr(755,root,root) %{_libdir}/libmu_cpp.so
%attr(755,root,root) %{_libdir}/libmu_imap.so
%attr(755,root,root) %{_libdir}/libmu_maildir.so
%attr(755,root,root) %{_libdir}/libmu_mailer.so
%attr(755,root,root) %{_libdir}/libmu_mbox.so
%attr(755,root,root) %{_libdir}/libmu_mh.so
%attr(755,root,root) %{_libdir}/libmu_nntp.so
%attr(755,root,root) %{_libdir}/libmu_pop.so
%attr(755,root,root) %{_libdir}/libmu_py.so
%attr(755,root,root) %{_libdir}/libmu_scm.so
%attr(755,root,root) %{_libdir}/libmu_sieve.so
%{_libdir}/libmailutils.la
%{_libdir}/libmu_auth.la
%{_libdir}/libmu_cfg.la
%{_libdir}/libmu_cpp.la
%{_libdir}/libmu_imap.la
%{_libdir}/libmu_maildir.la
%{_libdir}/libmu_mailer.la
%{_libdir}/libmu_mbox.la
%{_libdir}/libmu_mh.la
%{_libdir}/libmu_nntp.la
%{_libdir}/libmu_pop.la
%{_libdir}/libmu_py.la
%{_libdir}/libmu_scm.la
%{_libdir}/libmu_sieve.la
# static-only
%{_libdir}/libmu_argp.a
%{_includedir}/mailutils
%{_aclocaldir}/mailutils.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libmailutils.a
%{_libdir}/libmu_auth.a
%{_libdir}/libmu_cfg.a
%{_libdir}/libmu_cpp.a
%{_libdir}/libmu_imap.a
%{_libdir}/libmu_maildir.a
%{_libdir}/libmu_mailer.a
%{_libdir}/libmu_mbox.a
%{_libdir}/libmu_mh.a
%{_libdir}/libmu_nntp.a
%{_libdir}/libmu_pop.a
%{_libdir}/libmu_py.a
%{_libdir}/libmu_scm.a
%{_libdir}/libmu_sieve.a

%files -n gnu-mail
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mail
%{_mandir}/man1/mail.1*

%files -n gnu-pop3d
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pop3d
%{_mandir}/man1/pop3d.1*
%{_mandir}/man1/popauth.1*

%files -n gnu-imap4d
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/imap4d
%{_mandir}/man1/imap4d.1*
