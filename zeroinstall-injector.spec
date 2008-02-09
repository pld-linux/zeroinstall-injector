Summary:	The Zero Install Injector (0launch)
Name:		zeroinstall-injector
Version:	0.31
Release:	0.1
License:	GPL
Group:		Applications/File
Source0:	http://dl.sourceforge.net/zero-install/%{name}-%{version}.tar.bz2
# Source0-md5:	f67fda4e7b5fe1079cd240a44ce34c6e
URL:		http://0install.net/injector.html
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zero Install Injector makes it easy for users to install software
without needing root privileges. It takes the URL of a program and
runs it (downloading it first if necessary). Any dependencies of the
program are fetched in the same way. The user controls which version
of the program and its dependencies to use.

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT/%{_prefix}/man/* $RPM_BUILD_ROOT%{_mandir}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/0*
%{_mandir}/man1/0*
%dir %{py_sitescriptdir}/zeroinstall
%{py_sitescriptdir}/zeroinstall/*.py[co]
%dir %{py_sitescriptdir}/zeroinstall/0launch-gui
%{py_sitescriptdir}/zeroinstall/0launch-gui/*.py[co]
%{py_sitescriptdir}/zeroinstall/0launch-gui/*.xml
%{py_sitescriptdir}/zeroinstall/0launch-gui/*.glade
%{py_sitescriptdir}/zeroinstall/0launch-gui/0launch-gui
%dir %{py_sitescriptdir}/zeroinstall/injector
%{py_sitescriptdir}/zeroinstall/injector/*.py[co]
%dir %{py_sitescriptdir}/zeroinstall/zerostore
%{py_sitescriptdir}/zeroinstall/zerostore/*.py[co]
%{_pixmapsdir}/*
%{_desktopdir}/*
#%{py_sitedir}/%{module}-*.egg-info
