%define tarball_name boost_1_31_0

Name: boost
Summary: The Boost C++ Libraries
Version: 1.31.0
Release: 8
License: Boost Software License
URL: http://www.boost.org/
Group: System Environment/Libraries
Source: %{tarball_name}.tar.bz2
BuildRoot: %{_tmppath}/boost-%{version}-root
BuildRequires: libstdc++-devel python 
Obsoletes: boost-doc <= 1.30.2
Obsoletes: boost-python <= 1.30.2
Patch0: boost-compiler.patch
Patch1: boost-base.patch
Patch2: boost-gcc-tools.patch
Patch3: boost-lambda.patch

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library.  One goal is to establish "existing practice" and provide
reference implementations so that the Boost libraries are suitable for
eventual standardization. (Some of the libraries have already been
proposed for inclusion in the C++ Standards Committee's upcoming C++
Standard Library Technical Report.)

%package devel
Summary: The Boost C++ Headers
Group: System Environment/Libraries
Requires: boost = %{version}-%{release}
Obsoletes: boost-python-devel <= 1.30.2
Provides: boost-python-devel = %{version}-%{release}

%description devel
Headers for the Boost C++ libraries

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
PYTHON_VERSION=`python -V 2>&1 |sed 's,.* \([0-9]\.[0-9]\)\(\.[0-9]\)\?.*,\1,'`
PYTHON_FLAGS="-sPYTHON_ROOT=/usr -sPYTHON_VERSION=$PYTHON_VERSION"
#$BJAM $PYTHON_FLAGS "-sTOOLS=gcc" "-sBUILD=release <dllversion>1" 
$BJAM $PYTHON_FLAGS "-sTOOLS=gcc" "-sBUILD=release" 

%install
PWD=`pwd`
PREFIX=$RPM_BUILD_ROOT%{_prefix}
mkdir $RPM_BUILD_ROOT
mkdir $PREFIX
mkdir $PREFIX/lib
mkdir $PREFIX/include
# binary file list
for i in `find bin -type f -name \*.a`; do
  NAME=`basename $i | sed 's,-gcc,,' | sed 's,-mt,,' | sed 's,-1_31,,'`;
  install -m 644 $i $PREFIX/lib/$NAME;
done;
for i in `find bin -type f -name \*.so.1.31.0`; do
  NAME=`basename $i | sed 's,-gcc,,' | sed 's,-mt,,' | sed 's,-1_31,,'`;
  install -m 644 $i $PREFIX/lib/$NAME;
done;
(cd $PREFIX 
for i in `find lib -type f`; do
 	echo %{_prefix}/$i >> boost.list
done;
for i in `find lib -type l`; do
 	echo %{_prefix}/$i >> boost.list
done)
# include file list
for i in `find boost -type d`; do
	mkdir -p $PREFIX/include/$i
done
for i in `find boost -type f`; do
	install -m 644 $i $PREFIX/include/$i
done
#cp -R boost $PREFIX/include/boost-1_31/
#chmod -R 644 $PREFIX/include/boost-1_31
(cd $PREFIX 
for i in `find include -type f`; do
 	echo %{_prefix}/$i >> boost-devel.list
done)
mv $PREFIX/boost.list $PWD/
mv $PREFIX/boost-devel.list $PWD/
 
%clean
rm -rf $RPM_BUILD_ROOT 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f boost.list
%defattr(-, root, root)

