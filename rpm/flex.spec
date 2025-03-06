Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.6.4
Release: 1
License: BSD
URL: https://github.com/westes/flex
Source: %{name}-%{version}.tar.gz
Patch0: 0001-Disable-building-documentation.patch
Requires: m4
BuildRequires: gettext >= 0.19
BuildRequires: bison
BuildRequires: m4

# texinfo required, because of:
# flex/build-aux/missing: line 81: makeinfo: command not found
BuildRequires:  texinfo

# Flex required, because of:
# flex/build-aux/missing: line 81: flex: command not found
BuildRequires: flex

# Needed for tests
BuildRequires: libstdc++-devel

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

%package devel
Summary: Libraries for flex scanner generator

%description devel
This package contains the library with default implementations of
`main' and `yywrap' functions that the client binary can choose to use
instead of implementing their own.

%package doc
Summary: Documentation for flex scanner generator

%description doc
This package contains documentation for flex scanner generator.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%autogen
%configure --disable-dependency-tracking CFLAGS="-fPIC $RPM_OPT_FLAGS"
%make_build

%install
%make_install

( cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s libfl.a .%{_libdir}/libl.a
)
# For now, excluding the new .la and .so files as we haven't had
# any requests for them and adding them will require a new subpackage.
# The .so files contain 2 optional implementations of main and yywrap
# for developer convenience. They are also available in the .a file
# provided in flex-devel.
find %{buildroot} -name '*.la' -delete
# For some reason find -delete doesn't work on arm builds for these two so
# lets use rm.
rm %{buildroot}/%{_libdir}/libfl*.so
rm %{buildroot}/%{_libdir}/libfl*.so.2
find %{buildroot} -name '*.so.2.0.0' -delete

%find_lang flex

%check
%if ! 0%{?qemu_user_space_build}
echo ============TESTING===============
make check
echo ============END TESTING===========
%endif

%files -f flex.lang
%license COPYING
%{_bindir}/*
%{_includedir}/FlexLexer.h

%files devel
%{_libdir}/*.a

%files doc
%doc %{_datadir}/doc/flex/*
