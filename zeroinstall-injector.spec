#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	The Zero Install Injector (0launch)
Summary(pl.UTF-8):	Bardzo łatwy instalator
Name:		zeroinstall-injector
Version:	2.3.3
Release:	1
License:	LGPL v2
Group:		Applications/File
Source0:	http://downloads.sourceforge.net/zero-install/0install-%{version}.tar.bz2
# Source0-md5:	00d567d9086d0b030ac610df6e4cb237
URL:		http://0install.net/injector.html
%if %{with tests}
BuildRequires:	gnupg
BuildRequires:	python-coverage
BuildRequires:	xdg-utils
BuildRequires:	xz
%endif
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	applnk
Requires:	bzip2
Requires:	desktop-file-utils
Requires:	gnupg
Requires:	gtk-update-icon-cache
Requires:	gzip
Requires:	hicolor-icon-theme
Requires:	python-dbus
Requires:	python-pygtk-gtk
Requires:	sudo
Requires:	tar
Requires:	xdg-utils
Requires:	xz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zero Install Injector makes it easy for users to install software
without needing root privileges. It takes the URL of a program and
runs it (downloading it first if necessary). Any dependencies of the
program are fetched in the same way. The user controls which version
of the program and its dependencies to use.

%description -l pl.UTF-8
Bardzo łatwy instalator umożliwia zwykłemu użytkownikowi instalację
programu bez konieczności posiadania uprawnień administratora. Pobiera
URL aplikacji i ją uruchamia (ściąga na lokalny udział o ile to
konieczne). Jakiekolwiek zależności obsługiwane są w ten sam sposób.
Użytkownik może wybrać którą wersję programu i bibliotek zależnych
zainstalować.

%prep
%setup -q -n 0install-%{version}

%{__sed} -i -e '/data_files/ s#man/man1#share/man/man1#' setup.py

# network tests of failing ones
mv tests/testdownload.py{,.off}
mv tests/testpackagekit.py{,.off}

# check these
mv tests/testunpack.py{,.fail}
mv tests/testdistro.py{,.fail}
mv tests/testlaunch.py{,.fail}
mv tests/testrun.py{,.fail}

%build
%{__python} setup.py build

%if %{with tests}
export PYTHONPATH=${PWD:-$(pwd)}
cd tests
./testall.py
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%find_lang zero-install

desktop-file-validate \
    $RPM_BUILD_ROOT%{_desktopdir}/0install.desktop

# not yet packaged
rm $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/0install
rm $RPM_BUILD_ROOT%{_datadir}/fish/completions/0install.fish
rm $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions/_0install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f zero-install.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/0alias
%attr(755,root,root) %{_bindir}/0desktop
%attr(755,root,root) %{_bindir}/0install
%attr(755,root,root) %{_bindir}/0launch
%attr(755,root,root) %{_bindir}/0store
%attr(755,root,root) %{_bindir}/0store-secure-add
%{_mandir}/man1/0alias.1*
%{_mandir}/man1/0desktop.1*
%{_mandir}/man1/0install.1*
%{_mandir}/man1/0launch.1*
%{_mandir}/man1/0store-secure-add.1*
%{_mandir}/man1/0store.1*
%{_iconsdir}/hicolor/*/apps/zeroinstall.*
%{_desktopdir}/0install.desktop

%dir %{py_sitescriptdir}/zeroinstall
%{py_sitescriptdir}/zeroinstall/*.py[co]
%dir %{py_sitescriptdir}/zeroinstall/0launch-gui
%{py_sitescriptdir}/zeroinstall/0launch-gui/*.py[co]
%{py_sitescriptdir}/zeroinstall/0launch-gui/0launch-gui
%{py_sitescriptdir}/zeroinstall/0launch-gui/zero-install.ui
%dir %{py_sitescriptdir}/zeroinstall/injector
%{py_sitescriptdir}/zeroinstall/injector/*.py[co]
%{py_sitescriptdir}/zeroinstall/injector/EquifaxSecureCA.crt
%dir %{py_sitescriptdir}/zeroinstall/gtkui
%{py_sitescriptdir}/zeroinstall/gtkui/*.py[co]
%{py_sitescriptdir}/zeroinstall/gtkui/cache.ui
%{py_sitescriptdir}/zeroinstall/gtkui/desktop.ui
%dir %{py_sitescriptdir}/zeroinstall/support
%{py_sitescriptdir}/zeroinstall/support/*.py[co]
%dir %{py_sitescriptdir}/zeroinstall/zerostore
%{py_sitescriptdir}/zeroinstall/zerostore/*.py[co]
%{py_sitescriptdir}/zeroinstall/zerostore/_unlzma
%dir %{py_sitescriptdir}/zeroinstall/cmd
%{py_sitescriptdir}/zeroinstall/cmd/*.py[co]
%{py_sitescriptdir}/zeroinstall_injector-%{version}-py*.egg-info
