%define version 1.30.2
%define release 2
%define version_name 1.30.2

Name: boost
Summary: The Boost C++ Libraries
Version: %{version}
Release: %{release}
License: Freely distributable
URL: http://www.boost.org/
Group: System Environment/Libraries
Source: boost-%{version_name}.tar.bz2
BuildRoot: %{_tmppath}/boost-%{version}-root
BuildRequires: boost-jam >= 3.1.3 libstdc++-devel python 
Patch0: boost-thread.patch

%description
The Boost web site provides free peer-reviewed portable C++ source
libraries.  The emphasis is on libraries which work well with the C++
Standard Library.  One goal is to establish "existing practice" and
provide reference implementations so that the Boost libraries are
suitable for eventual standardization. Some of the libraries have
already been proposed for inclusion in the C++ Standards Committee's
upcoming C++ Standard Library Technical Report.

# according to ldd (and automatically generated RPM dependencies) it
# doesn't strictly require python, but IMHO it's cleaner to split it
# this way
%package python
Summary: Boost.Python library
Group: System Environment/Libraries
Requires: boost python

%description python
Use the Boost Python Library to quickly and easily export a C++ library to
Python such that the Python interface is very similar to the C++ interface.
It is designed to be minimally intrusive on your C++ design. In most cases,
you should not have to alter your C++ classes in any way in order to use
them with Boost.Python. The system should simply ``reflect'' your C++ classes
and functions into Python.

%package devel
Summary: Boost C++ development libraries and headers
Group: System Environment/Libraries
Requires: boost

%description devel
Headers and static libraries for the Boost C++ libraries

%package python-devel
Summary: Boost.Python development headers
Group: System Environment/Libraries
Requires: %{name}-devel 

%description python-devel
Headers for the Boost.Python library

%package doc
Summary: Boost C++ Library documentation
Group: System Environment/Libraries
Requires: %{name}-devel

%description doc
Documentation for the Boost C++ Library

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n boost-%{version_name} -q
%patch0 -p0

%build
PYTHON_VERSION=`python -V 2>&1 | sed 's,.* \([0-9]\.[0-9]\)\(\.[0-9]\)\?.*,\1,'`
bjam -sBUILD=release -sPYTHON_ROOT=/usr -sPYTHON_VERSION=$PYTHON_VERSION

%install
rm -f master.list python.list devel.list python-devel.list doc.list dir.list
# include files
mkdir -p $RPM_BUILD_ROOT%{_includedir}
for i in `find boost -type d`; do
	mkdir -p $RPM_BUILD_ROOT%{_includedir}/$i
        echo %{_includedir}/$i >> dir.list	
done
for i in `find boost -type f`; do
	install -m 644 $i $RPM_BUILD_ROOT%{_includedir}/$i
	if test "`echo $i | sed 's,python,,g'`" = "$i"; then
		echo %{_includedir}/$i >> devel.list
	else
		echo %{_includedir}/$i >> python-devel.list
	fi
done
# static libraries
mkdir -p $RPM_BUILD_ROOT%{_libdir}
for i in `find libs -type f -name '*.a' | grep gcc`; do
	install -m 644 $i $RPM_BUILD_ROOT%{_libdir}/`basename $i`
	if test "`echo $i | sed 's,python,,g'`" = "$i"; then
		echo %{_libdir}/`basename $i` >> devel.list
	else
		echo %{_libdir}/`basename $i` >> python-devel.list
	fi
done
# dynamic libraries
for i in `find libs -type f -name '*.so.%{version}' | grep gcc`; do
	install -m 755 $i $RPM_BUILD_ROOT%{_libdir}/`basename $i`
	#ldconfig fails to generate the symlinks for boost libs :-(
	LINK=`basename $i | sed 's,\.so\..*,.so,'`
	(cd $RPM_BUILD_ROOT%{_libdir} && ln -s `basename $i` $LINK)
	if test "`echo $i | sed 's,python,,g'`" = "$i"; then
		echo %{_libdir}/`basename $i` >> master.list
		echo %{_libdir}/$LINK >> master.list
	else
		echo %{_libdir}/`basename $i` >> python.list
		echo %{_libdir}/$LINK >> python.list
	fi
