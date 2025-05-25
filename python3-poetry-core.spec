#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	poetry-core
Summary:	Poetry PEP 517 Build Backend
Summary(pl.UTF-8):	Backend budowania PEP 517 z projektu Poetry
Name:		python3-%{module}
Version:	2.0.1
Release:	4
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/poetry-core/poetry_core-%{version}.tar.gz
# Source0-md5:	799f582e2644e6c2c7865498f3b37394
URL:		https://pypi.org/project/poetry/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
BuildRequires:	python3-build >= 0.10.0
BuildRequires:	python3-pytest >= 7.1.2
BuildRequires:	python3-pytest-mock >= 3.10
BuildRequires:	python3-setuptools >= 1:60
BuildRequires:	python3-tomli_w >= 1.0.0
BuildRequires:	python3-trove_classifiers >= 2022.5.19
BuildRequires:	python3-virtualenv >= 20.21
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A PEP 517 build backend implementation developed for Poetry. This
project is intended to be a lightweight, fully compliant,
self-contained package allowing PEP 517-compatible build frontends to
build Poetry-managed projects.

%description -l pl.UTF-8
Implementacja backendu budowania PEP 517 stworzona dla projektu
Poetry. Ten projekt ma być lekkim, w pełni zgodnym, samodzielnym
pakietem, pozwalającym na używanie frontendów budowania zgodnych z PEP
517 do budowania projektów zarządzanych przez Poetry.

%prep
%setup -q -n poetry_core-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_mock \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitescriptdir}/poetry
%{py3_sitescriptdir}/poetry/core
%{py3_sitescriptdir}/poetry_core-%{version}.dist-info
