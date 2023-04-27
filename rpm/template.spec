%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-mimick-vendor
Version:        0.3.2
Release:        4%{?dist}%{?release_suffix}
Summary:        ROS mimick_vendor package

License:        Apache License 2.0 and MIT
URL:            https://github.com/Snaipe/Mimick
Source0:        %{name}-%{version}.tar.gz

Requires:       %{name}-runtime%{?_isa?} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}

%description
Wrapper around mimick, it provides an ExternalProject build of mimick.

%package runtime
Summary:        Runtime-only files for mimick_vendor package
Requires:       ros-rolling-ros-workspace-runtime
BuildRequires:  git
BuildRequires:  ros-rolling-ament-cmake-devel
BuildRequires:  ros-rolling-ros-workspace-devel

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-lint-auto-devel
BuildRequires:  ros-rolling-ament-lint-common-devel
%endif

%description runtime
Runtime-only files for mimick_vendor package

%prep
%autosetup -p1

%build
# Suppress fortification, which conflicts with Mimick's -O0 requirement
%undefine _annotated_build
export CFLAGS="${CFLAGS:-%{optflags}} -Wp,-U_FORTIFY_SOURCE"

# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

for f in \
    /opt/ros/rolling/include/ \
    /opt/ros/rolling/share/ament_index/resource_index/packages/ \
    /opt/ros/rolling/share/mimick_vendor/cmake/ \
    /opt/ros/rolling/share/mimick_vendor/package.dsv \
    /opt/ros/rolling/share/mimick_vendor/package.xml \
; do
    if [ -e %{buildroot}$f ]; then echo $f; fi
done > devel_files

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files -f devel_files

%files runtime
/opt/ros/rolling
%exclude /opt/ros/rolling/include/
%exclude /opt/ros/rolling/share/ament_index/resource_index/packages/
%exclude /opt/ros/rolling/share/mimick_vendor/cmake
%exclude /opt/ros/rolling/share/mimick_vendor/package.dsv
%exclude /opt/ros/rolling/share/mimick_vendor/package.xml

%changelog
* Fri Mar 24 2023 Scott K Logan <scott@openrobotics.org> - 0.3.2-4
- Autogenerated by Bloom

* Tue Mar 21 2023 Scott K Logan <scott@openrobotics.org> - 0.3.2-3
- Autogenerated by Bloom

