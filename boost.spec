%define tarball_name boost_1_33_0

Name: boost
Summary: The Boost C++ Libraries
Version: 1.33.0
Release: 4
License: Boost Software License
URL: http://www.boost.org/
Group: System Environment/Libraries
Source: %{tarball_name}.tar.bz2
BuildRoot: %{_tmppath}/boost-%{version}-root
Prereq: /sbin/ldconfig
BuildRequires: libstdc++-devel python 
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
Obsoletes: boost-doc <= 1.30.2
Obsoletes: boost-python <= 1.30.2
Patch0: boost-base.patch
Patch1: boost-gcc-tools.patch
Patch2: boost-thread.patch
Patch3: boost-config-compiler-gcc.patch

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library.  One goal is to establish "existing practice" and provide
reference implementations so that the Boost libraries are suitable for
eventual standardization. (Some of the libraries have already been
proposed for inclusion in the C++ Standards Committee's upcoming C++
Standard Library Technical Report.)

%package devel
Summary: The Boost C++ headers and development libraries
Group: System Environment/Libraries
Requires: boost = %{version}-%{release}
Obsoletes: boost-python-devel <= 1.30.2
Provides: boost-python-devel = %{version}-%{release}

%description devel
Headers, static libraries, and shared object symlinks for the Boost
C++ libraries

%package doc
Summary: The Boost C++ html docs
Group: System Environment/Libraries
Requires: boost = %{version}-%{release}
Provides: boost-python-docs = %{version}-%{release}

%description doc
HTML documentation files for Boost C++ libraries

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{tarball_name} -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
#build bjam
(cd tools/build/jam_src && ./build.sh)
#build boost with bjam
BJAM=`find tools/build/jam_src/ -name bjam -a -type f`
PYTHON_VERSION=$(python -c 'import sys; print sys.version[:3]')
PYTHON_FLAGS="-sPYTHON_ROOT=/usr -sPYTHON_VERSION=$PYTHON_VERSION"
#$BJAM $PYTHON_FLAGS "-sTOOLS=gcc" "-sBUILD=release <dllversion>1" stage 
$BJAM $PYTHON_FLAGS "-sTOOLS=gcc" "-sBUILD=release" stage 

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}

# install lib
for i in `find stage -type f -name \*.a`; do
  NAME=`basename $i`;
  install -m 755 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;
for i in `find stage -type f -name \*.so.*`; do
  NAME=`basename $i`;
  install -m 755 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;
for i in `find stage -type l -name \*.so`; do
  NAME=`basename $i`;
  mv $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;

# install include files
for i in `find boost -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$i
done
for i in `find boost -type f`; do
  install -m 644 $i $RPM_BUILD_ROOT%{_includedir}/$i
done

#install doc files
cd doc/html; 
for i in `find . -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i
done
for i in `find . -type f`; do
  install -m 644 $i $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i
done
cd ../..;

%clean
rm -rf $RPM_BUILD_ROOT 

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files 
%defattr(-, root, root)
%{_libdir}/*.so.%{version}

%files devel
%defattr(-, root, root)
%{_includedir}/boost
%{_libdir}/*.a
%{_libdir}/*.so

%files doc
%defattr(-, root, root)
%{_docdir}/boost-%{version}

%changelog
* Tue Oct 11 2005 Nils Philippsen <nphilipp@redhat.com> 1.33.0-4
- build require bzip2-devel and zlib-devel

* Tue Aug 23 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.0-3
- Create doc package again.
- Parts of the above by Neal Becker <ndbecker2@gmail.com>.

* Fri Aug 12 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.0-1
- Update to boost-1.33.0, update SONAME to 2 due to ABI changes.
- Simplified PYTHON_VERSION by Philipp Thomas <pth@suse.de>

* Tue May 24 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-6
- (#153093: boost warns that gcc 4.0.0 is an unknown compiler)
- (#152205: development .so symlinks should be in -devel subpackage)
- (#154783: linker .so symlinks missing from boost-devel package)

* Fri Mar 18 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-5
- Revert boost-base.patch to old behavior.
- Use SONAMEVERSION instead of dllversion.

* Wed Mar 16 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-4
- (#142612: Compiling Boost 1.32.0 Failed in RHEL 3.0 on Itanium2) 
- (#150069: libboost_python.so is missing)
- (#141617: bad patch boost-base.patch)
- (#122817: libboost_*.so symlinks missing)
- Re-add boost-thread.patch.
- Change boost-base.patch to show thread tags.
- Change boost-gcc-tools.patch to use SOTAG, compile with dllversion.
- Add symbolic links to files.
- Sanity check can compile with gcc-3.3.x, gcc-3.4.2, gcc-4.0.x., gcc-4.1.x.

* Thu Dec 02 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-3
- (#122817: libboost_*.so symlinks missing)
- (#141574: half of the package is missing)
- (#141617: bad patch boost-base.patch)

* Wed Dec 01 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-2
- Remove bogus Obsoletes.

* Mon Nov 29 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-1
- Update to 1.32.0

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 1.31.0-9
- cleanup specfile
- fix multiarch problem

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 05 2004 Warren Togami <wtogami@redhat.com> 1.31.0-7
- missing Obsoletes boost-python

* Mon May 03 2004 Benjamin Kosnik <bkoz@redhat.com> 
- (#121630: gcc34 patch needed)

* Wed Apr 21 2004 Warren Togami <wtogami@redhat.com>
- #121415 FC2 BLOCKER: Obsoletes boost-python-devel, boost-doc
- other cleanups

* Tue Mar 30 2004 Benjamin Kosnik <bkoz@redhat.com> 
- Remove bjam dependency. (via Graydon).
- Fix installed library names.
- Fix SONAMEs in shared libraries.
- Fix installed header location.
- Fix installed permissions.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-2
- Update to boost-1.31.0

* Thu Jan 22 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-1
- Update to boost-1.31.0.rc2
- (#109307:  Compile Failure with boost libraries)
- (#104831:  Compile errors in apps using Boost.Python...)
- Unify into boost, boost-devel rpms.
- Simplify installation using bjam and prefix install.

* Tue Sep 09 2003 Nalin Dahyabhai <nalin@redhat.com> 1.30.2-2
- require boost-devel instead of devel in subpackages which require boost-devel
- remove stray Prefix: tag

* Mon Sep 08 2003 Benjamin Kosnik <bkoz@redhat.com> 1.30.2-1
- change license to Freely distributable
- verify installation of libboost_thread
- more boost-devel removals
- deal with lack of _REENTRANT on ia64/s390
- (#99458) rpm -e fixed via explict dir additions
- (#103293) update to 1.30.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove packager, change to new Group:

* Tue May 06 2003 Tim Powers <timp@redhat.com> 1.30.0-3
- add deffattr's so we don't have unknown users owning files