# Manually generate this via
# 1) cd $prefix
# 2) for i in `find include -type d`; do
#      echo $i >> boost-dir.list
#    done
%files devel -f boost-devel.list
%defattr(-, root, root)
%dir /usr/include
%dir /usr/include/boost
%dir /usr/include/boost/compatibility
%dir /usr/include/boost/compatibility/cpp_c_headers
%dir /usr/include/boost/bind
%dir /usr/include/boost/config
%dir /usr/include/boost/config/abi
%dir /usr/include/boost/config/compiler
%dir /usr/include/boost/config/platform
%dir /usr/include/boost/config/stdlib
%dir /usr/include/boost/date_time
%dir /usr/include/boost/date_time/gregorian
%dir /usr/include/boost/date_time/posix_time
%dir /usr/include/boost/detail
%dir /usr/include/boost/filesystem
%dir /usr/include/boost/format
%dir /usr/include/boost/format/detail
%dir /usr/include/boost/function
%dir /usr/include/boost/function/detail
%dir /usr/include/boost/graph
%dir /usr/include/boost/graph/detail
%dir /usr/include/boost/integer
%dir /usr/include/boost/io
%dir /usr/include/boost/iterator
%dir /usr/include/boost/iterator/detail
%dir /usr/include/boost/lambda
%dir /usr/include/boost/lambda/detail
%dir /usr/include/boost/math
%dir /usr/include/boost/math/special_functions
%dir /usr/include/boost/mpl
%dir /usr/include/boost/mpl/aux_
%dir /usr/include/boost/mpl/aux_/config
%dir /usr/include/boost/mpl/aux_/preprocessed
%dir /usr/include/boost/mpl/aux_/preprocessed/bcc
%dir /usr/include/boost/mpl/aux_/preprocessed/bcc551
%dir /usr/include/boost/mpl/aux_/preprocessed/gcc
%dir /usr/include/boost/mpl/aux_/preprocessed/msvc60
%dir /usr/include/boost/mpl/aux_/preprocessed/msvc70
%dir /usr/include/boost/mpl/aux_/preprocessed/mwcw
%dir /usr/include/boost/mpl/aux_/preprocessed/no_ctps
%dir /usr/include/boost/mpl/aux_/preprocessed/no_ttp
%dir /usr/include/boost/mpl/aux_/preprocessed/plain
%dir /usr/include/boost/mpl/aux_/preprocessor
%dir /usr/include/boost/mpl/aux_/range_c
%dir /usr/include/boost/mpl/aux_/test
%dir /usr/include/boost/mpl/limits
%dir /usr/include/boost/mpl/list
%dir /usr/include/boost/mpl/list/aux_
%dir /usr/include/boost/mpl/list/aux_/preprocessed
%dir /usr/include/boost/mpl/list/aux_/preprocessed/plain
%dir /usr/include/boost/mpl/math
%dir /usr/include/boost/mpl/multiset
%dir /usr/include/boost/mpl/multiset/aux_
%dir /usr/include/boost/mpl/set
%dir /usr/include/boost/mpl/set/aux_
%dir /usr/include/boost/mpl/vector
%dir /usr/include/boost/mpl/vector/aux_
%dir /usr/include/boost/mpl/vector/aux_/preprocessed
%dir /usr/include/boost/mpl/vector/aux_/preprocessed/no_ctps
%dir /usr/include/boost/mpl/vector/aux_/preprocessed/plain
%dir /usr/include/boost/mpl/vector/aux_/preprocessed/typeof_based
%dir /usr/include/boost/multi_array
%dir /usr/include/boost/numeric
%dir /usr/include/boost/numeric/interval
%dir /usr/include/boost/numeric/interval/compare
%dir /usr/include/boost/numeric/interval/detail
%dir /usr/include/boost/numeric/interval/ext
%dir /usr/include/boost/numeric/ublas
%dir /usr/include/boost/pending
%dir /usr/include/boost/pending/detail
%dir /usr/include/boost/pool
%dir /usr/include/boost/pool/detail
%dir /usr/include/boost/preprocessor
%dir /usr/include/boost/preprocessor/arithmetic
%dir /usr/include/boost/preprocessor/arithmetic/detail
%dir /usr/include/boost/preprocessor/array
%dir /usr/include/boost/preprocessor/comparison
%dir /usr/include/boost/preprocessor/config
%dir /usr/include/boost/preprocessor/control
%dir /usr/include/boost/preprocessor/control/detail
%dir /usr/include/boost/preprocessor/control/detail/edg
%dir /usr/include/boost/preprocessor/control/detail/msvc
%dir /usr/include/boost/preprocessor/debug
%dir /usr/include/boost/preprocessor/detail
%dir /usr/include/boost/preprocessor/facilities
%dir /usr/include/boost/preprocessor/iteration
%dir /usr/include/boost/preprocessor/iteration/detail
%dir /usr/include/boost/preprocessor/iteration/detail/bounds
%dir /usr/include/boost/preprocessor/iteration/detail/iter
%dir /usr/include/boost/preprocessor/list
%dir /usr/include/boost/preprocessor/list/detail
%dir /usr/include/boost/preprocessor/list/detail/edg
%dir /usr/include/boost/preprocessor/logical
%dir /usr/include/boost/preprocessor/punctuation
%dir /usr/include/boost/preprocessor/repetition
%dir /usr/include/boost/preprocessor/repetition/detail
%dir /usr/include/boost/preprocessor/repetition/detail/edg
%dir /usr/include/boost/preprocessor/repetition/detail/msvc
%dir /usr/include/boost/preprocessor/selection
%dir /usr/include/boost/preprocessor/seq
%dir /usr/include/boost/preprocessor/seq/detail
%dir /usr/include/boost/preprocessor/slot
%dir /usr/include/boost/preprocessor/slot/detail
%dir /usr/include/boost/preprocessor/tuple
%dir /usr/include/boost/python
%dir /usr/include/boost/python/converter
%dir /usr/include/boost/python/detail
%dir /usr/include/boost/python/object
%dir /usr/include/boost/python/suite
%dir /usr/include/boost/python/suite/indexing
%dir /usr/include/boost/python/suite/indexing/detail
%dir /usr/include/boost/random
%dir /usr/include/boost/random/detail
%dir /usr/include/boost/regex
%dir /usr/include/boost/regex/config
%dir /usr/include/boost/regex/v3
%dir /usr/include/boost/regex/v4
%dir /usr/include/boost/signals
%dir /usr/include/boost/signals/detail
%dir /usr/include/boost/spirit
%dir /usr/include/boost/spirit/actor
%dir /usr/include/boost/spirit/attribute
%dir /usr/include/boost/spirit/core
%dir /usr/include/boost/spirit/core/composite
%dir /usr/include/boost/spirit/core/composite/impl
%dir /usr/include/boost/spirit/core/impl
%dir /usr/include/boost/spirit/core/non_terminal
%dir /usr/include/boost/spirit/core/non_terminal/impl
%dir /usr/include/boost/spirit/core/primitives
%dir /usr/include/boost/spirit/core/primitives/impl
%dir /usr/include/boost/spirit/core/scanner
%dir /usr/include/boost/spirit/core/scanner/impl
%dir /usr/include/boost/spirit/debug
%dir /usr/include/boost/spirit/debug/impl
%dir /usr/include/boost/spirit/dynamic
%dir /usr/include/boost/spirit/dynamic/impl
%dir /usr/include/boost/spirit/error_handling
%dir /usr/include/boost/spirit/error_handling/impl
%dir /usr/include/boost/spirit/iterator
%dir /usr/include/boost/spirit/iterator/impl
%dir /usr/include/boost/spirit/meta
%dir /usr/include/boost/spirit/meta/impl
%dir /usr/include/boost/spirit/phoenix
%dir /usr/include/boost/spirit/symbols
%dir /usr/include/boost/spirit/symbols/impl
%dir /usr/include/boost/spirit/tree
%dir /usr/include/boost/spirit/tree/impl
%dir /usr/include/boost/spirit/utility
%dir /usr/include/boost/spirit/utility/impl
%dir /usr/include/boost/spirit/utility/impl/chset
%dir /usr/include/boost/test
%dir /usr/include/boost/test/detail
%dir /usr/include/boost/test/included
%dir /usr/include/boost/thread
%dir /usr/include/boost/thread/detail
%dir /usr/include/boost/tuple
%dir /usr/include/boost/tuple/detail
%dir /usr/include/boost/type_traits
%dir /usr/include/boost/type_traits/detail
%dir /usr/include/boost/utility
%dir /usr/include/boost/variant
%dir /usr/include/boost/variant/detail

%changelog
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
