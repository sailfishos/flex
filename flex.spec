#specfile originally created for Fedora, modified for Moblin Linux
Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.5.37
Release: 1
License: BSD
Group: Development/Tools
URL: http://flex.sourceforge.net/
Source: http://prdownloads.sourceforge.net/flex/flex-%{version}.tar.bz2
Patch0: flex-2.5.36-bison-2.6.1.patch
Requires: m4
BuildRequires: gettext bison m4
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-dependency-tracking CFLAGS="-fPIC $RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

( cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
  ln -s libfl.a .%{_libdir}/libl.a
)

%find_lang flex

%post
[ -e %{_infodir}/flex.info.gz ] && /sbin/install-info %{_infodir}/flex.info.gz --dir-file=%{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
    [ -e %{_infodir}/%{name}.info ] && /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%check
%if ! 0%{?qemu_user_space_build}
echo ============TESTING===============
make check
echo ============END TESTING===========
%endif

%files -f flex.lang
%defattr(-,root,root)
%doc %{_datadir}/doc/flex/
%{_bindir}/*
%doc %{_mandir}/man1/*
%{_libdir}/*.a
%{_includedir}/FlexLexer.h
%doc %{_infodir}/flex.info*

