%define version 1.31.0
%define release 1
%define version_name 1.31.0

Name: boost
Summary: The Boost C++ Libraries
Version: %{version}
Release: %{release}
License: Boost Software License
URL: http://www.boost.org/
Group: System Environment/Libraries
Source: boost-%{version_name}.tar.bz2
BuildRoot: %{_tmppath}/boost-%{version}-root
BuildRequires: boost-jam >= 3.1.7 libstdc++-devel python 
Patch0: boost-config-gcc.patch
Patch1: boost-tools-build.patch

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
Requires: boost

%description devel
Headers for the Boost C++ libraries

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n boost-%{version_name} -q
%patch0 -p0
%patch1 -p0

%build
PYTHON_VERSION=`python -V 2>&1 | sed 's,.* \([0-9]\.[0-9]\)\(\.[0-9]\)\?.*,\1,'`
PYTHON_FLAGS="-sPYTHON_ROOT=/usr -sPYTHON_VERSION=$PYTHON_VERSION"
BOOST_FLAGS="-sTOOLS=gcc -sBUILD=release"
bjam $PYTHON_FLAGS $BOOST_FLAGS --prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
rm -f boost.list boost-devel.list
bjam $PYTHON_FLAGS $BOOST_FLAGS --prefix=$RPM_BUILD_ROOT%{_prefix} install
PWD=`pwd`
# binary file list
(cd $RPM_BUILD_ROOT%{_prefix}
for i in `find lib -type f`; do
 	echo %{_prefix}/$i >> boost.list
done)
# include file list
(cd $RPM_BUILD_ROOT%{_prefix}
for i in `find include -type f`; do
 	echo %{_prefix}/$i >> boost-devel.list
done)
mv $RPM_BUILD_ROOT%{_prefix}/boost.list $PWD/
mv $RPM_BUILD_ROOT%{_prefix}/boost-devel.list $PWD/

%clean
rm -rf $RPM_BUILD_ROOT 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f boost.list
%defattr(-, root, root)

