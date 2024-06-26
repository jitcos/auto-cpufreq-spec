Name:           auto-cpufreq
Version:        2.2.0
Release:        4%{?dist}
Summary:        Automatic CPU speed & power optimizer for Linux

License:        MIT
URL:            https://github.com/AdnanHodzic/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        auto-cpufreq.service

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-poetry-core
BuildRequires:  python3-installer
BuildRequires:  python3-poetry-dynamic-versioning
BuildRequires:  dmidecode
BuildRequires:  gcc
BuildRequires:  cairo-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  gtk3-devel
BuildRequires:  binutils

AutoReq:        0:python3dist(requests)

Requires:       dmidecode
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-psutil
Requires:       python3-click
Requires:       python3-distro
Requires:       python3-requests
Requires:       python3-gobject
Requires:       gobject-introspection

%description
%{name} is an automatic CPU speed & power optimizer for Linux.


%prep
%setup -q
find . -type f | xargs sed -i 's|usr/local|usr|g'

%build

%install
POETRY_DYNAMIC_VERSIONING_BYPASS=1 python3 -m build --wheel --no-isolation
python3 -m installer --destdir="$RPM_BUILD_ROOT" dist/*.whl

mkdir -p $RPM_BUILD_ROOT/usr/share/%{name}/scripts/
mkdir -p $RPM_BUILD_ROOT/usr/share/%{name}/images/

install -Dm755 scripts/auto-cpufreq-install.sh "$RPM_BUILD_ROOT/usr/share/%{name}/scripts/"
install -Dm755 scripts/auto-cpufreq-install.sh "$RPM_BUILD_ROOT/usr/bin/%{name}-install"
install -Dm755 scripts/auto-cpufreq-remove.sh "$RPM_BUILD_ROOT/usr/share/%{name}/scripts/"
install -Dm755 scripts/auto-cpufreq-remove.sh "$RPM_BUILD_ROOT/usr/bin/%{name}-remove"
install -Dm755 scripts/cpufreqctl.sh "$RPM_BUILD_ROOT/usr/share/%{name}/scripts/"
install -Dm755 scripts/cpufreqctl.sh "$RPM_BUILD_ROOT/usr/bin/cpufreqctl.auto-cpufreq"
install -Dm644 %{SOURCE1} "$RPM_BUILD_ROOT/usr/lib/systemd/system/%{name}.service"
install -Dm644 scripts/style.css "$RPM_BUILD_ROOT/usr/share/%{name}/scripts/"
install -Dm644 images/icon.png "$RPM_BUILD_ROOT/usr/share/pixmaps/%{name}.png"
install -Dm644 images/icon.png "$RPM_BUILD_ROOT/usr/share/%{name}/images/icon.png"
install -Dm644 scripts/org.auto-cpufreq.pkexec.policy -t "$RPM_BUILD_ROOT/usr/share/polkit-1/actions/"
install -Dm644 scripts/auto-cpufreq-gtk.desktop -t "$RPM_BUILD_ROOT/usr/share/applications/"

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-gtk
%{_bindir}/%{name}-install
%{_bindir}/%{name}-remove
%{_bindir}/cpufreqctl.%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/auto-cpufreq-gtk.desktop
%{_datadir}/polkit-1/actions/org.auto-cpufreq.pkexec.policy
/usr/lib/systemd/system/%{name}.service
%{python3_sitelib}/auto_cpufreq
%{python3_sitelib}/auto_cpufreq-1.dist-info


%changelog
* Thu Mar 28 2024 m0ngr31 <joe@ipson.me> - 2.2.0
- Initial Package
