Name: boost
Summary: The Boost C++ Libraries
Version: 1.34.1
Release: 6%{?dist}
License: Boost Software License (GPL-Compatible, Free Software License)
URL: http://www.boost.org/
Group: System Environment/Libraries
#Source: %{name}_1_34_1.tar.bz2
Source: http://downloads.sourceforge.net/boost/boost_1_34_1.tar.bz2
Obsoletes: boost-doc <= 1.30.2
Obsoletes: boost-python <= 1.30.2
Provides: boost-python = %{version}-%{release}
Provides: boost-doc = %{version}-%{release}
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libstdc++-devel
BuildRequires: bzip2-libs
BuildRequires: bzip2-devel
BuildRequires: zlib
BuildRequires: zlib-devel
BuildRequires: python
BuildRequires: python-devel
BuildRequires: libicu
BuildRequires: libicu-devel
Patch0: boost-configure.patch
Patch1: boost-gcc-soname.patch
Patch2: boost-use-rpm-optflags.patch
Patch3: boost-run-tests.patch
Patch4: boost-regex.patch

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee's upcoming C++ Standard Library Technical Report.)

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: boost = %{version}-%{release}
Provides: boost-python-devel = %{version}-%{release}

%description devel
Headers and shared object symlinks for the Boost C++ libraries.

%package devel-static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: boost = %{version}-%{release}
Provides: boost-python-devel = %{version}-%{release}

%description devel-static
Static libraries for the Boost C++ libraries.

%package doc
Summary: The Boost C++ html docs
Group: Documentation
Provides: boost-python-docs = %{version}-%{release}

%description doc
HTML documentation files for Boost C++ libraries.

%prep
rm -rf %{buildroot}

%setup -q -n %{name}_1_34_1
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
BOOST_ROOT=`pwd`
staged_dir=stage
export BOOST_ROOT

# build make tools, ie bjam, necessary for building libs, docs, and testing
(cd tools/jam/src && ./build.sh)
BJAM=`find tools/jam/src/ -name bjam -a -type f`

#BUILD_FLAGS="--with-toolset=gcc --prefix=$RPM_BUILD_ROOT%{_prefix}"
BUILD_FLAGS="--with-toolset=gcc"
PYTHON_VERSION=$(python -c 'import sys; print sys.version[:3]')
PYTHON_FLAGS="--with-python-root=/usr --with-python-version=$PYTHON_VERSION"
REGEX_FLAGS="--with-icu"
./configure $BUILD_FLAGS $PYTHON_FLAGS $REGEX_FLAGS 
make all

# build docs, requires a network connection for docbook XSLT stylesheets
#cd ./doc
#chmod +x ../tools/boostbook/setup_boostbook.sh
#../tools/boostbook/setup_boostbook.sh
#$BOOST_ROOT/$BJAM --v2 -sICU_PATH=/usr --user-config=../user-config.jam html
#cd ..

%check
# --with tests activates checking
%define with_tests %{?_with_tests:1}%{!?_with_tests:0}
%define without_tests %{!?_with_tests:1}%{?_with_tests:0}

%if %{with_tests}
echo "<p>" `uname -a` "</p>" > status/regression_comment.html
echo "" >> status/regression_comment.html
echo "<p>" `g++ --version` "</p>" >> status/regression_comment.html
echo "" >> status/regression_comment.html

chmod +x tools/regression/run_tests.sh
./tools/regression/run_tests.sh

results1=status/cs-`uname`.html
results2=status/cs-`uname`-links.html
email=benjamin.kosnik@gmail.com
if [ -f $results1 ] && [ -f $results2 ]; then
  echo "sending results starting"
  testdate=`date +%Y%m%d`
  testarch=`uname -m`
  results=boost-results-$testdate-$testarch.tar.bz2
  tar -cvf boost-results-$testdate-$testarch.tar $results1 $results2
  bzip2 -f boost-results-$testdate-$testarch.tar 
  echo | mutt -s "$testdate boost regression $testarch" -a $results $email 
  echo "sending results finished"
else
  echo "error sending results"
fi
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}

# install lib
for i in `find stage -type f -name \*.a`; do
  NAME=`basename $i`;
  install -p -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;