done
# documentation
mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}
install -m 644 README $RPM_BUILD_ROOT%{_docdir}/boost-%{version}

# as the documentation doesn't completely reside in a directory of its
# own, we need to find out ourselves... this looks for HTML files and
# then collects everything linked from those.  this is certainly quite
# unoptimized wrt mkdir calls, but does it really matter?
for i in `find -type f -name '*.htm*'`; do
	# bjam docu is included in the boost-jam RPM
	if test "`echo $i | sed 's,jam_src,,'`" = "$i"; then
		mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/`dirname $i`
		for LINKED in `perl - $i $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i <<'EOT'
			sub rewrite_link
			{
				my $link = shift;
				# rewrite links from boost/* to %{_includedir}/boost/* and
				# ignore external links as well as document-internal ones.
				# HTML files are also ignored as they get installed anyway.
				if (!($link =~ s,^(?:../)*boost/,%{_includedir}/boost/,) && !($link =~ m,(?:^[^/]+:|^\#|\.html?(?:$|\#)),))
				{
					(my $file = $link) =~ s/\#.*//;
					print "$file\n";
				}
				$link;
			}
			open IN, @ARGV[0];
			open OUT, ">@ARGV[1]";
            my $in_link;
			while (<IN>)
			{
                $in_link and s/^\s*"([^"> ]*)"/'"' . rewrite_link($1) . '"'/e;
				s/(href|src)="([^"> ]*)"/"$1=\"" . rewrite_link($2) . '"'/eig;
				print OUT;
                $in_link = /href|src=\s*$/;
			}
EOT`; do
			TARGET=`dirname $i`/$LINKED
			# ignore non-existant linked files
			if test -f $TARGET; then
				mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/`dirname $TARGET`
				install -m 644 $TARGET $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$TARGET
			fi
		done
	fi
done

%clean
rm -rf $RPM_BUILD_ROOT 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post python -p /sbin/ldconfig

%postun python -p /sbin/ldconfig

%files -f master.list
%defattr(-, root, root)

%files python -f python.list
%defattr(-, root, root)

%files devel -f devel.list
%defattr(-, root, root)
%dir /usr/include/boost
%dir /usr/include/boost/bind
%dir /usr/include/boost/compatibility
%dir /usr/include/boost/compatibility/cpp_c_headers
%dir /usr/include/boost/config
%dir /usr/include/boost/config/compiler
%dir /usr/include/boost/config/platform
%dir /usr/include/boost/config/stdlib
%dir /usr/include/boost/date_time
%dir /usr/include/boost/date_time/gregorian
%dir /usr/include/boost/date_time/posix_time
%dir /usr/include/boost/detail
%dir /usr/include/boost/filesystem
%dir /usr/include/boost/format
%dir /usr/include/boost/function
%dir /usr/include/boost/function/detail
%dir /usr/include/boost/graph
%dir /usr/include/boost/graph/detail
%dir /usr/include/boost/integer
%dir /usr/include/boost/io
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
%dir /usr/include/boost/mpl/limits
%dir /usr/include/boost/mpl/list
%dir /usr/include/boost/mpl/list/aux_
%dir /usr/include/boost/mpl/list/aux_/preprocessed
%dir /usr/include/boost/mpl/list/aux_/preprocessed/plain
%dir /usr/include/boost/mpl/math
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
%dir /usr/include/boost/random
%dir /usr/include/boost/random/detail
%dir /usr/include/boost/regex
%dir /usr/include/boost/regex/v3
%dir /usr/include/boost/signals
%dir /usr/include/boost/signals/detail
%dir /usr/include/boost/spirit
%dir /usr/include/boost/spirit/attribute
%dir /usr/include/boost/spirit/core
%dir /usr/include/boost/spirit/core/composite
%dir /usr/include/boost/spirit/core/composite/impl
%dir /usr/include/boost/spirit/core/impl
%dir /usr/include/boost/spirit/core/meta
%dir /usr/include/boost/spirit/core/meta/impl
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

%files python-devel -f python-devel.list
%defattr(-, root, root)

%files doc
%defattr(-, root, root)
%doc %{_docdir}/boost-%{version}



%changelog
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
