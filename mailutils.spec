# TODO:
# - look at files in main package (more split?)
# - scripts for daemons
# - check optional gssapi (or maybe use gss?)
# - some dbm (gdbm? db as (n)dbm? db after update from db2 to db4.1 API?)
#
# Conditional build:
%bcond_with	gssapi	# use GSSAPI authentication (krb5 or heimdal; not ready for gss)
%bcond_without	sasl	# without SASL (using GNU SASL)
#
Summary:	GNU mail utilities
Summary(pl):	Narz�dzia pocztowe z projektu GNU
Name:		mailutils
Version:	0.3.1
Release:	0.1
License:	GPL
Group:		Applications/Mail
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	d2f0192b3dd95b33e764a0d480085cdd
URL:		http://www.gnu.org/software/mailutils/mailutils.html
BuildRequires:	gnutls-devel
BuildRequires:	guile-devel >= 1.4
%{?with_gss:BuildRequires:	heimdal-devel}
%{?with_sasl:BuildRequires:	libgsasl-devel >= 0.0.2}
BuildRequires:	libltdl-devel
BuildRequires:	pam-devel
BuildRequires:	readline-devel
Requires:	%{name}-libs = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	mailutils-doc

%define		_libexecdir	%{_sbindir}

%description
GNU mail utilities.

%description -l pl
Narz�dzia pocztowe z projektu GNU

%package libs
Summary:	GNU mail utilities libraries
Summary(pl):	Biblioteka narz�dzi pocztowych GNU
License:	LGPL
Group:		Libraries
Obsoletes:	libmailbox

%description libs
The runtime library libmailbox. This library contains various mailbox
access routines and support for a number of mailbox types, such as
mbox, mh, POP3, and IMAP4. It also support mime message handling, and
sending mail via SMTP and /usr/sbin/sendmail.

%description libs -l pl
Biblioteka libmailbox zawiera r�ne funkcje dost�pu do skrzynek
pocztowych obs�uguj�ce wiele typ�w skrzynek, takich jak mbox, mh, POP3
i IMAP4. Wspiera tak�e obs�ug� wiadomo�ci MIME i wysy�anie poczty
przez SMP oraz /usr/sbin/sendmail.

%package devel
Summary:	Header files for GNU mail utilities libraries
Summary(pl):	Pliki nag��wkowe bibliotek narz�dzi pocztowych GNU
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}
Obsoletes:	libmailbox-dev

%description devel
Header files for GNU mail utilities libraries.

%description devel -l pl
Pliki nag��wkowe bibliotek narz�dzi pocztowych GNU.

%package static
Summary:	GNU mail utilities static libraries
Summary(pl):	Statyczne biblioteki narz�dzi pocztowych GNU
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
GNU mail utilities static libraries.

%description static -l pl
Statyczne biblioteki narz�dzi pocztowych GNU.

%package -n gnu-mail
Summary:	GNU mail utilities mail(x) replacement
Summary(pl):	Zamiennik mail(x) z narz�dzi pocztowych GNU
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description -n gnu-mail
A replacement for /bin/mail(x) conforming to the UNIX98 specification
for mailx.

%description -n gnu-mail -l pl
Zamiennik /bin/mail(x) zgodny ze specyfikacj� UNIX98 dla mailx.

%package -n gnu-pop3d
Summary:	GNU mail utilites POP3 daemon
Summary(pl):	Demon POP3 z narz�dzi pocztowych GNU
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}
# inetd or standalone

%description -n gnu-pop3d
The GNU POP3 daemon. Uses libmailbox to support different styles of
mailboxes.

%description -n gnu-pop3d -l pl
Demon GNU POP3. Wykorzystuje libmailbox do obs�ugi r�nych rodzaj�w
skrzynek pocztowych.

%package -n gnu-imap4d
Summary:	GNU mail utilities IMAP4 daemon
Summary(pl):	Demon IMAP4 z narz�dzi pocztowych GNU
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}
# inetd or standalone

%description -n gnu-imap4d
The GNU IMAP4 daemon. Uses libmailbox to support different styles of
mailboxes.

%description -n gnu-imap4d -l pl
Demon GNU IMAP4. Wykorzystuje libmailbox do obs�ugi r�nych rodzaj�w
skrzynek pocztowych.

%prep
%setup -q

%build
%configure \
	--with-gnutls \
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

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/dotlock
%attr(755,root,root) %{_bindir}/frm
%attr(755,root,root) %{_bindir}/from
%attr(755,root,root) %{_bindir}/guimb
%attr(755,root,root) %{_bindir}/messages
%attr(755,root,root) %{_bindir}/readmsg
%attr(755,root,root) %{_bindir}/sieve
%attr(755,root,root) %{_bindir}/sieve.scm
%attr(755,root,root) %{_sbindir}/comsatd
%attr(755,root,root) %{_libexecdir}/mail.local
%attr(755,root,root) %{_libexecdir}/mail.remote
%dir %{_libdir}/mailutils
%{_datadir}/mailutils
%{_infodir}/*.info*

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

%files -n gnu-pop3d
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pop3d
%{_mandir}/man1/pop3d.1*
%{_mandir}/man1/popauth.1*

%files -n gnu-imap4d
%attr(755,root,root) %{_sbindir}/imap4d
%{_mandir}/man1/imap4d.1*
