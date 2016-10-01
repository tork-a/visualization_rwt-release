Name:           ros-indigo-rwt-moveit
Version:        0.0.3
Release:        0%{?dist}
Summary:        ROS rwt_moveit package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/rwt_moveit
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-interactive-marker-proxy
Requires:       ros-indigo-kdl-parser
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-moveit-msgs
Requires:       ros-indigo-orocos-kdl
Requires:       ros-indigo-robot-state-publisher
Requires:       ros-indigo-rosbridge-server
Requires:       ros-indigo-rospy
Requires:       ros-indigo-roswww
Requires:       ros-indigo-rwt-utils-3rdparty
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-tf
Requires:       ros-indigo-tf2-web-republisher
Requires:       ros-indigo-visualization-msgs
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-interactive-marker-proxy
BuildRequires:  ros-indigo-kdl-parser
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-moveit-msgs
BuildRequires:  ros-indigo-orocos-kdl
BuildRequires:  ros-indigo-robot-state-publisher
BuildRequires:  ros-indigo-rosbridge-server
BuildRequires:  ros-indigo-rospy
BuildRequires:  ros-indigo-roswww
BuildRequires:  ros-indigo-rwt-utils-3rdparty
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-tf2-web-republisher
BuildRequires:  ros-indigo-visualization-msgs

%description
This package provides a web user interface of MoveIt! on top of visualizer in
ros3djs.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Sat Oct 01 2016 Isaac I.Y. Saito <iiysaito@opensource-robotics.tokyo.jp> - 0.0.3-0
- Autogenerated by Bloom

