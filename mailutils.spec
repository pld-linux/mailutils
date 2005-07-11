# TODO:
# - look at files in main package (more split?)
# - scripts for daemons
# - check optional gssapi (or maybe use gss?)
# - some dbm (gdbm? db as (n)dbm? db after update from db2 to db4.1 API?)
# - security http://security.gentoo.org/glsa/glsa-200505-20.xml
# - security http://security.gentoo.org/glsa/glsa-200506-02.xml
#
# Conditional build:
%bcond_with	gssapi	# use GSSAPI authentication (krb5 or heimdal; not ready for gss)
%bcond_without	sasl	# without SASL (using GNU SASL)
#
Summary:	GNU mail utilities
Summary(pl):	Narzêdzia pocztowe z projektu GNU
Name:		mailutils
Version:	0.6.90
Release:	3
License:	GPL
Group:		Applications/Mail
#Source0:	ftp://ftp.gnu.org/gnu/mailutils/%{name}-%{version}.tar.bz2
Source0:	ftp://alpha.gnu.org/gnu/mailutils/%{name}-%{version}.tar.bz2
# Source0-md5:	682099acd143479aff2ed9e80f214ad6
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/mailutils/mailutils.html
BuildRequires:	gnutls-devel >= 1.2.5
BuildRequires:	guile-devel >= 1.4
%{?with_gss:BuildRequires:	heimdal-devel >= 0.7}
%{?with_sasl:BuildRequires:	gsasl-devel >= 0.0.2}
BuildRequires:	libltdl-devel
BuildRequires:	pam-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	mailutils-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}

%description
GNU mail utilities.

%description -l pl
Narzêdzia pocztowe z projektu GNU

%package libs
Summary:	GNU mail utilities libraries
Summary(pl):	Biblioteka narzêdzi pocztowych GNU
License:	LGPL
Group:		Libraries
Obsoletes:	libmailbox

%description libs
The runtime library libmailbox. This library contains various mailbox
access routines and support for a number of mailbox types, such as
mbox, mh, POP3, and IMAP4. It also support mime message handling, and
sending mail via SMTP and /usr/sbin/sendmail.

%description libs -l pl
Biblioteka libmailbox zawiera ró¿ne funkcje dostêpu do skrzynek
pocztowych obs³uguj±ce wiele typów skrzynek, takich jak mbox, mh, POP3
i IMAP4. Wspiera tak¿e obs³ugê wiadomo¶ci MIME i wysy³anie poczty
przez SMP oraz /usr/sbin/sendmail.

%package devel
Summary:	Header files for GNU mail utilities libraries
Summary(pl):	Pliki nag³ówkowe bibliotek narzêdzi pocztowych GNU
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	libmailbox-dev

%description devel
Header files for GNU mail utilities libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek narzêdzi pocztowych GNU.

%package static
Summary:	GNU mail utilities static libraries
Summary(pl):	Statyczne biblioteki narzêdzi pocztowych GNU
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNU mail utilities static libraries.

%description static -l pl
Statyczne biblioteki narzêdzi pocztowych GNU.

%package -n gnu-mail
Summary:	GNU mail utilities mail(x) replacement
Summary(pl):	Zamiennik mail(x) z narzêdzi pocztowych GNU
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description -n gnu-mail
A replacement for /bin/mail(x) conforming to the UNIX98 specification
for mailx.

%description -n gnu-mail -l pl
Zamiennik /bin/mail(x) zgodny ze specyfikacj± UNIX98 dla mailx.

%package -n gnu-pop3d
Summary:	GNU mail utilites POP3 daemon
Summary(pl):	Demon POP3 z narzêdzi pocztowych GNU
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}
# inetd or standalone

%description -n gnu-pop3d
The GNU POP3 daemon. Uses libmailbox to support different styles of
mailboxes.

%description -n gnu-pop3d -l pl
Demon GNU POP3. Wykorzystuje libmailbox do obs³ugi ró¿nych rodzajów
skrzynek pocztowych.

%package -n gnu-imap4d
Summary:	GNU mail utilities IMAP4 daemon
Summary(pl):	Demon IMAP4 z narzêdzi pocztowych GNU
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}
# inetd or standalone

%description -n gnu-imap4d
The GNU IMAP4 daemon. Uses libmailbox to support different styles of
mailboxes.

%description -n gnu-imap4d -l pl
Demon GNU IMAP4. Wykorzystuje libmailbox do obs³ugi ró¿nych rodzajów
skrzynek pocztowych.

%prep
%setup -q
%patch0 -p1

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
%attr(755,root,root) %{_bindir}/movemail
%attr(755,root,root) %{_bindir}/readmsg
%attr(755,root,root) %{_bindir}/sieve
%attr(755,root,root) %{_bindir}/sieve.scm
%attr(755,root,root) %{_sbindir}/comsatd
%attr(755,root,root) %{_libexecdir}/mail.local
%attr(755,root,root) %{_libexecdir}/mail.remote
%dir %{_libdir}/mailutils
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
%{_infodir}/muint.info*

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
