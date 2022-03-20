cmake_minimum_required(VERSION 3.0)
project(march-twentith-bridge VERSION 0.1.0)

find_package(catkin REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  std_msgs
  tf2_msgs
  geometry_msgs
  gazebo_msgs
  qqq
)

catkin_package()

catkin_install_python(PROGRAMS scripts/bridge.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
