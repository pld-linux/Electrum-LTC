# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define		egg_name	Electrum_LTC
Summary:	Litecoin Wallet
Summary(pl.UTF-8):	Zarządca portwala Litecoin
Name:		Electrum-LTC
Version:	2.9.3.1
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://electrum-ltc.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	139fa66266ba9a32b8889e161491edba
URL:		https://electrum-ltc.org/
BuildRequires:	python-PySocks >= 1.6.6
BuildRequires:	python-ecdsa > 0.9
BuildRequires:	python-jsonrpclib
BuildRequires:	python-ltc_scrypt
BuildRequires:	python-pbkdf2
BuildRequires:	python-protobuf
BuildRequires:	python-pyaes
BuildRequires:	python-qrcode
BuildRequires:	python-requests
BuildRequires:	python-six
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714

%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lightweight Litecoin wallet

# %%description -l pl.UTF-8

%package -n python3-%{pypi_name}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}

%description -n python3-%{pypi_name} -l pl.UTF-8

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

# Fix for strange *.desktop pixmap location rules in setup.py (inherited from Electrum)
export XDG_DATA_HOME=%{_datadir}
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst RELEASE-NOTES
%attr(755,root,root) %{_bindir}/electrum-ltc
%{_desktopdir}/electrum-ltc.desktop
%{_pixmapsdir}/electrum-ltc.png
%{py_sitescriptdir}/electrum_ltc
%{py_sitescriptdir}/electrum_ltc_gui
%{py_sitescriptdir}/electrum_ltc_plugins
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc AUTHORS README.rst RELEASE-NOTES
#%%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif

