# TODO:
# - look at files in main package (more split?)
# - scripts for daemons
# - check optional gssapi (or maybe use gss?)
# - some dbm (gdbm? db as (n)dbm? db after update from db2 to db4.1 API?)
#
# Conditional build:
%bcond_without	gssapi	# GSSAPI authentication (krb5 or heimdal; not ready for gss)
%bcond_without	sasl	# without SASL (using GNU SASL)
#
Summary:	GNU mail utilities
Summary(pl.UTF-8):	Narzędzia pocztowe z projektu GNU
Name:		mailutils
Version:	1.2
Release:	1
License:	GPL v3+
Group:		Applications/Mail
Source0:	ftp://ftp.gnu.org/gnu/mailutils/%{name}-%{version}.tar.bz2
# Source0-md5:	0a5bf84e908f15343414c6a95118a373
Patch0:		%{name}-info.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-tinfo.patch
URL:		http://www.gnu.org/software/mailutils/mailutils.html
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.8.5
BuildRequires:	fribidi-devel
BuildRequires:	gettext-devel >= 0.15
BuildRequires:	gnu-radius-devel
BuildRequires:	gnutls-devel >= 1.2.5
%{?with_sasl:BuildRequires:	gsasl-devel >= 0.2.3}
BuildRequires:	guile-devel >= 1.4
%{?with_gssapi:BuildRequires:	krb5-devel}
BuildRequires:	libltdl-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRequires:	unixODBC-devel
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
%patch1 -p1
%patch2 -p0

rm -f po/stamp-po

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gnutls \
	--with-mysql \
	--with-postgres \
	--with-odbc=odbc \
	%{?with_sasl:--with-gsasl} \
	%{?with_gssapi:--with-gssapi}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

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
%attr(755,root,root) %{_libexecdir}/mail.local
%attr(755,root,root) %{_libexecdir}/mail.remote
%dir %{_libdir}/mailutils
%attr(755,root,root) %{_libdir}/mailutils/*.so
%{_datadir}/mailutils
%{_infodir}/mailutils.info*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mailutils-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/mailutils

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

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
