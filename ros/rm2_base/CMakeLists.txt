cmake_minimum_required(VERSION 3.8)
project(rm2_base)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_ros REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# add_library(rm2_base src/rm2_base.cpp)
# target_compile_features(rm2_base PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
# target_include_directories(rm2_base PUBLIC
#   $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
#   $<INSTALL_INTERFACE:include>)

# Causes the visibility macros to use dllexport rather than dllimport,
# which is appropriate when building the dll but not consuming it.
# target_compile_definitions(rm2_base PRIVATE "RM2_BASE_BUILDING_LIBRARY")

install(
  DIRECTORY include/
  DESTINATION include
)

add_executable(rm2_base src/rm2_base_node.cpp)
target_include_directories(rm2_base PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
# target_link_libraries(rm2_base_node rm2_base)

install(TARGETS rm2_base
  DESTINATION lib/${PROJECT_NAME})
install(
  TARGETS rm2_base
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_include_directories(
  include
)
ament_export_libraries(
  rm2_base
)
ament_export_targets(
  export_${PROJECT_NAME}
)
ament_target_dependencies(rm2_base rclcpp std_msgs geometry_msgs)

ament_package()
