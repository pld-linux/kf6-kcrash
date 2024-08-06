#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	6.4
%define		qtver		5.15.2
%define		kfname		kcrash

Summary:	Graceful handling of application crashes
Name:		kf6-%{kfname}
Version:	6.4.0
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	98cab6fb842961ff1fe1d7472297151e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kwindowsystem-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kwindowsystem >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KCrash provides support for intercepting and handling application
crashes.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6Crash.so.6
%attr(755,root,root) %{_libdir}/libKF6Crash.so.*.*
%{_datadir}/qlogging-categories6/kcrash.categories
%{_datadir}/qlogging-categories6/kcrash.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KCrash
%{_libdir}/cmake/KF6Crash
%{_libdir}/libKF6Crash.so