for i in `find stage -type f -name \*.so`; do
  NAME=$i;
  SONAME=$i.3;
  VNAME=$i.%{version};
  base=`basename $i`;
  NAMEbase=$base;
  SONAMEbase=$base.3;
  VNAMEbase=$base.%{version};
  mv $i $VNAME;
  ln -s $VNAMEbase $SONAME;
  ln -s $VNAMEbase $NAME;
  install -p -m 755 $VNAME $RPM_BUILD_ROOT%{_libdir}/$VNAMEbase;
  mv $SONAME $RPM_BUILD_ROOT%{_libdir}/$SONAMEbase;
  mv $NAME $RPM_BUILD_ROOT%{_libdir}/$NAMEbase;
done;

# install include files
for i in `find boost -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$i
done
for i in `find boost -type f`; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_includedir}/$i
done

#install doc files
cd doc/html; 
for i in `find . -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i
done
for i in `find . -type f`; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i
done
cd ../..;

# remove scripts used to generate include files 
find $RPM_BUILD_ROOT%{_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-, root, root, -)
%{_libdir}/*.so.%{version}
%{_libdir}/*.so.3

%files devel
%defattr(-, root, root, -)
%{_includedir}/boost
%{_libdir}/*.so

%files devel-static
%defattr(-, root, root, -)
%{_libdir}/*.a

%files doc
%defattr(-, root, root, -)
%doc %{_docdir}/boost-%{version}

%changelog
* Mon Jan 14 2008 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-6
- Fixes for boost.regex (rev 42674).

* Wed Sep 19 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-5
- (#283771: Linking against boost libraries fails).

* Tue Aug 21 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-4
- Rebuild.

* Wed Aug 08 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-3
- Rebuild for icu 3.8 bump.

* Thu Aug 02 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-2
- SONAME to 3.

* Tue Jul 31 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-1
- Update to boost_1_34_1.
- Source via http.
- Philipp Thomas <pth.suse.de> fix for RPM_OPT_FLAGS
- Philipp Thomas <pth.suse.de> fix for .so sym links.
- (#225622) Patrice Dumas review comments. 

* Tue Jun 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1.rc1-0.1
- Update to boost_1_34_1_RC1.

* Mon Apr 02 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-13
- (#225622: Merge Review: boost)
  Change static to devel-static.

* Mon Mar 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-12
- (#233523: libboost_python needs rebuild against python 2.5)
  Use patch.

* Mon Mar 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-11
- (#225622: Merge Review: boost)
  Source to http.
  BuildRoot to preferred value.
  PreReq to post/postun -p
  Clarified BSL as GPL-Compatible, Free Software License.
  Remove Obsoletes.
  Add Provides boost-python.
  Remove mkdir -p $RPM_BUILD_ROOT%{_docdir}
  Added periods for decription text. 
  Fix Group field.
  Remove doc Requires boost.
  Preserve timestamps on install.
  Use %defattr(-, root, root, -)
  Added static package for .a libs.
  Install static libs with 0644 permissions.
  Use %doc for doc files.

* Mon Jan 22 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.0-0.5
- Update to boost.RC_1_34_0 snapshot as of 2007-01-19.
- Modify build procedures for boost build v2.
- Add *-mt variants for libraries, or at least variants that use
  threads (regex and thread).

* Thu Nov 23 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-10
- (#182414: boost: put tests in %check section) via Rex Dieter
- Fix EVR with %{?dist} tag via Gianluca Sforna

* Wed Nov 15 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-9
- (#154784: boost-debuginfo package is empty)

* Tue Nov 14 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-8
- (#205866: Revert scanner.hpp change.)

* Mon Nov 13 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-7
- (#205866: boost::spirit generates warnings with -Wshadow)
- (#205863: serialization lib generates warnings)
- (#204326: boost RPM missing dependencies)
- (#193465: [SIGNAL/BIND] Regressions with GCC 4.1)
- BUILD_FLAGS, add, to see actual compile line.
- REGEX_FLAGS, add, to compile regex with ICU support.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-6.1
- rebuild

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 1.33.1-6
- buildrequire python-devel for Python.h

* Thu Feb 16 2006 Florian La Roche <laroche@redhat.com> - 1.33.1-5
- use the real version number to point to the shared libs

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 05 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-4
- Fix symbolic links.

* Wed Jan 04 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-3
- Update to boost-1.33.1.
- (#176485: Missing BuildRequires)
- (#169271: /usr/lib/libboost*.so.? links missing in package)

* Thu Dec 22 2005 Jesse Keating <jkeating@redhat.com> 1.33.1-2
- rebuilt

* Mon Nov 14 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-1
- Update to boost-1.33.1 beta.
- Run testsuite, gather results.

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
