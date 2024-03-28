Name:           auto-cpufreq
Version:        2.2.0
Release:        1%{?dist}
Summary:        Automatic CPU speed & power optimizer for Linux

License:        MIT
URL:            https://github.com/AdnanHodzic/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# This is a downstream only patch. Upstream's build scripts expect the script
# to be installed in a venv located at a specific path.
Patch0:         fix-systemd-unit-file-paths.patch

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  dmidecode
BuildRequires:  gcc
BuildRequires:  cairo-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  gtk3-devel
BuildRequires:  binutils

Requires:       dmidecode

%description
%{name} is an automatic CPU speed & power optimizer for Linux.


%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files auto_cpufreq
install -Dpm 0644 scripts/%{name}.service -t %{buildroot}%{_unitdir}
install -d %{buildroot}%{_datadir}/%{name}
cp -pr scripts %{buildroot}%{_datadir}/%{name}/scripts


%check
%pyproject_check_import


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files -f %{pyproject_files}
%license LICENSE
%doc README.md

%{_bindir}/%{name}
%{_datadir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Thu Mar 28 2024 m0ngr31 <joe@ipson.me> - 2.2.0
- Initial Package