%files devel -f boost-devel.list
%defattr(-, root, root)
%dir /usr/include/boost-1_31
%dir /usr/include/boost-1_31/boost
%dir /usr/include/boost-1_31/boost/compatibility
%dir /usr/include/boost-1_31/boost/compatibility/cpp_c_headers
%dir /usr/include/boost-1_31/boost/bind
%dir /usr/include/boost-1_31/boost/config
%dir /usr/include/boost-1_31/boost/config/abi
%dir /usr/include/boost-1_31/boost/config/compiler
%dir /usr/include/boost-1_31/boost/config/platform
%dir /usr/include/boost-1_31/boost/config/stdlib
%dir /usr/include/boost-1_31/boost/date_time
%dir /usr/include/boost-1_31/boost/date_time/gregorian
%dir /usr/include/boost-1_31/boost/date_time/posix_time
%dir /usr/include/boost-1_31/boost/detail
%dir /usr/include/boost-1_31/boost/filesystem
%dir /usr/include/boost-1_31/boost/format
%dir /usr/include/boost-1_31/boost/format/detail
%dir /usr/include/boost-1_31/boost/function
%dir /usr/include/boost-1_31/boost/function/detail
%dir /usr/include/boost-1_31/boost/graph
%dir /usr/include/boost-1_31/boost/graph/detail
%dir /usr/include/boost-1_31/boost/integer
%dir /usr/include/boost-1_31/boost/io
%dir /usr/include/boost-1_31/boost/iterator
%dir /usr/include/boost-1_31/boost/iterator/detail
%dir /usr/include/boost-1_31/boost/lambda
%dir /usr/include/boost-1_31/boost/lambda/detail
%dir /usr/include/boost-1_31/boost/math
%dir /usr/include/boost-1_31/boost/math/special_functions
%dir /usr/include/boost-1_31/boost/mpl
%dir /usr/include/boost-1_31/boost/mpl/aux_
%dir /usr/include/boost-1_31/boost/mpl/aux_/config
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/bcc
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/bcc551
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/gcc
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/msvc60
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/msvc70
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/mwcw
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/no_ctps
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/no_ttp
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessed/plain
%dir /usr/include/boost-1_31/boost/mpl/aux_/preprocessor
%dir /usr/include/boost-1_31/boost/mpl/aux_/range_c
%dir /usr/include/boost-1_31/boost/mpl/aux_/test
%dir /usr/include/boost-1_31/boost/mpl/limits
%dir /usr/include/boost-1_31/boost/mpl/list
%dir /usr/include/boost-1_31/boost/mpl/list/aux_
%dir /usr/include/boost-1_31/boost/mpl/list/aux_/preprocessed
%dir /usr/include/boost-1_31/boost/mpl/list/aux_/preprocessed/plain
%dir /usr/include/boost-1_31/boost/mpl/math
%dir /usr/include/boost-1_31/boost/mpl/multiset
%dir /usr/include/boost-1_31/boost/mpl/multiset/aux_
%dir /usr/include/boost-1_31/boost/mpl/set
%dir /usr/include/boost-1_31/boost/mpl/set/aux_
%dir /usr/include/boost-1_31/boost/mpl/vector
%dir /usr/include/boost-1_31/boost/mpl/vector/aux_
%dir /usr/include/boost-1_31/boost/mpl/vector/aux_/preprocessed
%dir /usr/include/boost-1_31/boost/mpl/vector/aux_/preprocessed/no_ctps
%dir /usr/include/boost-1_31/boost/mpl/vector/aux_/preprocessed/plain
%dir /usr/include/boost-1_31/boost/mpl/vector/aux_/preprocessed/typeof_based
%dir /usr/include/boost-1_31/boost/multi_array
%dir /usr/include/boost-1_31/boost/numeric
%dir /usr/include/boost-1_31/boost/numeric/interval
%dir /usr/include/boost-1_31/boost/numeric/interval/compare
%dir /usr/include/boost-1_31/boost/numeric/interval/detail
%dir /usr/include/boost-1_31/boost/numeric/interval/ext
%dir /usr/include/boost-1_31/boost/numeric/ublas
%dir /usr/include/boost-1_31/boost/pending
%dir /usr/include/boost-1_31/boost/pending/detail
%dir /usr/include/boost-1_31/boost/pool
%dir /usr/include/boost-1_31/boost/pool/detail
%dir /usr/include/boost-1_31/boost/preprocessor
%dir /usr/include/boost-1_31/boost/preprocessor/arithmetic
%dir /usr/include/boost-1_31/boost/preprocessor/arithmetic/detail
%dir /usr/include/boost-1_31/boost/preprocessor/array
%dir /usr/include/boost-1_31/boost/preprocessor/comparison
%dir /usr/include/boost-1_31/boost/preprocessor/config
%dir /usr/include/boost-1_31/boost/preprocessor/control
%dir /usr/include/boost-1_31/boost/preprocessor/control/detail
%dir /usr/include/boost-1_31/boost/preprocessor/control/detail/edg
%dir /usr/include/boost-1_31/boost/preprocessor/control/detail/msvc
%dir /usr/include/boost-1_31/boost/preprocessor/debug
%dir /usr/include/boost-1_31/boost/preprocessor/detail
%dir /usr/include/boost-1_31/boost/preprocessor/facilities
%dir /usr/include/boost-1_31/boost/preprocessor/iteration
%dir /usr/include/boost-1_31/boost/preprocessor/iteration/detail
%dir /usr/include/boost-1_31/boost/preprocessor/iteration/detail/bounds
%dir /usr/include/boost-1_31/boost/preprocessor/iteration/detail/iter
%dir /usr/include/boost-1_31/boost/preprocessor/list
%dir /usr/include/boost-1_31/boost/preprocessor/list/detail
%dir /usr/include/boost-1_31/boost/preprocessor/list/detail/edg
%dir /usr/include/boost-1_31/boost/preprocessor/logical
%dir /usr/include/boost-1_31/boost/preprocessor/punctuation
%dir /usr/include/boost-1_31/boost/preprocessor/repetition
%dir /usr/include/boost-1_31/boost/preprocessor/repetition/detail
%dir /usr/include/boost-1_31/boost/preprocessor/repetition/detail/edg
%dir /usr/include/boost-1_31/boost/preprocessor/repetition/detail/msvc
%dir /usr/include/boost-1_31/boost/preprocessor/selection
%dir /usr/include/boost-1_31/boost/preprocessor/seq
%dir /usr/include/boost-1_31/boost/preprocessor/seq/detail
%dir /usr/include/boost-1_31/boost/preprocessor/slot
%dir /usr/include/boost-1_31/boost/preprocessor/slot/detail
%dir /usr/include/boost-1_31/boost/preprocessor/tuple
%dir /usr/include/boost-1_31/boost/python
%dir /usr/include/boost-1_31/boost/python/converter
%dir /usr/include/boost-1_31/boost/python/detail
%dir /usr/include/boost-1_31/boost/python/object
%dir /usr/include/boost-1_31/boost/python/suite
%dir /usr/include/boost-1_31/boost/python/suite/indexing
%dir /usr/include/boost-1_31/boost/python/suite/indexing/detail
%dir /usr/include/boost-1_31/boost/random
%dir /usr/include/boost-1_31/boost/random/detail
%dir /usr/include/boost-1_31/boost/regex
%dir /usr/include/boost-1_31/boost/regex/config
%dir /usr/include/boost-1_31/boost/regex/v3
%dir /usr/include/boost-1_31/boost/regex/v4
%dir /usr/include/boost-1_31/boost/signals
%dir /usr/include/boost-1_31/boost/signals/detail
%dir /usr/include/boost-1_31/boost/spirit
%dir /usr/include/boost-1_31/boost/spirit/actor
%dir /usr/include/boost-1_31/boost/spirit/attribute
%dir /usr/include/boost-1_31/boost/spirit/core
%dir /usr/include/boost-1_31/boost/spirit/core/composite
%dir /usr/include/boost-1_31/boost/spirit/core/composite/impl
%dir /usr/include/boost-1_31/boost/spirit/core/impl
%dir /usr/include/boost-1_31/boost/spirit/core/non_terminal
%dir /usr/include/boost-1_31/boost/spirit/core/non_terminal/impl
%dir /usr/include/boost-1_31/boost/spirit/core/primitives
%dir /usr/include/boost-1_31/boost/spirit/core/primitives/impl
%dir /usr/include/boost-1_31/boost/spirit/core/scanner
%dir /usr/include/boost-1_31/boost/spirit/core/scanner/impl
%dir /usr/include/boost-1_31/boost/spirit/debug
%dir /usr/include/boost-1_31/boost/spirit/debug/impl
%dir /usr/include/boost-1_31/boost/spirit/dynamic
%dir /usr/include/boost-1_31/boost/spirit/dynamic/impl
%dir /usr/include/boost-1_31/boost/spirit/error_handling
%dir /usr/include/boost-1_31/boost/spirit/error_handling/impl
%dir /usr/include/boost-1_31/boost/spirit/fusion
%dir /usr/include/boost-1_31/boost/spirit/fusion/detail
%dir /usr/include/boost-1_31/boost/spirit/fusion/iterator
%dir /usr/include/boost-1_31/boost/spirit/fusion/iterator/detail
%dir /usr/include/boost-1_31/boost/spirit/fusion/iterator/detail/tuple_iterator
%dir /usr/include/boost-1_31/boost/spirit/fusion/iterator/detail/single_view_iterator
%dir /usr/include/boost-1_31/boost/spirit/fusion/sequence
%dir /usr/include/boost-1_31/boost/spirit/fusion/sequence/detail
%dir /usr/include/boost-1_31/boost/spirit/iterator
%dir /usr/include/boost-1_31/boost/spirit/iterator/impl
%dir /usr/include/boost-1_31/boost/spirit/meta
%dir /usr/include/boost-1_31/boost/spirit/meta/impl
%dir /usr/include/boost-1_31/boost/spirit/phoenix
%dir /usr/include/boost-1_31/boost/spirit/symbols
%dir /usr/include/boost-1_31/boost/spirit/symbols/impl
%dir /usr/include/boost-1_31/boost/spirit/tree
%dir /usr/include/boost-1_31/boost/spirit/tree/impl
%dir /usr/include/boost-1_31/boost/spirit/utility
%dir /usr/include/boost-1_31/boost/spirit/utility/impl
%dir /usr/include/boost-1_31/boost/spirit/utility/impl/chset
%dir /usr/include/boost-1_31/boost/test
%dir /usr/include/boost-1_31/boost/test/detail
%dir /usr/include/boost-1_31/boost/test/included
%dir /usr/include/boost-1_31/boost/thread
%dir /usr/include/boost-1_31/boost/thread/detail
%dir /usr/include/boost-1_31/boost/tuple
%dir /usr/include/boost-1_31/boost/tuple/detail
%dir /usr/include/boost-1_31/boost/type_traits
%dir /usr/include/boost-1_31/boost/type_traits/detail
%dir /usr/include/boost-1_31/boost/utility
%dir /usr/include/boost-1_31/boost/variant
%dir /usr/include/boost-1_31/boost/variant/detail

%changelog
* Thu Jan  22 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0
- Update to boost-1.31.0.rc2
- (#109307:  Compile Failure with boost libraries)
- (#104831:  Compile errors in apps using Boost.Python...)
- Unify into boost, boost-devel rpms.
- Simplify installation using bjam and prefix install.

* Tue Sep  9 2003 Nalin Dahyabhai <nalin@redhat.com> 1.30.2-2
- require boost-devel instead of devel in subpackages which require boost-devel
- remove stray Prefix: tag

* Mon Sep  8 2003 Benjamin Kosnik <bkoz@redhat.com> 1.30.2-1
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

* Tue May  6 2003 Tim Powers <timp@redhat.com> 1.30.0-3
- add deffattr's so we don't have unknown users owning files
